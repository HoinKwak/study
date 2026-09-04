#!/usr/bin/env python3
"""선물 브리핑 다이제스트 생성 — 원자료 6벤뉴 → digest.md + brief_staging.json.

⚠️2026-09-03 컨테이너 재시작으로 스크래치패드가 비워지면서 기존 2단계 파이프라인
   (build_skeleton.py + mkdigest.py)이 통째로 유실됐다. 저장소에 없었던 것이 원인이라
   재작성분은 research/tools/ 에 두고 커밋한다.

사용: python3 build_digest.py <SP> <ts> [prev_ts]
  - <SP>/prices_prev.json 이 있으면 '실측%'(직전 회차 대비 실제 가격변동률)를 산출한다.
    없으면 실측% 열을 '-'로 두고, 다음 회차를 위해 prices_cur.json 을 반드시 남긴다.
  - why/tag 는 저장소의 research/futures/brief.json(직전 발행본)에서 이월한다.
  - 이월 서사가 이번 회차 실측% 부호와 어긋나면 기계적으로 폐기한다(수치는 넣지 않는다).
"""
import json, io, os, re, sys

SP = sys.argv[1]; TS = sys.argv[2]
PREV_TS = sys.argv[3] if len(sys.argv) > 3 else '(미상)'
R = '/home/user/study/research/'
J = lambda f: json.load(io.open(os.path.join(SP, f), encoding='utf-8'))

rows = []           # dict(sec, sym, venue, vol, oi, fund, chg, px)
cur_px = {}         # 'okx:BTC' / 'hl:BTC' -> price

# ---------- OKX (CEX 기준 실측% 소스) ----------
# ⚠️OKX `oi`는 계약 수라 ctVal 환산이 필요하지만 `oiUsd`가 이미 달러라 그대로 쓴다.
oi_map = {x['instId']: float(x.get('oiUsd') or 0) / 1e6
          for x in J('okx_oi.json').get('data', [])}
fund = J('okx_funding.json')
for t in J('okx_raw.json').get('data', []):
    iid = t['instId']
    if not iid.endswith('-USDT-SWAP'): continue
    sym = iid.split('-')[0]
    last = float(t.get('last') or 0)
    if last <= 0: continue
    o24 = float(t.get('open24h') or 0)
    vol = float(t.get('volCcy24h') or 0) * last / 1e6      # ⚠️volCcy24h는 코인 수량이라 last를 곱해야 달러
    f = fund.get(iid, {})
    rows.append(dict(sec='cex', sym=sym, venue='OKX(직접API,신선)', vol=vol,
                     oi=oi_map.get(iid),
                     fund=float(f['fundingRate']) * 100 if f.get('fundingRate') else None,
                     chg=(last / o24 - 1) * 100 if o24 else None, px=last))
    cur_px['okx:' + sym] = last

# ---------- Binance / Bybit / Aster (CoinGecko) ----------
def cg(fn, label, sec='cex'):
    try: d = J(fn)
    except Exception: return
    for t in d.get('tickers', []):
        # ⚠️같은 API에 분기물이 섞여 있어 base로만 매칭하면 BTC/ETH가 오염된다.
        if t.get('contract_type') != 'perpetual': continue
        sym = (t.get('base') or '').upper()
        if not sym or (t.get('target') or '').upper() not in ('USDT', 'USD'): continue
        v = t.get('converted_volume', {}).get('usd')
        rows.append(dict(sec=sec, sym=sym, venue=label,
                         vol=float(v) / 1e6 if v else None,
                         oi=float(t['open_interest_usd']) / 1e6 if t.get('open_interest_usd') else None,
                         fund=float(t['funding_rate']) if t.get('funding_rate') is not None else None,
                         chg=t.get('h24_percentage_change'), px=t.get('last')))
cg('cg_binance_futures.json', 'Binance(신선)')
cg('cg_bybit.json', 'Bybit(CG대체,직접API 지역차단)')
cg('cg_aster.json', 'Aster(CG,신선)', 'dex')

# ---------- Hyperliquid / HyENA (DEX 기준 실측% 소스) ----------
def hl(fn, label, keep_px):
    try: meta, ctxs = J(fn)
    except Exception: return
    for u, c in zip(meta['universe'], ctxs):
        sym = u['name']
        # ⚠️스켈레톤은 midPx가 아니라 markPx를 쓴다(과거 재계산 불일치의 원인).
        px = float(c.get('markPx') or 0); prev = float(c.get('prevDayPx') or 0)
        rows.append(dict(sec='dex', sym=sym, venue=label,
                         vol=float(c.get('dayNtlVlm') or 0) / 1e6,
                         oi=float(c.get('openInterest') or 0) * px / 1e6,
                         fund=float(c.get('funding') or 0) * 100,
                         chg=(px / prev - 1) * 100 if prev else None, px=px or None))
        if keep_px and px: cur_px['hl:' + sym] = px
hl('hl_raw.json', 'Hyperliquid', True)
hl('hyna_raw.json', 'HyENA(HIP-3)', False)

# ---------- dYdX ----------
try:
    for k, m in J('dydx_raw.json')['markets'].items():
        sym = m['ticker'].split('-')[0]
        oracle = float(m.get('oraclePrice') or 0); pc = float(m.get('priceChange24H') or 0)
        rows.append(dict(sec='dex', sym=sym, venue='dYdX(공식indexer)',
                         vol=float(m.get('volume24H') or 0) / 1e6,
                         oi=float(m.get('openInterest') or 0) * oracle / 1e6,
                         fund=float(m.get('nextFundingRate') or 0) * 100,   # ⚠️주기가 CEX 8h와 달라 극단 논의에서 제외
                         chg=pc / (oracle - pc) * 100 if (oracle - pc) else None, px=oracle))
except Exception: pass

# ---------- 실측%(직전 회차 대비 실제 가격변동률) ----------
prev_px, real = {}, {}
pp = os.path.join(SP, 'prices_prev.json')
if os.path.exists(pp):
    prev_px = json.load(io.open(pp, encoding='utf-8'))
for k, v in cur_px.items():
    if k in prev_px and prev_px[k]:
        real[k] = (v / prev_px[k] - 1) * 100
json.dump(cur_px, io.open(os.path.join(SP, 'prices_cur.json'), 'w', encoding='utf-8'))

def real_of(r):
    pre = 'okx' if r['venue'].startswith('OKX') else ('hl' if r['venue'] == 'Hyperliquid' else None)
    return real.get(pre + ':' + r['sym']) if pre else None

# ---------- 이월 why/tag + 방향 모순 폐기 ----------
DOWN = re.compile(r'하락|낙폭|급락|음전환|마이너스 전환|반락|약세')
UP   = re.compile(r'상승|급등|반등|플러스 전환|양전환|강세')
prevj, purged = {}, 0
try:
    b = json.load(io.open(R + 'futures/brief.json', encoding='utf-8'))
    for s in ('cex', 'dex'):
        for x in b[s]:
            prevj[(x['symbol'], (x.get('venue') or x.get('protocol') or '').split('(')[0])] = (x.get('why'), x.get('tag'))
except Exception: pass

PURGE = '직전 회차 이월 서사가 방향과 어긋나 폐기 — 서사 미작성(수치는 다이제스트 열 참조)'
for r in rows:
    w, tg = prevj.get((r['sym'], r['venue'].split('(')[0]), (None, None))
    rp = real_of(r)
    if w and rp is not None:
        m = re.search(r'실측\s*\(?[^)]{0,12}?\)?\s*([+-]?\d+\.\d+)%', w)
        if m:
            st = float(m.group(1))
            contra = (st > 0) != (rp > 0) and abs(st) > 0.3 and abs(rp) > 0.3
        else:
            contra = ((rp > 0.5 and DOWN.search(w) and not UP.search(w)) or
                      (rp < -0.5 and UP.search(w) and not DOWN.search(w)))
        if contra: w, tg, purged = PURGE, 'no-narrative', purged + 1
    # ⚠️2026-09-03: 실측 부호만 보던 폐기 규칙은 **이월 서사가 든 chg24 숫자**를 못 걸렀다.
    #   ZEC(이월 -2.44% vs 이번 +18.21%)·XPL(-4.04% vs +16.13%)·BEAT(-8.89% vs -6.57%)가
    #   그대로 발행본에 인용됐다. 이월 서사가 chg24를 명시하면 이번 값과 대조한다.
    if w and w != PURGE and r.get('chg') is not None:
        mc = re.search(r'chg24[^\n]{0,40}?([+-]?\d+\.\d+)%(?!\s*→)', w)
        if mc:
            sc = float(mc.group(1))
            if (sc > 0) != (r['chg'] > 0) or abs(sc - r['chg']) > max(abs(r['chg']) * 0.25, 1.0):
                w, tg, purged = PURGE, 'no-narrative', purged + 1
    r['why'], r['tag'] = (w or PURGE), (tg or 'no-narrative')

# ---------- 유니버스 축약 + 주식화 토큰 제외 ----------
# ⚠️루틴 규약: 토큰화 주식·ETF·상품 perp(지수·금·은·원유 등)은 전부 제외하고
#   크립토 네이티브만 담는다. 벤뉴별 거래대금 상위 60종목으로 줄인다.
# ⚠️2026-09-03 22:30Z: 아래 목록이 부족해 SPCX·CRCL·SKHY·TEAM·MRVL·AVGO·GPRO·SAMSUNG·DELL·BZ가
#   발행 대상에 그대로 섞여 있었다(에이전트가 서술에서만 걸러 보고했다).
#   ⚠️반대 방향 주의: `CP`는 $0.0362짜리 크립토라 주식(Canadian Pacific)으로 오인해 빼면 안 된다
#   — 심볼만 보고 판단하지 말고 가격대까지 확인할 것.
# ⚠️보강(9/4 22:30Z): **금 연동 토큰 PAXG(Paxos Gold)·XAUT(Tether Gold)**가
#   목록에 없어 brief.json에 6행 남아 있었다(에이전트가 md 서술에서만 걸러 보고했다).
#   루틴 규약이 '금·은' 상품을 명시 제외하므로 심볼 목록에 추가한다 — `XAU`/`GOLD` 같은
#   원자재 티커만 막으면 **금 연동 크립토 토큰은 그대로 통과**한다.
EQUITY = set('''NVDA SPY SOXL MU SNDK SKHYNIX SKHY TSLA AAPL AMZN META MSFT GOOG GOOGL COIN MSTR
HOOD PLTR AMD INTC NFLX QQQ IWM DIA GLD SLV USO UNG XAU XAG XAUUSD XAGUSD GOLD SILVER OIL WTI PAXG XAUT
BRENT NDX SPX DJI VIX EUR GBP JPY
SPCX CRCL TEAM MRVL AVGO GPRO SAMSUNG DELL BZ ORCL CRM ADBE UBER ABNB SHOP SQ PYPL BABA NKE
DIS BA JPM GS V MA WMT COST KO PEP XOM CVX LLY UNH JNJ PFE'''.split())
def _is_equity(sym):
    # ⚠️2026-09-03: HyENA 심볼은 'hyna:GOLD'처럼 네임스페이스 접두가 붙어 있어
    #   접두를 떼지 않으면 상품 perp(금·은)가 필터를 그대로 통과한다.
    s = sym.upper().split(':')[-1].lstrip('K')
    return s in EQUITY or s.endswith('-USD-STOCK')
_dropped = sorted({r['sym'] for r in rows if _is_equity(r['sym'])})
rows = [r for r in rows if not _is_equity(r['sym'])]
if _dropped:
    print('주식화/상품 토큰 제외: ' + ', '.join(_dropped))
# ⚠️CoinGecko가 coin_id를 못 붙인 심볼은 새로 상장된 주식화 토큰일 수 있다(BZ·CRCL·SKHY가 그랬다).
#   자동 제외는 하지 않고(신규 크립토도 미매핑일 수 있다) 경고만 띄운다.
# 심볼별로 **모든 CG 벤뉴를 합쳐** coin_id가 하나라도 있으면 크립토로 본다.
# ⚠️벤뉴 하나만 보면 TWT·METIS처럼 진짜 크립토도 미매핑으로 잡힌다(한 벤뉴에서만 None).
_seen, _mapped = set(), set()
for _f in ('cg_binance_futures.json', 'cg_bybit.json', 'cg_aster.json'):
    try:
        for t in J(_f).get('tickers', []):
            if t.get('contract_type') != 'perpetual': continue
            _seen.add(t.get('base'))
            if t.get('coin_id'): _mapped.add(t.get('base'))
    except Exception: pass
# ⚠️Hyperliquid 메인 유니버스는 크립토 네이티브라 CG가 못 붙인 것도 여기 있으면 남긴다(PURR).
try: _hl = {a['name'] for a in J('hl_raw.json')[0]['universe']}
except Exception: _hl = set()
_nocoin = (_seen - _mapped) - _hl
_nocoin -= EQUITY
# ⚠️이름 목록만으로는 못 따라간다 — 벤뉴들이 토큰화 주식을 계속 추가한다(9/3에 14종이
#   목록을 통과해 발행 직전까지 갔다: CL[원유]·KORU[ETF]·UNITREE·AAOI·LITE·AXTI·NATGAS 등).
#   CoinGecko가 perpetual로 잡으면서도 coin_id를 못 붙인 심볼은 크립토 네이티브가 아니다.
#   신규 크립토가 미매핑일 가능성이 있으므로 제외 목록을 반드시 로그로 남긴다.
_live = {r['sym'] for r in rows} & _nocoin
if _live:
    print('coin_id 미매핑 제외(주식화 추정): ' + ', '.join(sorted(_live)))
    rows = [r for r in rows if r['sym'] not in _nocoin]

# ⚠️2026-09-03 발견: 같은 벤뉴의 BTCUSDT·BTCUSDC·BTCUSD_PERP(COIN-M)가 전부 심볼 'BTC'로
#   정규화돼 (심볼,벤뉴) 중복 행이 51건 생겼다. 16:30Z 발행본이 그 상태로 나갔다.
#   거래대금이 가장 큰 계약(사실상 USDT 무기한)만 남긴다.
_seen = {}
for r in rows:
    k = (r['venue'], r['sym'])
    if k not in _seen or (r['vol'] or 0) > (_seen[k]['vol'] or 0):
        _seen[k] = r
_dedup = len(rows) - len(_seen)
rows = list(_seen.values())
if _dedup:
    print('중복 계약 제거: %d행 (같은 심볼의 USDC/COIN-M 등)' % _dedup)

_by_venue = {}
for r in rows: _by_venue.setdefault(r['venue'], []).append(r)
rows = []
for v, rs in _by_venue.items():
    rs.sort(key=lambda r: -(r['vol'] or 0))
    rows.extend(rs[:60])

# ---------- 출력 ----------
rows.sort(key=lambda r: -(r['vol'] or 0))
out = ['# 선물 브리핑 데이터 요약 — 현재 %s / 직전 %s' % (TS, PREV_TS), '']
if prev_px:
    out += ["**'실측%' 열 = 직전 회차 대비 실제 가격 변동률**(OKX·Hyperliquid 직접 스냅샷 비교). 이번 회차 유일한 실제 가격 근거입니다.",
            'chg24는 24h 롤링 창 값이라 실측%와 방향이 다를 수 있고, 그 괴리가 롤오프 아티팩트의 증거입니다.']
else:
    out += ['⚠️**이번 회차는 실측% 열이 없습니다** — 직전 회차 가격 스냅샷(`prices_prev.json`)이',
            '컨테이너 재시작으로 유실됐습니다. chg24(24h 롤링)만으로 서술하고 "최근 2시간 변동"은',
            '이번 회차에 한해 쓰지 마십시오. 다음 회차부터는 정상 복구됩니다.']
out += ['⚠️맨 오른쪽 `직전 why`는 **과거 회차에 쓰인 이월 텍스트**입니다. 그 안의 수치를 이번 회차 관측으로 재진술하지 마세요.', '']

for sec, title in (('cex', 'CEX'), ('dex', 'DEX')):
    rs = [r for r in rows if r['sec'] == sec]
    out += ['## %s (%d건)' % (title, len(rs)), '',
            '| 심볼 | %s | vol24($M) | OI($M) | funding | chg24 | 현재가 | 실측%% | 직전 why(이월·인용금지) |'
            % ('벤뉴' if sec == 'cex' else '프로토콜'),
            '|---|---|---:|---:|---:|---:|---:|---:|---|']
    for r in rs:
        rp = real_of(r)
        n = lambda v, f: (f % v) if v is not None else '-'
        out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            r['sym'], r['venue'], n(r['vol'], '%.1f'), n(r['oi'], '%.1f'),
            n(r['fund'], '%.4f%%'), n(r['chg'], '%+.2f%%'),
            ('$%s' % format(r['px'], ',.6g')) if r['px'] else '-',
            n(rp, '%+.2f%%'), (r['why'] or '')[:110]))
    out.append('')

io.open(os.path.join(SP, 'digest.md'), 'w', encoding='utf-8').write('\n'.join(out))
stag = {'ts': TS, 'market': '', 'themes': [],
        'cex': [{'symbol': r['sym'], 'venue': r['venue'], 'vol24_usd': (r['vol'] or 0) * 1e6,
                 'oi_usd': (r['oi'] or 0) * 1e6, 'funding': (r['fund'] or 0) / 100,
                 'chg24': r['chg'], 'why': r['why'], 'tag': r['tag']} for r in rows if r['sec'] == 'cex'],
        'dex': [{'symbol': r['sym'], 'protocol': r['venue'], 'vol24_usd': (r['vol'] or 0) * 1e6,
                 'oi_usd': (r['oi'] or 0) * 1e6, 'funding': (r['fund'] or 0) / 100,
                 'chg24': r['chg'], 'why': r['why'], 'tag': r['tag']} for r in rows if r['sec'] == 'dex']}
json.dump(stag, io.open(os.path.join(SP, 'brief_staging.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('digest 생성 · cex %d · dex %d · 실측%% %d건 · prices_cur %d건 · 방향모순 폐기 %d건'
      % (len(stag['cex']), len(stag['dex']), len(real), len(cur_px), purged))
