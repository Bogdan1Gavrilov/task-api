from langchain_core.tools import tool
from langchain_experimental.tools.python.tool import PythonREPLTool
import re
from typing import Optional
from langchain_core.tools import tool
from ddgs import DDGS


from app.rag.chain import build_rag_chain
from app.config import settings

_chain = None
_retriever = None
_python_repl = PythonREPLTool()

def _ensure_rag_ready() -> None:
    global _chain, _retriever
    if _chain is None:
        _chain, _retriever = build_rag_chain()


@tool
def documentation_search(query: str) -> str:
    """Search the scikit-learn documentation corpus for a given query.

    Use this tool when the iser asks about scikit-learn classes, methods,
    parameters, or general ML concepts (Ridge, Lasso, decision trees, metrics).

    Args:
        query: natural language question or keyword search.
    Returns:
        Answer text followed by a list of source URLs.
    """
    _ensure_rag_ready()
    docs = _retriever.invoke(query)
    answer = _chain.invoke(query)
    sources = [doc.metadata.get("source", "unknown") for doc in docs]
    sources_block = "\n".join(f"- {url}" for url in sources)
    return f"{answer}\n\nSources:\n{sources_block}"


# SECURITY NOTE: PythonREPLTool executrs arbitary code in the same process
# as our app. It is NEVER exposed directly to end users - only the agent
# decides what to send into it. For production with untrusted users, wrap
# in a sandbox (gvisor, e2b.dev, firecracker).
@tool
def python_repl(code:str) -> str:
    """Execute Python code and return the printed output.

    Use this tool for arithmetic, computing formelas or transforming data.
    The code runs in a sandboxed REPL; use `print()` to surface results.

    Args:
        code: Python source code to execute.
    Returns:
        stdout of the executed code or error message.
    """
    return _python_repl.run(code)


@tool
def web_search(query: str) -> str:
    """Search the web via DuckDuckGo got recent or general-knowledge info.

    Use this tool when the question requires fresh data (release notes,
    latest versions, news) that is NOT in documentation corpus.

    Args:
        query: free-text search query.
    Returns:
        Top-3 search results as title + snippet text.
    """

    if not settings.enable_web_search:
        return "Web search is disabled by administrator."

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query, 
                max_results=5,
                region='ru-ru',
                safesearch='moderate'
            ))
            
            if not results:
                return "По вашему запросу ничего не найдено."
            
            formatted = []
            for i, r in enumerate(results[:5], 1):
                title = r.get('title', 'Без названия')
                body = r.get('body', 'Нет описания')
                href = r.get('href', '')
                formatted.append(
                    f"{i}. **{title}**\n"
                    f"   {body[:200]}\n"
                    f"   Источник: {href}"
                )
            
            return "\n\n".join(formatted)
            
    except Exception as e:
        return f"Ошибка поиска: {str(e)}"

TOOLS = [documentation_search, python_repl, web_search]