"""地址解析与批量去重。"""

MIN_LOCAL = 3
MIN_LOCAL_INTERNAL = 1
MAX_LABEL = 63
INTERNAL_DOMAINS = frozenset(["internal.example"])
_LABEL_CHARS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
)


class Counter:
    """记录本轮检查过的已见地址条数。"""

    def __init__(self):
        self.scanned = 0


def _err(reason):
    return {"status": "error", "reason": reason, "normalized": None}


def _valid_domain(domain):
    for label in domain.split("."):
        if not label or len(label) > MAX_LABEL:
            return False
        if label.startswith("-") or label.endswith("-"):
            return False
        if any(ch not in _LABEL_CHARS for ch in label):
            return False
    return True


def parse(addr):
    if addr.count("@") != 1:
        return _err("bad-form")
    local, domain = addr.split("@")
    if not local or not domain:
        return _err("bad-form")
    if local.startswith(".") or local.endswith(".") or ".." in local:
        return _err("bad-local")
    if not _valid_domain(domain):
        return _err("bad-domain")
    min_local = MIN_LOCAL_INTERNAL if domain.lower() in INTERNAL_DOMAINS else MIN_LOCAL
    if len(local) < min_local:
        return _err("bad-local")
    return {"status": "ok", "reason": None, "normalized": local + "@" + domain.lower()}


def check_all(addrs, counter):
    out = []
    seen = set()
    valid = 0
    for addr in addrs:
        result = parse(addr)
        row = {"address": addr, "status": result["status"], "reason": result["reason"],
               "normalized": result["normalized"]}
        if result["status"] == "ok":
            valid += 1
            counter.scanned += 1
            seen.add(result["normalized"])
        row["scanned"] = counter.scanned
        out.append(row)
    return {"rows": out, "valid": valid, "unique": len(seen), "scanned": counter.scanned}
