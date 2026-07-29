# 초프존(EMA 기울기 레짐) 필터 돈치안 브레이크아웃 [단타]

- **출처**: 지표 원안 LazyBear "Chop Zone" (TradingView 빌트인/커뮤니티 스크립트) — 설명 https://www.luxalgo.com/blog/chop-zone-indicator-identifying-choppy-vs-trending-markets/ ,
  TradingView 공식 문서 https://www.tradingview.com/support/solutions/43000589111-chop-zone/ ,
  응용 전략 예 "CHOP Zone Entry Strategy + DMI/PSAR Exit" by IronCasper https://www.tradingview.com/script/GrP0zABg-CHOP-Zone-Entry-Strategy-DMI-PSAR-Exit/
- **참여지표**: 정확한 좋아요 수는 스크립트별 상이(원문 접근 제한으로 개별 수치 미확인) — TradingView Chop Zone 계열 스크립트는 다수 존재하는 대중적 지표. 정량 참여지표는 "미확인"으로 표기.
- **백테스트 근거**: 없음(개념·규칙 기반). 정량 수치 원문 미확인.
- **타임프레임**: 15m 신호 / 1h 레짐 확인.
- **시장/대상**: BTC·ETH·유동성 상위 알트 무기한.

## 핵심 아이디어
초프존은 **34기간 EMA의 기울기(각도)를 arctan 변환**해 시장이 뚜렷한 추세(강한 상승/하락)인지, 약한 추세인지, 완전 횡보(choppy)인지를 6단계 색상 구간으로 분류하는 지표. 표준 Choppiness Index(TR/레인지 로그 비율, 이미 보유한 `choppiness-index-regime-breakout-swing`)와 **계산식이 완전히 다름**(EMA 기울기 기반 vs TR 로그 비율 기반) — 신호 상관이 낮을 가능성이 있어 별도 후보로 채택.

## 진입 규칙
1. `ema34 = EMA(close, 34)`
2. `avg_range = SMA(|high-low|, 15)` (변동성 정규화 분모)
3. `slope_deg = atan( (ema34_t - ema34_{t-5}) / avg_range ) * 180/π` (5봉 전 대비 기울기를 각도로 변환 — LuxAlgo 문서 기반 근사식, 원 Pine 정확 상수는 비공개라 근사임을 유의)
4. 레짐 분류(근사 임계값): `|slope_deg| ≥ 5` = 강한 추세(트렌드), `1.5 ≤ |slope_deg| < 5` = 약한 추세, `|slope_deg| < 1.5` = 횡보(초프).
5. **15m 레짐이 "강한 추세"**이고 방향이 상승(slope_deg > 0)일 때: 종가가 **Donchian(20) 상단** 상향 돌파 + 거래량 ≥ 20MA×1.5 → **롱**.
6. 방향이 하락(slope_deg < 0)이고 동일 조건으로 Donchian 하단 하향 돌파 → **숏**.
7. **횡보 구간(|slope_deg| < 1.5)에서는 신규 진입 금지**(필터 역할).

## 청산 규칙
- 익절: 진입 시 ATR(14, 15m) × 2.0 목표, 또는 slope_deg가 부호를 유지한 채 1.5 아래로 약화되면(추세 소멸) 분할 청산.
- 손절: 진입 반대편 Donchian 채널 경계(진입 시점 채널 폭 기준) 또는 ATR(14) × 1.2.
- 시간 청산: 진입 후 20봉(15m, 약 5시간) 내 목표 미달성 시 절반 청산 후 잔여 트레일.

## 파라미터
- ema_len=34 (고정 권장, 범위 21~50)
- avg_range_len=15 (범위 10~20)
- slope_lookback=5 (범위 3~8)
- slope_strong=5.0 / slope_weak=1.5 (도 단위, 임계값은 자산별 캘리브레이션 필요 — 고정값 아님)
- donchian_len=20 (범위 15~30)
- vol_mult=1.5 (범위 1.2~2.0)
- atr_tp_mult=2.0 / atr_sl_mult=1.2

## 코딩 난이도 / 데이터 요구
- 필요한 지표: EMA(34), 롤링 고저 레인지 평균, atan 변환(numpy), Donchian 채널, 거래량 MA, ATR. 전부 캔들 OHLCV 기반.
- 주의: **바이낸스 REST 캔들+거래량으로 완전 충족**. 다만 `slope_deg` 임계값(5/1.5)은 원 지표 스케일과 정확히 일치하지 않을 수 있어(비공개 상수) **백테스트 시 임계값을 자산별 슬로프 분포(백분위수)로 재보정** 필요.

## 스카우트 메모
- 강점: "레짐(추세/횡보) 자체를 EMA 기울기 각도로 정량화"하는 새로운 필터 축 — 기존 볼린저 스퀴즈(밴드폭) 필터와 원리가 다름. 15m 저빈도 강필터로 수수료 부담 완화 시도.
- 의심점: 원 Pine 스크립트의 정확한 정규화 상수가 비공개라 본 스펙은 근사치. 참여지표(좋아요 수)를 정확히 확인 못해 스크리닝 근거가 개념적 신뢰(대중적 지표)에 의존. 필터가 겹겹이라(레짐+돌파+거래량) 신호 빈도가 매우 낮을 위험 — 신호 빈도부터 먼저 점검 필요.
- 우리 단타 슬리브와의 관계: 기존 라이브 `scalp15m`(볼린저 이탈+거래량+스퀴즈≤35%)와 **부분 중복 가능성**(둘 다 "압축→추세 시작" 구조 추구) — 채택 전 두 필터의 신호 상관을 반드시 확인 권장. 대체보다는 **대안 필터 비교용**으로 적합.
