"""Phase 66 permissioned internet access and research ledger."""

from __future__ import annotations

import datetime as dt
import hashlib
import html
import ipaddress
import json
import os
import re
import socket
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path
from typing import Any

from . import legacy, pandas_analysis


INTERNET_FILES = {
    "Internet Access Overview.md": """# Internet Access Overview

Raphael may prepare research requests and, after confirmation, query the local
SearXNG service without opening browser tabs. Results, sources, pandas analysis,
and niche scores are saved locally. One confirmed public URL may also be
reviewed directly.

## Boundary

- Search is confirmation-gated and limited to the local SearXNG provider
- No autonomous browsing loops or browser-tab automation
- No account login
- No credentials
- No purchasing or spending
- No posting, uploading, email, or messaging
- No Command Bus bypass
""",
    "Search Requests.md": "# Internet Search Requests\n\nNo requests recorded yet.\n",
    "Search Results.md": "# Internet Search Results\n\nNo results recorded yet.\n",
    "Source Review.md": "# Internet Source Review\n\nNo sources reviewed yet.\n",
    "Internet Safety Policy.md": """# Internet Safety Policy

## Allowed

- Confirmed headless public-web search through localhost-only SearXNG
- Current information and trend research
- Public software documentation
- Public prices and market analysis
- Etsy and POD research without login or platform actions
- Saving URLs, summaries, uncertainty, and reliability notes locally
- Local pandas analysis and scoring of saved results

## Blocked

- Autonomous browsing loops
- Account login or session use
- Credential collection or storage
- Purchases, subscriptions, bids, or spending
- Posts, uploads, listings, emails, messages, comments, or forms
- External actions beyond confirmed read-only research
- Private, loopback, link-local, or local-network URL fetching

## Truthfulness

Raphael must never claim it searched, opened, or reviewed a source unless that
specific action occurred. Weak or missing evidence must be marked uncertain.
""",
    "Internet Brief.md": "# Internet Brief\n\nNo internet brief generated yet.\n",
}


def internet_root(config: legacy.RaphaelConfig) -> Path:
    return legacy.ensure_safe_path(config.vault / "00_Raphael" / "Internet Access", config)


def state_path(config: legacy.RaphaelConfig) -> Path:
    return legacy.ensure_safe_path(config.os_root / "internet" / "internet_state.json", config)


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2), encoding="utf-8")
    temp.replace(path)


def ensure_internet_access(config: legacy.RaphaelConfig) -> Path:
    root = internet_root(config)
    root.mkdir(parents=True, exist_ok=True)
    for name, content in INTERNET_FILES.items():
        path = root / name
        if not path.exists():
            legacy.write_file(path, content, config)
    if not state_path(config).exists():
        _write_json(state_path(config), {"version": 1, "requests": [], "results": [], "sources": [], "analyses": [], "niche_scores": []})
    return root


def _load_state(config: legacy.RaphaelConfig) -> dict[str, Any]:
    ensure_internet_access(config)
    try:
        data = json.loads(state_path(config).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        data = {"version": 1, "requests": [], "results": [], "sources": [], "analyses": [], "niche_scores": []}
    data.setdefault("version", 1)
    data.setdefault("requests", [])
    data.setdefault("results", [])
    data.setdefault("sources", [])
    data.setdefault("analyses", [])
    data.setdefault("niche_scores", [])
    return data


def _save_state(config: legacy.RaphaelConfig, data: dict[str, Any]) -> None:
    _write_json(state_path(config), data)
    _write_ledgers(config, data)


def _result_by_id(data: dict[str, Any], request_id: str) -> dict[str, Any]:
    target = request_id.strip().upper()
    for item in data["results"]:
        if str(item.get("request_id", "")).upper() == target:
            return item
    raise FileNotFoundError(f"Internet result not found: {request_id}")


def _latest_result(data: dict[str, Any]) -> dict[str, Any]:
    if not data["results"]:
        raise FileNotFoundError("No completed internet results found.")
    return sorted(data["results"], key=lambda row: str(row.get("recorded", "")), reverse=True)[0]


def _make_id(question: str) -> str:
    seed = f"{question}|{dt.datetime.now().isoformat()}".encode("utf-8")
    return f"INET-{dt.datetime.now():%Y%m%d}-{hashlib.sha1(seed).hexdigest()[:8].upper()}"


def _clean_text(value: str, limit: int = 12000) -> str:
    return legacy.redact_secrets(value.strip())[:limit]


def _urls(text: str) -> list[str]:
    found = re.findall(r"https?://[^\s<>()\[\]{}\"']+", text)
    return list(dict.fromkeys(url.rstrip(".,;:") for url in found))


def _uncertainty(source_count: int, summary: str) -> str:
    if source_count == 0:
        return "High — no source URLs were supplied."
    if source_count == 1:
        return "Medium — only one source was supplied; corroboration is recommended."
    if len(summary.strip()) < 80:
        return "Medium — the saved summary is brief."
    return "Low — multiple sources were supplied, subject to source-quality review."


def _request_by_id(data: dict[str, Any], request_id: str) -> dict[str, Any]:
    target = request_id.strip().upper()
    for item in data["requests"]:
        if item["request_id"].upper() == target:
            return item
    raise FileNotFoundError(f"Internet request not found: {request_id}")


def _source_host(url: str) -> str:
    return urllib.parse.urlparse(url).hostname or url


def _source_note(item: dict[str, Any]) -> str:
    snippet = _clean_text(str(item.get("snippet", "")), 140)
    reliability = str(item.get("reliability", "Unreviewed"))
    if snippet:
        return f"{reliability}; {snippet}"
    return str(item.get("reliability_notes", "")) or reliability


def _sentences(text: str) -> list[str]:
    clean = re.sub(r"\s+", " ", _clean_text(text, 2000)).strip()
    if not clean:
        return []
    parts = re.split(r"(?<=[.!?])\s+", clean)
    return [part.strip(" -") for part in parts if len(part.strip(" -")) > 20]


def _prefer_primary_sources(items: list[dict[str, Any]], question: str) -> list[dict[str, Any]]:
    q = question.casefold()

    def score(item: dict[str, Any]) -> tuple[int, int]:
        host = _source_host(str(item.get("url", ""))).casefold()
        title = str(item.get("title", "")).casefold()
        value = 0
        if host.endswith(".gov") or "whitehouse.gov" in host or "weather.gov" in host:
            value += 80
        if host.endswith(".edu"):
            value += 30
        if any(token in host for token in ["docs.", "developer.", "support."]):
            value += 20
        if "weather" in q and ("weather.gov" in host or "weather" in title):
            value += 60
        if "president" in q and ("whitehouse.gov" in host or "president" in title):
            value += 60
        if item.get("reliability") == "High":
            value += 15
        return value, -int(item.get("rank", 999))

    return sorted(items, key=score, reverse=True)


def _overview_answer(question: str, items: list[dict[str, Any]]) -> tuple[str, list[str], str, str]:
    if not items:
        return (
            "I do not have enough saved source material to answer this yet.",
            ["No usable public result rows were saved.", "Run or retry a confirmed headless search.", "Do not treat this as established fact."],
            "Low",
            "No source-backed snippets are available.",
        )
    snippets = [sentence for item in items for sentence in _sentences(str(item.get("snippet", "")))]
    q = question.casefold()
    if "president" in q:
        officeholder = ""
        joined = " ".join(snippets)
        match = re.search(r"\bpresident\s+(?:is|:)\s+([A-Z][A-Za-z .'-]{2,80})", joined)
        if match:
            officeholder = match.group(1).strip(" .")
        if not officeholder:
            match = re.search(r"\b([A-Z][A-Za-z .'-]{2,80})\s+is\s+(?:the\s+)?(?:current\s+)?(?:\d+(?:st|nd|rd|th)\s+)?president\b", joined)
            if match:
                officeholder = match.group(1).strip(" .")
        source_line = snippets[0] if snippets else f"The top source is {items[0].get('title', _source_host(items[0].get('url', '')))}."
        answer = f"The saved sources indicate the president is {officeholder}." if officeholder else source_line
        points = [
            f"Best source found: {items[0].get('title') or _source_host(items[0].get('url', ''))}.",
            "Official or primary sources were prioritized when present.",
            "If sources conflict or omit the officeholder, treat the answer as uncertain.",
        ]
    elif "weather" in q:
        weather_terms = ["temp", "temperature", "high", "heat index", "rain", "wind", "storm", "forecast"]
        weather_bits = [s for s in snippets if any(term in s.casefold() for term in weather_terms)]
        selected = weather_bits[:2] or snippets[:2]
        answer = " ".join(selected) if selected else "Weather sources were found, but their snippets did not include enough current conditions to summarize safely."
        points = [
            "Weather.gov/NWS or local weather sources are preferred when available.",
            "Temperature, high, rain, and wind are only included when present in saved snippets.",
            "For severe weather decisions, open the cited local forecast directly.",
        ]
    else:
        selected = snippets[:3]
        answer = " ".join(selected[:2]) if selected else f"The search found source material for: {question}."
        points = selected[:3] if selected else [
            f"Top source: {items[0].get('title') or _source_host(items[0].get('url', ''))}.",
            f"Saved sources: {len(items)}.",
            "Use snippets or raw JSON for the underlying result rows.",
        ]
    official_count = sum(1 for item in items if str(item.get("reliability")) == "High")
    confidence = "High" if len(items) >= 3 and official_count else "Medium" if len(items) >= 2 else "Low"
    reason = "multiple saved sources were used" + (" with at least one high-reliability source" if official_count else "")
    return answer[:650], points[:3], confidence, reason


def generate_ai_overview(config: legacy.RaphaelConfig, result: dict[str, Any]) -> dict[str, Any]:
    count = max(1, int(getattr(config, "internet_ai_overview_source_count", 3)))
    items = _prefer_primary_sources(list(result.get("items", [])), str(result.get("question", "")))[:count]
    answer, points, confidence, reason = _overview_answer(str(result.get("question", "")), items)
    sources = [
        {
            "rank": index,
            "title": item.get("title") or _source_host(str(item.get("url", ""))),
            "url": item.get("url", ""),
            "note": _source_note(item),
            "snippet": item.get("snippet", ""),
            "reliability": item.get("reliability", "Unreviewed"),
        }
        for index, item in enumerate(items, 1)
    ]
    return {
        "request_id": result.get("request_id", ""),
        "question": result.get("question", ""),
        "answer": answer,
        "key_points": points,
        "sources": sources,
        "confidence": confidence,
        "confidence_reason": reason,
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
    }


def format_ai_overview(overview: dict[str, Any]) -> str:
    source_lines = []
    for index, source in enumerate(overview.get("sources", []), 1):
        title = source.get("title") or _source_host(str(source.get("url", "")))
        note = source.get("note", "")
        url = source.get("url", "")
        source_lines.append(f"{index}. {title} - {note}" + (f"\n   {url}" if url else ""))
    return "\n".join([
        "Answer:",
        str(overview.get("answer", "")).strip() or "No source-backed answer could be generated.",
        "",
        "Key points:",
        *(f"- {point}" for point in overview.get("key_points", [])[:3]),
        "",
        "Sources:",
        *(source_lines or ["No sources available."]),
        "",
        "Confidence:",
        f"{overview.get('confidence', 'Low')} - {overview.get('confidence_reason', 'Insufficient evidence.')}",
    ])


def internet_overview(config: legacy.RaphaelConfig, request_id: str) -> dict[str, Any]:
    data = _load_state(config)
    result = _result_by_id(data, request_id)
    overview = result.get("ai_overview") or generate_ai_overview(config, result)
    result["ai_overview"] = overview
    _save_state(config, data)
    return overview


def internet_latest_overview(config: legacy.RaphaelConfig) -> dict[str, Any]:
    data = _load_state(config)
    return internet_overview(config, _latest_result(data)["request_id"])


def internet_snippets(config: legacy.RaphaelConfig, request_id: str) -> dict[str, Any]:
    data = _load_state(config)
    result = _result_by_id(data, request_id)
    return {
        "request_id": result["request_id"],
        "question": result.get("question", ""),
        "snippets": [
            {
                "rank": item.get("rank"),
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("snippet", ""),
                "reliability": item.get("reliability", "Unreviewed"),
            }
            for item in result.get("items", [])
        ],
    }


def internet_latest_snippets(config: legacy.RaphaelConfig) -> dict[str, Any]:
    data = _load_state(config)
    return internet_snippets(config, _latest_result(data)["request_id"])


def internet_save_overview_to_knowledge(config: legacy.RaphaelConfig, request_id: str = "LATEST") -> Path:
    data = _load_state(config)
    result = _latest_result(data) if request_id.upper() == "LATEST" else _result_by_id(data, request_id)
    overview = result.get("ai_overview") or generate_ai_overview(config, result)
    target = legacy.ensure_safe_path(
        config.vault / "09_Knowledge" / "Research" / "Internet Overviews" / f"{overview.get('request_id', 'INTERNET')}.md",
        config,
    )
    source_lines = [
        f"- [{source.get('title') or _source_host(str(source.get('url', '')))}]({source.get('url', '')}) - {source.get('note', '')}"
        for source in overview.get("sources", [])
    ]
    content = f"""# Internet Overview - {overview.get('request_id', '')}

## Question

{overview.get('question', '')}

## Overview

{format_ai_overview(overview)}

## Preserved Sources

{chr(10).join(source_lines) or "- No sources available."}

## Raw Result Location

Saved in `{state_path(config)}` under request `{overview.get('request_id', '')}`.
"""
    legacy.write_generated_note(target, content, config)
    return target


def internet_raw_result(config: legacy.RaphaelConfig, request_id: str = "LATEST") -> dict[str, Any]:
    data = _load_state(config)
    return _latest_result(data) if request_id.upper() == "LATEST" else _result_by_id(data, request_id)


def format_raw_result(config: legacy.RaphaelConfig, request_id: str = "LATEST") -> str:
    return json.dumps(internet_raw_result(config, request_id), indent=2)


def format_snippets(snippets: dict[str, Any]) -> str:
    lines = [f"Snippets for {snippets.get('request_id', '')}:", ""]
    for item in snippets.get("snippets", []):
        lines.append(f"{item.get('rank')}. {item.get('title')}")
        lines.append(str(item.get("url", "")))
        lines.append(str(item.get("snippet", "")))
        lines.append("")
    return "\n".join(lines).rstrip()


def internet_request(config: legacy.RaphaelConfig, question: str) -> dict[str, Any]:
    if not config.internet_access_enabled:
        raise RuntimeError("Internet Access is disabled in config/settings.json.")
    clean = _clean_text(question, 2000)
    if not clean:
        raise ValueError("Internet question cannot be empty.")
    data = _load_state(config)
    request = {
        "request_id": _make_id(clean),
        "question": clean,
        "status": "Pending Confirmation",
        "provider": config.internet_provider,
        "created": dt.datetime.now().isoformat(timespec="seconds"),
        "search_opened": False,
        "completed": "",
    }
    data["requests"].append(request)
    _save_state(config, data)
    return request


def internet_search(config: legacy.RaphaelConfig, question: str) -> dict[str, Any]:
    if not config.internet_access_enabled:
        raise RuntimeError("Internet Access is disabled in config/settings.json.")
    if config.internet_allow_autonomous_browsing:
        raise RuntimeError("Unsafe configuration: autonomous browsing must remain disabled.")
    if config.internet_allow_account_login or config.internet_allow_external_actions:
        raise RuntimeError("Unsafe configuration: login and external actions must remain disabled.")
    if config.internet_provider == "searxng" and config.internet_headless_search_enabled:
        return internet_headless_search(config, question)
    if config.internet_requires_confirmation:
        legacy.pod_confirmation_granted("Open a read-only public web search for this question?")
    clean = _clean_text(question, 2000)
    data = _load_state(config)
    request = next(
        (row for row in reversed(data["requests"]) if row["question"].casefold() == clean.casefold() and row["status"] != "Completed"),
        None,
    )
    if request is None:
        request = internet_request(config, clean)
        data = _load_state(config)
        request = _request_by_id(data, request["request_id"])
    query_url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": clean})
    opened = False
    if config.internet_provider == "manual_or_browser":
        opened = bool(webbrowser.open(query_url, new=2))
    request["status"] = "Browser Search Opened" if opened else "Approved for Manual Search"
    request["search_opened"] = opened
    request["search_url"] = query_url
    request["approved"] = dt.datetime.now().isoformat(timespec="seconds")
    _save_state(config, data)
    return {
        "request_id": request["request_id"],
        "status": request["status"],
        "search_opened": opened,
        "search_url": query_url,
        "truthfulness": "No result is claimed. Sources and a summary must be recorded explicitly.",
    }


def searxng_status(config: legacy.RaphaelConfig) -> dict[str, Any]:
    url = os.environ.get("SEARXNG_URL", config.searxng_url).rstrip("/")
    try:
        request = urllib.request.Request(
            url + "/search?" + urllib.parse.urlencode({"q": "Raphael health check", "format": "json"}),
            headers={"User-Agent": "RaphaelOS-Headless-Search/1.0", "Accept": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return {
            "enabled": config.internet_headless_search_enabled,
            "healthy": isinstance(payload, dict) and isinstance(payload.get("results", []), list),
            "url": url,
            "http_status": response.status,
            "result_count": len(payload.get("results", [])),
            "error": "",
        }
    except Exception as exc:
        return {
            "enabled": config.internet_headless_search_enabled,
            "healthy": False,
            "url": url,
            "http_status": "",
            "result_count": 0,
            "error": str(exc),
        }


def internet_headless_search(config: legacy.RaphaelConfig, question: str) -> dict[str, Any]:
    if not config.internet_access_enabled or not config.internet_headless_search_enabled:
        raise RuntimeError("Headless Internet Access is disabled in config/settings.json.")
    if config.internet_provider != "searxng":
        raise RuntimeError("internet_provider must be `searxng` for headless search.")
    if config.internet_allow_autonomous_browsing or config.internet_allow_account_login or config.internet_allow_external_actions:
        raise RuntimeError("Unsafe Internet Access configuration detected.")
    if config.internet_requires_confirmation:
        legacy.pod_confirmation_granted("Run a confirmed localhost-only SearXNG search?")
    clean = _clean_text(question, 2000)
    if not clean:
        raise ValueError("Internet query cannot be empty.")
    data = _load_state(config)
    request_row = next(
        (row for row in reversed(data["requests"]) if row["question"].casefold() == clean.casefold() and row["status"] != "Completed"),
        None,
    )
    if request_row is None:
        request_row = internet_request(config, clean)
        data = _load_state(config)
        request_row = _request_by_id(data, request_row["request_id"])
    url = os.environ.get("SEARXNG_URL", config.searxng_url).rstrip("/") + "/search?" + urllib.parse.urlencode({
        "q": clean,
        "format": "json",
        "language": "en",
        "safesearch": 1,
    })
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "RaphaelOS-Headless-Search/1.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    raw_results = payload.get("results", [])
    if not isinstance(raw_results, list):
        raise RuntimeError("SearXNG response did not contain a results array.")
    timestamp = dt.datetime.now().isoformat(timespec="seconds")
    records = []
    for index, item in enumerate(raw_results[: config.internet_max_sources_per_request], 1):
        if not isinstance(item, dict):
            continue
        source_url = str(item.get("url", "")).strip()
        if not source_url.startswith(("http://", "https://")):
            continue
        host = urllib.parse.urlparse(source_url).hostname or ""
        reliability, notes = _reliability(host, str(item.get("title", "")), "")
        records.append({
            "rank": index,
            "title": _clean_text(str(item.get("title", "")), 500),
            "url": source_url,
            "snippet": _clean_text(str(item.get("content", "")), 2000),
            "engine": str(item.get("engine", "")),
            "published_date": str(item.get("publishedDate", "") or item.get("published_date", "")),
            "timestamp": timestamp,
            "reliability": reliability,
            "reliability_notes": notes,
        })
    request_id = request_row["request_id"]
    result = {
        "request_id": request_id,
        "question": clean,
        "summary": f"Headless SearXNG search saved {len(records)} result(s).",
        "sources": [row["url"] for row in records],
        "source_count": len(records),
        "uncertainty": _uncertainty(len(records), " ".join(row["snippet"] for row in records)),
        "recorded": timestamp,
        "provider": "searxng",
        "headless": True,
        "browser_opened": False,
        "items": records,
    }
    if config.internet_ai_overview_enabled:
        result["ai_overview"] = generate_ai_overview(config, result)
    data["results"] = [row for row in data["results"] if row["request_id"] != request_id]
    data["results"].append(result)
    request_row.update({"status": "Completed", "completed": timestamp, "search_opened": False, "provider": "searxng"})
    known = {row["url"]: row for row in data["sources"]}
    for row in records:
        source = {
            "url": row["url"], "request_id": request_id, "reliability": row["reliability"],
            "title": row["title"], "notes": row["reliability_notes"], "reviewed": timestamp,
        }
        if row["url"] in known:
            known[row["url"]].update(source)
        else:
            data["sources"].append(source)
    _save_state(config, data)
    return result


def internet_analyze_results(config: legacy.RaphaelConfig, request_id: str) -> dict[str, Any]:
    if not config.internet_analysis_with_pandas:
        raise RuntimeError("Pandas Internet analysis is disabled.")
    data = _load_state(config)
    result = next((row for row in data["results"] if row["request_id"].upper() == request_id.upper()), None)
    if not result:
        raise FileNotFoundError(f"Internet result not found: {request_id}")
    records = list(result.get("items", []))
    analysis = pandas_analysis.analyze_records(records)
    analysis.update({"request_id": result["request_id"], "analyzed": dt.datetime.now().isoformat(timespec="seconds")})
    data["analyses"] = [row for row in data["analyses"] if row["request_id"] != result["request_id"]]
    data["analyses"].append(analysis)
    _save_state(config, data)
    return analysis


def internet_niche_score(config: legacy.RaphaelConfig, request_id: str) -> dict[str, Any]:
    data = _load_state(config)
    result = next((row for row in data["results"] if row["request_id"].upper() == request_id.upper()), None)
    if not result:
        raise FileNotFoundError(f"Internet result not found: {request_id}")
    pd = pandas_analysis.require_pandas()
    frame = pd.DataFrame(result.get("items", [])).fillna("")
    corpus = " ".join(
        (frame.get("title", pd.Series(dtype=str)).astype(str) + " " + frame.get("snippet", pd.Series(dtype=str)).astype(str)).tolist()
    ).lower()
    count = int(len(frame))
    demand_terms = sum(corpus.count(term) for term in ["trend", "popular", "best seller", "bestseller", "demand", "gift"])
    competition_terms = sum(corpus.count(term) for term in ["etsy", "amazon", "marketplace", "competitor", "saturated"])
    evergreen_terms = sum(corpus.count(term) for term in ["evergreen", "year round", "timeless", "gift", "hobby", "profession"])
    product_terms = sum(corpus.count(term) for term in ["shirt", "t-shirt", "tee", "apparel", "print", "design", "pod"])
    quality_map = {"High": 100, "Medium-High": 85, "Medium": 65, "Unreviewed": 40}
    source_quality = int(frame.get("reliability", pd.Series(dtype=str)).map(quality_map).fillna(50).mean()) if count else 0
    demand = min(100, 35 + demand_terms * 8 + count * 2)
    competition = min(100, competition_terms * 9 + count * 2)
    evergreen = min(100, 30 + evergreen_terms * 10)
    product_fit = min(100, 25 + product_terms * 9)
    confidence = min(100, count * 10 + (20 if source_quality >= 70 else 0))
    overall = round(demand * .25 + (100 - competition) * .15 + evergreen * .2 + product_fit * .2 + source_quality * .1 + confidence * .1)
    score = {
        "request_id": result["request_id"],
        "demand_signal": demand,
        "competition_signal": competition,
        "evergreen_potential": evergreen,
        "product_fit": product_fit,
        "source_quality": source_quality,
        "confidence": confidence,
        "overall_niche_score": overall,
        "scored": dt.datetime.now().isoformat(timespec="seconds"),
        "result_count": count,
    }
    data["niche_scores"] = [row for row in data["niche_scores"] if row["request_id"] != result["request_id"]]
    data["niche_scores"].append(score)
    _save_state(config, data)
    return score


def internet_result(config: legacy.RaphaelConfig, request_id: str, summary: str) -> dict[str, Any]:
    clean = _clean_text(summary)
    if not clean:
        raise ValueError("Internet result summary cannot be empty.")
    data = _load_state(config)
    request = _request_by_id(data, request_id)
    urls = _urls(clean)[: config.internet_max_sources_per_request]
    uncertainty = _uncertainty(len(urls), clean)
    result = {
        "request_id": request["request_id"],
        "question": request["question"],
        "summary": clean,
        "sources": urls,
        "source_count": len(urls),
        "uncertainty": uncertainty,
        "recorded": dt.datetime.now().isoformat(timespec="seconds"),
    }
    data["results"] = [row for row in data["results"] if row["request_id"] != request["request_id"]]
    data["results"].append(result)
    request["status"] = "Completed"
    request["completed"] = result["recorded"]
    if config.internet_save_sources:
        known = {row["url"] for row in data["sources"]}
        for url in urls:
            if url not in known:
                data["sources"].append({
                    "url": url,
                    "request_id": request["request_id"],
                    "reliability": "Unreviewed",
                    "notes": "Saved from an explicitly recorded result.",
                    "reviewed": "",
                })
    _save_state(config, data)
    return result


def _public_url(url: str) -> tuple[str, str]:
    parsed = urllib.parse.urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Only public http/https URLs are allowed.")
    host = parsed.hostname
    for info in socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80)):
        address = ipaddress.ip_address(info[4][0])
        if (
            address.is_private or address.is_loopback or address.is_link_local
            or address.is_reserved or address.is_multicast or address.is_unspecified
        ):
            raise PermissionError("Private, local, reserved, and link-local URLs are blocked.")
    return parsed.geturl(), host.lower()


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        _public_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _reliability(host: str, title: str, content_type: str) -> tuple[str, str]:
    official_markers = (".gov", ".edu", "docs.", "developer.", "support.")
    if host.endswith(".gov") or host.endswith(".edu"):
        return "High", "Government or educational domain; still verify scope and publication date."
    if any(marker in host for marker in official_markers):
        return "High", "Appears to be official documentation or support material."
    if "documentation" in title.lower() or "application/json" in content_type:
        return "Medium-High", "Structured or documentation-like source; verify publisher identity."
    return "Medium", "Public source reviewed for accessibility only; corroborate important claims."


def internet_source_review(config: legacy.RaphaelConfig, url: str) -> dict[str, Any]:
    if config.internet_requires_confirmation:
        legacy.pod_confirmation_granted("Fetch and review this one public URL without login or credentials?")
    safe_url, host = _public_url(url)
    opener = urllib.request.build_opener(_SafeRedirect())
    request = urllib.request.Request(
        safe_url,
        headers={"User-Agent": "RaphaelOS-Permissioned-Research/1.0", "Accept": "text/html,application/json,text/plain"},
    )
    with opener.open(request, timeout=15) as response:
        final_url, final_host = _public_url(response.geturl())
        content_type = response.headers.get("Content-Type", "")
        body = response.read(1_000_000)
        text = body.decode(response.headers.get_content_charset() or "utf-8", errors="replace")
    title_match = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.I | re.S)
    title = html.unescape(re.sub(r"\s+", " ", title_match.group(1)).strip()) if title_match else final_host
    reliability, notes = _reliability(final_host, title, content_type)
    review = {
        "url": final_url,
        "host": final_host,
        "title": title[:300],
        "content_type": content_type,
        "reliability": reliability,
        "notes": notes,
        "reviewed": dt.datetime.now().isoformat(timespec="seconds"),
        "login_used": False,
        "credentials_used": False,
    }
    data = _load_state(config)
    existing = next((row for row in data["sources"] if row["url"] == final_url), None)
    if existing:
        existing.update(review)
    else:
        data["sources"].append({"request_id": "", **review})
    _save_state(config, data)
    return review


def _write_ledgers(config: legacy.RaphaelConfig, data: dict[str, Any]) -> None:
    root = internet_root(config)
    request_blocks = []
    for row in reversed(data["requests"]):
        request_blocks.append(f"""## {row['request_id']}

- Question: {row['question']}
- Status: {row['status']}
- Provider: {row['provider']}
- Created: {row['created']}
- Search opened: {row.get('search_opened', False)}
- Search URL: {row.get('search_url', '') or 'Not opened'}
- Completed: {row.get('completed', '') or 'No'}
""")
    result_blocks = []
    for row in reversed(data["results"]):
        item_lines = []
        for item in row.get("items", []):
            item_lines.append(
                f"- [{item.get('title', 'Untitled')}]({item.get('url', '')}) "
                f"— {item.get('snippet', '')} "
                f"(reliability: {item.get('reliability', 'Unreviewed')}; "
                f"captured: {item.get('timestamp', row.get('recorded', ''))})"
            )
        analysis = next((item for item in data["analyses"] if item["request_id"] == row["request_id"]), None)
        score = next((item for item in data["niche_scores"] if item["request_id"] == row["request_id"]), None)
        result_blocks.append(f"""## {row['request_id']}

### Question

{row['question']}

### AI Overview

{format_ai_overview(row.get('ai_overview') or generate_ai_overview(config, row)) if row.get('items') else 'No AI overview available.'}

### Summary

{row['summary']}

### Sources

{chr(10).join(f'- {url}' for url in row['sources']) or '- No source URLs supplied.'}

### Headless Results

{chr(10).join(item_lines) or '- No structured result rows supplied.'}

### Pandas Analysis

{json.dumps(analysis, indent=2) if analysis else 'Not analyzed.'}

### Niche Score

{json.dumps(score, indent=2) if score else 'Not scored.'}

### Uncertainty

{row['uncertainty']}

### Recorded

{row['recorded']}
""")
    source_blocks = []
    for row in reversed(data["sources"]):
        source_blocks.append(f"""## {row['url']}

- Request: {row.get('request_id', '') or 'Unlinked'}
- Reliability: {row.get('reliability', 'Unreviewed')}
- Title: {row.get('title', '') or 'Not reviewed'}
- Notes: {row.get('notes', '')}
- Reviewed: {row.get('reviewed', '') or 'No'}
""")
    legacy.write_generated_note(
        root / "Search Requests.md",
        "# Internet Search Requests\n\n" + ("\n".join(request_blocks) if request_blocks else "No requests recorded yet.\n"),
        config,
    )
    legacy.write_generated_note(
        root / "Search Results.md",
        "# Internet Search Results\n\n" + ("\n".join(result_blocks) if result_blocks else "No results recorded yet.\n"),
        config,
    )
    legacy.write_generated_note(
        root / "Source Review.md",
        "# Internet Source Review\n\n" + ("\n".join(source_blocks) if source_blocks else "No sources reviewed yet.\n"),
        config,
    )


def internet_status_data(config: legacy.RaphaelConfig) -> dict[str, Any]:
    data = _load_state(config)
    return {
        "enabled": config.internet_access_enabled,
        "requires_confirmation": config.internet_requires_confirmation,
        "provider": config.internet_provider,
        "save_sources": config.internet_save_sources,
        "allow_autonomous_browsing": config.internet_allow_autonomous_browsing,
        "allow_account_login": config.internet_allow_account_login,
        "allow_external_actions": config.internet_allow_external_actions,
        "max_sources_per_request": config.internet_max_sources_per_request,
        "ai_overview_enabled": config.internet_ai_overview_enabled,
        "ai_overview_default": config.internet_ai_overview_default,
        "ai_overview_source_count": config.internet_ai_overview_source_count,
        "ai_overview_include_sources": config.internet_ai_overview_include_sources,
        "raw_json_on_request_only": config.internet_raw_json_on_request_only,
        "root": str(internet_root(config)),
        "pending": [row for row in data["requests"] if row["status"] != "Completed"],
        "completed": [row for row in data["requests"] if row["status"] == "Completed"],
        "results": data["results"],
        "sources": data["sources"],
        "analyses": data["analyses"],
        "niche_scores": data["niche_scores"],
        "headless_search_enabled": config.internet_headless_search_enabled,
        "pandas_analysis_enabled": config.internet_analysis_with_pandas,
        "searxng": searxng_status(config),
        "pandas": pandas_analysis.pandas_status(),
    }


def internet_status_text(config: legacy.RaphaelConfig) -> str:
    data = internet_status_data(config)
    return f"""# Internet Access Status

- Enabled: {data['enabled']}
- Confirmation required: {data['requires_confirmation']}
- Provider: {data['provider']}
- SearXNG healthy: {data['searxng']['healthy']}
- SearXNG URL: {data['searxng']['url']}
- Headless search enabled: {data['headless_search_enabled']}
- AI overview default: {data['ai_overview_default']}
- pandas analysis: {data['pandas']['status']} {data['pandas']['version']}
- Pending requests: {len(data['pending'])}
- Completed searches: {len(data['completed'])}
- Saved sources: {len(data['sources'])}
- Autonomous browsing: {data['allow_autonomous_browsing']}
- Account login: {data['allow_account_login']}
- External actions: {data['allow_external_actions']}
- Root: `{data['root']}`
"""


def internet_review(config: legacy.RaphaelConfig) -> Path:
    data = internet_status_data(config)
    weak = [row for row in data["results"] if not row["uncertainty"].startswith("Low")]
    content = f"""# Internet Access Review

Generated: {dt.datetime.now().isoformat(timespec='seconds')}

## Summary

- Pending requests: {len(data['pending'])}
- Completed searches: {len(data['completed'])}
- Saved sources: {len(data['sources'])}
- Results needing stronger evidence: {len(weak)}

## Pending

{chr(10).join(f"- `{row['request_id']}` — {row['question']} ({row['status']})" for row in data['pending']) or "- None."}

## Evidence Warnings

{chr(10).join(f"- `{row['request_id']}` — {row['uncertainty']}" for row in weak) or "- No current evidence warnings."}

## Safety

No autonomous browsing, login, credentials, spending, posting, uploading,
email, messaging, or external platform action is enabled.
"""
    path = internet_root(config) / "Internet Access Review.md"
    legacy.write_generated_note(path, content, config)
    return path


def internet_brief(config: legacy.RaphaelConfig) -> Path:
    data = internet_status_data(config)
    latest = data["results"][-5:]
    content = f"""# Internet Brief

Generated: {dt.datetime.now().isoformat(timespec='seconds')}

## Queue

- Pending: {len(data['pending'])}
- Completed: {len(data['completed'])}
- Sources: {len(data['sources'])}

## Latest Findings

{chr(10).join(f"- `{row['request_id']}` — {row['summary'][:300]} — Uncertainty: {row['uncertainty']}" for row in latest) or "- No completed findings."}

## Boundary

This brief summarizes saved evidence only. It does not browse, log in, spend,
post, upload, email, message, or perform external actions.
"""
    path = internet_root(config) / "Internet Brief.md"
    legacy.write_generated_note(path, content, config)
    return path
