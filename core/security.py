import hashlib
import hmac
import logging

import requests
from django.conf import settings
from django.core.cache import cache


logger = logging.getLogger(__name__)


TURNSTILE_VERIFY_URL = (
    "https://challenges.cloudflare.com/turnstile/v0/siteverify"
)

TURNSTILE_MAX_TOKEN_LENGTH = 2048


class TurnstileError(Exception):
    """Base exception for Turnstile verification failures."""


class TurnstileUnavailableError(TurnstileError):
    """Raised when Cloudflare cannot be reached or is misconfigured."""


class RateLimitExceeded(Exception):
    """Raised when too many enquiries are submitted in one period."""


def get_client_ip(request):
    """
    Return the client IP address observed by Heroku.

    Heroku appends the originating address it detects to the right-hand
    side of X-Forwarded-For. The value is used only temporarily for
    Turnstile verification and rate limiting. It is not stored in the
    ContactEnquiry model or written to logs.
    """
    forwarded_for = request.META.get(
        "HTTP_X_FORWARDED_FOR",
        "",
    )

    if forwarded_for:
        addresses = [
            address.strip()
            for address in forwarded_for.split(",")
            if address.strip()
        ]

        if addresses:
            return addresses[-1]

    return request.META.get(
        "REMOTE_ADDR",
        "",
    ).strip()


def get_rate_limit_key(request):
    """
    Create a keyed, non-readable cache key for the client address.

    The raw address is not placed in the cache key or saved in the
    ContactEnquiry database record.
    """
    client_ip = get_client_ip(request) or "unknown"

    digest = hmac.new(
        key=settings.SECRET_KEY.encode("utf-8"),
        msg=client_ip.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()

    return f"contact-rate-limit:{digest}"


def enforce_contact_rate_limit(request):
    """
    Limit repeated contact-form submissions in a fixed time window.

    Only a keyed digest and temporary submission count are stored.
    The entry expires automatically after the configured window.
    """
    limit = settings.CONTACT_RATE_LIMIT
    window = settings.CONTACT_RATE_LIMIT_WINDOW
    cache_key = get_rate_limit_key(request)

    attempts = cache.get(
        cache_key,
        0,
    )

    if attempts >= limit:
        logger.warning(
            "Contact-form rate limit exceeded."
        )
        raise RateLimitExceeded

    cache.set(
        cache_key,
        attempts + 1,
        timeout=window,
    )


def verify_turnstile(request):
    """
    Verify the submitted Cloudflare Turnstile token.

    Returns True only if Cloudflare accepts the token and the configured
    hostname and action match the verification response.
    """
    token = request.POST.get(
        "cf-turnstile-response",
        "",
    ).strip()

    if not token:
        return False

    if len(token) > TURNSTILE_MAX_TOKEN_LENGTH:
        logger.warning(
            "Turnstile token exceeded the permitted length."
        )
        return False

    if not settings.TURNSTILE_SECRET_KEY:
        logger.error(
            "Turnstile secret key is not configured."
        )
        raise TurnstileUnavailableError

    payload = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": token,
    }

    client_ip = get_client_ip(request)

    if client_ip:
        payload["remoteip"] = client_ip

    try:
        response = requests.post(
            TURNSTILE_VERIFY_URL,
            data=payload,
            timeout=settings.TURNSTILE_TIMEOUT,
        )

        response.raise_for_status()
        result = response.json()

    except (
        requests.RequestException,
        ValueError,
    ) as exc:
        logger.exception(
            "Turnstile verification service could not be reached."
        )

        raise TurnstileUnavailableError from exc

    if not result.get("success"):
        logger.warning(
            "Turnstile rejected a contact-form submission. "
            "Error codes: %s",
            result.get("error-codes", []),
        )

        return False

    expected_hostname = (
        settings.TURNSTILE_EXPECTED_HOSTNAME.strip()
    )

    if expected_hostname:
        returned_hostname = result.get(
            "hostname",
            "",
        ).strip()

        if not hmac.compare_digest(
            returned_hostname,
            expected_hostname,
        ):
            logger.warning(
                "Turnstile hostname mismatch."
            )

            return False

    expected_action = (
        settings.TURNSTILE_EXPECTED_ACTION.strip()
    )

    if expected_action:
        returned_action = result.get(
            "action",
            "",
        ).strip()

        if not hmac.compare_digest(
            returned_action,
            expected_action,
        ):
            logger.warning(
                "Turnstile action mismatch."
            )

            return False

    return True