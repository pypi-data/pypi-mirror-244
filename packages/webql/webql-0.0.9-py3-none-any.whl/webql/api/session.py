import json
import logging
from typing import Generic

import requests

from webql.common.errors import WEBQL_2000_UNKNOWN_QUERY_ERROR, QueryError, QueryTimeoutError
from webql.syntax.parser import Parser
from webql.web import InteractiveItemTypeT, WebDriver

from ..common.api_constants import GET_WEBQL_ENDPOINT, SERVICE_URL
from .response_proxy import WQLResponseProxy

log = logging.getLogger(__name__)

QUERY_EXCEPTION_DEFAULT_ERROR = "Unknown Query Exception"
QUERY_EXCEPTION_DEFAULT_INTERNAL_ERROR_CODE = WEBQL_2000_UNKNOWN_QUERY_ERROR
RESPONSE_ERROR_KEY = "error"
RESPONSE_INTERNAL_ERROR_CODE_KEY = "internal_error_code"


class Session(Generic[InteractiveItemTypeT]):
    """A session with a WebQL service."""

    def __init__(self, web_driver: WebDriver[InteractiveItemTypeT]):
        """Initialize the session.

        Parameters:

        web_driver (WebDriver): The web driver that will be used in this session.
        """
        self._web_driver = web_driver

    def query(self, query: str, timeout: int = 120) -> WQLResponseProxy[InteractiveItemTypeT]:
        """Query the web page tree for elements that match the WebQL query.

        Parameters:

        query (str): The query string.
        timeout (optional): Optional timeout value for the connection with backend api service.

        Returns:

        dict: WebQL Response (Elements that match the query)
        """
        log.debug(f"querying {query}")

        parser = Parser(query)
        parser.parse()

        accessibility_tree = self._web_driver.get_accessiblity_tree()
        response = self._query(query, accessibility_tree, timeout)

        return WQLResponseProxy[InteractiveItemTypeT](response, self._web_driver)

    def stop(self):
        """Close the session."""
        log.debug("closing session")
        self._web_driver.stop_browser()

    def _query(self, query: str, accessibility_tree: dict, timeout: int) -> dict:
        """Make Request to WebQL API.

        Parameters:

        query (str): The query string.
        accessibility_tree (dict): The accessibility tree.
        timeout (int): The timeout value for the connection with backend api service

        Returns:

        dict: WebQL response in json format.
        """
        request_data = {"query": f"{query}", "accessibility_tree": accessibility_tree}
        url = SERVICE_URL + GET_WEBQL_ENDPOINT
        try:
            response = requests.post(url, json=request_data, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.ReadTimeout):
                raise QueryTimeoutError() from e
            server_error = e.response.text if e.response else None
            if server_error:
                try:
                    server_error_json = json.loads(server_error)
                    if isinstance(server_error_json, dict):
                        error = server_error_json.get(
                            RESPONSE_ERROR_KEY, QUERY_EXCEPTION_DEFAULT_ERROR
                        )
                        internal_error_code = server_error_json.get(
                            RESPONSE_INTERNAL_ERROR_CODE_KEY,
                            QUERY_EXCEPTION_DEFAULT_INTERNAL_ERROR_CODE,
                        )
                    else:
                        error = QUERY_EXCEPTION_DEFAULT_ERROR
                        internal_error_code = QUERY_EXCEPTION_DEFAULT_INTERNAL_ERROR_CODE
                except ValueError:
                    error = QUERY_EXCEPTION_DEFAULT_ERROR
                    internal_error_code = QUERY_EXCEPTION_DEFAULT_INTERNAL_ERROR_CODE
            else:
                error = QUERY_EXCEPTION_DEFAULT_ERROR
                internal_error_code = QUERY_EXCEPTION_DEFAULT_INTERNAL_ERROR_CODE
            raise QueryError(error, internal_error_code) from e
