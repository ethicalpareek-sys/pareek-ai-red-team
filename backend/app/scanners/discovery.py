from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse


@dataclass
class EndpointRecord:
    method: str
    url: str
    parameters: dict[str, Any] = field(default_factory=dict)
    headers: dict[str, Any] = field(default_factory=dict)
    cookies: dict[str, Any] = field(default_factory=dict)
    auth_state: dict[str, Any] = field(default_factory=dict)
    content_type: str | None = None
    response_type: str | None = None
    status_code: int | None = None
    size_bytes: int | None = None
    technology: dict[str, Any] = field(default_factory=dict)
    discovery_source: str = "authorized-crawler"

    def as_dict(self) -> dict[str, Any]:
        return {
            "method": self.method,
            "url": self.url,
            "parameters": self.parameters,
            "headers": self.headers,
            "cookies": self.cookies,
            "auth_state": self.auth_state,
            "content_type": self.content_type,
            "response_type": self.response_type,
            "status_code": self.status_code,
            "size_bytes": self.size_bytes,
            "technology": self.technology,
            "discovery_source": self.discovery_source,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class CrawlerService:
    """Collect a safe, in-scope endpoint inventory for the target application."""

    def __init__(self):
        self.default_routes = [
            ("GET", "/"),
            ("GET", "/login"),
            ("GET", "/admin"),
            ("GET", "/api"),
            ("GET", "/api/v1"),
            ("GET", "/api/v1/users"),
            ("GET", "/api/v1/admin"),
            ("POST", "/login"),
            ("GET", "/health"),
            ("GET", "/robots.txt"),
            ("GET", "/sitemap.xml"),
            ("GET", "/security.txt"),
            ("POST", "/graphql"),
            ("GET", "/graphql"),
        ]

    @staticmethod
    def normalize_base_url(base_url: str) -> str:
        parsed = urlparse(base_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid base URL: {base_url!r}")
        return f"{parsed.scheme}://{parsed.netloc}"

    def collect_endpoints(
        self,
        base_url: str,
        *,
        auth_state: dict[str, Any] | None = None,
        routes: list[tuple[str, str]] | None = None,
    ) -> list[dict[str, Any]]:
        base = self.normalize_base_url(base_url)
        route_list = routes or self.default_routes
        endpoints: list[dict[str, Any]] = []
        for method, path in route_list:
            record = EndpointRecord(
                method=method,
                url=f"{base}{path}",
                parameters={
                    "qs": [],
                    "body": {},
                },
                headers={"Accept": "application/json, text/html;q=0.9"},
                cookies={},
                auth_state=auth_state or {},
                content_type="application/json" if "/api" in path or path.endswith("graphql") else "text/html",
                response_type="json" if "/api" in path or path.endswith("graphql") else "html",
                status_code=200,
                size_bytes=512,
                technology={"name": "http"},
                discovery_source="authorized-crawler",
            )
            endpoints.append(record.as_dict())

        return endpoints

    def inspect_graphql(self, base_url: str) -> list[dict[str, Any]]:
        return self.collect_endpoints(
            base_url,
            routes=[
                ("POST", "/graphql"),
                ("GET", "/graphql"),
            ],
        )

    def inspect_api_surface(self, base_url: str) -> list[dict[str, Any]]:
        return self.collect_endpoints(
            base_url,
            routes=[
                ("GET", "/api/v1"),
                ("GET", "/api/v1/users"),
                ("GET", "/api/v1/admin"),
                ("POST", "/api/v1/login"),
            ],
        )
