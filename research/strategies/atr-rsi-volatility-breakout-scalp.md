# [단타] ATR-RSI 변동성 브레이크아웃 스캘핑 (ATR_RSI_Strategy v2 no-repaint)

- **출처**: https://www.tradingview.com/script/mqh6UJ9p-ATR-RSI-Strategy-v2-with-no-repaint-liwei666/ (TradingView, 작성자 liwei666) / 보강(로직 설명): https://medium.com/@redsword_23261/atr-rsi-enhanced-trend-following-trading-system-65b2a6b7ac67
- **참여지표**: 좋아요 17,996 / 조회수 73,344 (본 리서치 라운드 중 참여지표 최고치)
- **백테스트 근거**: **BTCUSDTPERP 15분봉, 116 트레이드, Sharpe 1.4, 수수료 0.05% 반영.** 순이익률·승률·PF·MaxDD는 스크립트 설명 페이지에 원문 기재 없음(요약 수준) — 표본기간도 불명. Sharpe만으로는 리스크 프로파일 파악 제한적 → 반드시 우리 프레임에서 승률/PF/MDD까지 재측정 필요.
- **타임프레임**: 15m
- **시장/대상**: BTC 무기한(원 스크립트 BTCUSDTPERP) / ETH 등 유동성 큰 페어로 확장 가능

## 진입 규칙
- 공통 필터(변동성 국면): ATR(atr_length=14)이 그 이동평균 atr_ma(atr_ma_length≈30)보다 클 때만 진입 허용("고변동성 국면"). ATR/atr_ma 정규화 비율이 [atr_ma_norm_min, atr_ma_norm_max] 범위 안일 때만(과도 극단 변동성 배제).
- 롱: 변동성 필터 통과 + RSI(rsi_length=14)가 **50+rsi_entry**(예 65) 를 상향 돌파
- 숏: 변동성 필터 통과 + RSI가 **50−rsi_entry**(예 35) 를 하향 돌파

## 청산 규칙
- 익절: 퍼센트 기반 TP(진입가 대비 +X%, 스캘핑이므로 1.5~3% 권장)
- 손절: **trailing_percent** 퍼센트 트레일링 스탑(유리한 방향으로만 갱신)
- 시간/조건 청산: 별도 없음(TP/트레일로 관리)

## 파라미터
- atr_length=14 (범위 10~20)
- atr_ma_length=30 [추정] (범위 20~50)
- atr_ma_norm_min=0.8 [추정], atr_ma_norm_max=1.5 [추정] (고정된 원문값 미공개, 그리드서치 필요)
- rsi_length=14 (범위 7~21)
- rsi_entry=15 [추정] (매수>65/매도<35, 범위 10~25)
- trailing_percent=1.5% [추정] (범위 1~3%)
- tp_percent=2.5% [추정] (범위 1.5~4%)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: ATR(14), ATR의 이동평균, RSI(14) — 전부 바이낸스 OHLCV REST 캔들로 계산 가능.
- 난이도: 낮음. 트레일링 스탑만 봉/틱마다 재계산 필요(우리 워커에 유사 SL/TP 관리 로직 이미 존재, `scalp.py` 참고). 오더북 심도·틱데이터 불필요.
- 주의: 파인스크립트 소스가 비공개(작성자 "TO GET ACCESS SEND ME A MESSAGE")라 **정확 기본값(4개 튜닝 파라미터) 미확인** — 재현 시 자체 그리드서치 전제.

## 스카우트 메모
- 강점: 이번 라운드 중 **참여지표(좋아요·조회수)가 압도적으로 높은** 스크립트. "고변동성 국면에서만 진입"이라는 명시적 레짐 게이트가 있어 레인지장 노이즈를 자동 회피하는 구조 — 우리 기존 스캘프의 스퀴즈 게이트(`scalp.py`의 squeeze_pctile)와 철학은 유사하나 트리거 지표(ATR변동성+RSI 돌파 vs 볼밴 이탈+거래량스파이크)가 완전히 다름.
- 의심점: Sharpe만 공개되고 승률/PF/MDD가 없어 손실 분포·연속손실 리스크 불명. 정확 파라미터 비공개로 재현성 낮음(그리드서치 필요, 과최적화 주의).
- 우리 단타 슬리브와의 관계: **보완**. 기존 볼린저+거래량+OI 스캘프와 신호원이 달라 상관 낮을 가능성 → 별도 슬리브로 A/B 테스트 후보로 적합.
