"""Dune Analytics 무료 API 클라이언트 — 쿼리 생성·실행·폴링·결과조회.

무료 키로 CRUD(POST /query)·execute 모두 가능(2026-07 실측). UI 없이 SQL을 코드로 돌린다.
키: .env 의 DUNE_API_KEY. 프록시: HTTPS_PROXY 자동.
"""
from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path

_BASE = "https://api.dune.com/api/v1"


def _key() -> str:
    k = os.environ.get("DUNE_API_KEY")
    if not k:
        env = Path(__file__).resolve().parents[2] / ".env"
        if env.exists():
            for ln in env.read_text().splitlines():
                if ln.startswith("DUNE_API_KEY="):
                    k = ln.split("=", 1)[1].strip()
                    break
    if not k:
        raise RuntimeError("DUNE_API_KEY 없음(.env 확인)")
    return k


def _req(method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        _BASE + path, data=data, method=method,
        headers={"X-Dune-API-Key": _key(), "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:  # noqa: S310
        return json.load(r)


def create_query(name: str, sql: str, private: bool = True) -> int:
    """SQL로 쿼리 생성 → query_id."""
    r = _req("POST", "/query", {"name": name, "query_sql": sql, "is_private": private})
    return int(r["query_id"])


def update_query(query_id: int, sql: str) -> None:
    _req("PATCH", f"/query/{query_id}", {"query_sql": sql})


def run(query_id: int, params: dict | None = None, poll: float = 3.0, timeout: float = 300.0) -> list[dict]:
    """쿼리 실행 후 완료까지 폴링, 결과 rows 반환."""
    body = {"query_parameters": params} if params else None
    ex = _req("POST", f"/query/{query_id}/execute", body)
    eid = ex["execution_id"]
    t0 = time.time()
    while time.time() - t0 < timeout:
        st = _req("GET", f"/execution/{eid}/status")
        state = st.get("state")
        if state == "QUERY_STATE_COMPLETED":
            res = _req("GET", f"/execution/{eid}/results")
            return res.get("result", {}).get("rows", [])
        if state in ("QUERY_STATE_FAILED", "QUERY_STATE_CANCELLED"):
            raise RuntimeError(f"Dune 실행 실패: {state} — {st.get('error')}")
        time.sleep(poll)
    raise TimeoutError("Dune 실행 타임아웃")


def run_sql(name: str, sql: str, params: dict | None = None, **kw) -> list[dict]:
    """SQL을 즉석 생성해 실행(1회성). query_id 재사용이 필요하면 create_query+run 사용."""
    qid = create_query(name, sql)
    return run(qid, params=params, **kw)


if __name__ == "__main__":
    # 프로브: Solana DEX 테이블 존재·컬럼 확인
    rows = run_sql(
        "memewallet_probe",
        "SELECT block_time, trader_id, amount_usd, "
        "token_bought_symbol, token_sold_symbol "
        "FROM dex_solana.trades LIMIT 3",
    )
    print("dex_solana.trades 프로브 OK, 샘플:")
    for r in rows:
        print(" ", r)
