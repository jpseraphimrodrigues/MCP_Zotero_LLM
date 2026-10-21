from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from .client import ZoteroClient

mcp = FastMCP("Zotero Local")
zotero = ZoteroClient()


def _compact(item: dict[str, Any]) -> dict[str, Any]:
    data = item.get("data", item)
    return {
        "key": item.get("key", data.get("key")),
        "itemType": data.get("itemType"),
        "title": data.get("title"),
        "creators": data.get("creators", []),
        "date": data.get("date"),
        "publicationTitle": data.get("publicationTitle"),
        "abstractNote": data.get("abstractNote"),
        "DOI": data.get("DOI"),
        "url": data.get("url"),
        "tags": data.get("tags", []),
        "collections": data.get("collections", []),
        "notes": item.get("meta", {}).get("numChildren", 0),
    }


@mcp.tool()
def testar_conexao() -> str:
    """Confirma se o Zotero local está aberto e acessível."""
    collections = zotero.collections(limit=1)
    return f"OK: Zotero acessível; amostra de coleções retornada: {len(collections)}."


@mcp.tool()
def listar_colecoes(limite: int = 100) -> str:
    """Lista coleções com nome e chave, para uso nas consultas seguintes."""
    return json.dumps(zotero.collections(limite), ensure_ascii=False, indent=2)


@mcp.tool()
def buscar_itens(termo: str, limite: int = 30) -> str:
    """Busca itens da biblioteca por título, autor, DOI, resumo ou palavra-chave."""
    items = zotero.items(termo, limite)
    return json.dumps([_compact(item) for item in items], ensure_ascii=False, indent=2)


@mcp.tool()
def listar_itens_da_colecao(chave_colecao: str, limite: int = 100) -> str:
    """Lista os itens de uma coleção usando a chave retornada por listar_colecoes."""
    items = zotero.collection_items(chave_colecao, limite)
    return json.dumps([_compact(item) for item in items], ensure_ascii=False, indent=2)


@mcp.tool()
def obter_item(chave_item: str) -> str:
    """Obtém os metadados completos de um item pelo seu key Zotero."""
    return json.dumps(zotero.item(chave_item), ensure_ascii=False, indent=2)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
