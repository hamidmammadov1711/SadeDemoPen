def mask_sensitive(data: dict) -> dict:
    return {
        k: "***" if k.lower() in ["password", "token", "secret"] else v
        for k, v in data.items()
    }
