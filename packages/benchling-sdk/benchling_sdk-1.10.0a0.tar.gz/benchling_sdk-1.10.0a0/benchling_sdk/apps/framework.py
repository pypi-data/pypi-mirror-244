from __future__ import annotations

import collections
from typing import Dict, List, Optional, OrderedDict, Protocol, Tuple, Type, TypeVar, Union

import attr
from benchling_api_client.v2.extensions import UnknownType
from ordered_set import OrderedSet

from benchling_sdk.apps import helpers
from benchling_sdk.apps.config.errors import UnsupportedConfigItemError
from benchling_sdk.apps.config.types import ConfigItemPath, ConfigurationReference
from benchling_sdk.apps.errors import MalformedAppWebhookError, MissingTenantUrlProviderError
from benchling_sdk.benchling import Benchling
from benchling_sdk.helpers.logging_helpers import log_stability_warning, StabilityLevel
from benchling_sdk.models import AppConfigItem, ListAppConfigurationItemsSort
from benchling_sdk.models.webhooks.v0 import WebhookEnvelopeV0

log_stability_warning(StabilityLevel.ALPHA)


AppType = TypeVar("AppType", bound="App")
AppWebhookType = WebhookEnvelopeV0


class TenantUrlProvider(Protocol):
    """Return a base URL."""

    def __call__(self) -> str:
        """Return a base URL."""
        pass


def tenant_url_provider_static(tenant_url: str) -> TenantUrlProvider:
    """Create a provider function that always returns a static tenant URL."""

    def _url() -> str:
        return tenant_url

    return _url


def tenant_url_provider_lazy() -> TenantUrlProvider:
    """
    Create a provider function for app that will be initialized at runtime, such as from a webhook.

    Useful for when a base_url for Benchling is not known in advance but can be supplied at runtime.
    """

    def _deferred() -> str:
        raise MissingTenantUrlProviderError(
            "Unable to initialize base URL for tenant. Expected a URL to "
            "be provided at runtime but none was specified. Either specify "
            "a url provider or use TenantUrlProvider.static_url"
        )

    return _deferred


class BenchlingProvider(Protocol):
    """Return a Benchling instance."""

    # TODO BNCH-52772 probably need to eliminate this relationship
    def __call__(self, tenant_url_provider: TenantUrlProvider) -> Benchling:
        """Return a Benchling instance."""
        pass


# TODO BNCH-52772 This should be refactored to a callable Protocol if we're being consistent


class ConfigProvider(Protocol):
    """
    Config provider.

    Provides a list of ConfigurationReference.
    """

    def config(self) -> List[ConfigurationReference]:
        """Implement to provide a list of configuration items, for instance from Benchling APIs."""
        pass


class ConfigItemStoreProvider(Protocol):
    """Return a config item store."""

    def __call__(self, app_id: str) -> ConfigItemStore:
        """Return a config item store."""
        pass


def benchling_provider_static(benchling: Benchling) -> BenchlingProvider:
    """Create a provider function that always returns a static Benchling."""

    def _static_benchling(tenant_url_provider: TenantUrlProvider) -> Benchling:
        return benchling

    return _static_benchling


@attr.s(auto_attribs=True)
class App:
    """
    App.

    See https://docs.benchling.com/docs/getting-started-benchling-apps

    Accepts providers as arguments to lazily initialize since some required attributes may not be
    known until runtime. Also allows for easier mocking in tests.
    """

    id: str
    _benchling_provider: BenchlingProvider
    _tenant_url_provider: TenantUrlProvider
    _config_store: ConfigItemStore
    _benchling: Optional[Benchling] = attr.ib(default=None, init=False)

    @property
    def benchling(self) -> Benchling:
        """Return a Benchling instance for the App."""
        if self._benchling is None:
            self._benchling = self._benchling_provider(self._tenant_url_provider)
        return self._benchling

    @property
    def config_store(self) -> ConfigItemStore:
        """Return a ConfigItemStore instance for the App."""
        return self._config_store

    def reset(self) -> None:
        """
        Reset the app.

        Generally clears all states and internal caches, which may cause subsequent invocations of the App
        to be expensive.
        """
        self._benchling = None
        if self._config_store is not None:
            self._config_store.invalidate_cache()

    def with_base_url(self: AppType, base_url: str) -> AppType:
        """Create a new copy of the app with a different base URL."""
        updated_tenant_url_provider = tenant_url_provider_static(base_url)
        modified_app = attr.evolve(self, tenant_url_provider=updated_tenant_url_provider)
        modified_app.reset()
        return modified_app

    def with_webhook(self: AppType, webhook: Union[dict, AppWebhookType]) -> AppType:
        """Create a new copy of the app with a different base URL provided by a webhook."""
        if isinstance(webhook, dict):
            if "baseUrl" not in webhook:
                raise MalformedAppWebhookError("The webhook specified did not contain a baseUrl")
            base_url = webhook["baseUrl"]
        else:
            base_url = webhook.base_url
        return self.with_base_url(base_url)

    def create_session_context(
        self: AppType,
        name: str,
        timeout_seconds: int,
        context_enter_handler: Optional[helpers.session_helpers.SessionContextEnterHandler[AppType]] = None,
        context_exit_handler: Optional[helpers.session_helpers.SessionContextExitHandler[AppType]] = None,
    ) -> helpers.session_helpers.SessionContextManager[AppType]:
        """
        Create Session Context.

        Create a new app session in Benchling.
        """
        # Avoid circular import + MyPy "is not defined" if using relative like above
        from benchling_sdk.apps.helpers.session_helpers import new_session_context

        return new_session_context(self, name, timeout_seconds, context_enter_handler, context_exit_handler)

    def continue_session_context(
        self: AppType,
        session_id: str,
        context_enter_handler: Optional[helpers.session_helpers.SessionContextEnterHandler[AppType]] = None,
        context_exit_handler: Optional[helpers.session_helpers.SessionContextExitHandler[AppType]] = None,
    ) -> helpers.session_helpers.SessionContextManager[AppType]:
        """
        Continue Session Context.

        Fetch an existing app session from Benchling and enter a context with it.
        """
        # Avoid circular import + MyPy "is not defined" if using relative like above
        from benchling_sdk.apps.helpers.session_helpers import continue_session_context

        return continue_session_context(self, session_id, context_enter_handler, context_exit_handler)

    @classmethod
    def init(
        cls: Type[AppType],
        app_id: str,
        benchling_provider: BenchlingProvider,
        tenant_url_provider: TenantUrlProvider,
        config_item_store: ConfigItemStore,
    ) -> AppType:
        """
        Init.

        Initialize an app from its class.
        """
        return cls(app_id, benchling_provider, tenant_url_provider, config_item_store)


class BenchlingConfigProvider(ConfigProvider):
    """
    Benchling Config provider.

    Provides a BenchlingAppConfiguration retrieved from Benchling's API.
    """

    _benchling_provider: BenchlingProvider
    _tenant_url_provider: TenantUrlProvider
    _app_id: str
    _benchling: Optional[Benchling]

    def __init__(
        self, benchling_provider: BenchlingProvider, tenant_url_provider: TenantUrlProvider, app_id: str
    ):
        """
        Initialize Benchling Config Provider.

        :param benchling_provider: A provider for a Benchling instance.
        :param tenant_url_provider: A provider for a tenant url.
        :param app_id: The app_id from which to retrieve configuration.
        """
        self._benchling_provider = benchling_provider
        self._tenant_url_provider = tenant_url_provider
        self._app_id = app_id
        self._benchling = None

    @property
    def benchling(self) -> Benchling:
        """Return the Benchling instance used to gather configuration."""
        if self._benchling is None:
            self._benchling = self._benchling_provider(self._tenant_url_provider)
        return self._benchling

    def config(self) -> List[ConfigurationReference]:
        """Provide a Benchling app configuration from Benchling's APIs."""
        app_pages = self.benchling.apps.list_app_configuration_items(
            app_id=self._app_id,
            page_size=100,
            sort=ListAppConfigurationItemsSort.CREATEDATASC,
        )

        # Eager load all config items for now since we don't yet have a way of lazily querying by path
        all_config_pages = list(app_pages)
        # Punt on UnknownType for now as apps using manifests with new types could lead to unpredictable results
        all_config_items = [
            _supported_config_item(config_item) for page in all_config_pages for config_item in page
        ]

        return all_config_items


class StaticConfigProvider(ConfigProvider):
    """
    Static Config provider.

    Provides a BenchlingAppConfiguration from a static declaration. Useful for mocking or testing.
    """

    _configuration_items: List[ConfigurationReference]

    def __init__(self, configuration_items: List[ConfigurationReference]):
        """
        Initialize Static Config Provider.

        :param configuration_items: The configuration items to return.
        """
        self._configuration_items = configuration_items

    def config(self) -> List[ConfigurationReference]:
        """Provide Benchling app configuration items from a static reference."""
        return self._configuration_items


class ConfigItemStore:
    """
    Dependency Link Store.

    Marshalls an app configuration from the configuration provider into an indexable structure.
    Only retrieves app configuration once unless its cache is invalidated.
    """

    _configuration_provider: ConfigProvider
    _configuration: Optional[List[ConfigurationReference]] = None
    _configuration_map: Optional[Dict[ConfigItemPath, ConfigurationReference]] = None
    _array_path_row_names: Dict[Tuple[str, ...], OrderedSet[str]] = dict()

    def __init__(self, configuration_provider: ConfigProvider):
        """
        Initialize Dependency Link Store.

        :param configuration_provider: A ConfigProvider that will be invoked to provide the
        underlying config from which to organize dependency links.
        """
        self._configuration_provider = configuration_provider
        self._array_path_row_names = dict()

    @property
    def configuration(self) -> List[ConfigurationReference]:
        """
        Get the underlying configuration.

        Return the raw, stored configuration. Can be used if the provided accessors are inadequate
        to find particular configuration items.
        """
        if not self._configuration:
            self._configuration = self._configuration_provider.config()
        return self._configuration

    @property
    def configuration_path_map(self) -> Dict[ConfigItemPath, ConfigurationReference]:
        """
        Config links.

        Return a map of configuration item paths to their corresponding configuration items.
        """
        if not self._configuration_map:
            self._configuration_map = {tuple(item.path): item for item in self.configuration}
        return self._configuration_map

    def config_by_path(self, path: List[str]) -> Optional[ConfigurationReference]:
        """
        Config by path.

        Find an app config item by its exact path match, if it exists. Does not search partial paths.
        """
        # Since we eager load all config now, we know that missing path means it's not configured in Benchling
        # Later if we support lazy loading, we'll need to differentiate what's in our cache versus missing
        return self.configuration_path_map.get(tuple(path))

    def config_keys_by_path(self, path: List[str]) -> OrderedSet[str]:
        """
        Config keys by path.

        Find a set of app config keys at the specified path, if any. Does not return keys that are nested
        beyond the current level.

        For instance, given paths:
        ["One", "Two"]
        ["One", "Two", "Three"]
        ["One", "Two", "Four"]
        ["One", "Two", "Three", "Five"]
        ["Zero", "One", "Two", "Three"]

        The expected return from this method when path=["One", "Two"] is a set {"Three", "Four"}.
        """
        # Convert path to tuple, as list is not hashable for dict keys
        path_tuple = tuple(path)
        if path_tuple not in self._array_path_row_names:
            self._array_path_row_names[path_tuple] = OrderedSet(
                [
                    config_item.path[len(path)]
                    # Use the list instead of configuration_map to preserve order
                    for config_item in self.configuration
                    # The +1 is the name of the array row
                    if len(config_item.path) >= len(path) + 1
                    # Ignoring flake8 error E203 because black keeps putting in whitespace padding :
                    and config_item.path[0 : len(path_tuple)] == path  # noqa: E203
                    and config_item.value is not None
                ]
            )
        return self._array_path_row_names[path_tuple]

    def array_rows_to_dict(self, path: List[str]) -> OrderedDict[str, Dict[str, ConfigurationReference]]:
        """Given a path to the root of a config array, return each element as a named dict."""
        # TODO BNCH-52772 Improve docstring if we keep this method
        array_keys = self.config_keys_by_path(path)
        # Although we don't have a way of preserving order when pulling array elements from the API right now
        # we should intentionally order these to accommodate a potential ordered future
        array_elements_map = collections.OrderedDict()
        for key in array_keys:
            # Don't care about order for the keys within a row, only the order of the rows themselves
            array_elements_map[key] = {
                array_element_key: self.config_by_path([*path, key, array_element_key])
                for array_element_key in self.config_keys_by_path([*path, key])
                if self.config_by_path([*path, key, array_element_key]) is not None
            }
        # TODO BNCH-52772 MyPy thinks the inner dict values can be None
        return array_elements_map  # type: ignore

    def invalidate_cache(self) -> None:
        """
        Invalidate Cache.

        Will force retrieval of configuration from the ConfigProvider the next time the link store is accessed.
        """
        self._configuration = None
        self._configuration_map = None
        self._array_path_row_names = dict()


def init_app(
    app_id: str,
    benchling_provider: BenchlingProvider,
    tenant_url_provider: TenantUrlProvider,
    config_item_store: Optional[ConfigItemStore] = None,
) -> App:
    """
    Init App.

    Initializes a Benchling App with a series of functions to provide App dependencies at runtime.
    """
    if config_item_store is None:
        config_item_store = ConfigItemStore(
            BenchlingConfigProvider(benchling_provider, tenant_url_provider, app_id)
        )
    return App.init(app_id, benchling_provider, tenant_url_provider, config_item_store)


def init_static_app(app_id: str, benchling: Benchling, config_store: Optional[ConfigItemStore] = None) -> App:
    """
    Init Static App.

    Initializes a Benchling App with static values. Suitable for apps that communicate with a single URL.

    If ConfigItemStore is None, will initialize a default ConfigItemStore that loads config from the Benchling instance.
    """
    tenant_url_provider = tenant_url_provider_static(benchling.client.base_url)
    benchling_provider = benchling_provider_static(benchling)
    if config_store is None:
        config_store = ConfigItemStore(
            BenchlingConfigProvider(benchling_provider, tenant_url_provider, app_id)
        )
    return init_app(app_id, benchling_provider, tenant_url_provider, config_store)


def _supported_config_item(config_item: AppConfigItem) -> ConfigurationReference:
    if isinstance(config_item, UnknownType):
        raise UnsupportedConfigItemError(
            f"Unable to read app configuration with unsupported type: {config_item}"
        )
    return config_item
