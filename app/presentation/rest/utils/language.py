def detect_language(request) -> str:
    raw = request.headers.get("accept-language", "en")
    value = raw.lower().strip()
    if value.startswith("fa") or "fa" in value:
        return "fa"
    return "en"
