from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import analyze


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze an enterprise workload modernization case.")
    parser.add_argument("input", type=Path, help="Workload JSON")
    parser.add_argument("--output", type=Path, help="Write analysis JSON")
    args = parser.parse_args()
    result = analyze(json.loads(args.input.read_text()))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
