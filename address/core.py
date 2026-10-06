"""地址解析与批量去重。"""

MIN_LOCAL = 3
INTERNAL_DOMAINS = frozenset(["internal.example"])


class Counter:
    """记录本轮检查过的已见地址条数。"""

    def __init__(self):
        self.scanned = 0


def _err(reason):
    return {"status": "error", "reason": reason, "normalized": None}


def _valid_domain(domain):
    for label in domain.split("."):
        if not label or len(label) > 63:
            return False
        if label.startswith("-") or label.endswith("-"):
            return False
        for ch in label:
            if not (("a" <= ch <= "z") or ("A" <= ch <= "Z")
                    or ("0" <= ch <= "9") or ch == "-"):
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
    domain = domain.lower()
    min_local = 1 if domain in INTERNAL_DOMAINS else MIN_LOCAL
    if len(local) < min_local:
        return _err("bad-local")
    return {"status": "ok", "reason": None, "normalized": local + "@" + domain}


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
