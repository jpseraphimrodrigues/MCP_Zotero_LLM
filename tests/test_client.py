from unittest.mock import Mock, patch

from zotero_mcp.client import ZoteroClient


def test_collections_uses_local_api():
    response = Mock()
    response.json.return_value = [{"key": "ABC", "data": {"name": "Paper"}}]
    response.raise_for_status.return_value = None
    with patch("zotero_mcp.client.httpx.get", return_value=response) as get:
        result = ZoteroClient().collections(limit=1)
    assert result[0]["key"] == "ABC"
    assert get.call_args.kwargs["headers"]["Zotero-API-Version"] == "3"
