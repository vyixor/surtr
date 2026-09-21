#!/usr/bin/env python3
"""
fetch_requests.py

Drop-in helper to fetch & scrape multiple URLs from a simple Python list.
Features:
 - Inputs: plain URL string, compact key=value;... string, or dict per request
 - Parsers: text, json, bs4 (BeautifulSoup)
 - Selectors: tag, tag.prop, tag.prop='value', css:...[@attr]
 - Concurrency via ThreadPoolExecutor + requests.Session()
 - Retries with exponential backoff
 - UA rotation, proxies, default headers
 - Scheduling: global delay_between_requests, per-request 'delay', or per_request_schedule list
 - Output:
    * Default: print requested results (plain text) only (no status/errors)
    * save="file.txt": save plain text concatenation
    * save_json="file.json": save full structured details (status, error, content, request)
"""

from __future__ import annotations
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Tuple, Union
import os
import sys
import requests
from pathlib import Path
from colorama import init as colorama_init, Fore, Style
import math
import threading
import tempfile
import ast
from colorama import init as colorama_init, Fore, Style
import random
import getpass
from urllib.parse import urlparse
# Attempt to import BeautifulSoup at runtime; may be None if not installed.
try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:
    BeautifulSoup = None  # type: ignore
    
    
    
# Initialize colorama (for Windows)
colorama_init()

# ----- Utilities for pretty progress -----
_BAR_LEN = 38
# ----------------- Configuration defaults -----------------
DEFAULT_TIMEOUT = 10.0
DEFAULT_METHOD = "GET"
VALID_PARSERS = {"text", "json", "bs4","sbs4"}
VALID_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"}
MAX_RETRIES_DEFAULT = 2
BACKOFF_FACTOR = 0.5  # seconds
TEXT_SEPARATOR = "\n\n-----\n\n"  # used when printing or saving plain-text multiple request results
RESULT_SEPARATOR = "\n\n######\n\n" #used when printing or saving plain-text multiple results
returndata = False
fulldata = []

# --- 100 VALID & MODERN USER AGENTS (2024–2025) ---
_UA_POOL = [
    # Windows Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",

    # Windows Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.3485.94",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.3445.67",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.3235.55",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.3212.88",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.3130.50",

    # Windows Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",

    # macOS Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_9) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",

    # macOS Chrome & Firefox
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_9; rv:138.0) Gecko/20100101 Firefox/138.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",

    # Linux Desktop
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/123.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",

    # Android Chrome
    "Mozilla/5.0 (Linux; Android 15; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Infinix X671) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 15; V2405A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36",

    # Android Edge & Opera
    "Mozilla/5.0 (Linux; Android 14; SM-G996B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36 EdgA/140.0.3500.91",
    "Mozilla/5.0 (Linux; Android 14; Redmi Note 13 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36 OPR/123.0.0.0",
    "Mozilla/5.0 (Linux; Android 15; TECNO CL6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; vivo 2015) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-A546E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",

    # iPhone Safari
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.8 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.7 Mobile/15E148 Safari/604.1",

    # iPad Safari
    "Mozilla/5.0 (iPad; CPU OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.8 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.7 Mobile/15E148 Safari/604.1",

    # Android Tablets
    "Mozilla/5.0 (Linux; Android 15; SM-X910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Lenovo TB-J616F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Xiaomi Pad 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 15; Samsung Galaxy Tab S9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; HUAWEI MatePad 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",

    # Misc. Browsers (Brave, Vivaldi, Opera GX)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Brave/139",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Vivaldi/6.7",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Brave/137",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Vivaldi/6.8",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 OPR/123.0.0.0",

    # Legacy-compatible fallback
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.4 Mobile/15E148 Safari/604.1"
]


def get_random_user_agent():
    """
    Return a random, valid modern User-Agent string.
    Ideal for rotating UA headers in web scraping or API requests.
    """
    return random.choice(_UA_POOL)

#SELECT RANDOMLY
_DEFAULT_UA_POOL = get_random_user_agent()

# ----------------- Helpers: compact parser & normalizer -----------------
def _parse_compact_kv(s: str) -> Dict[str, Any]:
    """
    Parse compact key=value;key2=value2;... strings.
    Special keys: headers and queries accept comma-separated k:v pairs.
    """
    out: Dict[str, Any] = {}
    if not isinstance(s, str):
        return out
    s = s.strip()
    if not s:
        return out
    parts = re.split(r'\s*;\s*', s)
    for part in parts:
        if not part:
            continue
        if '=' not in part:
            out[part] = True
            continue
        k, v = part.split('=', 1)
        k = k.strip()
        v = v.strip()
        if k in ("headers", "queries"):
            kvs = {}
            if v:
                for item in re.split(r'\s*,\s*', v):
                    if not item:
                        continue
                    if ':' in item:
                        kk, vv = item.split(':', 1)
                        kvs[kk] = vv
                    else:
                        kvs[item] = ""
            out[k] = kvs
        elif k in ("url", "method", "parser", "select", "save"):
            out[k] = v
        elif k == "timeout":
            try:
                out[k] = float(v)
            except Exception:
                out[k] = v
        elif k == "delay":
            try:
                out[k] = float(v)
            except Exception:
                out[k] = v
        elif k == "body":
            out[k] = v
        else:
            out[k] = v
    return out

def _normalize_item(item: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Normalize one list item (string or dict) into a validated dict with keys:
      url, method, parser, headers, queries, select, timeout, body, retries, delay (seconds)
    """
    if isinstance(item, dict):
        req = dict(item)  # shallow copy
    elif isinstance(item, str):
        s = item.strip()
        # plain url
        if s.startswith("http://") or s.startswith("https://"):
            req = {"url": s}
        else:
            req = _parse_compact_kv(s)
    else:
        raise TypeError("Each request must be a dict or string (url or compact).")

    # URL
    url = req.get("url")
    if not isinstance(url, str) or not url.strip()  :
        raise ValueError("Each request must include 'url' (string).")
    url = url.strip()

    # NEW: Allow local files / raw content for bs4/text/json parsers
    parser = req.get("parser", "text").lower().strip()
    if parser == "bs4":
      # Relax URL check — allow file paths or raw strings
      if os.path.isfile(url) or (not url.startswith(("http://", "https://")) and len(url) > 10):
        normalized: Dict[str, Any] = {"url": url}

      elif url.startswith(("http://", "https://")):
        normalized: Dict[str, Any] = {"url": url}

      else:
        raise ValueError(f"Invalid URL/content for parser '{parser}': {url[:100]}...")
   
    else:
      # Strict check for other parsers
      if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError(f"URL must start with http:// or https://: {url}")
      normalized: Dict[str, Any] = {"url": url}
    
    
    # Method
    method = req.get("method", DEFAULT_METHOD)
    if not isinstance(method, str):
        raise ValueError("method must be a string")
    method = method.strip().upper()
    if method not in VALID_METHODS:
        raise ValueError(f"Unsupported HTTP method: {method}")
    normalized["method"] = method

    # Parser
    parser = req.get("parser", "text")
    if not isinstance(parser, str):
        raise ValueError("parser must be a string")
    parser = parser.strip().lower()
    if parser not in VALID_PARSERS:
        raise ValueError(f"parser must be one of {VALID_PARSERS}")
    if parser == "bs4" and BeautifulSoup is None:
        raise ValueError("parser 'bs4' requested but BeautifulSoup is not installed (pip install beautifulsoup4).")
    normalized["parser"] = parser

    # Headers and queries
    headers = req.get("headers") or {}
    if not isinstance(headers, dict):
        raise ValueError("headers must be a dict")
    normalized["headers"] = headers

    queries = req.get("queries") or {}
    if not isinstance(queries, dict):
        raise ValueError("queries must be a dict")
    normalized["queries"] = queries

    # Select
    sel = req.get("select")
    normalized["select"] = sel.strip() if isinstance(sel, str) and sel.strip() else None

    # Timeout
    timeout = req.get("timeout", DEFAULT_TIMEOUT)
    try:
        timeout = float(timeout)
        if timeout <= 0:
            raise ValueError("timeout must be > 0")
    except Exception:
        raise ValueError("timeout must be a positive number")
    normalized["timeout"] = timeout

    # Body
    if "body" in req:
        normalized["body"] = req["body"]

    # Delay (per-request scheduling)
    delay = req.get("delay", 0.0)
    try:
        delay = float(delay)
        if delay < 0:
            delay = 0.0
    except Exception:
        delay = 0.0
    normalized["delay"] = delay

    # retries
    retries = req.get("retries", MAX_RETRIES_DEFAULT)
    try:
        retries = int(retries)
        if retries < 0:
            retries = MAX_RETRIES_DEFAULT
    except Exception:
        retries = MAX_RETRIES_DEFAULT
    normalized["retries"] = retries

    return normalized

# ----------------- Selector processing -----------------
_select_re = re.compile(
    r"""^\s*([a-zA-Z0-9_-]+)          # tag
        (?:\.([a-zA-Z0-9_-]+)        # optional .prop
            (?:=(?:'|")?(.*?)(?:'|")?)?  # optional = 'value'
        )?\s*$""",
    re.VERBOSE,
)

def _process_bs4_select(soup: Any, select: str) -> Any:
    """
    Process select expressions.
    - 'tag' -> element text(s)
    - 'tag.prop' -> attribute values
    - "tag.prop='value'" -> filter by attribute equality and return text(s)
    - 'css:selector' and optional '@attr' (e.g. css:div.card@data-id)
    Note: `soup` annotated as Any to avoid type-checker runtime name issues.
    """
    if BeautifulSoup is None:
        raise RuntimeError("bs4 is required for HTML selection (install beautifulsoup4)")

    select = select.strip()
    # CSS syntax: css:selector[@attr]
    if select.startswith("css:"):
        payload = select[4:]
        if "@" in payload:
            css_sel, attr = payload.rsplit("@", 1)
            css_sel = css_sel.strip()
            found = soup.select(css_sel)
            vals = []
            for el in found:
                if attr in el.attrs:
                    v = el.attrs.get(attr)
                    if isinstance(v, list):
                        vals.append(" ".join(map(str, v)))
                    else:
                        vals.append(str(v))
            return vals[0] if len(vals) == 1 else vals
        else:
            found = soup.select(payload)
            results = [el.get_text(strip=True) for el in found]
            return results[0] if len(results) == 1 else results

    # try tag.prop pattern
    m = _select_re.match(select)
    if not m:
        # fallback: treat select as CSS selector
        try:
            found = soup.select(select)
        except Exception as e:
            raise ValueError(f"Invalid select expression: {select} ({e})")
        results = [el.get_text(strip=True) for el in found]
        return results[0] if len(results) == 1 else results

    tag, prop, val = m.group(1), m.group(2), m.group(3)
    if prop is None:
        found = soup.find_all(tag)
        results = [el.get_text(strip=True) for el in found]
        return results[0] if len(results) == 1 else results

    # prop exists
    if val is None:
        found = soup.find_all(tag)
        vals = []
        for el in found:
            if prop in el.attrs:
                v = el.attrs.get(prop)
                if isinstance(v, list):
                    vals.append(" ".join(map(str, v)))
                else:
                    vals.append(str(v))
        return vals[0] if len(vals) == 1 else vals
    else:
        found = soup.find_all(tag, attrs={prop: val})
        results = [el.get_text(strip=True) for el in found]
        return results[0] if len(results) == 1 else results

# ----------------- Fetching single request -----------------
def _fetch_one(session: requests.Session, normalized: Dict[str, Any], *,
               ua: Optional[str] = None, proxies: Optional[dict] = None,
               start_delay: float = 0.0) -> Dict[str, Any]:
    """
    Execute a single validated/normalized request.
    - start_delay: seconds to sleep before starting this request (scheduling)
    Returns structured result dict: {ok, status, content, error, parser, url}
    """
    # scheduling sleep
    if start_delay and start_delay > 0:
        time.sleep(float(start_delay))

    url = normalized["url"]
    method = normalized["method"]
    headers = dict(normalized.get("headers") or {})
    params = dict(normalized.get("queries") or {})
    timeout = normalized.get("timeout", DEFAULT_TIMEOUT)
    parser = normalized.get("parser", "text")
    body = normalized.get("body", None)
    retries = int(normalized.get("retries", MAX_RETRIES_DEFAULT))

    if ua:
        headers.setdefault("User-Agent", ua)

    result: Dict[str, Any] = {"ok": False, "status": None, "content": None, "error": None, "parser": parser, "url": url}

    last_exc = None
    for attempt in range(0, retries + 1):
        try:
    
            #validate local file 
            is_local_or_raw = not url.startswith(("http://", "https://"))
            if is_local_or_raw and parser != "bs4":
                raise Exception("Local file or raw content is only supported with 'bs4' parser.")
            #if not local file fetch data from url
            if not is_local_or_raw:
              if method == "GET":
                r = session.get(url, headers=headers, params=params, timeout=timeout, proxies=proxies)
              else:
                if isinstance(body, dict):
                    r = session.request(method, url, headers=headers, params=params, json=body, timeout=timeout, proxies=proxies)
                else:
                    r = session.request(method, url, headers=headers, params=params, data=body, timeout=timeout, proxies=proxies)
              result["status"] = r.status_code
              result["ok"] = 200 <= r.status_code < 300

            if parser == "json":
                try:
                    result["content"] = r.json()
                except Exception as e:
                    result["error"] = f"JSON parse error: {e}"
                    result["content"] = r.text
            elif parser == "text":
                result["content"] = r.text
            #(strict bs4 parser)
            elif parser == "sbs4":
                if BeautifulSoup is None:
                    raise RuntimeError("bs4 not installed")
                soup = BeautifulSoup(r.text, "html.parser")
                sel = normalized.get("select")
                if sel:
                    try:
                        result["content"] = _process_bs4_select(soup, sel)
                    except Exception as e:
                        result["error"] = f"select processing error: {e}"
                        result["content"] = None
                else:
                    result["content"] = soup.prettify()
            #(normal bs4 parser)
            elif parser == "bs4":
                if BeautifulSoup is None:
                   raise RuntimeError("bs4 not installed")

                # NEW: Support local file or raw HTML string
                if url.startswith(("http://", "https://")):
                   html_content = r.text
                else:
                   # Treat as local file path or raw HTML
                   if os.path.isfile(url):
                     with open(url, "r", encoding="utf-8", errors="ignore") as f:
                          html_content = f.read()
                   else:
                        # Assume raw HTML string
                         html_content = url

                soup = BeautifulSoup(html_content, "html.parser")
                sel = normalized.get("select")
                if sel:
                  try:
                     result["content"] = _process_bs4_select(soup, sel)
                  except Exception as e:
                      result["error"] = f"select processing error: {e}"
                      result["content"] = None
                else:
                     result["content"] = soup.prettify()
                result["status"] = "Done"
                result["ok"] = True
                
            return result

        except requests.RequestException as e:
            last_exc = e
            result["error"] = f"request error (attempt {attempt}): {e}"
            if attempt < retries:
                delay = BACKOFF_FACTOR * (2 ** attempt)
                time.sleep(delay)
                continue
            else:
                result["ok"] = False
                result["status"] = None
                return result
        except Exception as e:
            result["ok"] = False
            result["error"] = f"unexpected error: {e}"
            return result

    if last_exc:
        result["ok"] = False
        result["error"] = str(last_exc)
    return result

def _format_size(n: float) -> str:
    """human-readable bytes"""
    for unit in ("B","KB","MB","GB","TB"):
        if n < 1024.0:
            return f"{n:3.1f}{unit}"
        n /= 1024.0
    return f"{n:.1f}PB"

def _print_progress_bar(prefix: str, downloaded: int, total: Optional[int], start_time: float):
    """
    Prints a single-line progress bar using colorama.
    If total is None, show downloaded bytes only.
    """
    elapsed = max(1e-6, time.time() - start_time)
    speed = downloaded / elapsed  # bytes/sec
    if total and total > 0:
        pct = min(1.0, downloaded / total)
        filled = int(pct * _BAR_LEN)
        bar = "[" + Fore.GREEN + "=" * filled + Fore.RESET + " " * (_BAR_LEN - filled) + "]"
        pct_text = f"{pct*100:5.1f}%"
        left_text = f"{_format_size(downloaded)}/{_format_size(total)}"
    else:
        bar = "[" + Fore.GREEN + "=" * min(_BAR_LEN, int(downloaded/1024)) + Fore.RESET + "]"
        pct_text = "  N/A"
        left_text = f"{_format_size(downloaded)}"
    speed_text = f"{_format_size(speed)}/s"
    elapsed_text = f"{int(elapsed)}s"
    out = f"\r{prefix} {bar} {pct_text} {left_text} {speed_text} {elapsed_text}"
    print(out + " " * 5, end="", flush=True)

def _clear_line():
    print("\r" + " " * 160 + "\r", end="", flush=True)

# ----- Single-stream download with progress -----
def stream_download(url: str,
                    filename: str,
                    session: Optional[requests.Session] = None,
                    chunk_size: int = 8192,
                    timeout: int = 30,
                    show_progress: bool = True,
                    headers: Optional[Dict[str,str]] = None,
                    proxies: Optional[Dict[str,str]] = None) -> Tuple[str, Dict[str, Any]]:
    """
    Download a file by streaming and show a colorama progress bar.
    Returns (filename, metadata_dict).
    metadata_dict includes: status_code, total (int or None), error (if any)
    """
    sess = session or requests.Session()
    meta = {"status_code": None, "total": None, "error": None}
    start_time = time.time()
    downloaded = 0

    try:
        with sess.get(url, stream=True, timeout=timeout, headers=headers, proxies=proxies) as r:
            r.raise_for_status()
            total = r.headers.get("Content-Length")
            total_n = int(total) if total and total.isdigit() else None
            meta["total"] = total_n
            meta["status_code"] = r.status_code

            # ensure target dir exists
            os.makedirs(os.path.dirname(os.path.abspath(filename)) or ".", exist_ok=True)

            with open(filename, "wb") as fh:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if not chunk:
                        continue
                    fh.write(chunk)
                    downloaded += len(chunk)
                    if show_progress:
                        _print_progress_bar("Downloading:", downloaded, total_n, start_time)
    except Exception as e:
        meta["error"] = str(e)
        # cleanup partial file?
        # leave partial for resume possibility — caller can remove if desired
        if show_progress:
            _clear_line()
            print(Fore.RED + f"Download failed: {e}" + Fore.RESET)
        raise
    else:
        if show_progress:
            _print_progress_bar("Downloading:", downloaded, total_n, start_time)
            print()  # newline after finished
        return filename, meta

# ----- Segmented (IDM-like) downloader -----
def segmented_download(url: str,
                       filename: str,
                       parts: int = 4,
                       session: Optional[requests.Session] = None,
                       chunk_size: int = 8192,
                       timeout: int = 30,
                       headers: Optional[Dict[str,str]] = None,
                       proxies: Optional[Dict[str,str]] = None,
                       max_workers: Optional[int] = None,
                       show_progress: bool = True,
                       retries: int = 2) -> Tuple[str, Dict[str, Any]]:
    """
    Download by splitting into 'parts' byte ranges and fetching concurrently.
    If server doesn't support ranges or content-length unknown, falls back to stream_download.
    Returns (filename, metadata) where metadata contains status and per-part info.
    """
    sess = session or requests.Session()
    meta: Dict[str, Any] = {"status_code": None, "supports_ranges": False, "total": None, "parts": parts, "parts_meta": []}

    # 1) HEAD to get size and support for ranges
    try:
        head = sess.head(url, timeout=timeout, allow_redirects=True, headers=headers, proxies=proxies)
        meta["status_code"] = head.status_code
        # prefer Content-Length from HEAD, fallback to GET later
        total = head.headers.get("Content-Length")
        total_n = int(total) if total and total.isdigit() else None
        accept_ranges = head.headers.get("Accept-Ranges", "").lower()
    except Exception:
        # If HEAD fails, try a lightweight GET for headers (not streaming body)
        try:
            r = sess.get(url, stream=True, timeout=timeout, headers=headers, proxies=proxies)
            r.raise_for_status()
            total = r.headers.get("Content-Length")
            total_n = int(total) if total and total.isdigit() else None
            accept_ranges = r.headers.get("Accept-Ranges", "").lower()
            r.close()
        except Exception as e:
            # cannot determine -> fallback to single stream
            if show_progress:
                print(Fore.YELLOW + "Could not get HEAD info; falling back to single-stream download." + Fore.RESET)
            return stream_download(url, filename, session=sess, chunk_size=chunk_size, timeout=timeout, show_progress=show_progress, headers=headers, proxies=proxies), meta

    meta["total"] = total_n
    meta["supports_ranges"] = (accept_ranges == "bytes")

    if total_n is None or not meta["supports_ranges"]:
        # Attempt a small-range request to test range support
        try:
            test_headers = dict(headers or {})
            test_headers["Range"] = "bytes=0-0"
            tr = sess.get(url, headers=test_headers, timeout=timeout, stream=True, proxies=proxies)
            supports = tr.status_code == 206  # partial content
            tr.close()
            if supports:
                meta["supports_ranges"] = True
            else:
                meta["supports_ranges"] = False
        except Exception:
            meta["supports_ranges"] = False

    if total_n is None or not meta["supports_ranges"]:
        if show_progress:
            print(Fore.YELLOW + "Server does not support ranged downloads or size unknown — using single-stream download." + Fore.RESET)
        return stream_download(url, filename, session=sess, chunk_size=chunk_size, timeout=timeout, show_progress=show_progress, headers=headers, proxies=proxies), meta

    # 2) Calculate ranges
    total_bytes = total_n
    part_size = total_bytes // parts
    ranges: List[Tuple[int,int]] = []
    for i in range(parts):
        start = i * part_size
        end = ((i + 1) * part_size - 1) if i < parts - 1 else (total_bytes - 1)
        ranges.append((start, end))

    # 3) Prepare temp files and shared counters
    temp_dir = tempfile.mkdtemp(prefix="segdl_")
    part_files: List[str] = [os.path.join(temp_dir, f"part_{i}") for i in range(parts)]
    downloaded_lock = threading.Lock()
    total_downloaded = 0

    start_time = time.time()

    # helper to download single range with retries
    def _download_range(i: int, byte_range: Tuple[int,int]) -> Dict[str, Any]:
        nonlocal total_downloaded
        start, end = byte_range
        headers_here = dict(headers or {})
        headers_here["Range"] = f"bytes={start}-{end}"
        attempt = 0
        part_meta = {"index": i, "range": (start, end), "size": end - start + 1, "downloaded": 0, "error": None, "status": None}
        while attempt <= retries:
            try:
                with sess.get(url, headers=headers_here, stream=True, timeout=timeout, proxies=proxies) as r:
                    part_meta["status"] = r.status_code
                    r.raise_for_status()
                    with open(part_files[i], "wb") as fh:
                        for chunk in r.iter_content(chunk_size=chunk_size):
                            if not chunk:
                                continue
                            fh.write(chunk)
                            chunk_len = len(chunk)
                            part_meta["downloaded"] += chunk_len
                            with downloaded_lock:
                                nonlocal_var = globals().get("__placeholder__", None)  # no-op to avoid linter warnings
                                # update outer total
                                nonlocal_total = None
                                # but Python cannot assign to outer variable unless nonlocal declared; we mutate through closure using list
                            # We'll instead use a mutable container:
                    # success
                break
            except Exception as e:
                attempt += 1
                part_meta["error"] = str(e)
                if attempt <= retries:
                    time.sleep(0.5 * attempt)
                    continue
                else:
                    return part_meta
        return part_meta

    # The above attempt to mutate outer total via nonlocal was avoided for clarity.
    # We'll implement a proper worker that reports progress through a queue-like pattern.

    # Revised design: use per-part loops that update a shared dict via lock.
    shared = {"downloaded": 0}
    parts_meta: List[Dict[str,Any]] = [{"index": i, "range": ranges[i], "size": ranges[i][1]-ranges[i][0]+1, "downloaded": 0, "error": None, "status": None} for i in range(parts)]

    def _worker(i: int):
        headers_here = dict(headers or {})
        start, end = ranges[i]
        headers_here["Range"] = f"bytes={start}-{end}"
        attempt = 0
        pmeta = parts_meta[i]
        while attempt <= retries:
            try:
                with sess.get(url, headers=headers_here, stream=True, timeout=timeout, proxies=proxies) as r:
                    pmeta["status"] = r.status_code
                    r.raise_for_status()
                    with open(part_files[i], "wb") as fh:
                        for chunk in r.iter_content(chunk_size=chunk_size):
                            if not chunk:
                                continue
                            fh.write(chunk)
                            chunk_len = len(chunk)
                            pmeta["downloaded"] += chunk_len
                            with downloaded_lock:
                                shared["downloaded"] += chunk_len
                            if show_progress:
                                _print_progress_bar("Downloading (parts):", shared["downloaded"], total_bytes, start_time)
                # finished this part successfully
                return
            except Exception as e:
                attempt += 1
                pmeta["error"] = str(e)
                if attempt <= retries:
                    time.sleep(0.5 * attempt)
                    continue
                else:
                    return

    # 4) Launch workers
    if max_workers is None:
        max_workers = parts
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(_worker, i) for i in range(parts)]
        # Wait for all to complete
        for fut in as_completed(futures):
            pass

    # final progress print
    if show_progress:
        _print_progress_bar("Downloading (parts):", shared["downloaded"], total_bytes, start_time)
        print()

    # Check for errors and sizes
    ok = True
    for i, pm in enumerate(parts_meta):
        if pm.get("error"):
            ok = False
    if not ok:
        # cleanup temp files? we keep them for debugging but try to remove
        # attempt to remove the temp dir
        try:
            for f in part_files:
                if os.path.exists(f):
                    os.remove(f)
            os.rmdir(temp_dir)
        except Exception:
            pass
        raise Exception(f"One or more parts failed; see parts_meta for details: {parts_meta}")

    # 5) Join parts
    os.makedirs(os.path.dirname(os.path.abspath(filename)) or ".", exist_ok=True)
    with open(filename, "wb") as fh_out:
        for part_file in part_files:
            with open(part_file, "rb") as pf:
                while True:
                    buf = pf.read(8192)
                    if not buf:
                        break
                    fh_out.write(buf)

    # cleanup temp
    try:
        for f in part_files:
            os.remove(f)
        os.rmdir(temp_dir)
    except Exception:
        pass

    meta["parts_meta"] = parts_meta
    return filename, meta

# ----- High-level helper that decides which method to use -----
def download_from_request(req: Dict[str,Any],
                          *,
                          session: Optional[requests.Session] = None) -> Dict[str,Any]:
    """
    Inspect request dict and perform file download if `download` true.
    Expected keys:
      - url (required)
      - save_as (filename) or derive name from URL
      - download_parts (int) optional: try segmented download
      - chunk_size, timeout, show_progress, headers, proxies, retries
    Returns metadata dict.
    """
    url = req.get("url")
    if not url:
        raise ValueError("request dict missing 'url'")

    # ----- NEW: Default save path -----
    save_as = req.get("save_as") or req.get("save") or req.get("saveto")

    if not save_as:
        # No path given → use user's Downloads folder
        username = getpass.getuser()
        downloads_dir = os.path.join("C:\\Users", username, "Downloads")
        os.makedirs(downloads_dir, exist_ok=True)
        save_as = os.path.join(downloads_dir, os.path.basename(urlparse(url).path) or "download.bin")
    else:
        # Path given but no filename → use server filename
        save_path = Path(save_as)
        if save_path.is_dir() or not save_path.suffix:
            filename_from_url = os.path.basename(urlparse(url).path) or "download.bin"
            save_as = str(save_path / filename_from_url)

    # Rest of your function remains unchanged...
    
    parts = int(req.get("download_parts", 0) or 0)
    chunk_size = int(req.get("chunk_size", 8192))
    timeout = int(req.get("timeout", 30))
    headers = req.get("headers")
    proxies = req.get("proxies")
    retries = int(req.get("retries", 2))
    show_progress = bool(req.get("show_progress", True))

    sess = session or requests.Session()

    if parts and parts > 1:
        # try segmented download
        try:
            (fname, meta) = segmented_download(url, save_as, parts=parts, session=sess, chunk_size=chunk_size, timeout=timeout, headers=headers, proxies=proxies, show_progress=show_progress, retries=retries)
            return {"ok": True, "method": "segmented", "filename": fname, "meta": meta}
        except Exception as e:
            # fallback to stream download for robustness
            if show_progress:
                print(Fore.YELLOW + "Segmented download failed, falling back to single-stream: " + str(e) + Fore.RESET)
            (fname, meta2) = stream_download(url, save_as, session=sess, chunk_size=chunk_size, timeout=timeout, show_progress=show_progress, headers=headers, proxies=proxies)
            return {"ok": True, "method": "stream_fallback", "filename": fname, "meta": meta2}
    else:
        (fname, meta) = stream_download(url, save_as, session=sess, chunk_size=chunk_size, timeout=timeout, show_progress=show_progress, headers=headers, proxies=proxies)
        return {"ok": True, "method": "stream", "filename": fname, "meta": meta}
    
    
    
    
# ----------------- Main function -----------------
def fetch_requests(requests_list: List[Union[str, Dict[str, Any]]], *,
                   save: Optional[str] = None,
                   save_json: Optional[str] = None,
                   max_workers: int = 8,
                   rotate_user_agents: bool = True,
                   default_headers: Optional[dict] = None,
                   proxies: Optional[dict] = None,
                   default_retries: int = MAX_RETRIES_DEFAULT,
                   delay_between_requests: float = 0.0,
                   per_request_schedule: Optional[List[float]] = None) -> Dict[str, Any]:
    """
    requests_list: list of items (plain URL strings, compact strings, or dicts)
    save: filename -> save concatenated plain-text fetched results
    save_json: filename -> save FULL details (structured JSON)
    max_workers: concurrency
    rotate_user_agents: rotate built-in UA pool (True) or single UA
    default_headers: headers merged with per-request headers
    proxies: requests-compatible proxies dict
    default_retries: default per-request retries when not specified
    delay_between_requests: schedule requests at i * delay_between_requests seconds (unless overridden)
    per_request_schedule: optional list of start_delay floats (same length as requests_list), overrides above
    """

    # Validate per_request_schedule if provided
    if per_request_schedule is not None:
        if not isinstance(per_request_schedule, list) or len(per_request_schedule) != len(requests_list):
            raise ValueError("per_request_schedule must be a list with the same length as requests_list")

    # Normalize inputs and validate early
    normalized_items: List[Dict[str, Any]] = []
    for idx, itm in enumerate(requests_list):
        try:
            norm = _normalize_item(itm)
            if "retries" not in norm or norm.get("retries") is None:
                norm["retries"] = default_retries
            if default_headers:
                hdrs = dict(default_headers)
                hdrs.update(norm.get("headers") or {})
                norm["headers"] = hdrs
            normalized_items.append(norm)
        except Exception as e:
            normalized_items.append({"_validation_error": str(e), "url": getattr(itm, "url", f"invalid_{idx}")})

    # Prepare UA pool and session
    ua_pool = list(_UA_POOL) if rotate_user_agents else [(_DEFAULT_UA_POOL)]
    ua_len = len(ua_pool)
    session = requests.Session()

    # Prepare concurrent execution
    results_ordered: List[Optional[Dict[str, Any]]] = [None] * len(normalized_items)
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {}
        for i, norm in enumerate(normalized_items):
            if "_validation_error" in norm:
                results_ordered[i] = {
                    "ok": False,
                    "status": None,
                    "content": None,
                    "error": f"validation error: {norm['_validation_error']}",
                    "parser": None,
                    "url": norm.get("url", f"invalid_{i}")
                }
                continue

            # Determine start_delay precedence:
            # 1) per_request_schedule list (if given)
            # 2) per-request 'delay' field
            # 3) global delay_between_requests * i
            if per_request_schedule is not None:
                start_delay = float(per_request_schedule[i] or 0.0)
            else:
                start_delay = float(norm.get("delay", 0.0) or 0.0)
                if start_delay == 0.0 and delay_between_requests:
                    start_delay = float(i) * float(delay_between_requests)

            ua = ua_pool[i % ua_len]
            fut = ex.submit(_fetch_one, session, norm, ua=ua, proxies=proxies, start_delay=start_delay)
            futures[fut] = i

        # Collect results as they finish, preserving original order by assigning into results_ordered
        for fut in as_completed(futures):
            idx = futures[fut]
            
            try:
                res = fut.result()
            except Exception as e:
                res = {"ok": False, "status": None, "content": None, "error": f"executor error: {e}", "parser": None, "url": normalized_items[idx].get("url")}
            results_ordered[idx] = res

    # Build aggregated mapping and plain text list
    aggregated: Dict[str, Any] = {}
    plain_text_results: List[str] = []
    for i, (orig, res) in enumerate(zip(requests_list, results_ordered)):
        key = str(i)
        aggregated[key] = {"request": orig, **(res or {})}
        content = (res or {}).get("content")
        if content is None:
            plain_text_results.append("")
        else:
            if isinstance(content, (dict, list)):
                try:
                    text_content = json.dumps(content, ensure_ascii=False, indent=2)
                except Exception:
                    text_content = str(content)
            else:
                text_content = str(content)
            plain_text_results.append(text_content)

    # Save plain text if requested
    if save:
        try:
            with open(save, "w", encoding="utf-8", errors="replace") as fh:
                joined = [t for t in plain_text_results if t]

                #for multiple requests results
                if len(joined) > 1:
                  for jon in joined: 
                     fh.write(TEXT_SEPARATOR)
                     try:
                        jtype = ast.literal_eval(jon)
                        if isinstance(jtype, list):
                           fh.write(RESULT_SEPARATOR.join(jtype))
                        else:
                           fh.write(jon)
                     except: #parsing error
                        fh.write(jon)
            
                else:
                  joinedblocks = TEXT_SEPARATOR.join(joined)
                  try:  
                    jtype = ast.literal_eval(joinedblocks)
                    if isinstance(jtype, list):
                      fh.write(RESULT_SEPARATOR.join(jtype))
                    else:
                      fh.write(TEXT_SEPARATOR.join(joined))
                  except: #parsing error
                     fh.write(TEXT_SEPARATOR.join(joined))
                

        except Exception as e:
            aggregated["_save_error"] = str(e)

    # Save JSON details if requested
    if save_json:
        try:
            with open(save_json, "w", encoding="utf-8") as gf:
                json.dump(aggregated, gf, ensure_ascii=False, indent=2)
        except Exception as e:
            aggregated["_save_json_error"] = str(e)

    # Default behavior: print plain text results only (no status/errors), joined and in order
    if not save and not save_json and not returndata:
        out_blocks = [t for t in plain_text_results if t]
        
        if out_blocks:
             #for multiple requests results
             if len(out_blocks) > 1:
               for out in out_blocks: 
                 print(TEXT_SEPARATOR)
                 try:
                   gettype = ast.literal_eval(out)
                   if isinstance(gettype, list):
                     print(RESULT_SEPARATOR.join(gettype))
                   else:
                     print(out)
                 except: #parsing error
                     print(out)
            
             else:
              joinblocks = TEXT_SEPARATOR.join(out_blocks)
              try:  
               gettype = ast.literal_eval(joinblocks)
               if isinstance(gettype, list):
                  print(RESULT_SEPARATOR.join(gettype))
               else:
                 print(TEXT_SEPARATOR.join(out_blocks))
              except: #parsing error
                 print(TEXT_SEPARATOR.join(out_blocks))
        else:
            # print nothing if no content
            print("", end="")

    if returndata:
        fulldata.clear()
        out_blocks = [t for t in plain_text_results if t]
        
        if out_blocks:
             #for multiple requests results
             if len(out_blocks) > 1:
               for out in out_blocks: 
                 fulldata.append(TEXT_SEPARATOR)
                 try:
                   gettype = ast.literal_eval(out)
                   if isinstance(gettype, list):
                     fulldata.append(RESULT_SEPARATOR.join(gettype))
                   else:
                     fulldata.append(out)
                 except: #parsing error
                     fulldata.append(out)
            
             else:
              joinblocks = TEXT_SEPARATOR.join(out_blocks)
              try:  
               gettype = ast.literal_eval(joinblocks)
               if isinstance(gettype, list):
                  fulldata.append(RESULT_SEPARATOR.join(gettype))
               else:
                 fulldata.append(TEXT_SEPARATOR.join(out_blocks))
              except: #parsing error
                 fulldata.append(TEXT_SEPARATOR.join(out_blocks))
        else:
            # print nothing if no content
            fulldata.append("")
        
    return aggregated




#------------------- worker function----------------------------
def prompt(msg: str, default: Optional[str] = None) -> str:
    if default is None:
        s = input(f"{msg} ").strip()
    else:
        s = input(f"{msg} [{default}] ").strip()
        if not s:
            s = default
    return s

def load_list_from_path(path: str) -> List[Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, "rt", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Invalid JSON file")
    return data

def parse_inline_list(text: str) -> List[Any]:
    """
    Try to parse text as JSON list; if that fails, try to treat as a single compact string wrapped as a list.
    """
    text = text.strip()
    if not text:
        return []
    # If it looks like a list or object, try JSON
    if text.startswith("[") or text.startswith("{"):
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return parsed
            elif isinstance(parsed, dict):
                return [parsed]
        except Exception as e:
            raise ValueError(f"Invalid JSON provided: {e}")
    # Otherwise, treat it as a single compact string or URL
    return [text]

def ask_yesno(prompt_text: str, default_yes: bool = True) -> bool:
    default = "Y/n" if default_yes else "y/N"
    r = input(f"{prompt_text} ({default}): ").strip().lower()
    if not r:
        return default_yes
    return r[0] == "y"


def usehelp():
    try: 
        print("\nfetcher — interactive starter\nType 'exit' at any prompt to quit.\n")
        # Input mode
        mode = prompt("Enter input mode: \n(1) Paste list, \n(2) Path to JSON file \n(3) Download file \n(4) Download using json \n(enter 1,2,3 or 4)", "1")
        if mode.lower() in ("exit", "quit"):
            return
        
        if mode.strip() == "3":
            dp = 0
            url = prompt("Enter file url")
            if url.lower() in ("exit", "quit"):
                return
            saveto = prompt("Enter path to save the file")
            if saveto.lower() in ("exit", "quit"):
                return
            if not saveto:
                saveto = None
                
            sd = prompt("Do you want to use segmented download type for faster downloads (Y/n)","y")
            if sd.lower() in ("exit", "quit"):
                return
            
            if sd.lower() == "y":
                dp = prompt("Enter the number of download parts",0)
                try: 
                    int(dp)
                except:
                    print("Invalid download parts value - ignoring")
                    dp = 0
            req = {"url":url,"save_as":saveto,"download_parts":dp}
            os.system('cls' if os.name == 'nt' else 'clear') 
            print("\nStarting download")
            rundownload = download_from_request(req=req)   
            ask = input("\n Task completed do you want to see the aggregated data (y/n)")
            if ask.lower() == "y":
               os.system('cls' if os.name == 'nt' else 'clear') 
               print(rundownload)
            return
        
        if mode.strip() == "4":
            jsonfile = prompt("Enter json file path")
            if jsonfile.lower() in ("exit", "quit"):
                return
            
            if Path(jsonfile).suffix == '.json' and os.path.exists(jsonfile):
                  requests_list = load_list_from_path(jsonfile)
                  #get the dict data
                  req = requests_list[0]
                  os.system('cls' if os.name == 'nt' else 'clear') 
                  print("\nStarting download")
                  rundownload = download_from_request(req=req)   
                  ask = input("\n Task completed do you want to see the aggregated data (y/n)")
                  if ask.lower() == "y":
                    os.system('cls' if os.name == 'nt' else 'clear') 
                    print(rundownload)
            else:
                print("Check your json file path if it exists and is valid json file")
            return
        
        
        if mode.strip() == "2":
            path = prompt("Enter path to JSON file containing a list of requests (absolute or relative)")
            if path.lower() in ("exit", "quit"):
                return
            requests_list = load_list_from_path(path)
        else:
            print("\nPaste your request LIST (JSON array or compact lines). End with a blank line.")
            print("Example: [\"https://example.com\", \"url=https://x;parser=bs4;select=h1\"]\n")
            lines = []
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                if line.strip().lower() in ("exit", "quit"):
                    return
                if line.strip() == "":
                    break
                lines.append(line)
            raw = "\n".join(lines).strip()
            if not raw:
                print("No input provided — exiting.")
                return
            requests_list = parse_inline_list(raw)

        # Save options
        save_filename = prompt("Save plain-text results to (leave blank to print to screen)", "")
        save_filename = save_filename.strip() or None

        save_json_filename = prompt("Save full JSON details to (filename.json) (leave blank to skip)", "")
        save_json_filename = save_json_filename.strip() or None

        # Concurrency and timing
        max_workers = prompt("Max workers (concurrency)", "8")
        try:
            max_workers_i = int(max_workers)
        except Exception:
            max_workers_i = 8

        delay_between_requests = prompt("Global delay between requests in seconds (float)", "0.0")
        try:
            delay_between_requests_f = float(delay_between_requests)
        except Exception:
            delay_between_requests_f = 0.0

        # Optional per-request schedule
        per_request_schedule = None
        use_schedule = ask_yesno("Do you want to provide a per-request schedule (list of start times)?", False)
        if use_schedule:
            s = prompt("Enter JSON array of start times (e.g. [0.0,5.0,10.0])")
            try:
                arr = json.loads(s)
                if isinstance(arr, list):
                    per_request_schedule = [float(x) for x in arr]
                else:
                    print("Invalid schedule — ignoring.")
                    per_request_schedule = None
            except Exception:
                print("Invalid schedule — ignoring.")
                per_request_schedule = None

        rotate_ua = ask_yesno("Rotate user agents? (recommended to reduce blocks)", True)

        # Proxies
        proxies = None
        use_proxies = ask_yesno("Use a proxies dictionary for all requests? (enter JSON style)", False)
        if use_proxies:
            ptxt = prompt("Enter proxies dict as JSON (e.g. {\"http\":\"http://x:port\",\"https\":\"http://x:port\"})", "")
            try:
                proxies = json.loads(ptxt)
                if not isinstance(proxies, dict):
                    proxies = None
            except Exception:
                print("Invalid proxies JSON — ignoring proxies.")
                proxies = None
                
        os.system('cls' if os.name == 'nt' else 'clear') 
        print("\nStarting fetch — this may take a while depending on requests and schedule...\n")

        # Call fetch_requests
        aggregated = fetch_requests(
            requests_list,
            save=save_filename,
            save_json=save_json_filename,
            max_workers=max_workers_i,
            rotate_user_agents=rotate_ua,
            proxies=proxies,
            delay_between_requests=delay_between_requests_f,
            per_request_schedule=per_request_schedule
        )
        

        # If saved plain text or saved json, inform user briefly
        if save_filename:
            print(f"\nPlain text results saved to: {save_filename}")
        if save_json_filename:
            print(f"Full details saved to: {save_json_filename}")
            
            
        ask = input("\n Task completed do you want to see the aggregated data (y/n)")
        if ask.lower() == "y":
            os.system('cls' if os.name == 'nt' else 'clear') 
            print(aggregated)
            
        # If neither saved, results were printed to screen by fetch_requests already.
        print("\nDone. Press Enter to exit.")
        input()
    except Exception as e:
        raise Exception(e)





"""
fetcher
-fetch "[url1,url2]"  or -fetch-json "json filename" 

-save filename or -save-json jsonfilename
-max-worker number
-request-delays float
-request-schedule [0.0,5.0,10.0]
-rotate-user-agents" yes|no
-proxies {\"http\":\"http://x:port\",\"https\":\"http://x:port\"}
-retries number
-show-aggregated
-timeout float
-method get|post etc
-backoff-factor float
-text-separator string "\n\n-----\n\n"
-result-separator string "\n\n######\n\n"
-headers Dict
-getdata   

download arguments
-fetch-download to download direct instead of fetch
-fetch-download-json to use json file instead of args
-url string
-saveto string
-split-download number
-chunk-size number
-timeout number
-headers dict
-proxies dict
-retries number
-show-progress yes/no


"""
    
def main(commandlist: List):
    global MAX_RETRIES_DEFAULT,DEFAULT_TIMEOUT,VALID_METHODS,returndata 
    global DEFAULT_METHOD,BACKOFF_FACTOR,TEXT_SEPARATOR,RESULT_SEPARATOR
    if len(commandlist) == 1 and commandlist[0] == "fetcher":
        usehelp()
        return
    try:
        my_header = None
        mode = None
        save_filename = None
        save_json_filename = None
        max_workers_i = 8
        rotate_ua = True
        proxies = None
        my_header = None
        delay_between_requests_f = 0.0
        per_request_schedule = None
        
        
        if "-fetch" in commandlist:
            mode="1"
    
        elif "-fetch-json" in commandlist:
           mode="2"
       
       
        #if user uses downloads
        elif "-fetch-download" in commandlist: 
          req= {}
          try:
            if  "-url" in commandlist:
                  nm = commandlist.index("-url") + 1
                  req["url"] = commandlist[nm]
            else:
                raise Exception("Usage: -fetch-download -url 'site url' -saveto 'path to save'")
            if "-saveto" in commandlist:
                nm = commandlist.index("-saveto") + 1
                req["save_as"] = commandlist[nm]
            else:
                req["save_as"] = None
                #raise Exception("Usage: -fetch-download -url 'site url' -saveto 'path to save'")
            
            if "-split-download" in commandlist:
                nm = commandlist.index("-split-download") + 1
                try:
                  req["download_parts"] = int(commandlist[nm])
                except Exception as e:
                    raise Exception("Invalid value in -split-download")
            
            if "-chunk-size" in commandlist:
                nm = commandlist.index("-chunk-size") + 1
                try:
                  req["chunk_size"] = int(commandlist[nm])
                except Exception as e:
                    raise Exception("Invalid value in -chunk-size")
            
            if "-timeout" in commandlist:
                nm = commandlist.index("-timeout") + 1
                try:
                  req["timeout"] = int(commandlist[nm])
                except Exception as e:
                    raise Exception("Invalid value in -timeout")
                
            if "-headers" in commandlist:    
               nm = commandlist.index("-headers") + 1
               hdr = commandlist[nm].strip()
               try:
                  my_header = ast.literal_eval(hdr)
                  if not isinstance(my_header,Dict):
                    raise Exception("Improper format in -headers try {\"Authorization\":\"Bearer TOKEN\"} next time")
                  else:
                     req["headers"] = my_header        
               except Exception:
                 raise Exception("Invalid  value in -headers")  
                 
                
            if "-proxies" in commandlist:    
               nm = commandlist.index("-proxies") + 1
               prx = commandlist[nm].strip()
               try:
                  my_proxy = ast.literal_eval(prx)
                  if not isinstance(my_proxy,Dict):
                    raise Exception("Improper format in -proxies try {\"http\":\"http://p1:port\",\"https\":\"http://p1:port\"} next time")
                  else:
                     req["proxies"] = my_proxy   
                          
               except Exception:
                 raise Exception("Invalid  value in -headers")  
                    
            if "-retries" in commandlist:
               nm = commandlist.index("-retries") + 1
               try:
                  req["retries"] = int(commandlist[nm])
               except Exception as e:
                  raise Exception("Invalid value in -retries")    
              
            if "-show-progress" in commandlist:
               try:
                 nm = commandlist.index("-show-progress") + 1
                 vle = commandlist[nm].strip()
                 if vle.lower() == "yes":
                   req["show_progress"] = True
                 else:
                   req["show_progress"] = False
               except:
                  raise Exception("Invalid value in -show-progress try yes|no next time")
            
            rundownload = download_from_request(req=req)
            
            if "-show-aggregated" in commandlist:
              print(rundownload)
            return
          except Exception as e:
              raise Exception (f"fetch-download error : {e}")
         
        elif "-fetch-download-json" in commandlist:
          try:
            nm = commandlist.index("-fetcher-download-json") + 1
            jsonfile = commandlist[nm]
            if Path(jsonfile).suffix == '.json' and os.path.exists(jsonfile):
               requests_list = load_list_from_path(jsonfile)
               #get the dict data
               req = requests_list[0]
               rundownload = download_from_request(req=req)
               
               if "-show-aggregated" in commandlist:
                  print(rundownload)
                  
               return
            else:
                raise Exception("must be a json file")  
          except Exception as e:
              raise Exception("fetcher json file error")
          
        if mode is None:
            #close if nothing was selected
            return  
        
        if mode== "2":
            nm = commandlist.index("-fetch-json") + 1
            jsonfile = commandlist[nm]
            if Path(jsonfile).suffix == '.json':
               requests_list = load_list_from_path(jsonfile)
            else:
                raise Exception("must be a json file")
            
        else:
            try:
              nm = commandlist.index("-fetch") + 1
              raw_data = commandlist[nm]
              try:
                  requests_list = json.loads(raw_data)
              except json.JSONDecodeError:
                 requests_list = ast.literal_eval(raw_data)
    
              if not isinstance(requests_list, list):
                    raise ValueError("Invalid or no URL input provided. Try: [\"url1\", \"url2\"]")


            except (json.JSONDecodeError, ValueError) as e:
               raise Exception(f"URL parse error: {e}. Check your JSON syntax.")
            except IndexError:
               raise Exception("No input found after -fetch. Example: -fetch '[{\"url\":\"https://example.com\"}]'")
            except Exception as e:
               raise Exception(f"URL parse error: {e}")
            
        if "-save" in commandlist:
          nm = commandlist.index("-save") + 1
          savefile = commandlist[nm]
          # Save options
          save_filename =  savefile.strip() or None
        
        if "-save-json" in commandlist:
          nm = commandlist.index("-save-json") + 1
          savejsonfile = commandlist[nm]
          # Save options
          save_json_filename = savejsonfile.strip() or None

        # Concurrency and timing
        if "-max-worker" in commandlist:
           nm = commandlist.index("-max-worker") + 1
           max_workers = commandlist[nm]
           try:
              max_workers_i = int(max_workers)
           except Exception:
              max_workers_i = 8

        if "-request-delays"  in commandlist:
           nm = commandlist.index("-request-delays") + 1
           delay_between_requests = commandlist[nm]
           try:
              delay_between_requests_f = float(delay_between_requests)
           except Exception:
              delay_between_requests_f = 0.0

        # Optional per-request schedule
        per_request_schedule = None
        if "-request-schedule"  in commandlist:
           try:
                nm = commandlist.index("-request-schedule") + 1
                s = commandlist[nm]
                arr = json.loads(s)
                if isinstance(arr, list):
                    per_request_schedule = [float(x) for x in arr]
                else:
                    print("Invalid schedule — ignoring.")
                    per_request_schedule = None
           except Exception:
                print("Invalid schedule — ignoring.")
                per_request_schedule = None
        
        
        if "-rotate-user-agents" in commandlist:
          rotate_ua = False
          try:
            nm = commandlist.index("-rotate-user-agents") + 1
            vle = commandlist[nm].strip()
            if vle.lower() == "yes":
              rotate_ua = True
            else:
               rotate_ua = False 
          except:
              print("Invalid value in -rotate-user-agents — ignoring.")
              rotate_ua = False
              
        # Proxies
        proxies = None
        if "-proxies"  in commandlist:
            nm = commandlist.index("-proxies") + 1
            ptxt = commandlist[nm]
            try:
                proxies = ast.literal_eval(ptxt)
                if not isinstance(proxies, dict):
                    proxies = None
            except Exception:
                print("Invalid -proxies — ignoring proxies.")
                proxies = None

        if "-retries" in commandlist:
            
            nm = commandlist.index("-retries") + 1
            rtis = commandlist[nm].strip()
            try:
               MAX_RETRIES_DEFAULT = int(rtis)
            except Exception:
                 MAX_RETRIES_DEFAULT = 2
                 print("Invalid  value in -retries — ignoring")
        
        if "-timeout" in commandlist:   
            nm = commandlist.index("-timeout") + 1
            tio = commandlist[nm].strip()
            try:
               DEFAULT_TIMEOUT = float(tio)
            except Exception:
                 DEFAULT_TIMEOUT = 10.0
                 print("Invalid  value in -timeout — ignoring")
        
        if "--backoff-factor" in commandlist:   
            nm = commandlist.index("--backoff-factor") + 1
            tio = commandlist[nm].strip()
            try:
               BACKOFF_FACTOR = float(tio)
            except Exception:
                 BACKOFF_FACTOR = 0.5
                 print("Invalid  value in -backoff-factor — ignoring")
                 
                 
        if "-method" in commandlist:
            nm = commandlist.index("-method") + 1
            mthod = commandlist[nm].strip()
            try:
                if not mthod.upper() in VALID_METHODS:
                    print("Invalid  value in -method — ignoring")
                else:    
                   DEFAULT_METHOD = mthod.upper()
            except Exception:
                 DEFAULT_METHOD = "GET"
                 print("Invalid  value in -method — ignoring")
        
     
        if "-text-separator" in commandlist:
            nm = commandlist.index("-text-separator") + 1
            tsr = commandlist[nm].strip()
            try:
                TEXT_SEPARATOR = f"\n\n{tsr}\n\n" 
            except Exception:
                 TEXT_SEPARATOR = "\n\n-----\n\n" 
                 print("Invalid  value in -text-separator — ignoring")
 
        
        if "-result-separator" in commandlist:
            nm = commandlist.index("-result-separator") + 1
            rsr = commandlist[nm].strip()
            try:
                RESULT_SEPARATOR = f"\n\n{rsr}\n\n"
            except Exception:
                 RESULT_SEPARATOR = "\n\n######\n\n"
                 print("Invalid  value in -result-separator — ignoring")
 
        if "-headers" in commandlist:
            nm = commandlist.index("-headers") + 1
            hdr = commandlist[nm].strip()
            try:
                my_header = ast.literal_eval(hdr)
                if not isinstance(my_header,Dict):
                    print("Improper format in -headers try {\"Authorization\":\"Bearer TOKEN\"} next time —  ignoring")
                    my_header = None
            except Exception:
                 my_header = None
                 print("Invalid  value in -headers — ignoring")
        
        if "-getdata" in commandlist:
            returndata = True
        
        #print("\nStarting fetch — this may take a while depending on requests and schedule...\n")

        # Call fetch_requests
        aggregated = fetch_requests(
            requests_list,
            save=save_filename,
            save_json=save_json_filename,
            max_workers=max_workers_i,
            rotate_user_agents=rotate_ua,
            proxies=proxies,
            default_headers=my_header,
            delay_between_requests=delay_between_requests_f,
            per_request_schedule=per_request_schedule
        )
        
        if "-show-aggregated" in commandlist:
            print(aggregated)
        
        if "-getdata" in commandlist and fulldata:
              returndata = False
              getall = "\n".join(fulldata)
              fulldata.clear()
              return getall
        # If saved plain text or saved json, inform user briefly
        #if save_filename:
        #    print(f"\nPlain text results saved to: {save_filename}")
        #if save_json_filename:
        #    print(f"Full details saved to: {save_json_filename}")
        
    except Exception as e:
        raise e





# ----------------- End of module -----------------
