# crypto-trader

바이낸스 선물(USDT-M) 기반 멀티 시그널 자동매매 시스템.

코인글래스 파생 데이터(펀딩비·미결제약정·청산·롱숏비율)와 기술지표(RSI·MACD·ADX·캔들패턴)를
**가중 점수**로 합산해 BTC / ETH / SOL 페어를 자동 매매합니다.

> ⚠️ **주의**: 자동매매는 실제 손실 위험이 있습니다. 반드시 **테스트넷/페이퍼 트레이딩**으로
> 충분히 검증한 뒤 소액으로 실전에 적용하세요. 이 프로젝트는 투자 조언이 아닙니다.

---

## 현재 상태 (Phase 1)

- [x] 프로젝트 구조 / 설정 관리
- [x] 바이낸스 선물 커넥터 (ccxt, 테스트넷 지원)
- [x] 코인글래스 v4 클라이언트
- [x] 기술지표 시그널 (RSI, EMA, MACD, ADX, ATR, 캔들패턴)
- [x] 파생 데이터 시그널 (펀딩비, OI, 청산, 롱숏비율)
- [x] 시그널 가중 합산 엔진
- [x] 리스크 관리 (포지션 사이징, SL/TP, 레버리지 상한)
- [x] 페이퍼 트레이딩 실행 엔진 + 메인 루프
- [ ] 백테스팅 프레임워크 (Phase 2)
- [ ] 실전 주문 실행 + 포지션 리컨실 (Phase 3)
- [ ] 모니터링 / 알림 / 대시보드 (Phase 4)

자세한 설계는 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) 참고.

---

## 빠른 시작

```bash
# 1. 의존성 설치
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. 환경변수 설정
cp .env.example .env
# .env 파일을 열어 바이낸스 테스트넷 키 / 코인글래스 키 입력

# 3. 페이퍼 트레이딩 실행 (기본: 드라이런)
python -m scripts.run_paper
```

## ⚠️ 네트워크 요구사항 (지역 제한)

바이낸스 API(`api.binance.com`, `fapi.binance.com`)는 **일부 지역에서 HTTP 451
(Unavailable For Legal Reasons)로 차단**됩니다. 이 경우 실시간 데이터/주문이 불가하니
**바이낸스가 허용하는 지역의 서버/VPN**에서 실행하세요.

- 공개 캔들 데이터는 미러 `https://data-api.binance.vision` 로 우회 조회 가능(현물 기준).
- 파생 데이터(`fapi/futures/data`)는 미러가 없어 허용 지역에서만 동작합니다.
- 이 저장소를 만든 컨테이너 환경은 451로 차단되어 있어, 코어 로직은 미러의 실데이터로
  검증했습니다(테스트 18건 통과 + 실캔들 시그널 파이프라인 확인).

## 바이낸스 테스트넷 키 발급

1. https://testnet.binancefuture.com 접속
2. 우측 상단 API Key 발급 → `.env`의 `BINANCE_API_KEY`, `BINANCE_API_SECRET`에 입력
3. `BINANCE_TESTNET=true` 확인

## 코인글래스 키 발급

- https://www.coinglass.com/pricing (일부 데이터는 유료 플랜 필요)
- `.env`의 `COINGLASS_API_KEY`에 입력
- 키가 없어도 바이낸스 네이티브 파생 데이터로 폴백 동작합니다.
