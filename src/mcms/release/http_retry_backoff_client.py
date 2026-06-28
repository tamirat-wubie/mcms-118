from __future__ import annotations

from dataclasses import dataclass

@dataclass
class HTTPRetryBackoffClientResult:
    request_key: str
    status_code: int
    attempt_count: int
    max_attempts: int
    retry_after_seconds: int | None
    rate_limit_reset_epoch: int | None
    now_epoch: int
    selected_wait_seconds: int
    retry_allowed: bool
    retry_status: str
    explanation: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def evaluate_http_retry_backoff(request_key: str, status_code: int, attempt_count: int, max_attempts: int, retry_after_seconds: int | None, rate_limit_reset_epoch: int | None, now_epoch: int, base_backoff_seconds: int = 2) -> HTTPRetryBackoffClientResult:
    if not request_key or status_code < 100 or attempt_count < 0 or max_attempts <= 0 or now_epoch < 0 or base_backoff_seconds <= 0:
        return HTTPRetryBackoffClientResult(request_key, status_code, attempt_count, max_attempts, retry_after_seconds, rate_limit_reset_epoch, now_epoch, 0, False, "insufficient_data", "Retry/backoff input is invalid.")
    if attempt_count >= max_attempts:
        status="retry_budget_exhausted"; allowed=False; wait=0; explanation="Retry budget is exhausted."
    elif retry_after_seconds is not None and retry_after_seconds >= 0:
        status="retry_after_header_honored"; allowed=True; wait=retry_after_seconds; explanation="Retry-After header is honored."
    elif rate_limit_reset_epoch is not None and rate_limit_reset_epoch > now_epoch:
        status="rate_limit_reset_honored"; allowed=True; wait=rate_limit_reset_epoch-now_epoch; explanation="Rate-limit reset epoch is honored."
    elif status_code in {408,425,429,500,502,503,504}:
        status="exponential_backoff_selected"; allowed=True; wait=base_backoff_seconds*(2**attempt_count); explanation="Retryable status uses exponential backoff."
    elif 200 <= status_code < 400:
        status="retry_not_required"; allowed=False; wait=0; explanation="Request succeeded; retry is not required."
    else:
        status="non_retryable_error"; allowed=False; wait=0; explanation="HTTP status is not retryable."
    if wait > 3600:
        status="retry_safety_boundary"; allowed=False; explanation="Retry wait exceeds safety boundary."
    return HTTPRetryBackoffClientResult(request_key, status_code, attempt_count, max_attempts, retry_after_seconds, rate_limit_reset_epoch, now_epoch, wait, allowed, status, explanation)
