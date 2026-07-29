# [스윙] Time Segmented Volume(TSV) 제로라인·시그널 크로스 추세추종

- **출처**: https://www.prorealcode.com/topic/time-segmented-volume-by-worden-brothers-code/ (ProRealCode, 공식에 가까운 구현 코드) / https://help.tc2000.com/m/69404/l/747088-time-segmented-volume (TC2000 공식 설명) / https://candlestickpatterns.pw/blog/2022/12/15/time-segmented-volume/ / https://www.tradingview.com/script/z68zqJ2d-Time-Segmented-Volume-TSV/
- **참여지표**: - (Worden Brothers가 만든 독점적 지표를 다수 플랫폼이 재구현·소개, 특정 바이럴 게시물 조회수 확인 안 됨)
- **백테스트 근거**: 없음(QuantifiedStrategies.com에 백테스트 페이지가 있으나 접속 시 봇 차단(CAPTCHA)으로 원문 수치 확인 실패 — **정량 수치 원문 미확인**, 절대 추정 수치 기재하지 않음). 지표 설명 기반으로 분류.
- **타임프레임**: 4h 신호 / 1d 추세 필터
- **시장/대상**: BTC·ETH·주요 알트 USDT-M 무기한

## 진입 규칙
- 지표: TSV = Σ[i=1..N]( volume_i × sign(close_i − close_i−1) × |close_i − close_i−1| ), N봉 롤링합(방향성 거래대금 누적). Signal = SMA(TSV, M).
- 스윙 권장 파라미터(자료 기준: "1H~Daily 스윙 = TSV Length 21~34, Signal 10~21"): N=21, M=10.
- 롱: TSV가 0선을 상향 돌파 + TSV > Signal(상승 국면) + 1d 종가 > 1d EMA(50)(상위 추세 확인) → LONG.
- 숏: TSV가 0선을 하향 돌파 + TSV < Signal + 1d 종가 < 1d EMA(50) → SHORT.

## 청산 규칙
- 익절: 없음(추세추종형) — TSV가 Signal선을 반대로 재크로스(모멘텀 꺾임)하면 청산. 그 전까지 chandelier 트레일(신고가/신저가 − ATR(14,4h)×2.5)로 보유.
- 손절: 진입가 − ATR(14,4h)×1.5(롱)/+ATR×1.5(숏).
- 시간/조건 청산: TSV가 0선을 재역행 돌파하면 무조건 청산(방향성 상실 확정).

## 파라미터
- tsv_length=21 (범위 13~34), signal_length=10 (범위 7~21)
- atr_period=14, sl_atr_mult=1.5, trail_atr_mult=2.5
- trend_filter_ema=50 (1d)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 종가 변화 방향 × 거래량의 N봉 롤링합, 그 SMA(Signal), ATR, EMA. 모두 바이낸스 REST 캔들+거래량으로 완전 충족.
- 주의: 오더북/틱/OI 불필요. OBV·CMF류와 계산 축은 비슷하지만 "가격 변화폭 × 거래량"을 직접 합산하는 점이 다른 거래량 지표(단순 방향 부호만 쓰는 OBV, True Range 기반 CMF)와 공식상 구분됨.
- 오탈자 방지 메모: TSV는 상표(Time Segmented Volume®, Worden Brothers)라 플랫폼마다 세부 구현(가중치·정규화)이 조금씩 다름 — 백테스트 시 위 공식(가장 널리 재구현된 버전)을 기준으로 삼음.

## 스카우트 메모
- 강점: 거래량과 가격변화율을 동시에 반영해 "거래량 없는 가짜 돌파"를 자연스럽게 걸러낼 개연성. 우리 기존 CVD·OBV·CMF 계열과는 다른 각도(변화폭 가중)라 앙상블 시 상관관계가 낮을 가능성.
- 의심점: 백테스트 근거 원문을 확인하지 못해(봇 차단) 순수 지표 설명에만 의존 — 실제 엣지는 미검증. 4h/1d에서 거래량 데이터가 15m 원본을 리샘플(합산)한 것이라 방향 부호(sign) 판정이 원본 15m 개별 변화가 아니라 4h/1d 종가 기준으로 근사되는 갭 있음(스펙과 실구현이 완전 동일하지 않을 수 있음, 백테스트 시 명시 필요).
- 우리 단타 슬리브와의 관계: **중장기(스윙) 신규 후보**, 기존 라이브와 직접 대체 관계 없음. 기존 obv-ma-breakout-divergence-scalp.md·chaikin-money-flow-breakout-swing.md와 "거래량 기반 추세확인"이라는 상위 카테고리는 겹치나 계산식이 명확히 다름.
