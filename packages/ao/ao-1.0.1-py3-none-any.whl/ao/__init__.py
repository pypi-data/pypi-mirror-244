import re
from typing import Dict

import requests
from requests.adapters import HTTPAdapter, Retry


# Request the summary of the page, by its title.
_WIKI_GET_REQUEST = 'https://en.wikipedia.org/api/rest_v1/page/summary/{}'

_NO_WIKI_ENTRY_ERROR = "Can't find a wikipedia entry for {}."

_TIMEOUT_ERROR = "Timeout: failed to find a wikipedia entry for {}."

_WONT_SEARCH_WIKI = "ao won't search wikipedia for the requested entry: {}."


def _format_str(name: str) -> str:
    """
    :returns: formatted name (without the underscores)
    """
    return name.replace('_', ' ').strip()


def _get_with_retries(get_url: str) -> Dict:
    """
    Executes http.get() request with smart retries.
    :returns: the response json.
    """
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    return s.get(get_url, timeout=2).json()


def _prettify_result(result: str) -> str:
    return re.sub('[ \t]+', ' ', result.strip())


def _get_wiki_search_result(name: str) -> str:
    """
    Requests the first paragraph of the wiki entry with this name.
    :returns: string of the first paragraph, or error string if failed.
    """
    try:
        result_json = _get_with_retries(_WIKI_GET_REQUEST.format(name))
        result = result_json['extract']
        return _prettify_result(result)
    except requests.RequestException:
        return _TIMEOUT_ERROR.format(name)
    except LookupError:
        return _NO_WIKI_ENTRY_ERROR.format(name)


def _is_in_blacklist(name: str) -> bool:
    """
    :returns: True if this name should not trigger a wiki search.
    """
    if name.startswith('_ipython_') and name.endswith('_'):
        return True
    return False


def __getattr__(name: str) -> str:
    """
    :returns: The first wikipedia paragraph describing the requested name. Returns an error string on an error.
    """
    if _is_in_blacklist(name):
        return _WONT_SEARCH_WIKI.format(name)

    question = _format_str(name)
    return _get_wiki_search_result(question)
