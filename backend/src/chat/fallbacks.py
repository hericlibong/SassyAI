TIMEOUT_FALLBACK_MESSAGE = (
    "The sarcasm engine is taking an unscheduled nap. Try again in a moment."
)
PROVIDER_ERROR_FALLBACK_MESSAGE = (
    "The sarcasm engine tripped over its own ego. Please try again shortly."
)


def get_timeout_fallback() -> str:
    return TIMEOUT_FALLBACK_MESSAGE


def get_provider_error_fallback() -> str:
    return PROVIDER_ERROR_FALLBACK_MESSAGE
