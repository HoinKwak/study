# [단타] STARC Bands (Stoller Average Range Channel) 평균회귀 스캘프

- **출처**: 지표 개념 원저자 Manning Stoller. 참고 2차자료 — [LightningChart 블로그](https://lightningchart.com/blog/trader/starc-bands/), [TradingPedia](https://www.tradingpedia.com/forex-trading-indicators/starc-bands/), [STARC Bands Strategy — TradingView 스크립트(HPotter)](https://www.tradingview.com/script/VKUCQZnV-STARC-Bands-Strategy/), [Synapse Trading](https://synapsetrading.com/stoller-average-range-channel-starc-bands/), [QuantifiedStrategies(원문 봇검증 차단으로 본문 미확인)](https://www.quantifiedstrategies.com/stoller-average-range-channels/)
- **참여지표**: TradingView HPotter "STARC Bands Strategy" 스크립트 — **좋아요/즐겨찾기 83 / 조회·사용 3,607**(WebFetch로 원문 페이지 직접 확인). 그 외 STARC 관련 2차 블로그·포럼(ForexFactory 스레드 등) 다수 존재 — 오래된(2000년대 초 개발) 고전 지표라 "핫한" 신규 콘텐츠는 아니지만 다수 플랫폼(TradingTechnologies, WealthCharts, cTrader류)이 기본 내장 지표로 채택할 만큼 검증된 개념.
- **백테스트 근거**: **없음(정량 수치 원문 미확인)**. QuantifiedStrategies.com의 전용 백테스트 페이지가 존재하나 봇 검증(Cloudflare)에 막혀 WebFetch로 본문(승률·PF·표본기간)을 확인하지 못했다. TradingView HPotter 스크립트 페이지에도 성과 수치는 게시돼 있지 않음. → **참여지표(좋아요/사용횟수) + 지표 개념 신뢰도 기반**으로 채택, 수치 인용 없음.
- **타임프레임**: 15m 신호 / 1h 확인(레인지 국면 필터용).
- **시장/대상**: BTC·ETH·주요 알트 USDT 무기한.

## 지표 정의
- 중심선 SMA(period=6) — 원저자 기본값은 5~6봉 단기 SMA로 소스마다 약간 다름(검색 결과 "5-period 또는 6-period"가 혼재 인용됨 → 본 스펙은 6으로 고정하고 5~10 범위 스윕 권장).
- 상단밴드 = SMA(6) + ATR(15) × k
- 하단밴드 = SMA(6) − ATR(15) × k
- k(배수)는 소스마다 1.3~2.0으로 다르게 인용됨(가장 흔한 값은 **2.0**, 일부 자료는 1.3) → 기본값 2.0, 튜닝 범위 1.2~2.2.

## 진입 규칙
- **레인지 국면 필터(선행 조건)**: 기존 `regime.py`의 국면 판정(또는 ADX(14)<20~25) 로 RANGE 국면일 때만 아래 신호 채택. STARC는 추세장에서 밴드에 붙어 계속 달리는(밴드 워크) 손실 패턴이 흔한 순수 평균회귀 지표이므로 추세 필터가 필수.
- **롱**: 저가(low)가 하단밴드를 터치 또는 종가가 하단밴드 아래로 마감 후, 다음 봉이 하단밴드 위로 재진입(되돌림 확인) + 해당 구간 거래량이 과열 투매가 아닌 평이한 수준(직전 20봉 평균 대비 2배 미만, 청산 캐스케이드성 급락 배제).
- **숏**: 고가(high)가 상단밴드를 터치 또는 종가가 상단밴드 위로 마감 후, 다음 봉이 상단밴드 아래로 재진입.

## 청산 규칙
- 익절: 중심선(SMA6) 도달 시 1차 익절(50%), 반대쪽 밴드 도달 시 잔량 청산. 또는 고정 R:R 1.5~2.0.
- 손절: 진입 신호봉의 밴드 터치 극단값(저가/고가) 바깥으로 ATR(15)×0.5 버퍼.
- 시간/조건 청산: 진입 후 국면이 RANGE→TREND로 전환되면(레짐 필터 반전) 즉시 손절/청산(밴드 워크 대응).

## 파라미터
- sma_period=6 (범위 5~10)
- atr_period=15 (범위 10~20)
- band_mult=2.0 (범위 1.2~2.2)
- adx_regime_threshold=25 (범위 20~30, 이보다 낮아야 레인지로 판정)
- stop_buffer_atr=0.5 (범위 0.3~1.0)
- vol_spike_exclude_mult=2.0 (범위 1.5~3.0, 이 배수 넘는 급증봉은 청산성 캔들로 간주해 진입 제외)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: SMA, ATR, ADX(또는 기존 regime.py 국면판정), 거래량 이동평균. **전부 바이낸스 REST 캔들(OHLCV)로 충족.** 오더북·틱 불필요.
- 난이도: 낮음(볼린저/켈트너 채널류와 계산 구조 동일, 밴드 폭 정의만 ATR 기반으로 다름).

## 스카우트 메모
- 강점: 개념이 단순·명확해 구현 난이도 최저. ATR 기반 밴드라 변동성 적응력이 볼린저(표준편차 기반)와 다른 반응 곡선을 가져 **기존 `bollinger-band-fade-range`/`keltner-channel-breakout`과는 밴드 산식이 달라 신호 상관이 완전히 겹치진 않을 것**으로 추정(단, 개념적으로 "채널 평균회귀"군에 속해 있어 근본적으로는 유사 계열).
- 의심점: (1) 정량 백테스트 근거를 전혀 확보 못함 — QS 페이지 봇차단, TradingView 스크립트도 성과 미게시. (2) 밴드 배수(k) 기본값이 출처마다 1.3~2.0으로 갈려 파라미터 확정성이 낮음 — 튜닝 필요. (3) 이미 우리 레포에 `bollinger-band-fade-range`, `keltner-channel-breakout`, `ma-envelope-percent-band-mean-reversion-scalp` 등 "중심선±변동성밴드 평균회귀" 계열이 다수 있어 **개념적 중복 위험이 상당함** — 신규 알파보다는 밴드 산식 비교 실험용으로 가치.
- 우리 단타 슬리브와의 관계: 현재 라이브 `scalp15m`(볼린저 이탈 돌파형)과 정반대 철학(돌파 추종 vs 평균회귀) — 보완재 후보. 다만 위 기존 평균회귀 스펙들과 백테스트 우선순위를 다퉈야 하므로, 이 스펙 단독보다는 "채널 평균회귀 계열 통합 비교 백테스트"로 묶어 검증하는 편이 효율적.
