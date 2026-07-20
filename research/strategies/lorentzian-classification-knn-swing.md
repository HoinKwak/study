# [스윙] 로렌치안 분류(k-NN 머신러닝) 다중지표 신호

- **출처**: https://www.tradingview.com/script/WhBzgfDu-Machine-Learning-Lorentzian-Classification/ (TradingView, 작성자 jdehorty, "Machine Learning: Lorentzian Classification") / 보조: https://tradesearcher.ai/strategies/2019-lorentzian-classification-strategy
- **참여지표**: TradingView **좋아요 35,000 / 부스트 814 / 댓글 814 / 조회수 1,184,720** (WebFetch 원문 확인). TradingView 전체 스크립트 중 최상위권 인기 지표로 알려져 있고("Top 50 최다인기·2023년 최고가치 PineScript 수상" — 2차 소스), 검증 강도는 매우 높음.
- **백테스트 근거**: 원문(지표 페이지)엔 지표 설명만 있고 자체 백테스트 수치는 없음. TradeSearcher(3rd-party 자동 백테스터) 페이지에서 심볼별 스냅샷 확인: **FLOW/USDT 일봉 25트레이드 ROI 15.70%(R:R 2.31), Mantle 1h 49트레이드 ROI 23.95%(R:R 1.45), PLTR 일봉 45트레이드 ROI 37.00%(R:R 2.02)** — WebFetch 원문 확인함. 단, 승률·PF·낙폭 등 종합 통계는 없고 **개별 심볼 스냅샷(체리피킹 가능성 있음)** 이라 신뢰도는 제한적.
- **타임프레임**: 1h~1d (지표 자체는 TF 무관하나 kNN 특성상 노이즈 적은 상위TF에서 안정적). 본 스펙은 4h 스윙으로 채택.
- **시장/대상**: 크립토 무기한 전반(원 지표는 자산 불문 범용, 크립토 페어에서도 다수 사용례 확인)

## 진입 규칙
- 특징 벡터(기본 5슬롯): RSI(14), WT(WaveTrend, n1=10/n2=11), CCI(20), ADX(20), RSI(9) — 각 특징을 정규화 후 과거 최대 2000봉(Max Bars Back) 중 **로렌치안 거리**(`ln(1+|Δfeature|)`의 합) 기준 최근접이웃 k=8개를 탐색, 다수결로 향후 방향(+1/-1) 예측.
- 롱: k-NN 예측값이 양(+)이고, **변동성 필터**(단기 ATR이 장기 대비 과도하게 낮지 않음) 통과 + **레짐 필터**(추세 강도 지표, 기본 임계값 -0.1 이상 = 트렌딩 상태) 통과 + (옵션) 커널회귀 스무딩 라인이 상승 기울기일 때 진입.
- 숏: 예측값이 음(-)이고 동일 필터 통과 시 진입.
- 옵션 트렌드필터: 종가가 EMA(200) 위/아래인 방향으로만 롱/숏 허용(커뮤니티 변형에서 흔히 병행 — TradeSearcher 사례는 200EMA+Supertrend 조합 사용).

## 청산 규칙
- 익절: 커뮤니티 변형 기준 **1:1 R에서 절반 익절(본전 스탑 이동)**, 3:1 R에서 추가 익절, 잔여분은 Supertrend 또는 반대 k-NN 신호 시 청산.
- 손절: ATR 기반(진입가 대비 −1.5~2×ATR).
- 시간/조건 청산: k-NN 예측이 반대 부호로 전환되거나 커널회귀선이 방향 전환 시 즉시 청산.

## 파라미터
- neighbors_count(k)=8 (범위 1~100, 기본값 권장)
- max_bars_back=2000 (범위 500~5000)
- feature_set=[RSI14, WT(10,11), CCI20, ADX20, RSI9] (고정 5슬롯, 변경 가능)
- volatility_filter=on, regime_filter=on(threshold=-0.1, 범위 -10~10), adx_filter=off(threshold=20)
- kernel_lookback=8 (범위 3~50), kernel_relative_weight=8 (범위 0.25~25)
- ema_trend_filter=200 (옵션)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: RSI, WaveTrend, CCI, ADX(전부 OHLCV로 계산 가능) + **k-NN 최근접이웃 탐색을 직접 구현**해야 함(사이킷런 KNN이나 자체 벡터거리 계산, 매 봉마다 최대 2000봉 재탐색 — 계산량 있음, 벡터화 필요). 커널회귀(Nadaraya-Watson) 스무딩까지 재현하려면 추가 구현.
- 주의: 원 지표는 Pine Script 비공개 아님(오픈소스)이지만 로직이 복잡해 **재현 시 오류 여지 큼**(정규화 방식·거리식 디테일이 성능 좌우). 데이터는 전부 바이낸스 REST 캔들로 충분, 오더북 불필요. **코딩 난이도 상**.

## 스카우트 메모
- 강점: TradingView 사상 최고 인기 지표 중 하나(조회 118만·좋아요 3.5만)로 커뮤니티 검증 강도가 압도적. 우리 지표군(RSI/볼린저/OI 등 단일지표 조합)과 달리 **다중특징 k-NN 분류기**라는 완전히 다른 신호 생성 방식이라 상관관계 낮은 대체 신호가 될 수 있음.
- 의심점: 종합 승률/PF/MDD 통계를 원문에서 확인 못함(TradeSearcher 스냅샷 3건은 체리피킹 가능성). 구현 복잡도가 높아 **버그 발생 시 우리 프레임워크 재현 결과가 원 주장과 다를 위험** 큼(과거 ATR-RSI FAIL 사례처럼). 백테스트 우선순위는 낮게(먼저 단순 버전으로 검증) 잡는 게 안전.
- 우리 단타 슬리브와의 관계: 완전히 새로운 신호체계(ML 분류) — 기존 룰베이스 전략과 앙상블/필터로 조합 가능성. 다만 구현비용 대비 검증 전까지는 "연구용" 성격이 강함.
