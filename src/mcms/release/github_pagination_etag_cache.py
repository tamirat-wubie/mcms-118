from __future__ import annotations

from dataclasses import dataclass

@dataclass
class GitHubPaginationETagCacheResult:
    cache_key: str
    request_path: str
    status_code: int
    etag: str
    cached_etag: str
    link_header: str
    page_count_seen: int
    max_pages: int
    next_page_url: str
    cache_status: str
    explanation: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def parse_github_next_link(link_header: str) -> str:
    if not link_header:
        return ""
    for part in link_header.split(','):
        section = part.strip()
        if 'rel="next"' not in section:
            continue
        if section.startswith('<') and '>' in section:
            return section[1:section.index('>')]
    return ""


def evaluate_github_pagination_etag_cache(cache_key: str, request_path: str, status_code: int, etag: str, cached_etag: str, link_header: str, page_count_seen: int, max_pages: int) -> GitHubPaginationETagCacheResult:
    if not cache_key or not request_path or page_count_seen < 0 or max_pages <= 0:
        return GitHubPaginationETagCacheResult(cache_key, request_path, status_code, etag, cached_etag, link_header, page_count_seen, max_pages, "", "insufficient_data", "GitHub pagination/cache input is invalid.")
    next_page = parse_github_next_link(link_header)
    if status_code == 304:
        status="github_not_modified"; explanation="GitHub response is not modified; cached response can be reused."
    elif cached_etag and etag and cached_etag == etag:
        status="github_cache_hit"; explanation="ETag matches cached value."
    elif page_count_seen >= max_pages:
        status="github_pagination_conflict"; explanation="Maximum page count reached before pagination completed."
    elif next_page:
        status="github_next_page_detected"; explanation="GitHub Link header contains next page."
    elif etag:
        status="github_etag_saved"; explanation="GitHub ETag can be saved for future conditional requests."
    else:
        status="github_all_pages_collected"; explanation="No next page is present; all pages are collected."
    return GitHubPaginationETagCacheResult(cache_key, request_path, status_code, etag, cached_etag, link_header, page_count_seen, max_pages, next_page, status, explanation)
