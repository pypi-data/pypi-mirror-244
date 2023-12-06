"""Asynchronous Python client providing Open Data information of Zurich."""
from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import Any, Self, cast

from aiohttp import ClientError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import ODPZurichConnectionError, ODPZurichError
from .models import DisabledParking


@dataclass
class ODPZurich:
    """Main class for handling data fetching from Open Data Platform of Zurich."""

    request_timeout: float = 10.0
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to the Open Data Platform API of Zurich.

        Args:
        ----
            uri: Request URI, without '/', for example, 'status'
            method: HTTP method to use, for example, 'GET'
            params: Extra options to improve or limit the response.

        Returns:
        -------
            A Python dictionary (text) with the response from
            the Open Data Platform API of Zurich.

        Raises:
        ------
            ODPZurichConnectionError: Timeout occurred while
                connecting to the Open Data Platform API.
            ODPZurichError: If the data is not valid.
        """
        version = metadata.version(__package__)
        url = URL.build(
            scheme="https",
            host="www.ogd.stadt-zuerich.ch",
            path="/wfs/geoportal/",
        ).join(URL(uri))

        headers = {
            "Accept": "application/vnd.geo+json",
            "User-Agent": f"PythonODPZurich/{version}",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    params=params,
                    headers=headers,
                    ssl=True,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            msg = "Timeout occurred while connecting to the Open Data Platform API."
            raise ODPZurichConnectionError(
                msg,
            ) from exception
        except (ClientError, socket.gaierror) as exception:
            mag = "Error occurred while communicating with Open Data Platform API."
            raise ODPZurichConnectionError(
                mag,
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/vnd.geo+json" not in content_type:
            text = await response.text()
            msg = "Unexpected content type response from the Open Data Platform API"
            raise ODPZurichError(
                msg,
                {"Content-Type": content_type, "Response": text},
            )

        return cast(dict[str, Any], await response.json())

    async def disabled_parkings(self) -> list[DisabledParking]:
        """Get list of disabled parking.

        Returns
        -------
            A list of DisabledParking objects.
        """
        locations = await self._request(
            "Behindertenparkplaetze",
            params={
                "service": "WFS",
                "request": "GetFeature",
                "outputFormat": "GeoJSON",
                "typename": "behindertenparkplaetze_dav_p",
            },
        )
        return [DisabledParking.from_dict(item) for item in locations["features"]]

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The Open Data Platform Zurich object.
        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.
        """
        await self.close()
