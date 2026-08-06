# [단타] OI-가격 동방향 확장 컨퍼메이션 추세추종 (4사분면 중 미사용 2사분면)

- **출처**: https://cryptoquant.com/insights/quicktake/684ae1a2c26bc826d28c7152-Binance-Open-Interest-Divergence-Signals-Caution-as-Bitcoin-Approaches-110K (CryptoQuant, OI×가격 4분면 국면 분류 원 프레임) /
  https://bikotrading.com/trading-strategy-on-open-interest-and-delta (Bikotrading Academy) /
  https://www.utradealgos.com/blog/the-ultimate-guide-understanding-oi-based-strategies-in-algo-trading (uTradeAlgos)
  — **동일 출처를 우리 기존 스펙 `oi-roc-price-divergence-squeeze-reversal-scalp.md`가 이미 인용**하고 있으며, 그 스펙은 4분면(가격↑OI↑=건전추세, 가격↑OI↓=숏스퀴�즈소진, 가격↓OI↑=숏누적, 가격↓OI↓=롱청산플러시) 중 **OI 감소 2개 분면(다이버전스)만 반전 신호로 구현**함. 본 스펙은 **나머지 2개 분면(OI 증가, 컨퍼메이션)을 추세추종 신호로 별도 구체화**한 상보 전략.
- **참여지표**: 없음(전문 파생 데이터 블로그) — SNS 참여지표 미확인. 다만 "가격+OI 동방향=신규자금 유입 확인"은 파생상품 트레이딩 교육 콘텐츠에서 가장 기본적으로 가르치는 프레임 중 하나.
- **백테스트 근거**: 없음(개념 기반). **채택 전 자체 백테스트 필수**. 기존 `oi-roc-price-divergence-squeeze-reversal-scalp.md`(반전 버전)와 신호가 상호배타적(같은 데이터로 반대 논리)이므로, 채택 시 두 버전을 **나란히 백테스트해 어느 쪽이 실제 엣지가 있는지**(또는 둘 다 없는지) 판별 필요.
- **타임프레임**: 15m 신호 / 1h 확인
- **시장/대상**: BTC·ETH·시총상위 알트 무기한 (OI 데이터가 유의미하게 잡히는 유동성 상위 종목)

## 진입 규칙
- OI 변화율(ROC): 최근 N=20봉(15m) 대비 현재 OI % 변화. 가격 변화율(ROC): 동일 구간 종가 % 변화.
- **롱(신규 매수세 유입 확인)**: 가격 ROC ≥ +`price_roc_threshold`(예 +1.0%) **그리고** OI ROC ≥ +`oi_roc_threshold`(예 +3%, 신규 롱 포지션 유입으로 해석) **그리고** 같은 방향으로 거래대금이 최근 20봉 평균 대비 `volume_confirm_mult`=1.2배 이상 → 추세추종 롱.
- **숏(신규 매도세 유입 확인)**: 가격 ROC ≤ −`price_roc_threshold` **그리고** OI ROC ≥ +`oi_roc_threshold`(신규 숏 포지션 누적으로 해석) **그리고** 거래대금 확인 → 추세추종 숏.
- 확인 TF(1h): 진입 방향과 같은 부호로 EMA(20) 기울기가 양(롱)/음(숏)일 때만 진입(상위 TF 추세 정합 확인, 역추세 구간 배제).

## 청산 규칙
- 익절: ATR(15m,14) 트레일링 ×1.5 (신고가/신저가 갱신 시 갱신) 또는 목표 R:R `rr_target`=2.0:1 도달 중 먼저 도달.
- 손절: 신호봉 시가 기준(진입 방향 반대) 또는 ATR(14)×1.2 중 타이트한 쪽.
- 시간 청산: `max_hold_bars`=12봉(15m×12=3시간) 내 목표 미도달 시 강제청산(OI 컨퍼메이션 신호는 지속력이 짧다는 가정, 반전 버전과 동일 전제 적용).

## 파라미터
- oi_roc_lookback=20 (범위 12~30)
- oi_roc_threshold=3% (범위 2~6%, 클수록 신호 희소)
- price_roc_threshold=1.0% (범위 0.7~2.0%)
- volume_confirm_mult=1.2 (범위 1.0~1.5)
- atr_trail_mult=1.5 (범위 1.0~2.0)
- atr_stop_mult=1.2 (범위 1.0~1.8)
- rr_target=2.0 (범위 1.5~2.5)
- max_hold_bars=12 (15m 기준, 범위 8~20)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 미결제약정(OI) 시계열(`/fapi/v1/openInterestHist`), 가격 ROC, 거래대금, ATR, EMA(20, 1h).
- 주의: **바이낸스 REST(캔들+OI)로 완전 구현 가능**, 오더북/틱/실시간 청산 불필요. OI 실시간 조회는 최근 30일 제한 → 장기 백테스트는 `data.binance.vision/data/futures/um/daily/metrics/` 덤프 사용(기존 OI 관련 스펙들과 동일 인프라 재사용). "OI 증가=신규 포지션"이라는 해석은 실제 청산 데이터가 아닌 간접 추정이므로 다이버전스 버전과 마찬가지로 해석 오류 리스크 존재.
- 난이도: 낮음. 기존 `oi-roc-price-divergence-squeeze-reversal-scalp.md` 구현 코드에서 조건 부호만 뒤집으면 재사용 가능(엔지니어링 비용 매우 낮음 — 두 버전을 한 번의 백테스트 러닝으로 A/B 비교 가능).

## 스카우트 메모
- **강점**: 기존 스펙이 4분면 중 절반만 구현하고 나머지 절반을 텍스트로만 언급한 채 남겨둔 부분을 완결시키는 상보 전략. 반전(다이버전스) vs 추세추종(컨퍼메이션) 두 가설을 **동일 데이터·동일 구현비용으로 정면 비교**할 수 있어 검증 효율이 높음(코드 재사용률 높음 = 백테스트 착수 비용 거의 0).
- **의심점**: "가격+OI 동방향 확장이 추세 지속을 의미한다"는 직관은 그럴듯하나, 이미 널리 알려진 통설이라 **차익거래로 마모(arbitraged away)됐을 가능성**도 동일하게 존재(다이버전스 버전과 같은 리스크). 신규 진입 시그널 특성상 상위 TF 추세와 동일 방향으로만 진입하도록 필터를 걸었지만, 이는 사실상 "돌파+거래량" 계열(우리 라이브 scalp15m)과 신호가 겹칠 위험 — 상관관계 점검 필수.
- **우리 슬리브와의 관계**: 라이브 `scalp15m`(볼린저 이탈+거래량+OI 필터)과 OI를 필터로 쓰는 점에서 인접하나, 이 전략은 **볼린저 없이 순수 OI×가격×거래량 ROC 조합만으로 신호를 생성**한다는 점에서 신호 생성 메커니즘이 다름 — 대체가 아니라 신호소스 비교용. 반전 버전(`oi-roc-price-divergence-squeeze-reversal-scalp.md`)과는 같은 데이터의 반대 가설이므로 **동시 채택 불가**(상호배타), 백테스트로 승자만 선택.
