# [스윙] SSL Hybrid + QQE MOD 이중 추세확인 (4h/1h)

- **출처**: SSL Hybrid — https://www.tradingview.com/script/C3MlAWCw-SSL-Hybrid/ (Mihkel00, 2019-12-19 게시) /
  QQE MOD — https://www.tradingview.com/script/TpUW4muw-QQE-MOD/ (Mihkel00, 2020-01-20 게시, Glaz의 QQE 원 개념 확장) /
  QQE MOD 산식 상세: https://github.com/edyatl/qqe-mod (Python 이식판, RSI/스무딩/ATR 계수 확인) /
  조합 전략 규칙(2차자료, 원저작 아님): kevinmck100의 공개 스크립트 설명 — https://www.tradingview.com/script/YCob5r03-QQE-MOD-SSL-Hybrid-Waddah-Attar-Explosion/ 등 (검색엔진 스니펫으로만 확인, 정량 백테스트 없음)
- **참여지표**: SSL Hybrid TradingView 좋아요/부스트 **16.2K**, 조회수 **약 54.1만**, 댓글 497 (WebFetch 확인). QQE MOD 좋아요/부스트 **13.1K**(WebFetch 확인, 조회수는 페이지 파싱 불안정으로 미기재). 두 지표 모두 TradingView 상위권 인디케이터로, 조합 사용이 크립토 트레이더 커뮤니티에서 매우 흔함(다수 파생 스크립트 존재).
- **백테스트 근거**: 없음(원 지표·조합 스크립트 페이지 모두 정량 성과 미공개, 참여지표 기반 채택). "1H 타임프레임에서 특히 잘 작동" 등 서술은 있으나 수치화된 승률·PF는 원문에 없음 → **정량 수치 원문 미확인으로 표기**.
- **타임프레임**: 4h 신호 / 1h 확인(원 커뮤니티 권장은 1h 단독이나, 우리 인프라는 수수료 절감을 위해 4h 주신호로 상향 적용 — 자체 변형)
- **시장/대상**: BTC·ETH 및 유동성 상위 무기한

## 진입 규칙
- **SSL 베이스라인**(SSL Channel 표준 산식으로 근사, SSL Hybrid의 3중 레이어 중 1레이어): `SMA_high = SMA(high, ssl_len)`, `SMA_low = SMA(low, ssl_len)`.
  - `Hlv[t] = +1 if close > SMA_high[t] else (−1 if close < SMA_low[t] else Hlv[t−1])`
  - `SSL_Up = Hlv<0 ? SMA_low : SMA_high`, `SSL_Down = Hlv<0 ? SMA_high : SMA_low` → `SSL_Up > SSL_Down`이면 상승(Blue), 반대면 하락(Red).
- **QQE MOD**(github 이식판 확인 파라미터): QQE1 = RSI(rsi_len=6)를 EMA(rsi_smooth=5)로 스무딩 후 ATR류 변동폭(`QQE factor=3`)로 상·하 트레일링밴드 생성, 이를 다시 볼린저밴드(`bb_len=50, bb_mult=0.35`)로 감싸 제로라인 필터 삼음. QQE2는 동일 RSI/스무딩에 `factor=1.61`인 보조 트리거 라인. 두 QQE가 정렬되면 히스토그램이 **블루(상승)/골드(하락)**로 표시.
- 롱: `SSL_Up > SSL_Down`(SSL Blue) **AND** QQE MOD 히스토그램 블루 전환 **AND** `close`가 SSL 베이스라인 상단에 위치.
- 숏: `SSL_Up < SSL_Down`(SSL Red) **AND** QQE MOD 히스토그램 골드/레드 전환 **AND** `close`가 SSL 베이스라인 하단에 위치.
- (옵션, 조합 스크립트 3번째 필터) Waddah Attar Explosion 히스토그램이 데드존 위 & 방향 일치 — 코딩 복잡도 상승 대비 효용 불확실하여 기본 스펙에서는 제외, 추후 필터 강화용으로만 고려.

## 청산 규칙
- **추세반전 청산**: SSL 베이스라인 방향 반전(Blue↔Red) 또는 QQE MOD 히스토그램 색 반전 중 먼저 발생하는 신호에 청산.
- **손절**: `진입가 ∓ 1.5×ATR(14)` 또는 최근 5봉 스윙 고/저(원 조합 스크립트가 "직전 X봉 스윙 고/저를 SL로 사용"한다고 서술 — 정확한 X값은 원문 미확인, ATR 대체 추정).
- **익절**: 고정 TP 없음(반대신호까지 홀드). 조합 스크립트는 "SSL Hybrid EXIT 화살표에서 TP" 서술 있으나 3번째 SSL 레이어(exit layer) 산식 미확인 → 본 스펙에선 반대신호 청산으로 단순화.
- **시간 청산**: 없음.

## 파라미터
- ssl_len=10 (범위 5~20, SSL 베이스라인 SMA 기간)
- qqe_rsi_len=6 (고정, 원문 확인값), qqe_rsi_smooth=5 (고정)
- qqe_fast_factor=3, qqe_slow_factor=1.61 (고정, 원문 확인값)
- qqe_bb_len=50, qqe_bb_mult=0.35 (고정, 원문 확인값)
- sl_atr_mult=1.5 (범위 1.0~2.5)
- signal_tf=4h (범위 1h~4h)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: SMA(high/low), RSI, EMA(RSI 스무딩), ATR류 밴드, 볼린저밴드(RSI 기반). 전부 캔들 OHLCV로 산출 가능하나 **QQE MOD는 이중 스무딩+볼린저밴드 결합이라 구현 복잡도 중상**(다른 후보 대비 코딩량 많음).
- 주의: 오더북/틱 불필요. 다만 SSL Hybrid 원 지표의 2·3번째 레이어(continuation/exit SSL)와 Keltner "in zone" 로직은 본 스펙에서 단순화(베이스라인만 사용) — 원 지표 풀스펙 재현은 아님.

## 스카우트 메모
- 강점: 두 지표 모두 TradingView 최상위권 참여지표(SSL 1.6만·QQE 1.3만 좋아요)로 크립토 커뮤니티 신뢰도 높음. RSI+ATR+SMA 조합이라 추세 강도와 방향을 이중 확인해 단일지표보다 다이버전스/휩쏘 필터링 효과 기대.
- 의심점: 정량 백테스트가 전무해 **순수 참여지표 채택**. QQE MOD 산식이 복잡해(6/5/3/1.61/50/0.35 다중 파라미터) 과최적화된 "느낌"이 강함 — 원 저자가 왜 이 특정 숫자들을 택했는지 근거 불명, 우리 프레임에서 파라미터 민감도 점검 필수. SSL Hybrid도 본 스펙은 베이스라인만 근사 구현이라 원 지표(3레이어+Keltner)와 성과가 다를 수 있음.
- 우리 슬리브와의 관계: 보완(신규 계통, RSI+SMA채널 결합은 기존 볼린저/스토캐스틱RSI 계열과 다른 산식). 코딩 난이도가 상대적으로 높아 **백테스트 우선순위는 UT Bot/Range Filter 이후로 권장**.
