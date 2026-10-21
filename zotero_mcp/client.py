from __future__ import annotations

from typing import Any

import httpx


class ZoteroError(RuntimeError):
    """Raised when the local Zotero API cannot be reached or returns an error."""


class ZoteroClient:
    def __init__(self, base_url: str = "http://localhost:23119/api") -> None:
        self.base_url = base_url.rstrip("/")

    def get(self, path: str, **params: Any) -> Any:
        try:
            response = httpx.get(
                f"{self.base_url}/{path.lstrip('/')}",
                params=params,
                headers={"Zotero-API-Version": "3"},
                timeout=20,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ZoteroError(
                "Não foi possível acessar o Zotero em localhost:23119. "
                "Confirme que o Zotero está aberto e que a API local está habilitada."
            ) from exc
        return response.json()

    def collections(self, limit: int = 100) -> list[dict[str, Any]]:
        return self.get("users/0/collections", limit=limit, format="json")

    def items(self, query: str = "", limit: int = 50) -> list[dict[str, Any]]:
        return self.get(
            "users/0/items", q=query, limit=limit, format="json", include="data"
        )

    def collection_items(self, collection_key: str, limit: int = 100) -> list[dict[str, Any]]:
        return self.get(
            f"users/0/collections/{collection_key}/items",
            limit=limit,
            format="json",
            include="data",
        )

    def item(self, item_key: str) -> dict[str, Any]:
        return self.get(f"users/0/items/{item_key}", format="json", include="data")
