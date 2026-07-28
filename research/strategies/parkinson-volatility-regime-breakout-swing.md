# [스윙] Parkinson 고저범위 변동성 레짐 브레이크아웃 (4h)

- **출처**: https://www.bestexresearch.com/insights/standard-vs-parkinson-volatility-for-execution-algorithms-understanding-the-trade-offs (BestEx Research, 표준 vs Parkinson 변동성 비교) /
  https://quantra.quantinsti.com/glossary/Estimating-volatility-using-Parkinson-Estimator (Quantinsti, 공식·이론적 효율성 설명) /
  https://abouttrading.substack.com/p/calculating-parkinsons-volatility (Engineering Alpha, Python 구현) /
  https://www.cryptodatadownload.com/blog/posts/comparison-parkinson-volatility-implied-volatility/ (CryptoDataDownload, 크립토 데이터로 Parkinson vol 계산 사례)
- **참여지표**: - (퀀트 교육·리서치 블로그 다수, SNS 참여지표 미확인)
- **백테스트 근거**: **없음(개념/이론 기반)**. 검색된 원문들은 "Parkinson 추정치가 표준 종가기반 변동성보다 이론상 약 5배 통계적으로 효율적(고저 전체 경로를 사용하므로)"이라는 **추정 이론**만 제시하고, 이를 이용한 구체적 매매전략의 승률·PF·수익률 수치는 어디에도 없음. **채택 사유는 성과가 아니라 기존 스택(ATR·Choppiness·Hurst·Larry Williams noise-ratio 등)과 다른 변동성 추정 수학(고저 범위의 로그 제곱 기반)이라는 메커니즘 신선도** — 정량 근거 부재를 정직히 표기.
- **타임프레임**: 4h 신호 / 1d 레짐 확인 (변동성 레짐 전환은 스윙 성격 — 저빈도).
- **시장/대상**: BTC·ETH·주요 알트 무기한

## 진입 규칙
- **Parkinson 변동성 추정치** (표준 공식):
  `PV[i] = sqrt( (1/(4*ln2)) * mean( ln(High[j]/Low[j])^2, j=i-N+1..i ) )` (연율화 생략, 순수 롤링 추정치로 사용)
  - N=14봉(4h) 롤링 윈도우.
- **레짐 판정**: 최근 100봉(4h) 기준 `PV`의 백분위(percentile rank) 계산. `PV_pctile < 20` = 저변동성(수축) 레짐, `PV_pctile > 20`로 재상승 = 확장 전환.
- **롱**: 저변동성 레짐(`PV_pctile < 20`)에서 **N_hold봉 이내(예 10봉) `PV_pctile`이 50 이상으로 급등** + 해당 구간 종가가 최근 20봉 고가 상향 돌파(방향 확인) → 롱.
- **숏**: 동일 조건 + 최근 20봉 저가 하향 돌파 → 숏.
- 방향 판정은 순수 변동성 지표(무방향성)이므로 반드시 가격 돌파(Donchian류)와 결합해야 함 — PV는 "언제 진입 가능한 국면인가"만 걸러주는 레짐 필터.

## 청산 규칙
- 익절: ATR(14,4h)×2.5 트레일링 또는 R:R 2.0 고정.
- 손절: 돌파 시작점(레인지 반대편) 또는 진입가 -1.5×ATR.
- 시간 청산: `PV_pctile`이 다시 20 미만으로 수축 전환하면 조기 청산(확장 국면 종료 판단).

## 파라미터
- pv_window=14봉 (범위 10~20)
- regime_lookback=100봉 (범위 60~150)
- low_vol_pctile_th=20 (범위 10~30)
- expand_pctile_th=50 (범위 40~60)
- donchian_n=20 (범위 15~30)
- atr_trail_mult=2.5 (범위 2.0~3.5)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: High/Low만으로 계산(종가 불필요), 롤링 백분위 계산, Donchian(20).
- 주의: 바이낸스 REST 캔들(OHLC)만으로 충분, 오더북·틱데이터 불필요. Parkinson 추정치는 **갭(자정 리셋 등)을 반영 못하는 한계**가 있으나 크립토는 24/7이라 갭이 거의 없어 오히려 적합.

## 스카우트 메모
- **강점**: 기존 변동성 계열(ATR 기반 Chaikin Volatility, Choppiness, Larry Williams 노이즈비율, NR7)과 달리 **고저 로그범위 제곱 평균**이라는 별개 수학 — 종가 갭에 둔감하고 고저 경로를 온전히 반영해 변동성 수축을 더 빨리 포착한다는 이론적 근거. 브레이크아웃 방향은 기존 Donchian류를 재사용하되 "언제 진입할지" 게이트만 교체.
- **의심점**: 정량 백테스트 근거가 전무 — 순수 이론+메커니즘 신선도로만 채택했으므로 자체 백테스트에서 기대만큼의 엣지가 없을 가능성 높음. `pv_pctile` 임계치는 전부 [추정](원문에 수치 없음).
- **관계**: 기존 `chaikin-volatility-contraction-expansion-breakout-swing`(EMA 기반 H-L 변화율)·`ttm-squeeze-momentum-breakout-swing`(볼린저/켈트너 스퀴즈)과 **목적은 동일(변동성 수축→확장 브레이크아웃)**하나 추정 수학이 다름 — 세 개를 교차검증해 어느 변동성 정의가 우리 데이터에서 가장 잘 맞는지 비교할 가치 있음(중복이 아닌 "같은 문제의 다른 풀이" 비교군).
