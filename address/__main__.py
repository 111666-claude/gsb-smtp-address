"""命令行入口。"""

import argparse
import json

from . import core, samples


def main(argv=None):
    ap = argparse.ArgumentParser(prog="address")
    ap.add_argument("--sample", choices=["dots", "label", "case", "internal", "work"])
    sub = ap.add_subparsers(dest="cmd")
    check_parser = sub.add_parser("check")
    check_parser.add_argument("--file", required=True)
    args = ap.parse_args(argv)

    if args.sample:
        return samples.run(args.sample)
    if args.cmd is None:
        ap.print_help()
        return 2

    with open(args.file, encoding="utf-8") as fh:
        addrs = [line.strip() for line in fh if line.strip()]
    out = core.check_all(addrs, core.Counter())
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
