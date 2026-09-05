"""동적 유니버스에서 top20에 한 번이라도 든 종목(core7 제외)의 klines_1d 존재 기간에 맞춰
metrics(5분 OI) 다운로드 작업 목록(symbol day)을 생성 — stdout으로 출력."""
from __future__ import annotations

import sys

sys.path.insert(0, "/home/user/study/research/backtests/repro/oi-hhi-original-design-tautology-check")
import common  # noqa: E402


def main() -> None:
    univ = common.build_dynamic_universe()
    need = [s for s in univ.members_ever if s not in common.CORE7]
    lines = []
    for s in need:
        k = common.load_klines_1d(s)
        if k.empty:
            continue
        for d in k.index:
            lines.append(f"{s} {d.date().isoformat()}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
