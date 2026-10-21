# Zotero Local MCP

Servidor MCP local, somente leitura, para Codex e Claude Code consultarem o Zotero Desktop aberto.

## Requisitos

- Python 3.11+
- `uv`
- Zotero aberto com a API local habilitada

## Instalação e validação

```powershell
$env:UV_CACHE_DIR = "$PWD\.uv-cache"
uv sync
uv run pytest
uv run ruff check .
```

O servidor usa `stdio`; não é necessário abrir uma porta HTTP para o MCP.

## Codex

```powershell
codex mcp add zotero-local -- uv run --directory C:\DEV\MCP_Zotero_LLM zotero-local-mcp
```

O arquivo `config/codex-mcp.toml` contém a configuração equivalente para esta instalação. Ao clonar em outro computador, substitua o caminho pelo novo diretório ou use o comando acima a partir do caminho local.

## Claude Code

Copie `config/claude.mcp.json` para o projeto consumidor como `.mcp.json`, ou registre o mesmo comando com `claude mcp add`.

## Uso

Peça ao agente para chamar `testar_conexao`, depois `listar_colecoes`, `listar_itens_da_colecao` e `obter_item`. O servidor somente lê o Zotero; o agente grava o fichamento `.md` no repositório de trabalho.

Esta primeira versão ainda não extrai automaticamente o texto dos PDFs nem altera a biblioteca Zotero.
