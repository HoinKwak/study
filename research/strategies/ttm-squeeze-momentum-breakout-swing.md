# [스윙] TTM 스퀴즈(볼린저×켈트너 압축) 모멘텀 브레이크아웃

- **출처**: TradingView "Squeeze Momentum Indicator [LazyBear]" https://www.tradingview.com/script/nqQ1DT5a-Squeeze-Momentum-Indicator-LazyBear/ (원 개념: John Carter, *Mastering the Trade* Ch.11 "TTM Squeeze") /
  전략화 사례: https://medium.com/@FMZQuant/volatility-compression-momentum-breakout-tracking-strategy-quantitative-implementation-of-ttm-dfe0232ccf51 /
  백테스트 인용: https://trendspider.com/learning-center/introduction-to-ttm-squeeze/ , https://blog.pickmytrade.trade/squeeze-momentum-strategy/
- **참여지표**: TradingView 원 지표 **좋아요/부스트 677 · 조회(uses) 2,972,107회** — TradingView 역대 최다 사용 지표 중 하나(파생 스크립트 수십 개).
- **백테스트 근거**:
  - BitMEX XBTUSD·ETHUSD, **1h~4h 타임프레임에서 양호한 성과, MaxDD ≈ 12%** (구체 수익률·PF·표본수는 출처에 비공개 — 재검증 필요).
  - FMZQuant 구현: Binance Futures BTC_USDT, 2024-06-19~2025-06-17 백테스트 프레임 존재하나 **정량 성과 수치는 원문에 미기재**(규칙만 검증 가능).
  - 파생 전략(TradingView "Squeeze Momentum Strategy [LazyBear][Bitduke]") 최적화 버전은 **PF 1.215~2.309** 범위 보고(자산·기간 불명, 참고용).
  - → **표본 근거는 약~중간 수준**. 규칙은 명확하고 재현 가능하나 크립토 정량 수치는 우리 프레임워크로 직접 재검증 필요.
- **타임프레임**: 신호 1h, 확인/추세필터 4h (스윙 보유 수시간~수일)
- **시장/대상**: BTC·ETH 등 메이저 무기한(유동성 상위 알트 확장 가능)

## 진입 규칙
- **스퀴즈 감지**: 볼린저밴드(20, ×2.0)가 켈트너채널(20, ATR×1.5) **완전히 내부에 위치**하면 "스퀴즈 ON"(저변동성 압축).
- **모멘텀 히스토그램**: `donchian_mid = (최근20봉 최고가+최저가)/2`, `avg = (donchian_mid + SMA20종가)/2`, `momentum = LinReg(close - avg, 20)`. 값 부호·방향으로 색상(가속/감속) 판정.
- **트리거**: 스퀴즈 ON 상태가 **연속 3봉 이상 유지된 뒤 스퀴즈가 해제되는 첫 봉**(BB가 KC 밖으로 나가는 순간) + 모멘텀 히스토그램 값이 **0 위이고 직전봉보다 큰 값(가속)** → 롱.
- 숏: 동일 조건에서 모멘텀이 **0 아래이고 직전봉보다 작은 값(가속 하락)**.
- 확인: 4h 봉에서도 같은 방향 모멘텀(0 기준) 유지 시 신뢰도 상향(옵션 필터).

## 청산 규칙
- 익절: 모멘텀 히스토그램 **색이 반전(가속→감속)** 되는 시점 부분청산, 완전 반전(부호 전환) 시 전량 청산.
- 손절: 스퀴즈 구간(직전 3봉)의 반대쪽 극값 또는 진입가 ± 1.5×ATR(20).
- 시간 청산: 스퀴즈 해제 후 10봉 내 모멘텀이 가속을 못 보이면(횡보 전환) 청산.

## 파라미터
- bb_period=20, bb_mult=2.0 / kc_period=20, kc_mult=1.5 (범위 1.0~2.0)
- squeeze_min_bars=3 (범위 2~6)
- momentum_lookback=20 (범위 14~26)
- sl_atr_mult=1.5 (범위 1.0~2.5)
- htf_confirm=4h (옵션 on/off)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 볼린저밴드, 켈트너채널(ATR 기반), 선형회귀(모멘텀 히스토그램) — 전부 캔들 OHLC로 계산 가능.
- 주의: **바이낸스 REST 캔들만으로 완전 충족.** 오더북/틱/청산 불필요. 선형회귀 계산은 numpy `polyfit` 등으로 구현(약간의 코딩 손이 감).

## 스카우트 메모
- 강점: TradingView 역대 최인기 지표 중 하나(조회 300만↑)로 재현성 있는 파생 전략이 다수 존재 — 규칙이 표준화돼 있어 코딩 난이도 낮음. 켈트너+볼린저 이중 밴드라 우리 볼린저 전용 스퀴즈(`bollinger-squeeze-breakout-daily.md`)와 메커니즘이 다름(밴드 두 개 교차 + 모멘텀 오실레이터).
- 의심점: 크립토 정량 백테스트 수치가 출처마다 불명확/비공개 — **반드시 직접 재백테스트 필요**(허수 인기에 기댄 케이스일 수 있음).
- 우리 단타 슬리브와의 관계: **보완**. 기존 볼린저 돌파 스캘핑(scalp.py)과 유사 계열이지만 타임프레임(1h/4h)과 필터(켈트너+모멘텀)가 달라 스윙 슬리브 후보로 적합.
