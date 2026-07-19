# [스윙] 와이코프 스프링/업스러스트 매집·분산 되돌림 (Low-Volume False Break)

- **출처**: https://www.wyckoffanalytics.com/identifying-wyckoff-springs-with-algorithmic-trading-strategies/ (Wyckoff Analytics, "Identifying Wyckoff Springs with Algorithmic Trading Strategies") /
  https://algobars.com/strategy-templates/wyckoff-complete/wyckoff-upthrust/ (AlgoBars 전략 템플릿, R:R 규칙) /
  https://fibalgo.com/library/wyckoff-spring-upthrust (TradingView 인디케이터, 스프링 유형 분류) /
  https://www.tradingview.com/script/vQSBf9rh-Wyckoff-Range-Strategy/ (Wyckoff Range Strategy, lookback 파라미터)
- **참여지표**: - (교육/전략 문서, TradingView 스크립트 개별 조회수 미확인). 다만 "Wyckoff Method"는 크립토 트레이딩 커뮤니티(유튜브·X)에서 가장 널리 회자되는 고전 프레임워크 중 하나로 인지도는 매우 높음.
- **백테스트 근거**: **없음(정성적)**. 여러 출처가 "알고리즘화해 백테스트 가능"이라고는 하나 정량 수치(승률·PF)를 제시한 원문은 찾지 못함 — 정직히 참여지표/개념 기반으로 분류. AlgoBars 템플릿은 "4H–Daily 3:1 R:R"이라는 권장 손익비만 명시.
- **타임프레임**: 4h~1d 레인지 판정, 진입 확인은 1h. 저빈도(레인지 형성 자체가 드묾).
- **시장/대상**: BTC·ETH·시총상위 알트 무기한 (레인지 국면이 뚜렷한 종목에서 유효)

## 진입 규칙
- **레인지 정의**: 최근 lookback_bars(기본 40봉, 4h 기준 ≈1주) 동안의 **최고가(R_high)·최저가(R_low)**로 박스 설정. 박스 폭이 ATR(14) 대비 좁아야 함(예: (R_high−R_low) < 4×ATR) — 진짜 횡보 매집/분산 구간만 대상, 추세 구간 제외.
- **스프링(롱, 매집 국면)**: 종가 기준으로 (a) 레인지 형성 후 저점 R_low를 **꼬리로 이탈**(저가 < R_low), (b) **이탈 당일 거래량이 직전 20봉 평균 거래량보다 낮음**(vol < vol_ma20 × 0.9 — Wyckoff 원전 핵심: 매도자 소진, 매도 관심 부재), (c) 종가가 R_low **위로 복귀**(레인지 안으로 재진입, 저가에 그대로 마감하지 않음 — 꼬리/윗그림자 필요) → 그 봉 종가 롱 진입.
- **업스러스트(숏, 분산 국면)**: 대칭 — 고가가 R_high 위로 꼬리 이탈, 이탈 거래량 < vol_ma20×0.9, 종가가 R_high 아래로 복귀 → 숏 진입.
- (선택 확인) SOS(Sign of Strength)/SOW(Sign of Weakness): 스프링 다음 1~3봉 내 레인지 중심선(박스 중앙값)을 강한 거래량(vol > vol_ma20×1.3)으로 돌파하면 확신도↑, 미확인이어도 진입 자체는 스프링 조건만으로 가능(보수적 운용은 SOS 확인 후 진입).

## 청산 규칙
- 익절: 1차 목표 **레인지 반대편(R_high, 롱의 경우)**. 확장 목표(SOS 확인 시): 레인지 폭(R_high−R_low) 만큼 반대편으로 추가 투사(measured move).
- 손절: 스프링 저점(꼬리 끝) 바로 아래 − 0.3×ATR 버퍼(업스러스트는 대칭 위).
- 시간/조건 청산: 스프링 후 SOS가 max_confirm_bars(예 6봉, 4h) 내 미발생하고 레인지 중심선도 못 넘으면 실패로 간주해 청산(false spring/재이탈 리스크).

## 파라미터
- range_lookback=40봉 (범위 20~60, 4h 기준)
- range_width_max=4×ATR14 (범위 3~6×ATR)
- spring_vol_ratio=0.9 (이탈봉 거래량/20봉평균, 범위 0.7~1.0 — 낮을수록 엄격)
- sos_vol_ratio=1.3 (확인봉 거래량/20봉평균, 범위 1.2~1.8)
- stop_buffer=0.3×ATR (범위 0.2~0.5)
- max_confirm_bars=6봉 (범위 4~10, SOS 대기)
- rr_target=1.0×레인지폭 (기본), 확장 시 2.0×

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 롤링 N봉 고/저(레인지 박스), 거래량 이동평균(20), ATR(14). 전부 캔들+거래량으로 계산.
- 주의: **바이낸스 REST 캔들+거래량으로 충족.** 오더북/틱/실시간청산 불필요. 다만 (a) "진짜 횡보 레인지" 자동판정(폭 필터)이 성능에 민감, (b) SOS/SOW 확인 로직은 규칙이 다소 주관적이라 [설계 판단] 요소가 많음 — 백테스트로 파라미터 민감도 점검 필수.

## 스카우트 메모
- 강점: 기존 보유 `liquidity-sweep-reversal.md`(Turtle Soup, 20봉 이상 오래된 스윙레벨 + **높은 RVOL**로 스탑헌팅 확인)와 **핵심 메커니즘이 정반대**다 — 이건 다봉 레인지 박스 + **낮은 거래량**(매도/매수 관심 소진)으로 반전을 확인한다. 두 전략을 같은 캔들에 동시 적용하면 "이탈봉 거래량이 높은지 낮은지"로 서로 배타적 필터 역할을 해 신호 정제 가능.
- 의심점: 정량 백테스트 완전 부재 — 레인지 폭·거래량 임계값 등 자체 설계 요소가 많아 과최적화 위험. SOS/SOW 판정이 규칙 기반이라도 다소 주관적(레인지 중심선 돌파 기준 등) → 원전(사람 판단)과의 괴리 가능.
- 우리 단타 슬리브와의 관계: 스윙 슬리브 보완 후보(현재 스윙은 손익비 미달로 제외된 상태 — CLAUDE.md 참고). 레인지 박스+저거래량 필터는 우리 스캘프의 `regime.py`(레인지 판정)와 결합해 "레인지 국면에서만 스프링 페이드" 게이트로 재사용 가능성 있음.
