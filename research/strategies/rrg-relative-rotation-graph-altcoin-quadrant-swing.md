# [스윙] RRG(상대순환그래프) JdK RS-Ratio/RS-Momentum 사분면 알트코인 로테이션

- **출처**: https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-types/relative-rotation-graphs-rrg-charts (StockCharts ChartSchool, Julius de Kempenaer 원저) / https://stockcharts.com/articles/rrg/2019/11/how-to-plot-crypto-currencies-786.html (크립토 적용 사례) / 공식 근사치: https://github.com/BennyThadikaran/RRG-Lite/wiki/RS-ratio-and-Momentum-calculations , https://github.com/An0n1mity/RRGPy — WebFetch/WebSearch로 사분면 정의·근사 공식 확인.
- **참여지표**: - (StockCharts.com은 유료 구독 서비스 핵심 기능으로 20년 이상 운영되는 방법론, 개별 SNS 참여지표 미집계). RRG는 기관/차티스트 커뮤니티에서 섹터로테이션 표준 시각화 도구로 광범위 채택.
- **백테스트 근거**: **없음(정량 수치 원문 미확인)**. StockCharts 원문은 "RRG는 시각화 도구이지 정의된 규칙을 가진 매매 시스템이 아니다"라고 명시 — 이번 스펙은 그 시각화를 **코딩 가능한 정량 규칙**으로 재구성한 것(사분면 전환 = 진입/청산 트리거). 정확한 JdK 정규화 상수(원저자 공식)는 비공개이므로, 아래는 오픈소스 재구현체들이 공통으로 쓰는 **근사 공식**임을 명시.
- **타임프레임**: 1d 종가 기준 RS-Ratio/RS-Momentum 산출 → 스윙(수일~수주) 로테이션
- **시장/대상**: 바이낸스 동적 유니버스 상위 알트코인(개별 종목) vs 벤치마크(BTC 또는 전체 알트 시가총액 근사 바스켓)

## 진입 규칙
- **RS(상대강도) 정의**: `RS(t) = (심볼 종가(t) / 벤치마크 종가(t)) × 100`. 벤치마크는 BTCUSDT(또는 유니버스 평균).
- **JdK RS-Ratio(정규화 상대강도)**: `SMA_RS = RS.rolling(14).mean()`, `Std_RS = RS.rolling(14).std()`, `RS_Ratio(t) = 100 + (RS(t) − SMA_RS(t)) / Std_RS(t)`.
- **JdK RS-Momentum(정규화 상대강도 변화율)**: `ROC(t) = (RS_Ratio(t) − RS_Ratio(t−10)) / RS_Ratio(t−10)`, 이를 다시 14기간으로 평활·정규화: `RS_Momentum(t) = 100 + 10 × (ROC(t) − mean(ROC,14)) / std(ROC,14)`.
- **4분면 판정**: `RS_Ratio>100 & RS_Momentum>100` = **Leading**(주도주) / `RS_Ratio>100 & RS_Momentum<100` = **Weakening**(약화) / `RS_Ratio<100 & RS_Momentum<100` = **Lagging**(부진) / `RS_Ratio<100 & RS_Momentum>100` = **Improving**(개선).
- 롱: 개별 알트가 **Lagging → Improving 사분면으로 진입**한 순간(RS_Momentum이 100을 상향 돌파, RS_Ratio는 아직 100 미만) → 초기 롱 진입(선행 진입, 리스크 큼). **보수적 대안**: Improving → Leading 전환(RS_Ratio도 100 상향 돌파) 시 진입(확인 후 진입, 신호 지연되나 안정적).
- 숏: 대칭으로 Leading → Weakening(RS_Momentum이 100 하향 돌파) 시 롱 청산·숏 검토, Weakening → Lagging 전환 시 숏 진입.
- 유니버스 랭킹: 매일 전체 유니버스를 4분면별로 분류해 **Improving 사분면 중 RS_Momentum 상위 3~5종목**을 포지션 후보로 선정(포트폴리오형 로테이션).

## 청산 규칙
- 익절: 정액 목표 없음 — 해당 종목이 Leading 사분면에서 시계방향 회전을 지속하는 한 보유.
- 손절: 개별 포지션 ATR(14)×2.5 또는 최근 스윙로우 하회.
- 시간/조건 청산: 종목이 Weakening 사분면으로 전환(RS_Momentum이 100 하향 돌파)하면 청산(사분면 자체가 청산 신호). 최대 보유 기간 제한 없음(사분면 로테이션 자체가 청산 트리거이므로).

## 파라미터
- rs_norm_window=14 (RS-Ratio 정규화 롤링 기간, 범위 10~20)
- roc_lookback=10 (RS-Ratio 변화율 계산 기간, 범위 5~15)
- momentum_norm_window=14 (RS-Momentum 정규화 롤링 기간, 범위 10~20)
- quadrant_center=100 (고정, JdK 정의)
- top_n_improving=3~5 (Improving 사분면 내 진입 후보 수)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 유니버스 각 심볼의 일봉 종가 + BTC(벤치마크) 종가만 있으면 계산 가능 — 바이낸스 REST klines로 완전 충족.
- 난이도: **중간**. 지표 계산 자체(rolling mean/std, ROC)는 pandas로 간단하나, **정확한 원저자(JdK) 정규화 상수가 비공개**라 재구현체마다 미세하게 다름 — 우리 구현이 "진짜 RRG"와 100% 일치하진 않을 수 있음(근사치임을 인지하고 사용).
- 주의: 벤치마크(BTC) 자체가 하락장이면 전 종목이 "상대적으로는 개선"으로 보여도 절대가는 하락할 수 있음 — 반드시 BTC 자체의 절대 추세 필터(예: BTC>200SMA)와 결합 권장.

## 스카우트 메모
- **강점**: 기존 로테이션 계열(`cross-sectional-altcoin-momentum-rotation-swing`, `market-neutral-cross-sectional-altcoin-btc-longshort-swing`, `week52-high-proximity-altcoin-rotation-swing` 등)은 대부분 **단일 스코어(모멘텀·52주고점 근접도 등) 랭킹**인 반면, RRG는 **레벨(RS-Ratio)과 속도(RS-Momentum)를 별도 축으로 분리**해 "이미 오른 종목(Leading, 뒤늦게 진입 시 상투 위험)"과 "이제 막 반전 중인 종목(Improving, 선행 진입 기회)"을 구조적으로 구분한다는 점에서 메커니즘이 실질적으로 다름.
- **의심점**: 원저자 공식이 비공개라 재구현 신뢰도가 낮고, 원문 자체가 "매매 시스템이 아니라 시각화 도구"라 명시 — 사분면 전환을 매매신호로 강제 변환한 것은 이번 스카우트의 확장이며 **완전 미검증**. 정규화 윈도우(14/10/14)를 임의로 잡았으므로 파라미터 민감도가 클 수 있음.
- **우리 슬리브와의 관계**: 로테이션 계열의 신규 변형(대체가 아니라 **보완**) — 기존 로테이션 전략들과 병렬 백테스트해 어느 랭킹 방식(단일 모멘텀 vs RS-Ratio/Momentum 사분면)이 손익비가 나은지 비교할 가치 있음.
