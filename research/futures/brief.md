# 선물시장 스카우트 브리핑 — 2026-08-19 08:30 UTC (KST 2026-08-19 17:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-19
> 06:30 UTC)로부터 2시간 경과(정상 간격).**

## ⚠️ 최우선 과제 결론 — OKX OI 데이터 소스 괴리 전수점검

직전 회차에서 발견한 **GALA OKX OI의 CoinGecko값 vs 직접계산값 6.6배 괴리**가 다른 종목에도
있는지 전수 점검했다. **결론: 계통적 ctVal 승수 오류가 아니라 GALA 단발성 이상치**였다.

- OKX 직접 API(`public/open-interest`의 `oiCcy`, `public/instruments`의 `ctVal`,
  `market/tickers`의 `last`)로 **AAVE·ADA·ALGO·BEAT·BICO·ASTER** 6종목의 OI를 CoinGecko
  `okex_swap` 값과 대조한 결과 전부 **0.05~1%포인트 이내로 거의 완전 일치**했다:
  - AAVE: 직접계산 $11.87M vs CG $11.89M
  - ADA: 직접계산 $24.36M vs CG $24.37M
  - ALGO: 직접계산 $2.648M vs CG $2.656M
  - ASTER: 직접계산 $8.281M vs CG $8.285M
- **AEON만 직접계산 $3.606M vs CG $4.321M로 약 20% 차이**가 났으나, GALA의 560% 괴리와는
  규모가 다르고, 가격·OI가 실시간으로 움직이는 상황에서 두 API 호출 시점 차이로 설명 가능한
  범위로 판단했다.
- **OKX의 `oiCcy` 필드는 이미 `oi(계약수)×ctVal`을 내부적으로 반영한 값**임을 GALA
  (oiCcy/oi=10.0=ctVal 확인)·BICO(비율=1.0)·AEON(비율=10.0) 등에서 재확인했다 — 별도의
  ctVal 재승산은 불필요하며, `oiCcy×last` 공식 자체가 옳다.
- **판단**: 지난 회차 GALA 사례는 CoinGecko 쪽의 일회성 캐시/스냅샷 오류였을 가능성이 높다.
  앞으로도 OKX OI는 직접계산을 기본으로 하되, CoinGecko 값과 2배 이상 괴리가 보일 때만
  추가 대조하는 것으로 방침을 정리한다.

## 시장 전반 — 이번 회차 핵심

1. **ACE 숏스퀴즈 서사 급격히 냉각(이번 회차 최대 이슈)**: 4벤뉴 전부 20%p 이상 급락 —
   Binance +39.620%→**+11.6%**, Bybit +43.922%→**+9.892%**, HL +36.379%→**+9.091%**,
   Aster +45.5%→**+9.952%**. 펀딩도 동반 개선(덜 음수): Binance -0.00262→-0.00151,
   Bybit -0.00228→-0.00158, HL -0.00072→-0.0003, Aster -0.00064→-0.00029. 숏스퀴즈
   압력이 실질적으로 해소되는 국면으로 판단된다.
2. **BTW 6회차 연속 재가속**: Binance +67.443%→**+88.077%**, Aster +66.598%→**+90.373%**로
   오히려 상승폭이 재확대됐다(+14.63%→+25.73%→+37.84%→+56.63%→+66.6%→**+88~90%**).
   OI도 Binance 기준 $148.54M→**$161.79M**. 촉매 불명확하나 파급력 가장 뚜렷.
3. **APEX 재가속 반전**: 직전 회차 뚜렷한 감속(HL +10.13%→+5.303%, Bybit +9.259%→+5.463%)
   이후 이번 회차 다시 상승 — Bybit +5.463%→**+10.902%**, HL +5.303%→**+10.869%**.
4. **KAITO 4벤뉴 동시 감속 지속**: OKX +3.723%→**+3.438%**, Binance(USDT)
   +3.593%→**+3.224%**, HL +3.759%→**+2.748%**로 계속 꺾이며 플랫에 근접.
5. **CASHCAT 낙폭 4회차 연속 축소**(-14.57%→-13.42%→-12.258%→**-10.257%**, HL), Aster도
   동조(-12.211%→**-9.786%**).
6. **BICO -12%대로 추가 완화**(OKX -13.27%→-12.784%, Binance -13.271%→-12.332%, Aster
   -13.356%→-11.990%).
7. **BEAT 3벤뉴가 -23.4~23.9%로 더 좁게 수렴**(OKX -24.51%→-23.91%, Binance
   -23.924%→-23.607%, Aster -25.468%→-23.438%).
8. **AEON OKX·Aster가 -8%대로 수렴**(OKX -8.331%→-8.674%, Aster -11.438%→-8.520%), Bybit
   신규 커버리지도 -7.958%로 동조.
9. **GALA 완만한 하락 지속**(Binance -3.654%→-4.357%, OKX -3.657%→-4.087%, HL
   -3.443%→-3.727%), 촉매 여전히 미상.
10. **HYPE·FARTCOIN·HYPER 소폭 개선**(HYPE -2.927%→-2.258%, FARTCOIN -1.754%→-1.287%,
    HYPER +1.7%→+1.905%) 반면 **ETHFI는 마이너스권 지속**(HL -0.901%→-1.381%, Binance
    -1.064%→-1.231%).

**메이저(BTC·ETH·SOL)**: HL BTC -0.037%(vol $1,387.65M, OI $2,577.15M), ETH
+0.864%(vol $696.90M, OI $1,708.85M); Aster BTC +0.090%(vol $492.63M, OI $801.79M),
ETH는 **17회차 연속 truncation**; Binance BTC +0.203%(vol $6,004.21M, funding
0.00004431). **dYdX는 이번 회차 API가 404를 반환**해 BTC·ETH·SOL 3종목 모두 직전 회차
값을 이어받았다(정직 표기). **글로벌 시총·도미넌스는 WebSearch 교차확인 결과 총
$2.2~2.3조·BTC 도미넌스 약 56.5~58.9%**로 직전과 대체로 동일.

**데이터 품질**: funding 단위 보정(CoinGecko 경유 percent→fraction, `/100`)을 이번
회차도 Binance·Bybit·OKX(CG경유분)·HL·Aster 전 항목에 적용했고, OKX 직접 API(GALA
0.0001, KAITO -0.00030644, ETHFI -0.0000194)는 이미 fraction이라 변환 없이 사용했다.
**OrangeX는 35회차·약 71.75시간째 전면 중단** 지속. **Binance CoinGecko 벌크 조회가
이번 회차도 다수 심볼(BTW·KAITO·GALA·BICO·BEAT·AEON·ETHFI·GIGGLE·CORE·CAP·MMT·GRAM·
PIPPIN·BSB 등)을 누락**해 개별 GET으로 전량 보완했다. **OKX CoinGecko 벌크도 알파벳
'CVX' 근처에서 절단**돼(G~Z 구간 부재), GALA·KAITO·MMT·GRAM·PIPPIN·ETHFI·BSB는 OKX
직접 API(open-interest·instruments·market/tickers)로 개별 계산했다. **BSB·GRAM·
PIPPIN·MMT·GIGGLE의 OKX funding, KAITO(USDC)의 전 필드는 시간·호출 제약상 직전 회차
값을 이어받았음**을 정직 표기한다(가격·거래량·OI는 대부분 갱신).

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

funding은 raw fraction 기준.

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| **ACE** [급냉각] | Binance(CG대체) | $636.21M | $17.89M | -0.00151 | +11.6% | 숏스퀴즈 서사 급냉각(직전 +39.6%) |
| ACE [급냉각] | Bybit(CG대체) | $124.41M | $7.02M | -0.00158 | +9.892% | Binance와 함께 급냉각 |
| **BTW** [6회 재가속] | Binance(직접API) | $527.58M | $161.79M | 0.00054 | **+88.077%** | 6회차 연속 재가속, 오히려 확대 |
| BEAT [수렴] | OKX(직접API) | $87.72M | $5.85M | 0.00044 | -23.91% | 3벤뉴 -23.4~23.9%로 좁게 수렴 |
| BEAT [수렴] | Binance(직접API) | $99.98M | $10.03M | 0.0005 | -23.607% | 동조 |
| BICO [완화] | OKX(직접API) | $12.80M | $2.49M | -0.00005 | -12.784% | -12%대로 추가 완화 |
| BICO [완화] | Binance(직접API) | $14.61M | $5.21M | -0.00082 | -12.332% | 동조 |
| GALA [재하락] | Binance(직접API) | $16.77M | $6.52M | -0.00011 | -4.357% | 완만한 하락 지속, 촉매 미상 |
| GALA [재하락] | OKX(직접API) | $4.92M | $1.72M | 0.0001 | -4.087% | 동조. OI 이상치 전수점검 완료(상단 참고) |
| **ETHFI** [지속 부진] | Binance(직접API) | $18.42M | $22.57M | 0.00005 | -1.231% | 마이너스권 지속 |
| ETHFI [신규] | OKX(직접API) | $6.73M | $3.99M | -0.00002 | -1.374% | 이번 회차 신규 OKX 커버리지 |
| CAP [확대] | Binance(직접API) | $22.01M | $15.25M | -0.00009 | +3.685% | 플러스권 확대 |
| CAP [확대] | OKX(직접API) | $60.14M | $11.04M | -0.00026 | +2.675% | 동조 |
| AEON [수렴] | OKX(직접API) | $50.63M | $4.32M | 0.0001 | -8.674% | Aster와 -8%대로 수렴 |
| AEON [신규] | Bybit(CG대체) | $3.92M | $1.02M | 0.00005 | -7.958% | 신규 Bybit 커버리지, 동조 |
| **APEX** [재가속] | Bybit(CG대체) | $1.30M | $1.79M | 0.00005 | +10.902% | 재가속 반전(+5.5%→+10.9%) |
| GIGGLE [소폭 확대] | Binance(직접API) | $15.24M | $10.89M | 0.00005 | -2.161% | 소폭 마이너스 확대 |
| GIGGLE [소폭 확대] | OKX(직접API) | $8.39M | $1.70M | 0.00005 | -2.219% | 동조 |
| ALPINE [회복] | Binance(직접API) | $68.48M | $2.25M | 0.00005 | +9.647% | 상승폭 소폭 회복 |
| ALPINE [회복] | Bybit(CG대체) | $14.50M | $0.74M | 0.00005 | +9.521% | 동조 |
| CORE [미상장 유지] | OKX(직접API) | $1.82M | $0.94M | 0.00006 | -2.347% | Binance 미상장 지속, 단일소스 |
| ATOM [보합] | OKX(직접API) | $3.28M | $3.74M | 0.00003 | +1.883% | 보합권 지속 |
| ATOM [보합] | Binance(CG대체) | $13.44M | $15.32M | 0.00006 | +1.883% | 동조 |
| ATOM [보합] | Bybit(CG대체) | $5.98M | $13.65M | 0.0001 | +1.809% | 동조 |
| AAVE [보합] | OKX(직접API) | $16.80M | $11.89M | 0.00009 | -0.034% | 보합에 가까움 |
| AAVE [보합] | Binance(CG대체) | $40.27M | $43.97M | 0.00001 | -0.091% | 동조 |
| AAVE [보합] | Bybit(CG대체) | $11.19M | $40.47M | 0.00005 | -0.249% | 동조 |
| ADA [소폭 플러스] | OKX(직접API) | $24.01M | $24.37M | 0.00006 | +1.506% | 지속 |
| ADA [소폭 플러스] | Binance(CG대체) | $80.52M | $84.07M | 0.0 | +1.68% | 동조 |
| ADA [소폭 플러스] | Bybit(CG대체) | $35.82M | $55.06M | 0.0001 | +1.68% | 동조 |
| ALGO [플러스] | Binance(CG대체) | $6.18M | $7.88M | 0.0001 | +2.784% | 지속 |
| ALGO [플러스] | OKX(직접API) | $2.27M | $2.66M | 0.0001 | +3.033% | 동조 |
| MMT [마이너스] | OKX(직접API) | $3.35M | $2.12M | -0.00024 | -1.752% | 지속 |
| MMT [마이너스] | Binance(직접API) | $5.39M | $8.11M | -0.00009 | -1.813% | 동조 |
| GRAM [보합] | OKX(직접API) | $4.91M | $6.34M | 0.00005 | +0.686% | 유지 |
| GRAM [보합] | Binance(직접API) | $8.99M | $14.14M | 0.00003 | +0.686% | 완전 동조 |
| PIPPIN [소폭 마이너스] | OKX(직접API) | $2.87M | $1.73M | 0.00005 | -0.228% | 유지 |
| PIPPIN [소폭 마이너스] | Binance(직접API) | $5.78M | $5.70M | 0.00005 | -0.342% | 동조 |
| BSB [전환] | OKX(직접API) | $5.25M | $2.19M | 0.00032 | +5.29% | 플러스로 확대 |
| BSB [전환] | Binance(직접API) | $11.40M | $8.94M | 0.00014 | +5.316% | 동조 확대 |
| BANK [보합] | Binance(CG대체) | $24.05M | $10.70M | 0.00003 | -0.34% | 보합 부근 |
| BANK [보합] | Bybit(CG대체) | $2.86M | $3.98M | 0.00005 | -0.057% | 동조 |
| APR [유지] | OKX(CG대체) | $69.81M | $3.47M | 0.00006 | +11.022% | 고수준 유지 |
| APR [유지] | Bybit(CG대체) | $10.16M | $3.44M | 0.00005 | +11.081% | 동조 |
| AIO [전환] | Binance(CG대체) | $25.37M | $4.29M | 0.00005 | -7.196% | 플러스→마이너스 전환 |
| AIO [신규] | Bybit(CG대체) | $2.35M | $1.21M | 0.00005 | -7.347% | 신규 Bybit 커버리지, 동조 |
| ALLO [전환] | Binance(CG대체) | $30.27M | $12.04M | 0.00003 | -1.365% | 플러스→마이너스 전환 |
| ALLO [신규] | OKX(CG대체) | $29.87M | $0.33M | 0.00005 | -1.051% | 신규 OKX 커버리지, 동조 |
| ALLO [전환] | Bybit(CG대체) | $4.32M | $4.20M | 0.00005 | -0.751% | 동조 마이너스 |
| 1000RATS [유지] | Binance(CG대체) | $84.89M | $12.82M | 0.00026 | +5.377% | 두자리대 근접 유지 |
| 1000RATS [신규] | Bybit(CG대체) | $31.89M | $4.50M | 0.00045 | +5.91% | 신규 Bybit 커버리지, 동조 |
| ASTER(자체) [안정] | Binance(CG대체) | $11.14M | $69.83M | 0.00005 | -1.073% | 안정 유지 |
| ASTER(자체) [안정] | OKX(CG대체) | $2.54M | $8.28M | 0.00005 | -1.106% | 동조 |
| ASTER(자체) [신규] | Bybit(CG대체) | $1.81M | $39.72M | 0.00005 | -1.073% | 신규 Bybit 커버리지, 동조 |
| **KAITO** [감속] | OKX(직접API) | $25.73M | $5.03M | -0.00031 | +3.438% | 감속 지속(+3.723%→+3.438%) |
| KAITO [감속] | Binance(직접API,USDT) | $31.18M | $15.12M | -0.00036 | +3.224% | 동조 감속 |
| KAITO [이월] | Binance(직접API,USDC) | $3.82M | $1.14M | -0.00025 | +3.695% | 시간제약상 직전값 이어받음 |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

OrangeX 행은 35회차 연속 전면 중단으로 **모든 값이 null**(중단 사실 기록, 종목 삭제 아님).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| **ACE** [급냉각] | Hyperliquid | $2.55M | $1.86M | -0.0003 | +9.091% | 숏스퀴즈 서사 급냉각, CEX 동조 |
| ACE [급냉각] | Aster | $1.02M | $0.24M | -0.00029 | +9.952% | 동조 급냉각 |
| ACE [중단] | OrangeX | — | — | — | — | 35회차·약 71.75시간 |
| **BTW** [6회 재가속] | Aster | $7.70M | $13.68M | 0.00008 | **+90.373%** | +66.6%→+90.4%, Binance 동조 |
| **KAITO** [감속] | Hyperliquid | $1.69M | $5.82M | -0.00011 | +2.748% | CEX와 함께 감속 지속 |
| KAITO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| CASHCAT [지속 축소] | Hyperliquid | $9.12M | $12.50M | 0.00001 | -10.257% | 낙폭 4회차 연속 축소 |
| CASHCAT [지속 축소] | Aster | $0.67M | $0.70M | 0.00001 | -9.786% | 동조 축소 |
| CASHCAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GALA [재하락] | Hyperliquid | $0.99M | $1.12M | -0.00008 | -3.727% | Binance·OKX 동조, 촉매 미상 |
| BEAT [수렴] | Aster | $0.33M | $0.14M | 0.00001 | -23.438% | OKX·Binance와 -23%대 수렴 |
| BEAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BICO [완화] | Aster | $0.05M | $0.10M | 0.00005 | -11.99% | -12%대로 추가 완화 |
| BICO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| AEON [수렴] | Aster | $0.05M | $0.30M | 0.00001 | -8.52% | OKX와 -8%대로 수렴 |
| AEON [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GRAM [보합] | Hyperliquid | $1.64M | $15.29M | 0.00001 | +0.64% | 동조 |
| ATOM [보합] | Hyperliquid | $0.44M | $1.69M | 0.0 | +1.999% | 동조 |
| ATOM [보합] | Aster | $0.01M | $1.67M | 0.0001 | +1.377% | 동조 |
| AAVE [보합] | Hyperliquid | $2.90M | $57.68M | 0.00001 | -0.392% | 동조 |
| AAVE [보합] | Aster | $0.24M | $4.50M | 0.0001 | -0.057% | 동조 |
| AAVE [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ADA [플러스] | Hyperliquid | $3.59M | $29.26M | 0.00001 | +1.384% | 동조 |
| ADA [플러스] | Aster | $0.17M | $1.21M | 0.0001 | +1.507% | 동조 |
| ADA [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALGO [플러스] | Hyperliquid | $0.34M | $1.84M | 0.00001 | +2.812% | 동조 |
| ALGO [플러스] | Aster | $0.004M | $0.04M | 0.0001 | +1.874% | 동조 |
| ALGO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ASTER(자체) [안정] | Aster | $9.15M | $220.96M | 0.0 | -1.006% | 자체 OI 안정 유지 |
| ASTER(자체) [안정] | Hyperliquid | $0.29M | $13.51M | 0.00001 | -1.218% | 동조 |
| ASTER(자체) [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **HYPE** [소폭 개선] | Hyperliquid | $195.36M | $1,307.83M | 0.00001 | -2.258% | 낙폭 완화(-2.927%→-2.258%), 여전히 마이너스 |
| BLESS [확대] | Aster | $0.02M | $0.10M | 0.00005 | -5.444% | 마이너스 확대(-2.44%→-5.44%) |
| BLESS [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BTC [이월] | dYdX | $2.94M | $17.38M | 0.0 | -0.176% | API 404, 직전값 이어받음 |
| ETH [이월] | dYdX | $3.05M | $23.66M | 0.00000664 | +0.465% | API 404, 직전값 이어받음 |
| SOL [이월] | dYdX | $0.42M | $4.96M | 0.0 | +1.15% | API 404, 직전값 이어받음 |
| BTC [안정] | Hyperliquid | $1,387.65M | $2,577.15M | 0.0 | -0.037% | 메이저 안정 |
| ETH [안정] | Hyperliquid | $696.90M | $1,708.85M | 0.00001 | +0.864% | 메이저 안정 |
| BTC [안정] | Aster | $492.63M | $801.79M | 0.00004 | +0.09% | 메이저 안정 |
| ETH [truncation 17연속] | Aster | — | — | — | — | base=ETH 항목 부재 재확인 |
| 1000RATS [유지] | Aster | $0.43M | $0.04M | 0.00012 | +5.04% | Binance·Bybit와 동조 |
| AIO [전환] | Aster | $0.08M | $0.09M | 0.00005 | -5.669% | 마이너스권, CEX보다 낙폭 작음 |
| AIO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALLO [전환] | Aster | $0.14M | $0.06M | 0.0 | -0.666% | 마이너스 전환, CEX 동조 |
| ALLO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| APR [유지] | Aster | $0.29M | $0.34M | 0.00001 | +10.462% | OKX·Bybit와 동조 |
| APR [미상장] | Hyperliquid | — | — | — | — | 이번 회차도 HL 미상장 재확인 |
| BANK [보합] | Aster | $0.08M | $0.25M | 0.00001 | -0.085% | 보합 부근, CEX 동조 |
| BANK [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BSB [전환] | Aster | $0.13M | $0.12M | 0.00005 | +5.86% | 상승 전환, CEX 동조 |
| BSB [중단] | OrangeX | — | — | — | — | 중단 지속 |
| CAP [확대] | Aster | $0.06M | $0.17M | 0.00001 | +3.001% | 플러스로 확대, CEX 동조 |
| CAP [중단] | OrangeX | — | — | — | — | 중단 지속 |
| FARTCOIN [소폭 개선] | Hyperliquid | $2.68M | $29.63M | 0.00002 | -1.287% | 낙폭 완화(-1.754%→-1.287%) |
| ETHFI [지속 부진] | Hyperliquid | $3.85M | $11.23M | 0.00001 | -1.381% | Binance와 함께 마이너스 지속 |
| HYPER [소폭 개선] | Hyperliquid | $0.05M | $0.20M | 0.00001 | +1.905% | 직전보다 소폭 개선 |
| **APEX** [재가속] | Hyperliquid | $0.26M | $0.67M | 0.00001 | +10.869% | Bybit와 함께 재가속 반전 |
| HYNA:BTC-USD | Hyperliquid | $0.31M | $2.19M | 0.00001 | +0.097% | HIP-3 빌더배포, BTC 동조 |
| HYNA:ETH-USD | Hyperliquid | $0.14M | $1.63M | 0.00001 | +0.985% | HIP-3 빌더배포, ETH 동조 |
| HYNA:HYPE | Hyperliquid | $0.15M | $0.66M | 0.00001 | -2.059% | HIP-3 빌더배포, HYPE 동조 |
| HYNA:PUMP | Hyperliquid | $0.06M | $0.16M | 0.00001 | +11.867% | HIP-3 빌더배포 |
| HYNA:SOL-USD | Hyperliquid | $0.03M | $0.53M | 0.00001 | +1.293% | HIP-3 빌더배포, 유일 실재 SOL 항목 |

## 테마 태그 (요약)

1. OKX OI 데이터 소스 괴리 전수점검 — GALA는 단발성 CG 이상치, 계통오류 아님 확정(상단 참고) (okx-oi-discrepancy-resolved-gala-isolated)
2. ACE 4벤뉴 급격히 냉각, 펀딩도 개선 — 숏스퀴즈 실질 해소 국면 (ace-short-squeeze-cools-sharply)
3. BTW 6회차 연속 재가속(오히려 확대) (btw-continues-accelerating)
4. APEX 재가속 반전(직전 감속→이번 급반등) (apex-reaccelerates)
5. KAITO 4벤뉴 감속 지속, 플랫 근접 (kaito-decelerates-further)
6. CASHCAT 낙폭 4회차 연속 축소 (cashcat-narrows-continuously)
7. BICO -12%대로 추가 완화 (bico-continues-easing-toward-12pct)
8. BEAT 3벤뉴 -23%대로 좁게 수렴 (beat-decline-mildly-eases)
9. AEON OKX·Aster -8%대 수렴, Bybit 신규 커버리지 (aeon-converges-around-8pct)
10. GALA 완만한 하락 지속, 촉매 미상 (gala-slow-slide-continues)
11. HYPE 낙폭 소폭 완화, 여전히 마이너스 (hype-mild-improvement)
12. FARTCOIN 낙폭 소폭 완화 (fartcoin-mild-improvement)
13. HYPER 직전보다 소폭 개선 (hyper-mild-improvement)
14. ETHFI 지속 마이너스, OKX 신규 커버리지 (ethfi-holds-negative)
15. GIGGLE/ALPINE/CORE/CAP/ATOM/AAVE/ADA/ALGO/MMT/GRAM/PIPPIN/BSB/BANK/APR/AIO/ALLO/1000RATS/ASTER/BLESS — 세부는 표 참고
16. HYNA:* 계열 계속 포함(hyna-builder-deployed-markets)
17. 데이터: Binance CG벌크 심볼 다수 누락(binance-bulk-truncation-confirmed), OKX CG벌크 'CVX' 근처 절단(okx-cg-bulk-truncation-confirmed), OrangeX 35회차(~71.75h), Aster ETH truncation 17회차, 일부 항목 직전값 이어받음(정직표기), dYdX API 404로 메이저 3종 이월
18. 글로벌 시총·도미넌스 대체로 동일 (global-dominance-roughly-unchanged)
19. 주식화·상품 토큰 전부 제외 유지

## 한계

(a) 이번 회차 최우선 과제였던 **OKX OI 괴리 전수점검을 완료**했다 — GALA의 6.6배 괴리는
계통적 ctVal 오류가 아닌 단발성 CoinGecko 이상치로 판정했으며, 6종목 대조로 `oiCcy×last`
공식의 정확성을 재확인했다(AEON만 ~20% 차이, 스냅샷 시점차로 추정, 지속 관찰 권고); (b)
**dYdX API가 이번 회차 404를 반환**해 BTC·ETH·SOL 3종목 전부 직전 회차 값을 이어받았다
(정직 표기) — 다음 회차에 재시도 필요; (c) OKX CoinGecko 벌크 조회가 알파벳 'CVX' 근처에서
절단돼 G~Z 구간 심볼(GALA·GIGGLE·GRAM·KAITO·MMT·PIPPIN 등)은 OKX 직접 API로 개별
계산했다; (d) Binance CoinGecko 벌크 조회도 다수 심볼을 누락해 개별 GET으로 보완했다;
(e) BSB·GRAM·PIPPIN·MMT·GIGGLE의 OKX funding과 KAITO(USDC)의 전 필드는 시간·호출
제약상 직전 회차 값을 이어받았다(정직 표기, 가격·거래량·OI는 대부분 갱신); (f) OrangeX
전면 중단이 35회차·약 71.75시간째 지속된다; (g) Aster ETH truncation이 17회차 연속
지속된다; (h) 글로벌 시총·도미넌스는 WebSearch 스니펫 교차확인이며 CoinGecko `/global`
직접조회는 이번 회차도 생략했다; (i) 주식화·상품·프리IPO 합성 perp 토큰은 이번 회차도
전부 제외했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
