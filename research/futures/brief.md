# 선물시장 스카우트 브리핑 — 2026-08-19 02:30 UTC (KST 2026-08-19 11:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-19
> 00:30 UTC)로부터 2시간 경과(정상 간격).**

## [검증 반영] 부모 세션 검증에서 지적된 4건 — 이 회차 내 즉시 보완 (ts 동일 유지)

1. **Hyperliquid 커버리지 회귀 복원**: 최초 저장 시 상위거래량·워치리스트 매칭에만 집중해
   `SOL·FARTCOIN·ASTER·ETHFI·HYPER·APEX·HYNA:BTC-USD·HYNA:ETH-USD·HYNA:HYPE·HYNA:PUMP·
   HYNA:SOL-USD` 11개 종목이 의도치 않게 누락됐던 것을 CoinGecko
   `derivatives/exchanges/hyperliquid` 재조회로 전부 복원했다(`APR-USD`만 이번 회차도
   HL 티커 목록에 없어 실제 미상장으로 판정, null 유지). 이 중 **SOL-USD가 HL에 실존
   티커로 처음 확인**돼 과거 여러 회차의 '별도 SOL-USD 티커 미발견' 서술이 갱신됐다
   (HYNA:SOL-USD와는 별도 마켓). **HYNA:\* 계열은 Hyperliquid HIP-3 빌더배포
   (builder-deployed) 마켓으로 파악되며, 기초자산이 BTC/ETH/SOL/HYPE/PUMP로 크립토
   네이티브이므로 제외 대상이 아니라 판단해 별도 그룹으로 계속 포함한다.**
2. **OrangeX 항목 복원**: 32회차 연속 전면 중단 상태를 '항목 삭제'가 아니라 'chg24: null로
   중단 사실 기록'하는 기존 규약대로, 직전 회차에 있던 14개 심볼(AAVE·ADA·AEON·AIO·ALGO·
   ALLO·ASTER·BANK·BEAT·BICO·BLESS·BSB·CAP·KAITO)을 복원했다(ACE·CASHCAT은 최초
   저장에도 있었음, 총 16개로 원상복구).
3. **themes 축약을 되돌림**: 최초 저장 시 여러 종목을 'steady-continuation-group'
   하나로 묶어 압축했던 것을 개별 종목 단위 테마로 재분리해 직전 회차와의 신규/지속
   비교가 끊기지 않게 했다.
4. **venue 라벨 설명 보완**: `Binance(직접API)`는 이번 회차도 `www.binance.com/fapi`
   경로를 가리키며, 이는 CoinGecko를 거치지 않는 바이낸스 자체 API 직접호출이므로
   라벨 자체는 정확하다. 이전 시장 텍스트의 '직접 재시도를 생략'이라는 표현은
   **차단이 확인된 기본 도메인 `fapi.binance.com`에 한정**된 것이며, 대체 직접경로인
   `www.binance.com/fapi`는 이번 회차도 전 Binance 데이터 수집에 실제로 사용됐다 —
   혼동을 피하기 위해 아래 본문 문구를 명확화했다.

## 시장 전반 — 신규 발견이 많은 회차 (ACE 원인 구체화·GALA 신규 급락·ALPINE 신규 급등)

**이번 회차는 신규 발견이 많은 회차다.** ①ACE 급등 원인이 WebSearch로 처음 구체화(8/7
시작된 숏스퀴즈·초박형 유통량, 펀더멘털 뉴스 없음), ②GALA가 Binance·OKX·HL 3벤뉴 동시
-14%대로 신규 급락 관측대상 편입, ③Chiliz 팬토큰 ALPINE이 Binance·Bybit에서 +16~19%
신규 급등, ④GIGGLE이 기존 'OKX 단일소스'에서 Binance 상장이 신규 확인, ⑤BEAT 하락이
직전 회차(-14~15%)보다 뚜렷이 가속(-23~26%), ⑥CASHCAT이 직전 회차의 '낙폭축소 반전'을
다시 뒤집어 재악화, ⑦BTW(Aster)가 3회차 연속 재가속(+14.63%→+25.73%→+37.84%).

**ACE는 이번 회차도 계속 상승했다** — Binance +41.457%(vol $627.15M, funding
-0.00223545 raw), Bybit +43.499%(vol $116.58M, funding -0.00215[CG→frac]),
Hyperliquid +38.065%(funding -0.00059[CG→frac]), Aster +42.009%(funding
-0.00045[CG→frac]). OKX는 이번 회차도 SWAP 티커 자체가 존재하지 않는다(오류코드
51001). **WebSearch로 원인을 재탐색해 이번엔 구체적 설명을 확보했다**: Phemex
블로그·CoinMarketCap AI 요약에 따르면 8/7 무렵 시작된 급등은 펀더멘털 뉴스가 아니라
**숏스퀴즈**가 원인으로, 청산 대부분(당시 기준 $867.96K~$1.39M)이 숏 포지션에서
발생했고 유통량이 얇아 소액 매수에도 가격이 크게 움직이는 구조로 설명된다. 4벤뉴
전원의 지속적인 음수 펀딩(숏이 롱에 자금을 지불)은 이 숏스퀴즈 서사와 정합적이다.
다만 이 설명이 8/7 최초 급등에 대한 것이라 최근 회차들의 추가 상승분까지 완전히
설명하는지는 확정할 수 없어 정직 표기한다.

**GALA는 이번 회차 신규로 급락 관측 대상에 편입됐다** — Binance -14.420%(vol
$31.67M, OI $6.25M), OKX -14.38%(vol $10.73M, OI $1.75M, funding -0.00033[raw]),
Hyperliquid -14.81%(vol $1.14M, OI $1.12M, funding -0.00018[CG→frac]). 3벤뉴가
거의 동일한 낙폭으로 수렴해 개별 거래소 이슈가 아닌 종목 자체의 약세로 보이나,
WebSearch로는 이번 회차에 해당하는 특정 촉매를 찾지 못했다(직전 검색결과는 8/12
기준 -1.9%/-2.5% 완만한 조정 언급뿐) — **원인 미상으로 정직 표기**.

**ALPINE(Chiliz Alpine F1 팬토큰)은 Binance +16.436%(vol $71.13M, OI $2.49M,
funding 0.00003855 raw), Bybit +19.446%(vol $13.18M, OI $1.00M, funding
0.00005[CG→frac])로 신규 급등 관측**됐다. OKX·Aster에는 상장 자체가 없음을 개별
재확인(OKX 오류코드 51001). WebSearch 결과 과거(2025년 9월 +90%→이후 -87%, 11월
Biconomy 트레이딩 대회 등) 얇은 유동성발 급변동이 반복돼온 팬토큰 특성만 확인됐고,
**이번 회차의 구체적 촉매는 확인하지 못해 정직 표기**한다.

**GIGGLE은 기존 'OKX 단일소스'에서 벗어나 Binance 상장이 신규 확인**됐다 — Binance
last $32.95, chg -2.226%, vol $18.53M(funding 0.00005 raw), OI $10.99M. OKX는 chg
-2.43%(vol $10.20M, funding 0.00005 raw, OI $1.63M)로 동조. 2소스 모두 소폭
마이너스로 방향은 일치한다.

**BEAT는 하락이 뚜렷이 가속했다** — Binance -25.986%(vol $98.58M, funding
0.00037681 raw, OI $9.85M)로 직전 회차(-15.11%)보다 하락폭이 커졌고, OKX
-22.74%(vol $98.61M, funding 0.00063 raw, OI $5.41M)·Aster -22.826%(vol $0.30M,
funding 0.00001[CG→frac], OI $0.16M)도 동조 가속했다.

**CASHCAT은 직전 회차의 '낙폭축소 반전'이 다시 뒤집혀 낙폭이 재확대됐다** —
Hyperliquid -12.738%→**-14.57%**, Aster -12.307%→**-14.423%**로 2소스 모두 동조
재악화했다(온체인 cash-cat 가격은 이번 회차 재확인 생략).

**BTW(Aster)는 재가속을 더 이어갔다** — 직전 회차 +14.63%→+25.73%였던 것이 이번엔
**+37.842%**(vol $2.11M, OI $12.63M, funding 0.00005[CG→frac])로 확장 흐름이
3회차 연속 지속되고 있다.

**BICO는 하락 흐름이 지속됐다** — OKX -8.53%(vol $17.38M, funding -0.00015666,
OI $2.48M), Binance -8.24%(vol $18.74M, funding -0.00113771 raw, OI $5.03M),
Aster -7.219%(vol $0.08M, funding -0.00014[CG→frac], OI $0.09M) 모두 마이너스권
지속(직전 회차 -4%대에서 낙폭이 더 커짐).

**KAITO는 소폭 계속 상승했다**(OKX +2.00%, Binance/USDC +2.519%, HL +2.275%) —
직전 회차(+4.5~6.4%)보다는 상승폭이 줄었으나 방향은 유지.

**BSB·APR·1000RATS·ALLO는 대체로 두자리~한자리대 플러스권을 유지**했다(BSB
Binance +0.675%·OKX +0.75%, APR OKX +6.97%·Bybit +6.713%·Aster +6.985%,
1000RATS Binance +11.601%, ALLO Binance +3.638%·Bybit +3.482%·Aster +4.208%).

**ATOM·AAVE·ADA·ALGO 등 메이저 알트는 대체로 소폭 등락권에 머물렀다**(ATOM 전
벤뉴 -0.4~-0.7%, AAVE -0.9~-1.2%, ADA +0.5~+1.2%, ALGO +0.4~+0.7%).

**BANK는 소폭 플러스를 유지**했다(Binance +3.963%, Bybit +3.783%, Aster
+3.571%) — 직전 회차의 재가속(+5.0%) 대비로는 소폭 감속.

**[복원] HL 종목 요약(직전 회차 대비)**: FARTCOIN -3.56%→**-0.652%**(낙폭 축소),
HYPER -1.19%→**+1.495%**(플러스 반전), APEX +5.44%→**+9.647%**(추가 가속), ETHFI
-3.214%→**-2.548%**(소폭 개선), ASTER(HL) +0.042%→**+0.184%**(안정 유지),
HYNA:BTC-USD +0.437%→**+0.474%**(안정), HYNA:ETH-USD -0.172%→**+0.776%**(플러스
반전), HYNA:HYPE -1.679%→**-1.623%**(대체로 보합), HYNA:PUMP +11.403%→
**+11.988%**(가속 지속). **HYNA:SOL-USD는 이번 회차 값(+1.664%)이 직전 회차 값과
소수점까지 완전히 동일**해 CoinGecko 캐시 지연 가능성을 의심하며 정직 표기한다
(재확인 필요). **SOL-USD가 HL에 실존 티커로 처음 확인**됐다(vol $4.94M, OI
$32.89M, chg +0.196%) — 과거 여러 회차의 '별도 SOL-USD 티커 미발견' 서술이
갱신된다.

**메이저(BTC·ETH·SOL)는 이번 회차도 안정권**을 유지했다 — dYdX BTC +0.399%, ETH
+0.721%, SOL +1.964%; HL BTC +0.32%, ETH +0.54%, SOL +0.196%(신규 복원); Aster BTC
+0.411%. **BTC 도미넌스는 56.62%→56.56%, 총시총은 $2.288조→$2.283조**로 소폭 하락
(CoinGecko `/global` 재확인, ETH 도미넌스 10.10%→10.09%).

**데이터 품질**: funding 단위 보정(CoinGecko 경유 percent→fraction, `/100`)을
이번 회차도 전 항목에 적용했다. 전 종목 funding 스케일 점검 결과 최대 절대값은
Binance ACEUSDT -0.00223545(2.24e-3)로 0.01 미만이며 중앙값도 대체로
1e-5~5.7e-5 범위 안에 있어 이상 없음을 확인했다(부모 세션 검증 결과와 일치).
**OKX 개별조회 재확인**: 벌크 `market/tickers`에서 ATOM·CAP·CORE·BSB·ALPINE·
BANK·ACE가 이번 회차도 누락돼 개별 GET으로 재조회했다 — ALPINE·BANK·ACE는 개별
GET에서도 오류코드 51001(상품 자체 부재)로 확인돼 구조적 미상장으로 판정,
ATOM·CAP·CORE·BSB는 개별 GET으로 정상 확보됐다(벌크 누락이 상장 부재가 아니라
응답 절단 때문임을 재확인). **OKX `volCcy24h`(기초자산 수량) × `last` = USD
거래대금** 방식을 이번 회차도 전 종목에 적용했고, 직전 회차 값과 근접 일치함을
재확인했다(예: GRAM $5.20M vs 직전 $5.11M, APR $68.86M vs 직전 $68.81M, AEON
$64.66M vs 직전 $64.47M). **Bybit는 이번 회차 직접 API 재시도를 생략**하고
CoinGecko `derivatives/exchanges/bybit` 경유로 바로 진행했다(직전 3회 연속
403 확인됨, 이번 회차는 재확인하지 않아 정직 표기). **`fapi.binance.com`(바이낸스
기본 도메인) 직접 재시도만 생략**했고, 대체 직접경로인 `www.binance.com/fapi`는
이번 회차도 전 Binance 데이터 수집에 실제로 사용했다 — 이는 CoinGecko를 거치지
않는 바이낸스 자체 API 직접호출이므로 **venue 라벨 'Binance(직접API)'는
정확하다**(과거 지속 451 확인 이력에 근거해 기본 도메인만 재시도하지 않음).
Binance 벌크 `ticker/24hr`·`premiumIndex`는 응답이 커서 일부 심볼(ATOM·AAVE·
ADA·ACE·GRAM·CAP·CORE·BSB·AIO·KAITOUSDC·AEON 등)이 누락됐고, 개별 GET으로
재조회해 확보했다(CAP·APEX·AEON은 개별 GET에서 400 오류가 발생해 Binance
미상장으로 판정, 과거 회차와 일치). **OrangeX는 32회차·약 65.75시간째 전면
중단**(코드1000 "No service found" 재현). **Aster ETH truncation은 14회차
연속** 지속(직접 API 403, CoinGecko 경유 재조회에서도 ETH 항목 자체가 반환되지
않음).

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

funding은 raw fraction(예: 0.00005 = 8시간당 0.005%) 기준으로 통일. `[CG→frac]` 표기는
이번 회차 CoinGecko percent 값을 `/100` 보정했음을 뜻함.

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [계속 상승] | Binance(직접API) | $627.15M | $17.89M | -0.00223545 | +41.457% | 숏스퀴즈+초박형 유통량이 원인으로 처음 구체적 확인 | ace-short-squeeze-thin-float-confirmed |
| **ACE** [계속 상승] | Bybit(CoinGecko대체) | $116.58M | $7.40M | -0.00215 [CG→frac] | +43.499% | Binance·HL·Aster와 동조 지속 상승 | ace-short-squeeze-thin-float-confirmed |
| **BEAT** [하락 가속] | OKX(직접API) | $98.61M | $5.41M | 0.00062840 | -22.74% | 직전 회차(-14.82%)보다 낙폭 확대 | beat-decline-accelerates |
| BEAT [하락 가속] | Binance(직접API) | $98.58M | $9.85M | 0.00037681 | -25.986% | OKX·Aster와 동조, 3소스 중 최대 낙폭 | beat-decline-accelerates |
| **BICO** [하락 지속] | OKX(직접API) | $17.38M | $2.48M | -0.00015666 | -8.53% | 직전 회차(-4.06%)보다 낙폭 확대 | bico-decline-continues |
| BICO [하락 지속] | Binance(직접API) | $18.74M | $5.03M | -0.00113771 | -8.24% | OKX·Aster와 동조 하락 지속 | bico-decline-continues |
| **GALA** [신규 급락] | Binance(직접API) | $31.67M | $6.25M | 미확보 | -14.420% | 신규 급락 관측대상 편입, 촉매 미상 | gala-new-decline-cause-unknown |
| GALA [신규 급락] | OKX(직접API) | $10.73M | $1.75M | -0.00033111 | -14.38% | Binance·HL와 거의 동일한 낙폭 | gala-new-decline-cause-unknown |
| **ALPINE** [신규 급등] | Binance(직접API) | $71.13M | $2.49M | 0.00003855 | +16.436% | Chiliz F1 팬토큰 신규 급등, 촉매 미확인 | alpine-fan-token-surge-cause-unconfirmed |
| ALPINE [신규 급등] | Bybit(CoinGecko대체) | $13.18M | $1.00M | 0.00005 [CG→frac] | +19.446% | Binance보다 더 큰 폭, OKX·Aster 미상장 | alpine-fan-token-surge-cause-unconfirmed |
| **GIGGLE** [Binance 신규상장] | Binance(직접API) | $18.53M | $10.99M | 0.00005 | -2.226% | 기존 OKX 단일소스에서 Binance 상장 신규 확인 | giggle-binance-listing-confirmed |
| GIGGLE [Binance 신규상장] | OKX(직접API) | $10.20M | $1.63M | 0.00005 | -2.43% | Binance와 동조 소폭 마이너스 | giggle-binance-listing-confirmed |
| **KAITO** [감속] | OKX(직접API) | $26.42M | $4.98M | -0.00047223 | +2.00% | 소폭 상승 지속, 직전(+4.47%)보다 감속 | kaito-gains-moderate |
| KAITO [감속] | Binance(USDC, 직접API) | $3.48M | $1.07M | -0.00031193 | +2.519% | OKX·HL과 동조 소폭 상승 | kaito-gains-moderate |
| ATOM [소폭 마이너스] | OKX(직접API) | $3.84M | $3.78M | -0.00002574 | -0.703% | 3벤뉴 동조 | atom-mild-negative |
| ATOM [소폭 마이너스] | Binance(직접API) | $14.67M | $15.46M | 0.00006409 | -0.563% | OKX·Bybit·HL과 동조 | atom-mild-negative |
| ATOM [소폭 마이너스] | Bybit(CoinGecko대체) | $6.66M | $13.62M | -0.00004 [CG→frac] | -0.423% | Binance·OKX·HL과 동조 | atom-mild-negative |
| AAVE [소폭 마이너스] | OKX(직접API) | $18.25M | $11.75M | 0.00003356 | -0.95% | 소폭 마이너스권 유지 | aave-mild-negative |
| AAVE [소폭 마이너스] | Binance(직접API) | $41.82M | $43.51M | -0.00003107 | -0.967% | OKX·Bybit·HL과 동조 | aave-mild-negative |
| AAVE [소폭 마이너스] | Bybit(CoinGecko대체) | $11.71M | $39.75M | 0.00007 [CG→frac] | -0.887% | Binance·OKX·HL과 동조 | aave-mild-negative |
| ADA [소폭 플러스] | OKX(직접API) | $26.52M | $24.15M | 0.00009949 | +1.22% | 4벤뉴 동조 | ada-mild-positive |
| ADA [소폭 플러스] | Binance(직접API) | $86.36M | $83.27M | 0.00005 | +1.223% | OKX·Bybit·HL·Aster와 동조 | ada-mild-positive |
| ADA [소폭 플러스] | Bybit(CoinGecko대체) | $38.95M | $54.65M | 0.0001 [CG→frac] | +1.163% | Binance·OKX와 동조 | ada-mild-positive |
| ALGO [소폭 플러스] | Binance(직접API) | $5.47M | $7.73M | 0.00008923 | +0.683% | 소폭 플러스권 유지 | algo-mild-positive |
| MMT [플러스 지속] | OKX(직접API) | $4.06M | $2.12M | -0.00032050 | +1.847% | 플러스 방향 지속 | mmt-holds-positive |
| MMT [플러스 지속] | Binance(직접API) | $6.73M | $8.13M | 미확보 | +1.663% | OKX와 동조 플러스 유지 | mmt-holds-positive |
| AEON [소폭 플러스] | OKX(직접API) | $64.66M | $3.52M | 0.00000788 | +0.79% | 소폭 플러스권 지속 | aeon-mild-positive |
| AEON [소폭 플러스] | Bybit(CoinGecko대체) | $7.47M | $1.09M | 0.00005 [CG→frac] | +0.405% | OKX·Aster와 동조 | aeon-mild-positive |
| **GRAM** [보합] | OKX(직접API) | $5.20M | $6.38M | 0.00005 | 0.00% | 손익분기권 유지 | gram-flat |
| GRAM [보합] | Binance(직접API) | $9.13M | $14.17M | 0.00060370 | -0.076% | OKX·HL과 동조 보합권 | gram-flat |
| CAP [소폭 마이너스] | OKX(직접API) | $62.88M | $10.29M | -0.00014115 | -1.406% | 소폭 마이너스권 지속 | cap-mild-negative |
| CORE [소폭 마이너스] | OKX(직접API) | $2.05M | $0.99M | -0.00000856 | -1.743% | 소폭 마이너스권 지속, 단일소스 | core-mild-negative |
| PIPPIN [플러스 유지] | OKX(직접API) | $3.67M | $1.79M | 0.00005 | +5.83% | 플러스권 유지 | pippin-holds-positive |
| PIPPIN [플러스 유지] | Binance(직접API) | $6.42M | $5.89M | 0.00005 | +5.833% | OKX와 동조 | pippin-holds-positive |
| BSB [소폭 플러스] | OKX(직접API) | $5.57M | $2.16M | 0.00013598 | +0.75% | 소폭 플러스권 유지 | bsb-mild-positive |
| BSB [소폭 플러스] | Binance(직접API) | $10.57M | $8.45M | 0.00007243 | +0.675% | OKX·Aster와 동조 | bsb-mild-positive |
| BANK [플러스 감속] | Binance(직접API) | $24.24M | $11.16M | -0.00003005 | +3.963% | 직전 회차(+5.05%)보다 감속 | bank-holds-positive-decelerates |
| BANK [플러스 감속] | Bybit(CoinGecko대체) | $2.79M | $4.21M | -0.00004 [CG→frac] | +3.783% | Binance·Aster와 동조 | bank-holds-positive-decelerates |
| APR [플러스 유지] | OKX(직접API) | $68.86M | $3.39M | 0.00005305 | +6.97% | 두자리대에 근접한 플러스권 | apr-holds-positive |
| APR [플러스 유지] | Bybit(CoinGecko대체) | $10.47M | $3.31M | 0.00005 [CG→frac] | +6.713% | OKX·Aster와 동조 | apr-holds-positive |
| AIO [마이너스 축소] | Binance(직접API) | $40.90M | $4.64M | 0.00005 | -3.196% | 마이너스권 축소 흐름 유지 | aio-narrowing-negative |
| ALLO [플러스 유지] | Binance(직접API) | $30.58M | $12.54M | 0.00005 | +3.638% | 플러스 방향 유지 | allo-holds-positive |
| ALLO [플러스 유지] | Bybit(CoinGecko대체) | $4.75M | $4.43M | 0.00005 [CG→frac] | +3.482% | Binance·Aster와 동조 | allo-holds-positive |
| 1000RATS [두자리대 유지] | Binance(직접API) | $89.44M | $13.80M | 0.00060370 | +11.601% | 두자리대 상승 유지 | 1000rats-holds-double-digit |
| APEX [플러스 유지] | Bybit(CoinGecko대체) | $1.08M | $1.77M | 0.00005 [CG→frac] | +10.207% | 뚜렷한 상승 지속 | apex-holds-positive |
| ASTER(자체토큰) [안정] | Binance(직접API) | $13.62M | $69.74M | 0.00005 | +0.133% | CEX OI 안정 유지 | aster-cex-stable |
| ASTER(자체토큰) [안정] | OKX(직접API) | $3.23M | $8.28M | 0.00004130 | +0.10% | Binance와 동조 안정 | aster-cex-stable |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

funding은 raw fraction 기준. `[CG→frac]` = 이번 회차 CoinGecko percent 값을 `/100` 보정.
OrangeX 행은 32회차 연속 전면 중단으로 **모든 값이 null**이며, 이는 '종목 부재'가
아니라 '중단 사실 기록'임을 나타낸다(직전 회차 14개 심볼 복원 완료, 총 16개).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [계속 상승] | Hyperliquid | $3.45M | $1.90M | -0.00059 [CG→frac] | +38.065% | 숏스퀴즈+초박형 유통량 서사와 정합적 | ace-short-squeeze-thin-float-confirmed |
| **ACE** [계속 상승] | Aster | $0.96M | $0.27M | -0.00045 [CG→frac] | +42.009% | HL·Binance·Bybit와 동조 지속 상승 | ace-short-squeeze-thin-float-confirmed |
| ACE [서비스 중단] | OrangeX | — | — | — | — | 32회차·약 65.75시간 | orangex-service-outage-continues |
| **BTW** [3회차 재가속] | Aster | $2.11M | $12.63M | 0.00005 [CG→frac] | +37.842% | +14.63%→+25.73%→+37.84% 확장 지속 | btw-continues-accelerating |
| **CASHCAT** [재악화] | Hyperliquid | $8.53M | $12.30M | 0.00002 [CG→frac] | -14.57% | 직전 회차 낙폭축소 반전이 다시 뒤집힘 | cashcat-re-reverses-worsens |
| CASHCAT [재악화] | Aster | $0.62M | $0.66M | 0.00001 [CG→frac] | -14.423% | HL과 동조 재악화 | cashcat-re-reverses-worsens |
| CASHCAT [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| BEAT [하락 가속] | Aster | $0.30M | $0.16M | 0.00001 [CG→frac] | -22.826% | OKX·Binance와 동조 하락 가속 | beat-decline-accelerates |
| BEAT [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| BICO [하락 지속] | Aster | $0.08M | $0.09M | -0.00014 [CG→frac] | -7.219% | OKX·Binance와 동조 하락 지속 | bico-decline-continues |
| BICO [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| **GALA** [신규 급락] | Hyperliquid | $1.14M | $1.12M | -0.00018 [CG→frac] | -14.81% | Binance·OKX와 거의 동일한 낙폭 | gala-new-decline-cause-unknown |
| **KAITO** [감속] | Hyperliquid | $1.69M | $5.75M | -0.00005 [CG→frac] | +2.275% | OKX·Binance와 동조 소폭 상승 | kaito-gains-moderate |
| KAITO [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| AEON [소폭 마이너스] | Aster | $0.06M | $0.32M | 0.00005 [CG→frac] | -0.718% | OKX·Bybit와 대체로 동조, 부호는 소폭 엇갈림 | aeon-mild-positive |
| AEON [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| **GRAM** [보합] | Hyperliquid | $1.79M | $15.39M | 0.00001 [CG→frac] | -0.008% | OKX·Binance와 보합권 유지 | gram-flat |
| ATOM [소폭 마이너스] | Hyperliquid | $0.47M | $1.68M | 0.00001 [CG→frac] | -0.563% | OKX·Binance·Bybit와 동조 | atom-mild-negative |
| ATOM [엇갈림] | Aster | $0.01M | $1.68M | 0.0001 [CG→frac] | +0.141% | 타 벤뉴와 달리 소폭 플러스 | atom-mild-negative |
| AAVE [소폭 마이너스] | Hyperliquid | $2.94M | $56.90M | 0.00001 [CG→frac] | -1.166% | OKX·Binance·Bybit와 동조 | aave-mild-negative |
| AAVE [소폭 마이너스] | Aster | $0.23M | $4.44M | 0.0001 [CG→frac] | -1.034% | HL과 동조 | aave-mild-negative |
| AAVE [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| ADA [소폭 플러스] | Hyperliquid | $4.97M | $29.08M | 0.00001 [CG→frac] | +0.51% | OKX·Binance·Bybit와 동조 | ada-mild-positive |
| ADA [소폭 플러스] | Aster | $0.20M | $1.22M | 0.0001 [CG→frac] | +1.162% | HL과 동조 | ada-mild-positive |
| ADA [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| ALGO [소폭 플러스] | Hyperliquid | $0.39M | $1.81M | 0.00001 [CG→frac] | +0.397% | Binance와 동조 | algo-mild-positive |
| ALGO [엇갈림] | Aster | $0.01M | $0.04M | 0.00001 [CG→frac] | -0.613% | HL·Binance와 달리 소폭 마이너스 | algo-mild-positive |
| ALGO [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| ASTER(자체토큰) [안정] | Aster | $11.72M | $221.49M | 0.00007 [CG→frac] | +0.117% | 자체 OI 안정 유지 | aster-cex-stable |
| ASTER(자체토큰) [안정, 복원] | Hyperliquid | $0.41M | $13.51M | 0.00001 [CG→frac] | +0.184% | 최초 저장 시 누락 복원 — Aster프로토콜과 동조 | aster-cex-stable |
| ASTER(자체토큰) [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| **HYPE** [소폭 개선] | Hyperliquid | $243.00M | $1,309.21M | -0.00002 [CG→frac] | -1.306% | 직전 회차(-1.87%)보다 낙폭 소폭 축소 | hype-slightly-improves |
| **BLESS** [부호 재반전] | Aster | $0.03M | $0.10M | 0.00005 [CG→frac] | -0.642% | 직전 회차 플러스 반전(+3.47%)이 다시 소폭 마이너스로 | bless-flips-back-negative |
| BLESS [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| BTC [안정] | dYdX | $3.01M | $17.47M | 0.0 | +0.399% | 메이저 전반 안정권 유지 | majors-remain-stable |
| **ETH** [안정] | dYdX | $7.77M | $23.68M | 0.00001359 | +0.721% | HL과 함께 안정권 유지 | majors-remain-stable |
| SOL [안정] | dYdX | $0.44M | $4.96M | 0.0 | +1.964% | 메이저 중 상승폭 최대 유지 | majors-remain-stable |
| **SOL** [신규 확인, 복원] | Hyperliquid | $4.94M | $32.89M | 0.00001 [CG→frac] | +0.196% | 최초 저장 시 누락 복원 — HL에 SOL-USD 티커 실존 최초 확인 | sol-hl-ticker-confirmed |
| BTC [안정] | Hyperliquid | $1,429.72M | $2,645.73M | 0.0 | +0.32% | dYdX와 함께 안정권 유지 | majors-remain-stable |
| **ETH** [안정] | Hyperliquid | $717.60M | $1,677.48M | 0.00001 [CG→frac] | +0.54% | dYdX와 함께 안정권 유지 | majors-remain-stable |
| BTC [안정] | Aster | $535.48M | $805.21M | 0.00002 [CG→frac] | +0.411% | 메이저 전반 안정권 유지 | majors-remain-stable |
| ETH [truncation 14연속] | Aster | — | — | — | — | 직접 API 403, CG 경유도 항목 미반환 | truncation-continues-fourteenth-round |
| 1000RATS [두자리대 유지] | Aster | $0.35M | $0.04M | 0.00019 [CG→frac] | +13.559% | Binance와 함께 두자리대 상승 유지 | 1000rats-holds-double-digit |
| AIO [마이너스 축소] | Aster | $0.12M | $0.09M | 0.00005 [CG→frac] | -3.112% | Binance와 함께 마이너스권 축소 흐름 | aio-narrowing-negative |
| AIO [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| ALLO [플러스 유지] | Aster | $0.14M | $0.07M | 0.00001 [CG→frac] | +4.208% | Binance·Bybit와 함께 플러스 유지 | allo-holds-positive |
| ALLO [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| APR [플러스 유지] | Aster | $0.26M | $0.33M | 0.00001 [CG→frac] | +6.985% | OKX·Bybit와 동조 플러스 유지 | apr-holds-positive |
| APR [미상장 재확인] | Hyperliquid | — | — | — | — | 복원 시도했으나 이번 회차도 HL 목록에 없음(실제 부재) | not-listed-on-hyperliquid |
| BANK [플러스 감속] | Aster | $0.04M | $0.25M | 0.0 [CG→frac] | +3.571% | Binance·Bybit와 동조 플러스 유지 | bank-holds-positive-decelerates |
| BANK [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| BSB [소폭 플러스] | Aster | $0.11M | $0.12M | 0.00002 [CG→frac] | +1.222% | OKX·Binance와 동조 | bsb-mild-positive |
| BSB [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| CAP [소폭 마이너스] | Aster | $0.05M | $0.18M | -0.00004 [CG→frac] | -2.0% | OKX보다 더 큰 폭 마이너스 | cap-mild-negative |
| CAP [서비스 중단, 복원] | OrangeX | — | — | — | — | 직전 회차 항목 복원 | orangex-service-outage-continues |
| **FARTCOIN** [낙폭 축소, 복원] | Hyperliquid | $2.78M | $29.40M | 0.00001 [CG→frac] | -0.652% | 최초 저장 시 누락 복원 — 직전(-3.56%)보다 낙폭 축소 | fartcoin-narrows-decline |
| **ETHFI** [소폭 개선, 복원] | Hyperliquid | $3.38M | $11.44M | 0.00001 [CG→frac] | -2.548% | 최초 저장 시 누락 복원 — 직전(-3.21%)보다 소폭 개선 | ethfi-slightly-improves |
| **HYPER** [플러스 반전, 복원] | Hyperliquid | $0.06M | $0.20M | 0.00001 [CG→frac] | +1.495% | 최초 저장 시 누락 복원 — 직전(-1.19%)에서 플러스로 반전 | hyper-flips-positive |
| **APEX** [추가 가속, 복원] | Hyperliquid | $0.23M | $0.69M | 0.00001 [CG→frac] | +9.647% | 최초 저장 시 누락 복원 — Bybit와 함께 직전(+5.44%)보다 가속 | apex-holds-positive |
| **HYNA:BTC-USD** [복원] | Hyperliquid | $0.51M | $2.19M | 0.00001 [CG→frac] | +0.474% | HIP-3 빌더배포 마켓, BTC와 동조 안정 | hyna-builder-deployed-markets |
| **HYNA:ETH-USD** [플러스 반전, 복원] | Hyperliquid | $0.24M | $1.62M | 0.00001 [CG→frac] | +0.776% | HIP-3 빌더배포 마켓, 직전(-0.17%)에서 플러스 반전 | hyna-builder-deployed-markets |
| **HYNA:HYPE** [복원] | Hyperliquid | $0.14M | $0.63M | -0.00001 [CG→frac] | -1.623% | HIP-3 빌더배포 마켓, HYPE(HL)와 대체로 동조 | hyna-builder-deployed-markets |
| **HYNA:PUMP** [추가 가속, 복원] | Hyperliquid | $0.07M | $0.16M | 0.0 | +11.988% | HIP-3 빌더배포 마켓, 직전(+11.40%)보다 추가 가속 | hyna-builder-deployed-markets |
| **HYNA:SOL-USD** [복원, 값 동일 의심] | Hyperliquid | $0.03M | $0.53M | 0.00001 [CG→frac] | +1.664% | HIP-3 빌더배포 마켓, 값이 직전 회차와 소수점까지 동일 — 캐시 지연 의심 | hyna-builder-deployed-markets |

## 테마 태그

1. **ACE**: 숏스퀴즈+초박형 유통량이 원인으로 WebSearch에서 처음 구체적으로 확인
   (펀더멘털 뉴스 없음, 8/7 시작, 청산 대부분 숏 포지션) — 4벤뉴 지속 상승·지속
   음수 펀딩과 정합적 (ace-short-squeeze-thin-float-confirmed).
2. **GALA**: Binance·OKX·HL 3벤뉴 동시 -14%대 신규 급락 관측대상 편입, 촉매 미상
   (gala-new-decline-cause-unknown).
3. **ALPINE**(Chiliz F1 팬토큰): Binance·Bybit 신규 급등(+16~19%), 확정 촉매
   미확인(과거 얇은 유동성발 변동성 반복 이력)
   (alpine-fan-token-surge-cause-unconfirmed).
4. **GIGGLE**: 기존 'OKX 단일소스'에서 Binance 상장이 신규 확인(거래량 $18.5M)
   (giggle-binance-listing-confirmed).
5. **BEAT**: 하락 가속 — OKX·Binance·Aster 3소스 모두 직전 회차보다 낙폭
   확대(-23~26%) (beat-decline-accelerates).
6. **CASHCAT**: 직전 회차의 낙폭축소 반전이 다시 뒤집혀 재악화(-12%대→-14%대)
   (cashcat-re-reverses-worsens).
7. **BTW**(Aster): 3회차 연속 재가속(+14.63%→+25.73%→+37.84%)
   (btw-continues-accelerating).
8. **BICO**: 하락 지속, 직전 회차보다 낙폭 확대(-4%대→-7~9%대)
   (bico-decline-continues).
9. **KAITO**: 소폭 상승 지속하나 직전 회차보다 감속(+4.5~6.4%→+2.0~2.5%)
   (kaito-gains-moderate).
10. **BLESS**(Aster): 직전 회차 플러스 반전(+3.47%)이 다시 소폭 마이너스로(-0.64%)
    (bless-flips-back-negative).
11. **HYPE**(HL): 직전 회차보다 낙폭 소폭 축소(-1.87%→-1.31%)
    (hype-slightly-improves).
12. **ATOM**: 4벤뉴 대체로 소폭 마이너스권(-0.4~-0.7%), Aster만 소폭 플러스로
    엇갈림 (atom-mild-negative).
13. **AAVE**: 3벤뉴 소폭 마이너스권 유지(-0.9~-1.2%) (aave-mild-negative).
14. **ADA**: 4벤뉴 소폭 플러스권 수렴(+0.5~+1.2%) (ada-mild-positive).
15. **ALGO**: 소폭 플러스권 유지, Aster만 소폭 마이너스로 엇갈림 (algo-mild-positive).
16. **MMT**: OKX·Binance 모두 플러스 방향 지속 (mmt-holds-positive).
17. **AEON**: OKX·Bybit·Aster 대체로 동조, 소폭 플러스~보합 (aeon-mild-positive).
18. **GRAM**: OKX·Binance·HL 손익분기권 보합 유지 (gram-flat).
19. **CAP**: OKX·Aster 모두 소폭 마이너스권 지속 (cap-mild-negative).
20. **CORE**: 소폭 마이너스권 지속, OKX 단일소스 (core-mild-negative).
21. **PIPPIN**: OKX·Binance 모두 플러스권 유지 (pippin-holds-positive).
22. **BSB**: OKX·Binance·Aster 모두 소폭 플러스권 유지 (bsb-mild-positive).
23. **ALLO**: Binance·Bybit·Aster 모두 플러스 방향 유지 (allo-holds-positive).
24. **1000RATS**: Binance·Aster 모두 두자리대 상승 유지 (1000rats-holds-double-digit).
25. **APEX**: Bybit·HL 모두 플러스 방향 유지하며 뚜렷이 가속(HL +9.65%로 복원 후
    확인) (apex-holds-positive).
26. **BANK**: Binance·Bybit·Aster 모두 플러스 유지, 직전 회차보다 소폭 감속
    (bank-holds-positive-decelerates).
27. **APR**: OKX·Bybit·Aster 플러스권 유지, HL은 이번 회차도 미상장 확인
    (apr-holds-positive / not-listed-on-hyperliquid).
28. **AIO**: Binance·Aster 모두 마이너스권 축소 흐름 유지 (aio-narrowing-negative).
29. **ASTER**(자체토큰): Binance·OKX·Aster·HL(복원) 전 벤뉴 안정권 유지
    (aster-cex-stable).
30. **메이저**(BTC·ETH·SOL): dYdX·HL·Aster 전반 안정권 유지, SOL의 HL 티커가 이번
    회차 처음 실존 확인됨 (majors-remain-stable / sol-hl-ticker-confirmed).
31. **FARTCOIN**(HL, 복원): 직전 회차보다 낙폭 축소(-3.56%→-0.65%)
    (fartcoin-narrows-decline).
32. **ETHFI**(HL, 복원): 직전 회차보다 소폭 개선(-3.21%→-2.55%)
    (ethfi-slightly-improves).
33. **HYPER**(HL, 복원): 직전 회차(-1.19%)에서 플러스로 반전(+1.50%)
    (hyper-flips-positive).
34. **HYNA:\* 계열**(HL, 복원): Hyperliquid HIP-3 빌더배포 마켓으로 기초자산이
    BTC/ETH/SOL/HYPE/PUMP라 크립토 네이티브 — 제외 대상 아님, 계속 포함 유지.
    HYNA:SOL-USD는 값이 직전 회차와 완전 동일해 캐시 지연 의심
    (hyna-builder-deployed-markets).
35. **데이터**: Bybit 직접 API·`fapi.binance.com`(바이낸스 기본 도메인) 직접
    재시도는 이번 회차 생략하고 과거 지속 실패 이력에 근거해 각각 CoinGecko·
    `www.binance.com/fapi`(여전히 바이낸스 자체 직접 API) 경로를 사용 — venue
    라벨 'Binance(직접API)'는 정확함, 혼동 방지 위해 문구 명확화
    (data-retry-skipped-honest-disclosure).
36. **데이터**: OKX 벌크 tickers 누락 심볼(ATOM·CAP·CORE·BSB)은 개별 GET으로
    정상 확보, ALPINE·BANK·ACE는 개별 GET에서도 오류코드 51001로 구조적
    미상장 확정 (okx-individual-get-confirms-listing-status).
37. **데이터**: OrangeX 서비스 중단이 32회차(약 65.75시간)로 확대 — 부모 세션
    검증 지적에 따라 직전 회차 14개 심볼의 null 항목을 복원(총 16개)
    (orangex-service-outage-continues).
38. **데이터**: Aster ETH truncation 14회차 연속
    (truncation-continues-fourteenth-round).
39. **데이터**: Hyperliquid 커버리지 회귀(23→12종목) — 최초 저장 시 상위거래량·
    워치리스트 매칭에만 집중해 SOL·FARTCOIN·ASTER·ETHFI·HYPER·APEX·HYNA:\*
    11종목이 의도치 않게 누락된 것을 재조회로 전부 복원(APR-USD만 실제
    미상장으로 확인돼 제외 유지) (hl-coverage-regression-restored).
40. **글로벌**: BTC 도미넌스 56.62%→56.56%, 총시총 2.288조달러→2.283조달러로
    소폭 하락 (global-dominance-slightly-down).
41. **주식화·상품 토큰은 전부 제외.** 리스트 전 종목 크립토 네이티브 확인 유지
    (stock-commodity-tokens-excluded-crypto-native-confirmed).

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트(CoinGecko binance_futures/
bybit 상위 20 거래량·펀딩극단·24h 급등 스크리닝)를 조합해 수행했으며 완전한 전체
시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다(Binance 벌크 티커에서 AMZN·AAPL·AMAT·
ANTHROPIC·ATMO 등으로 추정되는 항목이 함께 조회됐으나 전부 배제); (c) OKX는
`market/tickers`(instType=SWAP, 벌크)와 `public/open-interest`(개별)·
`public/funding-rate`(개별) 엔드포인트를 사용했다 — 벌크 응답에서 ATOM·CAP·CORE·
BSB·ALPINE·BANK·ACE가 누락돼 개별 GET으로 재조회했다. ALPINE·BANK·ACE는 개별
GET에서도 오류코드 51001(상품 자체 부재)이 나와 **OKX 구조적 미상장으로 확정**했고,
ATOM·CAP·CORE·BSB는 개별 GET으로 정상 확보돼 **벌크 누락이 상장 부재가 아니라
응답 절단 때문임을 재확인**했다; (d) **OKX `volCcy24h`는 이번 회차도 기초자산(코인)
수량 단위로 확인**돼 `last`(가격)를 곱해 USD 거래대금을 산출했다 — 직전 회차
값과 근접 일치를 재확인(GRAM·APR·AEON 등); (e) 이번 회차는 Binance·Bybit 양쪽에
모두 존재하는 심볼(ATOM·AAVE·ADA)에 대해 **가중평균을 계산하지 않고 벤뉴별로
별도 행으로 표기**했다 — 직전 회차까지 쓰던 'B+B 가중평균'은 이번 회차 Binance
`premiumIndex`가 일부 심볼(ATOM·AAVE 등)에서 funding을 반환하지 않아 두 다리
모두 완전한 funding 데이터를 확보하지 못했기 때문에, 불완전한 가중평균보다
벤뉴별 원값을 그대로 보이는 편이 정직하다고 판단해 방식을 바꿨다(정직 표기);
(f) Hyperliquid 데이터는 이번 회차도 CoinGecko `derivatives/exchanges/hyperliquid`
경유로 확보했다(직접 API `info`는 POST 전용이라 GET 전용 도구로 접근 불가) — **HL
funding은 전부 CoinGecko 경유이므로 percent→fraction 보정을 적용**했다. **[검증
반영] HL 초기 조회가 상위거래량·워치리스트 매칭에만 집중해 SOL·FARTCOIN·ASTER·
ETHFI·HYPER·APEX·HYNA:\* 11종목이 누락됐던 것을 부모 세션 지적으로 재조회·복원**
했다(APR-USD는 재조회에서도 없어 실제 미상장으로 판정); (g) **Bybit 직접 API는
이번 회차 재시도를 생략**했다(직전 3회 연속 403 확인 이력에 근거) — CoinGecko
`derivatives/exchanges/bybit` 경유로 확보했다(funding은 percent→fraction 보정
적용); (h) **바이낸스 기본 도메인(`fapi.binance.com`)도 이번 회차 재시도를
생략**했다(과거 지속 451 확인 이력에 근거) — **대체 직접경로인
`www.binance.com/fapi`는 이번 회차도 전 Binance 데이터 수집에 실제로 사용했고,
이는 CoinGecko를 거치지 않는 바이낸스 자체 API이므로 venue 라벨 'Binance(직접
API)'는 정확하다.** 벌크 `ticker/24hr`·`premiumIndex`가 응답 크기로 인해 일부
심볼을 누락해 개별 GET으로 재조회했고, CAP·APEX·AEON은 개별 GET에서 400 오류가
발생해 **Binance 미상장으로 판정**(과거 회차와 일치); (i) **Aster 직접 API는
이번 회차도 403** — CoinGecko 파생거래소 id `aster`로 대부분 확보했다(funding은
percent→fraction 보정 적용). ETH는 truncation이 지속돼 **14회차 연속 미확인**
이다; (j) **OrangeX API의 전면 서비스 중단이 이번 회차도 지속**돼 32회차·약
65.75시간에 달했다(`getCurrencies` → 코드 1000 "No service found" 재현).
**[검증 반영] 직전 회차에 있던 14개 심볼(AAVE·ADA·AEON·AIO·ALGO·ALLO·ASTER·
BANK·BEAT·BICO·BLESS·BSB·CAP·KAITO)의 null 항목을 복원**해 '중단' 사실이
'원래 없던 종목'처럼 보이지 않도록 했다(총 16개, ACE·CASHCAT은 최초 저장에도
있었음); (k) **ACE 급등 원인을 WebSearch로 재탐색해 처음으로 구체적 설명을
확보**했다(Phemex 블로그·CoinMarketCap AI 요약: 8/7 시작된 숏스퀴즈, 펀더멘털
뉴스 없음, 청산 대부분 숏) — 다만 이 설명이 8/7 최초 급등에 대한 것이라 이후
회차들의 추가 상승분까지 완전히 설명하는지는 확정하지 않았다; (l) **GALA·ALPINE·
GIGGLE(Binance)은 이번 회차 신규로 관측 대상에 편입**됐다 — GALA·ALPINE의
구체적 촉매는 WebSearch로도 확인하지 못해 각각 정직하게 '미상' 표기했고, GIGGLE은
Binance 상장 자체가 신규 발견 사실이다; (m) **글로벌 시총·도미넌스**는 이번
회차 CoinGecko `/global` 엔드포인트로 재확인했다 — 총시가총액 약 $2.283조·BTC
도미넌스 56.56%·ETH 도미넌스 10.09%로 직전 회차(56.62%, $2.288조) 대비 소폭
하락; (n) **도구 제약 안내**: 이번 회차는 Bash 없이 WebFetch(GET 전용)·
WebSearch만으로 데이터를 수집했다 — Hyperliquid의 POST 전용 `info` 엔드포인트는
GET 도구로 접근 불가, Aster·Bybit 직접 API는 403이라 CoinGecko 대체 경로를
사용했다. OKX 개별 GET 엔드포인트와 dYdX 직접조회는 안정적으로 접근했다; (o)
**funding 단위 보정은 이번 회차도 전 항목에 적용**했으며 신규 스케일 이상은
발견되지 않았다(최대 절대값 Binance ACEUSDT -0.00223545, 0.01 미만); (p)
**신규 발견 핵심 5건**: ①ACE 급등 원인 최초 구체화(숏스퀴즈+초박형 유통량),
②GALA 신규 급락 관측대상 편입(3벤뉴 동시 -14%대, 촉매 미상), ③ALPINE(Chiliz F1
팬토큰) 신규 급등 관측대상 편입, ④GIGGLE Binance 신규상장 확인, ⑤OKX 개별
GET으로 ALPINE·BANK·ACE의 구조적 미상장을 확정(벌크 누락과 구분); (q) **[검증
반영] 부모 세션 검증에서 지적된 4건(HL 커버리지 회귀·OrangeX 항목 축소·themes
축약·Binance 라벨 설명 부족)을 이 회차 내에서 즉시 보완**했다 — HL 11종목·
OrangeX 14개 심볼을 복원했고, themes를 19개→41개로 재분리했으며, venue 라벨의
실제 의미를 명확히 설명했다. `ts`는 `2026-08-19T02:30:00Z`로 그대로 유지했다;
(r) **이번 회차 종합**: ①BEAT·BICO·CASHCAT 재악화(직전 개선/반전이 되돌려짐),
②BTW 3회차 연속 재가속, ③ACE 계속 상승·원인 최초 구체화, ④HYPE·FARTCOIN·ETHFI
소폭 개선·HYPER 플러스 반전(HL 복원으로 확인), ⑤BLESS 부호 재반전(플러스→소폭
마이너스), ⑥GALA·ALPINE·GIGGLE 신규 관측대상 편입, ⑦메이저 안정권 유지(SOL의
HL 티커 최초 확인 포함), ⑧OrangeX 서비스 중단 32회차(약 65.75시간) 지속, ⑨부모
세션 검증 4건 보완 완료.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
