"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "dots":
        out = core.parse("a..b@x.com")
        _line({"status": out["status"], "reason": out["reason"]})
        return 0
    if name == "label":
        out = core.parse("user@-bad.com")
        _line({"status": out["status"], "reason": out["reason"]})
        return 0
    if name == "case":
        got = core.check_all(["User@X.com", "User@x.com"], core.Counter())
        _line({"unique": got["unique"]})
        return 0
    if name == "internal":
        out = core.parse("ab@internal.example")
        _line({"status": out["status"], "normalized": out["normalized"]})
        return 0
    if name == "work":
        addrs = ["user%04d@x.com" % i for i in range(2000)]
        got = core.check_all(addrs, core.Counter())
        _line({"addresses": 2000, "scanned": got["scanned"]})
        return 0
    raise SystemExit("未知场景：" + name)
