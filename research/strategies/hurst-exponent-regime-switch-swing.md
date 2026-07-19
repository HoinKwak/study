# [스윙] Hurst 지수 기반 추세/평균회귀 레짐 스위칭

- **출처**: 개념·공식 — RobotWealth "Demystifying the Hurst Exponent Part 2"
  https://robotwealth.com/demystifying-the-hurst-exponent-part-2/ (WebFetch 확인, 분산법 공식) /
  Macrosynergy "Detecting trends and mean reversion with the Hurst exponent"
  https://macrosynergy.com/research/detecting-trends-and-mean-reversion-with-the-hurst-exponent/ /
  크립토 정량 검증 — MDPI(Mathematics 저널) "Anti-Persistent Values of the Hurst Exponent Anticipate
  Mean Reversion in Pairs Trading: The Cryptocurrencies Market as a Case Study"
  https://www.mdpi.com/2227-7390/12/18/2911 (WebFetch로 원문 수치 확인)
- **참여지표**: - (학술논문·퀀트 실무 블로그, SNS 참여지표 없음. 대신 동료검토 학술지 게재 및 실제 크립토
  데이터 정량검증이 참여지표를 대체함)
- **백테스트 근거**: **부분적으로 확인됨, 단 대상이 다름 — 반드시 구분해서 읽을 것.**
  - MDPI 논문(WebFetch로 원문 확인)은 **상위 20개 크립토(BTC·ETH·BNB·SOL·XRP·DOGE·ADA 등) 2019-01-01~2024-06-05
    시간봉 데이터**로 **코인트그레이션 페어 스프레드**에 Hurst(H<0.5) 필터를 추가했을 때: "co-integration
    기반 전략이 가장 수익성 높음(Investment $13.04, Profit $8.03, Profit 61.56%)", **H<0.5 필터 사용 시
    평균 보유기간이 약 13시간(필터 미사용 시 22시간)**으로 단축됨을 확인 — 즉 "Hurst<0.5일 때 평균회귀가
    실제로 더 빠르게 작동한다"는 것은 크립토 데이터로 정량 검증됨.
  - **단, 원 논문의 전략 자체는 코인트그레이션 페어 스프레드 트레이딩**(우리 기존 `btc-eth-zscore-spread.md`와
    유사 구조)이며, 본 스펙이 제안하는 **"단일 자산 추세추종↔평균회귀 전환"**은 그 응용/확장이지 논문에서
    직접 백테스트된 것이 아니다 → **본 스펙 고유의 정량 성과는 원문 미확인, 재검증 필수**로 정직히 표기.
- **타임프레임**: Hurst 산출은 4h 종가 롤링 window(약 7일=42봉, MDPI 논문에서 7일 window가 최적으로 확인됨).
  진입 신호는 4h~1d.
- **시장/대상**: BTC·ETH·상위 알트 무기한.

## 진입 규칙
- **Hurst 지수 계산**(분산법, RobotWealth 공식): 여러 lag τ에 대해 `tau[lag] = sqrt(std(price[lag:] - price[:-lag]))`
  계산 후 `log(tau)` vs `log(lag)` 선형회귀 기울기 `m`을 구해 `H = m * 2`. lag 범위 2~20(RobotWealth 권장,
  단 lag 선택이 결과에 큰 영향을 미친다는 점 주의 — 백테스트 시 lag 범위 민감도 확인 필수).
- **레짐 분류**(MDPI·Macrosynergy 통용 임계): `H > 0.55` = 추세(persistent), `H < 0.45` = 평균회귀
  (anti-persistent), `0.45~0.55` = 랜덤워크(무거래).
- **추세 레짐(H>0.55) 진입**: Donchian(20, 4h) 상단 돌파 시 롱, 하단 돌파 시 숏 (추세추종 서브전략).
- **평균회귀 레짐(H<0.45) 진입**: RSI(2, 4h) < 10이면 롱(과매도 반등), RSI(2, 4h) > 90이면 숏(과열 되돌림)
  — 볼린저 밴드(20, 2σ) 이탈 동반 시 신뢰도 가산.
- **랜덤워크 레짐(0.45≤H≤0.55)**: 신규 진입 금지(무거래).

## 청산 규칙
- 추세 레짐 포지션: Donchian(10, 4h) 반대 극값 이탈 청산 (터틀식 추세추종 청산), 손절은 ATR(14,4h)×2.
- 평균회귀 레짐 포지션: 볼린저 중심선(SMA20) 도달 시 익절, 손절은 진입가 대비 ATR(14,4h)×1.5.
- **레짐 전환 청산**: 보유 중 Hurst가 반대 레짐(예: 추세 포지션 보유 중 H<0.45로 전환)으로 넘어가면 즉시 청산
  (레짐 가정이 깨졌으므로).
- 시간 청산: 없음(레짐 지속 시 보유, 레짐 전환/청산조건까지).

## 파라미터
- hurst_window=42봉(4h, 약 7일 — MDPI 최적 window) (범위 24~168h 상당)
- hurst_lags=2~20 (분산법 lag range, 민감도 검증 필요)
- hurst_trend_th=0.55 / hurst_meanrev_th=0.45 (범위 각각 0.52~0.60 / 0.40~0.48)
- donchian_entry=20 / donchian_exit=10 (추세 레짐)
- rsi2_long=10 / rsi2_short=90 (평균회귀 레짐)
- atr_mult_sl_trend=2.0 / atr_mult_sl_meanrev=1.5

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 종가 기반 Hurst(분산법, numpy 선형회귀만 필요) + Donchian + RSI(2) + 볼린저 + ATR.
  **전부 4h(15m 리샘플) OHLCV로 계산 가능**, 추가 데이터 불필요.
- 난이도: 중상(Hurst 계산 자체는 간단하나, lag 선택·window 길이에 결과가 민감 — 파라미터 스윕 필수).
- 주의: 오더북·틱 데이터 불필요. 다만 롤링 Hurst 계산은 매봉 회귀분석이라 백테스트 벡터화 시 연산량 고려.

## 스카우트 메모
- 강점: 오늘 검증에서 지적된 "단일 지표 크로스의 엣지 부재" 문제에 대한 구조적 해법 — 시장이 **추세인지
  평균회귀인지를 먼저 통계적으로 판별**한 뒤 그에 맞는 서브전략을 적용하는 **메타/레짐 스위칭 구조**로,
  기존 `choppiness-index-regime-breakout-swing`(변동성 압축→돌파 단일방향)과 달리 **양방향(추세+평균회귀)
  서브전략을 모두 갖춘 진짜 레짐 스위처**라는 점이 구조적으로 다름.
  MDPI 논문이 크립토 데이터로 "H<0.5일 때 평균회귀가 더 빠르게 작동"함을 실증한 것은 신뢰할 만한 정량 근거.
- 의심점: 논문의 실제 백테스트 대상은 페어 스프레드이지 단일자산 방향성 전략이 아니므로, 본 스펙의
  추세추종/평균회귀 서브전략 자체 성과는 **완전히 미검증**. Hurst 계산의 lag/window 민감도가 커서
  과최적화 위험이 있음 — 반드시 파라미터 안정성(플라토) 확인 필요.
- 우리 슬리브와의 관계: 기존 `btc-eth-zscore-spread`(페어)와는 구조가 다름(단일자산). 기존 중기 슬리브
  (슈퍼트렌드+볼린저 눌림목)와 **레짐 감지 방식이 완전히 다른 정량 지표**를 사용해 보완재로 유망 —
  다만 구현 복잡도가 있어 백테스트 우선순위는 후순위 권장.
