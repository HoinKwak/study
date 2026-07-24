# [스윙] Bill Williams 마켓 퍼실리테이션 인덱스(BW MFI) Squat바 브레이크아웃

- **출처**: 지표 원안: Bill Williams(저서 *Trading Chaos*). 공식·존 컬러/규칙 정리:
  https://www.litefinance.org/blog/for-beginners/best-technical-indicators/what-is-market-facilitation-index/ ,
  https://forex-indicators.net/bill-williams/mfi , https://arongroups.co/forex-articles/market-facilitation-index/
  (WebFetch로 공식·Green/Fade/Fake/Squat 4구간 정의 확인).
- **참여지표**: - (Bill Williams 고전 지표, 정량 참여지표 미집계이나 업계 표준 인지도 높음)
- **백테스트 근거**: **없음(개념 기반)** — 원문들은 "지표 자체는 매수/매도 신호를 내지 않고 확인용 보조지표"라 명시. 정량 수치 없음, 채택 전 자체 백테스트 필수.
- **타임프레임**: 4h 신호 / 1d 확인
- **시장/대상**: BTC·ETH·시총상위 알트 무기한 (거래량 데이터가 유의미한 유동성 높은 종목 위주)

## 진입 규칙
- **MFI 계산**: `MFI_t = (high_t - low_t) / volume_t` (봉당 변동폭÷거래량 = 거래량 대비 가격변화 효율)
- **4구간 분류**(전봉 대비 MFI 방향 × Volume 방향):
  - **Green**(MFI↑, Volume↑): 신규 자금 유입, 추세 지속(진입엔 다소 늦음)
  - **Fade**(MFI↓, Volume↓): 모멘텀 소진, 추세 종료 임박
  - **Fake**(MFI↑, Volume↓): 거래량 뒷받침 없는 가짜 돌파 위험 → **진입 금지**
  - **Squat**(MFI↓, Volume↑): 매수·매도 세력이 대량거래로 힘겨루기 중이나 가격은 정체 → **에너지 응축, 브레이크아웃 전조**로 취급
- **롱**: Squat바 형성 후, **다음 봉이 Squat바의 고가를 종가 기준 상향 돌파** **AND** 그 돌파봉의 거래량이 Squat바 거래량 이상 **AND** 4h close가 EMA(50) 위(상위 추세 필터).
- **숏**: Squat바 형성 후, **다음 봉이 Squat바의 저가를 종가 기준 하향 돌파** **AND** 돌파봉 거래량이 Squat바 이상 **AND** 4h close가 EMA(50) 아래.
- Fake바 직후 돌파 시도는 신호 무시(거래량 뒷받침 없는 가짜 신호로 필터링).

## 청산 규칙
- 익절: `rr_target=2.5R`(스윙, 손익비 크게) 또는 Squat바 이후 형성된 스윙 고/저점(측정폭) 도달 시.
- 손절: Squat바의 저가(롱)/고가(숏) 바로 바깥, `stop_buffer=0.3×ATR(4h,14)`.
- 시간 청산: `max_hold_bars=15봉`(4h×15≈2.5일) 내 목표 미도달 시 청산 검토.

## 파라미터
- ema_trend_len=50 (4h)
- vol_confirm=Squat바 거래량 이상 (배수 조정 가능, 범위 1.0~1.3배)
- rr_target=2.5 (범위 2.0~3.5)
- stop_buffer_atr=0.3 (범위 0~0.5)
- max_hold_bars=15 (범위 10~20)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 고가·저가·거래량만으로 계산(`MFI=(H-L)/V`), EMA(50). 완전히 표준 klines OHLCV로 구현 가능.
- 주의: 공식이 매우 단순하나 **4구간 분류(Green/Fade/Fake/Squat)를 봉별로 정확히 라벨링하는 로직**이 필요 — 전봉 대비 방향 비교라 룩어헤드 주의(신호는 종가 확정 후에만 사용).

## 스카우트 메모
- 강점: Bill Williams 고전 지표이나 우리 보유 스펙에 **없는 신규 신호원**(가격변동폭÷거래량 비율 + 4구간 분류)이라 중복이 낮음. 계산이 단순해 데이터 요구·코딩 난이도 최저 수준. "Squat=에너지 응축→브레이크아웃"이라는 발상은 볼린저 스퀴즈·TTM 스퀴즈류(변동성 수축)와 유사한 카테고리이나 **거래량 기반 압축 감지**라는 점에서 결이 다름.
- 의심점: 원문 자체가 "신호를 내지 않는 확인용 지표"라 명시 — 여기서 제안한 "Squat 브레이크아웃" 진입 규칙은 스카우트가 구성한 것으로, **원문에 명시된 전략이 아님**(개념을 코딩 가능하게 재구성). 백테스트로 유효성 확인 필수.
- 우리 단타 슬리브와의 관계: 기존 볼린저 스퀴즈(bollinger-squeeze-breakout-daily), TTM 스퀴즈(ttm-squeeze-momentum-breakout-swing)와 "압축 후 브레이크아웃" 큰 틀은 유사하나 압축 판정 지표가 거래량 기반이라는 차별점. 대체보다는 보완(대체 확인 필터) 후보.
