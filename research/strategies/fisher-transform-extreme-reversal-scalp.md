# [단타] 피셔 트랜스폼 극단값 반전 스캘프

- **출처**: https://phemex.com/academy/what-is-fisher-transform (Phemex Academy, 크립토 거래소 자체 교육자료) /
  https://gocharting.com/docs/charting/technical-indicator/momentum/eshlers-fisher-transform-indicaotor (John
  Ehlers 원전 공식 설명) / https://www.luxalgo.com/blog/fisher-transform-clarity-for-turning-points/
- **참여지표**: -(지표 문서 기반. 크립토 거래소(Phemex) 자체 아카데미에 정식 게재돼 크립토 트레이더 노출도
  높음 — 정량 조회수 미확인)
- **백테스트 근거**: **없음(지표 문서 기반)**. John Ehlers 원전("Cybernetic Analysis for Stocks and Futures")은
  가우시안 정규화로 가격 극단을 예민하게 잡는다는 신호처리 이론적 근거는 확실하나, 공개된 크립토 정량
  백테스트(승률·PF)는 검색에서 확인되지 않음 — 채택 전 백테스트 필수.
- **타임프레임**: 5m~15m 신호 / 1h 레인지 필터(ADX로 추세 여부 판별)
- **시장/대상**: BTC·ETH·유동성 상위 알트 무기물(레인지·약추세 구간에 적합 — 강추세 구간은 필터로 배제)

## 진입 규칙
- **Fisher 계산**: N=10봉 최고/최저로 가격을 −1~1로 정규화(value = 2×((close−min(N))/(max(N)−min(N))−0.5)),
  0.999 클리핑 후 Fisher = 0.5×ln((1+value)/(1−value)), 직전 값과 평활(가중치 0.5). Trigger = Fisher를 1봉
  지연시킨 값.
- **레인지 필터**: 1h ADX(14) < 25 (강추세 구간 배제 — 극단값 반전 전략은 레인지·약추세에서만 유효).
- 롱: Fisher가 최근 5봉 내 −1.5 이하(극단 과매도)를 기록한 이후, Fisher가 Trigger를 상향 교차하는 봉의 종가에
  진입.
- 숏: Fisher가 최근 5봉 내 +1.5 이상(극단 과매수)을 기록한 이후, Fisher가 Trigger를 하향 교차하는 봉의 종가에
  진입.
- 옵션 확인 필터: RSI(14, 5m)도 동시에 극단(<25 롱 / >75 숏) 구간이었을 것(다중 지표 합의로 신호 질 향상).

## 청산 규칙
- 익절: 볼린저 밴드(20,2) 중심선(SMA20) 도달 시 50% 익절, 잔량은 Fisher가 0선을 재교차하거나 2.0R 도달 시 청산.
- 손절: 진입 신호 발생 시점 극단 저점/고점 − 1.0×ATR(14, 5m).
- 시간 청산: 8봉(5m 기준 40분) 내 1R 미도달 시 청산.

## 파라미터
- fisher_period=10 (범위 8~14)
- extreme_threshold=1.5 (범위 1.2~2.0)
- extreme_lookback=5봉 (범위 3~8)
- adx_max=25 (범위 20~30, 레인지 필터 강도)
- sl_atr_mult=1.0 (범위 0.8~1.5)
- max_hold=8봉(5m)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: Fisher Transform(직접 구현 필요 — 표준 라이브러리에 드묾, 공식 자체는 단순), Trigger(1봉 지연),
  ADX(14), RSI(14, 옵션), ATR(14), 볼린저(20,2).
- 주의: **REST 캔들만으로 완전 구현 가능**, 난이도 낮음(공식이 간단한 산술). min/max(N) 롤링 계산 시 0 분모
  방지(고가=저가 횡보 구간) 처리 필요.

## 스카우트 메모
- 강점: 가우시안 정규화 덕분에 일반 RSI/스토캐스틱보다 극단값에서 신호가 더 뾰족하게(sharp) 반응한다는 것이
  신호처리 이론적 장점 — ADX 레인지 필터를 걸어 강추세 칼받기를 구조적으로 차단한 설계.
- 의심점: 백테스트 근거 전무(규칙 3 최소요건만 충족) — 최우선 검증 대상 아님, 후순위 실험용으로 취급 권장.
  N=10 최고/최저 정규화는 파라미터에 민감할 수 있어 과최적화 주의.
- 우리 단타 슬리브와의 관계: 기존 스캘프(추세추종 돌파)와 **정반대**(레인지 평균회귀) — ADX 필터로 국면을
  분리하면 상호 배타적으로 병행 가능(추세 구간은 기존 스캘프, 레인지 구간은 이 전략). 기존 williams-r-extreme,
  mfi-extreme-mean-reversion과 컨셉이 유사한 "극단 오실레이터 반전" 계열이라 3종 중 최우수만 채택하는 것을
  권장.
