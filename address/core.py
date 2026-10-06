"""地址解析与批量去重。"""

MIN_LOCAL = 3
INTERNAL_DOMAINS = frozenset(["internal.example"])


class Counter:
    """记录本轮检查过的已见地址条数。"""

    def __init__(self):
        self.scanned = 0


def _err(reason):
    return {"status": "error", "reason": reason, "normalized": None}


def parse(addr):
    if addr.count("@") != 1:
        return _err("bad-form")
    local, domain = addr.split("@")
    if not local or not domain:
        return _err("bad-form")
    if local.startswith(".") or local.endswith("."):
        return _err("bad-local")
    if len(local) < MIN_LOCAL:
        return _err("bad-local")
    if ".." in domain:
        return _err("bad-domain")
    for label in domain.split("."):
        if not label:
            return _err("bad-domain")
    return {"status": "ok", "reason": None, "normalized": local + "@" + domain}


def check_all(addrs, counter):
    out = []
    seen = []
    valid = 0
    for addr in addrs:
        result = parse(addr)
        row = {"address": addr, "status": result["status"], "reason": result["reason"],
               "normalized": result["normalized"]}
        if result["status"] == "ok":
            valid += 1
            dup = False
            for item in seen:
                counter.scanned += 1
                if item == result["normalized"]:
                    dup = True
                    break
            if not dup:
                seen.append(result["normalized"])
        row["scanned"] = counter.scanned
        out.append(row)
    return {"rows": out, "valid": valid, "unique": len(seen), "scanned": counter.scanned}
