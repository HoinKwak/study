"""시간대 유틸 — 저장은 UTC, 표시는 KST(한국 표준시, UTC+9).

내부 타임스탬프는 UTC(offset-aware)로 저장하고, 사람에게 보여줄 때만 KST로 변환한다.
과거에 tz 없이 저장된 값(naive)은 UTC로 간주해 변환한다.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))


def kst_display(iso: str | None, fmt: str = "%m-%d %H:%M") -> str:
    """ISO8601 문자열 → KST 벽시계 표시. 파싱 실패 시 원문 반환."""
    if not iso:
        return "-"
    try:
        dt = datetime.fromisoformat(iso)
    except (ValueError, TypeError):
        return iso
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(KST).strftime(fmt)


def kst_struct(epoch_secs: float):
    """logging 포매터용 — epoch 초를 KST struct_time 으로."""
    return datetime.fromtimestamp(epoch_secs, KST).timetuple()
