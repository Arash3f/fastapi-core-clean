import logging

from app.utils.error_codes import ERROR_MESSAGES


def resolve_message(code, lang: str) -> str:
    if lang not in ERROR_MESSAGES:
        lang = "en"
    msg = ERROR_MESSAGES[lang].get(code)
    if msg:
        return msg
    logging.getLogger(__name__).warning(
        "Missing translation for code '%s' in language '%s'", code, lang
    )
    return "Unknown error"
