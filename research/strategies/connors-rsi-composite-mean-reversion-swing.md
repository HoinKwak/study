# [스윙] Connors RSI(CRSI) 3요소 복합 평균회귀

- **출처**: https://www.backtrader.com/recipes/indicators/crsi/crsi/ (Backtrader, CRSI 공식 정의 원문 확인) / https://www.asktraders.com/learn-to-trade/trading-strategies/connors-rsi/ (임계값·정성적 백테스트 원문 확인) / https://www.quantifiedstrategies.com/connors-rsi/ (제목상 "75% Win Rate" 주장 — **봇 차단(WebFetch 반복 실패)으로 본문 수치 원문 확인 불가**, 인용 보류) / https://www.tradingview.com/support/solutions/43000502017-connors-rsi-crsi/ (TradingView 공식 지표 설명)
- **참여지표**: - (퀀트 교육 사이트 다수가 반복 게재하는 고전 지표. Larry Connors가 2004년 저서 *Short Term Trading Strategies That Work*에서 발표, 이후 TradingView 기본 내장 지표로 채택될 만큼 채택도 높음. SNS 좋아요 등 정량 참여지표는 미집계)
- **백테스트 근거**: **원문 확인분만 인용, 정직 표기**.
  - asktraders.com(WebFetch 원문 확인): "CRSI 0~5 구간 진입 종목은 이후 5거래일 평균 +2.15% 상승, CRSI 95+ 구간은 이후 5거래일 평균 -0.94% 하락" — **미국 주식시장 대상, 표본기간·표본수·승률·PF 미공개**.
  - quantifiedstrategies.com 제목의 "75% Win Rate" 주장은 **본문 접근 차단으로 원문 미확인** → 신뢰도 낮음, 참고만 하고 채택하지 않음.
  - **크립토 백테스트 데이터 없음** — 우리 프레임워크(바이낸스 선물 klines)로 최초 검증 필요.
- **타임프레임**: 4h~1d 신호(원 지표는 일봉 설계, 크립토 스윙 적용 시 4h 권장) / 1d 상위 추세 확인
- **시장/대상**: BTC·ETH·시총상위 알트 무기한 (원 백테스트는 미국 주식)

## 진입 규칙
- **CRSI 정의**: `CRSI(3,2,100) = [RSI(종가,3) + RSI(연속상승/하락일수Streak,2) + PercentRank(1일 변동률,100)] / 3`
  - RSI(3): 표준 RSI, 3기간.
  - Streak RSI(2): "연속 상승/하락/보합 일수"(상승=+1씩 누적, 하락=-1씩 누적, 방향전환 시 0으로 리셋)를 시계열로 만들어 그 값에 RSI(2) 적용.
  - PercentRank(100): 오늘 1봉 수익률이 최근 100봉 수익률 분포에서 차지하는 백분위(0~100).
  - 세 값의 단순평균이 최종 CRSI(0~100).
- 롱: CRSI < 5(극단 과매도, 보수적으로 10) **그리고** 4h 종가 > SMA200(4h) 상승추세 필터. → 해당 봉 종가 진입.
- 숏: CRSI > 95(극단 과매수, 보수적으로 90) **그리고** 4h 종가 < SMA200(4h) 하락추세 필터. → 해당 봉 종가 진입.
- (옵션, 원전 언급) 추세필터 없이 역추세 전용으로 쓰려면 SMA200 조건 제거하되, 신호 빈도·손실 확대 위험 증가.

## 청산 규칙
- 익절: CRSI가 50~70 구간 재진입(평균 회귀 완료 판정) 시 종가 청산. 공격적으로는 CRSI > 70(롱 청산)/< 30(숏 청산).
- 손절: 진입가 −(1.5~2.5)×ATR(14, 4h).
- 시간 청산: 최대 홀딩 N봉(예: 4h TF 12~20봉, ≈2~3일) 초과 시 강제 청산.

## 파라미터
- rsi_len=3, streak_rsi_len=2, pctrank_len=100 (CRSI 3요소, 원전 표준값 고정 권장)
- crsi_long_th=5 (범위 3~10), crsi_short_th=95 (범위 90~97)
- crsi_exit_long=60 (범위 50~70), crsi_exit_short=40 (범위 30~50)
- trend_filter_sma=200 (SMA/EMA 선택 가능)
- sl_atr_mult=2.0 (범위 1.5~2.5), max_hold_bars=16 (4h 기준, 범위 12~24)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: RSI(2가지 다른 입력에 적용) + PercentRank(롤링 백분위, 직접 구현 필요 — 표준 TA 라이브러리에 없을 수 있음) + SMA200. Streak 계산(연속 상승/하락 카운터)은 간단한 상태 누적 로직.
- 난이도: **중간**. CRSI 자체 구현은 pandas rolling+rank로 어렵지 않으나 3개 서브지표를 정확히 구현·검증하는 과정에서 버그 위험(특히 Streak RSI, PercentRank 방향) — 단위테스트 권장.
- 데이터: 바이낸스 선물 klines(OHLC)만으로 충분. 오더북·틱데이터 불필요.

## 스카우트 메모
- **강점**: RSI(2) 단일 지표보다 신호가 더 "극단적"일 때만 발화(3요소 동시 극단이어야 임계값 통과)하므로 이론상 다이-2(RSI-2) 대비 거래빈도가 더 낮고 신호 질이 높을 가능성. 기존 `rsi2-mean-reversion.md`(RSI(2) 단일지표+SMA200)와 **명확히 다른 지표**(3요소 복합)라 중복 아님.
- **의심점**: 크립토 실증 백테스트가 전혀 없어(주식시장 자료만) 크립토 24/7·고변동성 환경에서 그대로 작동할지 불확실. PercentRank 계산 방식(상승률 vs 절대수익률 등 변형이 소스마다 다름)을 원전 표준(Connors 2004)으로 통일해 재검증 필요. quantifiedstrategies의 "75% 승률" 주장은 원문 미확인이라 배제.
- **우리 슬리브와의 관계**: 기존 볼린저 눌림목 중기(제거됨, 복원 가능) 및 RSI-2 스펙과 같은 "평균회귀 눌림목" 계열이나, 지표 자체가 달라 **보완재**로 검토 가능. 스윙 슬리브(4h) 재도입 논의 시 후보.
