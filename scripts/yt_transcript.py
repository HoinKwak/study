"""유튜브 영상 자막(트랜스크립트) 추출 — yt-dlp 래퍼.

    python -m scripts.yt_transcript "https://www.youtube.com/watch?v=..."
    python -m scripts.yt_transcript <video_id> --lang en --out out.txt --meta

- 프록시(HTTPS_PROXY 환경변수)를 자동 사용한다(원격 실행 환경 대응).
- 수동 자막 우선, 없으면 자동생성 자막. 여러 언어면 --lang 으로 접두 지정(기본 en).
- json3 → vtt 순으로 파싱해 평문으로 합친다(중복 라인 제거).
- 프로그램적으로는 fetch_transcript(url) 로 dict 반환.

CAPTCHA·로그인월로 막히는 서드파티 트랜스크립트 사이트 대신, yt-dlp 로 유튜브
자막 API 를 직접 받아 안정적으로 추출한다. (유튜브 전략·전망 영상 분석 파이프라인용)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def _base_cmd(proxy: str | None) -> list[str]:
    cmd = ["yt-dlp"]
    proxy = proxy or os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    if proxy:
        cmd += ["--proxy", proxy]
    return cmd


def _video_meta(url: str, proxy: str | None) -> dict:
    """제목·채널·업로드일·조회수 등 메타 (--print 로 한 줄씩)."""
    fields = ["title", "uploader", "upload_date", "duration", "view_count", "id"]
    fmt = "\n".join(f"%({f})s" for f in fields)
    try:
        out = subprocess.run(
            _base_cmd(proxy) + ["--skip-download", "--no-warnings", "--print", fmt, url],
            capture_output=True, text=True, timeout=120)
        vals = out.stdout.strip().split("\n")
        return dict(zip(fields, vals)) if len(vals) >= len(fields) else {}
    except (subprocess.SubprocessError, OSError):  # noqa: BLE001
        return {}


def _parse_json3(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    lines: list[str] = []
    for ev in data.get("events", []):
        segs = ev.get("segs")
        if not segs:
            continue
        txt = "".join(s.get("utf8", "") for s in segs).strip()
        if txt and (not lines or lines[-1] != txt):
            lines.append(txt)
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def _parse_vtt(path: Path) -> str:
    lines: list[str] = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or "-->" in ln or ln.upper().startswith(("WEBVTT", "KIND", "LANGUAGE", "NOTE")):
            continue
        ln = re.sub(r"<[^>]+>", "", ln)  # 인라인 타임태그 제거
        if ln and (not lines or lines[-1] != ln):
            lines.append(ln)
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def fetch_transcript(url: str, lang: str = "en", proxy: str | None = None) -> dict:
    """영상 자막을 평문으로 추출.

    반환: {'meta': {...}, 'source_file': str|None, 'transcript': str}. 실패 시 transcript=''.
    """
    meta = _video_meta(url, proxy)
    with tempfile.TemporaryDirectory() as td:
        tmpl = str(Path(td) / "sub.%(ext)s")
        subprocess.run(
            _base_cmd(proxy) + [
                "--skip-download", "--no-warnings",
                "--write-subs", "--write-auto-subs",
                "--sub-langs", f"{lang}.*,{lang}",
                "--sub-format", "json3/vtt/best",
                "-o", tmpl, url],
            capture_output=True, text=True, timeout=240)
        files = list(Path(td).glob("sub.*"))

        def pick(ext: str) -> list[Path]:
            cand = [f for f in files if f.suffix == ext]
            manual = [f for f in cand if "-orig" not in f.name]  # -orig=원본(대개 자동)
            return manual or cand

        text, used = "", None
        for f in pick(".json3"):
            text, used = _parse_json3(f), f.name
            if text:
                break
        if not text:
            for f in pick(".vtt"):
                text, used = _parse_vtt(f), f.name
                if text:
                    break
    return {"meta": meta, "source_file": used, "transcript": text}


def _normalize_url(url: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):  # video id 만 준 경우
        return f"https://www.youtube.com/watch?v={url}"
    return url


def main() -> None:
    ap = argparse.ArgumentParser(description="유튜브 자막(트랜스크립트) 추출 — yt-dlp")
    ap.add_argument("url", help="유튜브 URL 또는 11자 video id")
    ap.add_argument("--lang", default="en", help="자막 언어 접두(기본 en)")
    ap.add_argument("--out", help="저장 파일 경로(미지정 시 stdout)")
    ap.add_argument("--meta", action="store_true", help="상단에 제목·채널 등 메타 출력")
    ap.add_argument("--proxy", help="프록시(기본 HTTPS_PROXY 환경변수)")
    args = ap.parse_args()

    res = fetch_transcript(_normalize_url(args.url), lang=args.lang, proxy=args.proxy)
    if not res["transcript"]:
        print("자막을 찾지 못했습니다(자막 비공개·언어 불일치·차단 가능).", file=sys.stderr)
        sys.exit(2)

    header = ""
    if args.meta and res["meta"]:
        m = res["meta"]
        header = (f"# {m.get('title', '')}\n"
                  f"채널: {m.get('uploader', '')} · 업로드: {m.get('upload_date', '')} · "
                  f"조회수: {m.get('view_count', '')} · 길이(초): {m.get('duration', '')}\n"
                  f"단어수: {len(res['transcript'].split())}\n\n")
    body = header + res["transcript"] + "\n"
    if args.out:
        Path(args.out).write_text(body, encoding="utf-8")
        print(f"저장: {args.out} ({len(res['transcript'].split())} 단어)")
    else:
        sys.stdout.write(body)


if __name__ == "__main__":
    main()
