# [스윙] 엘더 포스 인덱스(EFI) 다이버전스 + 제로크로스

- **출처**: https://www.quantifiedstrategies.com/elder-force-index/ (QuantifiedStrategies, 백테스트 사이트) /
  https://www.tradingview.com/support/solutions/43000502259-elder-s-force-index-efi/ (TradingView 공식 지표 설명) /
  https://www.luxalgo.com/blog/elders-force-index-indicator-quantifying-market-force-and-direction/
- **참여지표**: -(백테스트/지표 문서 기반, 조회수 등 참여지표 확인 어려움)
- **백테스트 근거**: 원전(Alexander Elder, "Trading for a Living")은 주식시장 사례 연구 기반이며 정량 승률·PF는
  출처마다 상이. **명확한 단일 수치 없음(지표 문서+정성적 사례 기반)** — 채택 전 우리 프레임워크 백테스트 필수.
  다만 지표 자체(가격변화×거래량)가 OBV/CMF와 달리 **가격폭까지 반영**해 순수 거래량계 지표보다 다이버전스
  포착이 예민하다는 것이 정설.
- **타임프레임**: 4h 신호(다이버전스 탐지) / 1d EFI(13) 추세 필터
- **시장/대상**: BTC·ETH·주요 알트 무기물(거래량 데이터 신뢰 가능한 종목)

## 진입 규칙
- **추세 필터**: 1d EFI(13) = EMA13(raw EFI), raw EFI = (close[t]-close[t-1]) × volume[t].
  - EFI(13) > 0 → 상승추세 구간(롱만 탐색), EFI(13) < 0 → 하락추세 구간(숏만 탐색).
- **다이버전스 탐지(4h)**: EFI(2) = EMA2(raw EFI). 최근 lookback=20봉 내에서
  - 롱(강세 다이버전스): 가격이 더 낮은 저점(price_low2 < price_low1) 형성 **그러나** 동시점 EFI(2)는 더 높은
    (덜 음수인) 저점(efi_low2 > efi_low1) 형성.
  - 숏(약세 다이버전스): 가격이 더 높은 고점(price_high2 > price_high1) 형성 **그러나** EFI(2)는 더 낮은(덜
    양수인) 고점(efi_high2 < efi_high1).
- **트리거**: 다이버전스 확인 후, EFI(2)가 제로라인을 진입방향으로 재돌파(롱은 0 상향 돌파, 숏은 0 하향 돌파)
  하는 봉의 종가에 진입.

## 청산 규칙
- 익절: 직전 스윙 고점(롱)/저점(숏) 도달 시 50% 익절, 잔량은 2.5R 목표 또는 EFI(13) 추세 필터 반전 시 청산.
- 손절: 다이버전스 저점(롱) − 0.8×ATR(14) / 다이버전스 고점(숏) + 0.8×ATR(14).
- 시간 청산: 진입 후 15봉(4h, 약 2.5일) 내 1R 미도달 시 청산(모멘텀 미발생 판단).

## 파라미터
- efi_fast=2 (고정), efi_trend=13 (고정, Elder 표준)
- divergence_lookback=20봉 (범위 15~30)
- sl_atr_buf=0.8×ATR14 (범위 0.5~1.2)
- tp1_r=1.0R, max_hold=15봉

## 코딩 난이도 / 데이터 요구
- 필요한 지표: EFI(가격변화×거래량, EMA(2)와 EMA(13) 두 버전), ATR(14), 스윙 고/저점 탐지(로컬 극값).
- 주의: **REST 캔들+거래량으로 완전 구현 가능.** 다이버전스 탐지 로직(로컬 극값 페어링)은 liquidity-sweep,
  bollinger-rsi-divergence 등 기존 스펙에서 이미 유사 구현이 있어 재사용 가능 — 난이도 낮음~중간.

## 스카우트 메모
- 강점: OBV·CMF(이미 보유)와 달리 **1봉 가격변화폭**을 직접 곱해 거래량을 가중하므로, "거래량은 늘지만 가격은
  안 밀리는" 흡수(absorption) 국면을 더 예민하게 포착 — 다이버전스형 반전 포착에 특화.
- 의심점: 정규화 없이 원시(raw) 값을 쓰면 종목·기간별 스케일이 달라 다이버전스 판정 임계값이 흔들릴 수 있음
  (출처에서도 지적) → EMA(2)/EMA(13) 상대 비교(다이버전스는 절대값이 아닌 상대적 고저 비교)로 설계해 이 문제
  일부 회피했으나, 실제 구현 시 정규화(예: EFI/ATR) 검토 권장.
- 우리 단타 슬리브와의 관계: 기존 CVD taker volume divergence·OBV MA breakout divergence와 **컨셉이 겹침**(모두
  거래량-가격 다이버전스). 3종을 병행 백테스트해 가장 안정적인 1~2종만 채택하는 것을 권장 — 중복 후보군으로
  취급.
