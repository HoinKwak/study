# CLAUDE.md — 행동 규약 & 프로젝트 가이드

이 파일은 세션·대화 압축(compaction)과 무관하게 **항상** 지켜야 하는 규약이다.
대화가 압축되어 맥락이 리셋되어도 이 파일의 규칙은 그대로 적용된다.

---

## 📌 공지 (세션 시작 시 항상 먼저 확인·안내)

> 이 블록은 세션 시작(또는 압축 후 이어받기) 때 **가장 먼저 읽고**, 내용이 있으면
> 사장님께 답변 상단에 짧게 안내한다. 처리되면 해당 줄을 지운다. 비어 있으면 안내 생략.

_(현재 공지 없음)_

## 🧭 진행상황 스냅샷 (Live — 압축돼도 잃지 않게 주기적으로 갱신)

> 큰 작업 시작 전·컨텍스트 70% 초과 시·상태가 바뀔 때 이 블록을 최신화해 커밋한다.
> 이어받을 때 여기부터 읽으면 "지금 무엇을 어디까지 했는지" 한눈에 파악된다.
> (마지막 갱신: 2026-08-07, 00시 전략라운드 반영)

- **현재 모드**: 상시 세션에서 **정기 리서치 루틴 4종**을 발화받아 서브에이전트로 수행 → 검증 → 커밋·push 반복.
  - kol-watch(온체인 트렌딩 조기경보) 2h · futures-scout(선물 리서치) 2h · market-brief(시장 브리핑) 12h · strategy-scout→backtester→**backtest-reviewer**(전략 발굴+백테스트) 12h.
  - 매 사이클 공통 절차: `git pull` → `date -u`로 UTC 확보 → 서브에이전트에 그 UTC 명시(에이전트는 Bash 없어 날짜 환각 방지) → 산출물 스키마/ts/렌더 검증 → 파일경로별 `git add` → 한글 커밋(푸터 `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`) → push.
  - 검증 포인트: watch.json `ts/tokens/notable` 스키마·ts 일치·대시보드 렌더 스모크테스트; futures brief 주식화토큰 제외 스캔; ETF flows 과거이력 prefix보존·신규거래일만 append; chartist_views 인물 6인 고정.
- **미션 #28(진행중)**: **15m/1h VALID 전략 발굴**. 지금까지 발굴·백테스트한 다수 전략 **전부 FAIL**(backtest-reviewer로 재검증해 거짓 FAIL 아님 확인). 최근(8/7 00시 라운드): **처음으로 FAIL이 아닌 HOLD 2건**. 토큰 언락 공급쇼크 페이드 숏(표면 OOS net PF **2.035**·전체 2.955로 통과선 상회하나 표본 16건[IS 3건]·유일 반복표본 SpaceID n=9가 PF0.796 손실·플라시보 대조군 PF1.11로 알트 구조적 하락편향과 미분리·Keyrock 원문['팀 언락 평균 -25%'·'90% 부정적'] 미재현[팀 평균 +1.94%·음수비율 56.2%]. **리뷰어 신규발견이 HOLD를 보강**: 반복표본 SpaceID의 'Seed Round'가 클리프가 아니라 5년 분기별 1% 균등 선형 베스팅임을 vest_raw 직접확인으로 규명 — `min_unlock_pct_supply≥1%` 필터가 배치크기만 보고 불연속성 미검사하는 설계공백. 제외시 '진짜 클리프' 7건[전부 n=1]으로 더 얇아짐. OOS t=1.15 비유의)·현물BTC ETF 유출스트릭 컨트래리언(2.57년간 **거래 7건**뿐, 전체 net PF1.526이나 절반분할시 0.705 반전·파라미터 한칸에 0.24~1.61 요동·top1~2 제거시 1.53→0.87→0.31 붕괴·t=0.46. 구조적 발견: 7건 전량이 '순유입 전환 첫날 청산'으로 끝나 TP/SL/최대보유15일 미발동[평균보유 2.0일] — 스펙의 '1~3주 보유 +8~12%' 전제가 스펙 자체 청산규칙과 충돌. `bool Series.shift(1).fillna(False)`의 object-dtype 버그로 58건→7건 자체수정, **리뷰어가 버그 재구성해 58건 재현 후 7건이 옳음 확인**. 리뷰어가 `flows.json`의 **git 커밋이력을 분석해 각 flow 값의 파일 최초등장 시점을 실측**[대부분 D+1, 간헐 D+2~4]해 D+1 공표지연 가정이 낙관적이지 않음을 독립검증) 2종 **HOLD·VALID**(둘 다 라이브 미반영). 신규 스펙 5종 추가(전부 스윙 — 토큰언락·ETF유출스트릭·Deribit 옵션만기핀닝·BTC 200주MA·CME COT, 총 260). 발굴 기준 진화: '엣지 크기보다 **엣지 대비 거래빈도**가 생존을 가름'(OI컨퍼메이션 gross1.395 t=7.06 유의였으나 연~200건 빈도로 net 0.688 잠식 vs 위클리피벗은 수수료 부담 작았으나 신호 무엣지)을 근거로 저빈도·고엣지·논리적 근거 뚜렷한 이벤트드리븐 계열만 탐색. 스카우트가 COT 스펙에서 WebSearch 요약의 '승률 60~70%'를 원문 WebFetch로 재확인했다 존재하지 않아 폐기·'정량근거 없음' 표기(인용 환각 자체 차단). ⚠️규약 위반 1건 발견·정정: OI 리포트 말미에 모델 식별자 포함 Co-Authored-By 줄이 들어가 있어 제거, 전 산출물 재스캔 잔존 0건. 8/6 12시 라운드: OI-가격 컨퍼메이션 vs 다이버전스 **정면비교**(기존에 스펙만 있고 미구현이던 다이버전스를 이번에 처음 구현해 동일엔진 비교 — 컨퍼메이션 OOS gross PF1.395/net 0.688로 작은 gross 엣지가 수수료에 잠식[gross t=7.06 유의], 다이버전스 n=226으로 gross t=-1.11 비유의라 '표본부족으로 판단불가'가 정확하나 net t=-2.91로 FAIL 유지. 방향반전 대조군 net 1.073은 **리뷰어가 코드추적으로 절대레벨 재사용 없음 확인**해 과거 2건의 허위PF 버그 재발 아님이나 t=1.40 비유의로 채택 안 함. 리뷰어 신규발견: OI가 봉 시가 시각에 정렬[보수적 어긋남, 룩어헤드 아님]·7종목 동일날짜 0-fill 결측[2024-07-09~15 6일연속은 OOS 시작 직후]이 isna() 체크를 우회했으나 오염거래 제외해도 PF 변화 미미)·위클리 클래식 피벗포인트(브레이크아웃 OOS net PF1.18로 미달+IS는 0.93 손실로 방향 뒤집힘+top10 제거시 1.04 붕괴, 되돌림은 gross 0.90으로 수수료 이전부터 무엣지·청산 64.6%가 손절. **선정근거였던 '위클리라 수수료 부담 작음'은 실측 확인**[gross-net 차 0.05~0.12p]되어 실패 원인이 신호 자체임이 분명. 리뷰어가 resample 비의존 수동슬라이스로 BTC 233개 완전주 전수대조해 룩어헤드 0건 확증, 범위 밖 파라미터까지 확장스윕해 필터 제거시 OOS 1.34여도 IS 0.94로 '살아날 여지 없음' 확인) 2종 **FAIL·VALID**. 신규 스펙 5종 추가(OI컨퍼메이션·크로스섹셔널 초단기리버설·위클리피벗·Pi Cycle·스테이블코인 디페그, 총 255). 발굴 방향 전환: 최근 FAIL 2종이 모두 gross부터 무엣지였던 점을 근거로 '지표 정규화·조합' 계열을 의도적으로 배제하고 구조적으로 다른 엣지 원천(자산 간 관계·미사용 사분면·매크로 사이클·캘린더 레벨)을 탐색. 스카우트가 'CME 갭 채우기'를 발굴했다가 원문검증에서 2026-05-29부로 CME 24/7 전환돼 갭 미생성임을 확인하고 자체 폐기. 8/6 00시 라운드: MACD-V 모멘텀 생명주기 스캘프(IS PF0.76·OOS PF0.65, 7종목 전부 PF<1 — 리뷰어가 무비용진단을 7종목·IS까지 확장 재계산해 **풀링 gross PF OOS 0.981/IS 1.024로 애초에 gross 엣지 없음** 확정. 구현 중 단위사고(`asi8` ms vs `asm8` ns → 거래 0건)·부분익절 수수료 이중차감 버그 2건을 백테스터가 자체 발견·수정, 리뷰어가 재구성 검증)·더블 볼린저(20/1σ+50/1σ)+RSI50(연 ~2,900회 극단 고빈도, **OOS gross PF 0.88·net 0.60으로 수수료 이전부터 무엣지**, 방향반전은 더 나쁜 0.35, σ 넓혀 빈도 낮춰도 개선 없음. 리뷰어가 슬리피지까지 0으로 강제한 순수 무비용에서도 OOS PF1.028 t=1.11로 무의미 확인, 계좌 소진은 회계버그 아닌 음의기댓값 복리사이징의 정상 붕괴로 트레이스 검증) 2종 **FAIL·VALID**. 신규 스펙 5종 추가(츠바이크 브레드스 스러스트·RRG 사분면 로테이션·MACD-V·GARCH(1,1) 변동성예측·더블볼린저+RSI50, 총 250). ⚠️리뷰어 신규 지적(파이프라인 전체 해당, 미조치): 라이브는 증거금 기준(`build_plan_by_margin`, `.env POSITION_MARGIN_PCT=10.0`) 사이징인데 `research/impl` 약 20개 백테스트는 전부 리스크 기준(`build_plan_with_stop`)만 사용 — 이 전략만의 문제 아니고 PF 결론은 불변이나 구조적 괴리로 기록. 8/5 12시 라운드: Gator Oscillator 4국면 스퀴즈-확장(IS PF0.84 순손실·OOS PF1.18 미달, confirm_bars=2만 근접통과했으나 종목간 불일치+top20제거 붕괴로 기각 — 리뷰어가 SATED부분익절 dead code 신규발견해 기각근거 강화)·WRB되돌림 눌림목 스캘프(7종목 OOS 전부 PF<0.44, 방향반전 구현버그 발견·수정 후에도 역방향 PF0.36 무엣지) 2종 **FAIL·VALID**. 신규 스펙 5종 추가(Gator Oscillator·펀딩브레드스·WRB되돌림·월말계절성·USDTM-COINM베이시스, 총 245). 8/5 00시 라운드: 볼륨프로파일세션POC+테이프스피드(3종목 전체 PF 0.49~0.66, gross부터<1)·15분봉 턴오브더캔들효과(원문효과 미재현 p=0.70/0.20, net PF 0.003~0.054로 계좌 소진) 2종 FAIL·VALID. 8/4 12시: 합성청산클러스터·상위트레이더 포지션비율 2종 FAIL·VALID. 8/4 새벽: BTC 디커플링·펀딩플립+OI가속·AlphaTrend 3종 FAIL·VALID. 8/3 오후: 딥스매수·코랄트렌드+ADX·앵커드VWAP 3종 FAIL·VALID. 8/3 오전: QuantPedia MACD·TSMOM 월간 FAIL·VALID. 8/2: z-score 계열 4종 최종 FAIL 확정, CUSUM·아시아세션·RSI DCA 래더 FAIL·VALID. **scalp15m이 여전히 유일 라이브 전략**. 미검증 대기: 극값 스트릭·볼린저 반대밴드·HMM 국면·울프웨이브·ATR그리드·VA마이그레이션·주말모멘텀·아미후드비유동성·펀딩브레드스·월말계절성·USDTM-COINM베이시스·츠바이크 브레드스 스러스트(표본 희소)·RRG 사분면 로테이션(원저자 공식 비공개)·GARCH(1,1)(구현 복잡·룩어헤드 위험)·크로스섹셔널 초단기리버설(포트폴리오 엔진 필요, 착수 시 수수료0 진단 선행 권고)·Deribit 옵션만기 핀닝(원문도 '핀닝 최근 자주 실종' 회의적)·BTC 200주MA(터치 4회로 검정 불가)·CME COT(정량근거 없음·데이터소스 신규구축 필요)·Pi Cycle·스테이블코인 디페그(둘 다 표본 수년에 1~2회라 통계검증 원천적 곤란, 모니터링 용도)·VPIN·ICT 브레이커·52주 신고가/돈치안 앙상블/캐리 합성/왜도(포트폴리오 엔진 필요)·코인베이스 프리미엄·SSR(외부 데이터 필요)·`long-short-account-ratio-contrarian-swing`(정식 재검증 후보, 2022년 5%결측 구간 포함 IS 재설정 권고) 등. 참고: pandas 3.0.3은 `to_datetime(unit="ms")`가 `datetime64[ms]` 유지(ns 자동승격 아님) — `Timestamp.value`(항상 ns)와 섞으면 단위사고 재발 가능, 경계.
- **기타(8/1)**: 주간 API 한도 도달로 7/31 18:03Z~8/1 14:00Z 약 22h 루틴 중단 → 리셋 후 루틴별 1회 캐치업으로 복구(중복 재생 안 함). 사장님이 LIT(Lighter) 수동 트레이딩 중 — 차트 해석·미시구조 Q&A 진행(정보 제공만, 매매 판단 개입 없음). LIT 심층 리서치 노트 `research/notes/lit-research-2026-07-30.md` 커밋됨(토큰 정체·RH 파트너십 사실검증·HYPE 비교 밸류·12월 클리프 리스크). market-brief 검증 중 ETH ETF 과거이력 임의수정 발견→백업본 복원 사례 있음(append-only 검증 계속 철저히).
- **미조치 대기**: #45 Lighter 리더보드 커넥터, #46 폴리마켓 롱샷편향 실측 — 요청 없으면 착수 안 함.
- **다음 할 일**: 도착하는 정기 루틴 프롬프트를 계속 위 절차대로 처리. 새 지시가 없으면 라이브 전략·리스크 파라미터는 임의로 바꾸지 않는다.

### 🔁 봇 재시작 코드 (항상 여기 비치)
재시작은 **해당 창에서 Ctrl+C로 멈추고 → 재실행**. 어느 프로세스를 재시작할지는 §1 「재구동 안내 규약」의 변경위치 판정표 참조.

**공통 — `git pull` (한 번, 아무 창):**
```powershell
cd C:\Users\ghdls\Documents\study-claude-personal-ai-assistant-11xcgh\study-claude-personal-ai-assistant-11xcgh
git pull origin claude/personal-ai-assistant-11xcgh
```
**① 매매봇** (매매봇 창 Ctrl+C 후):
```powershell
cd C:\Users\ghdls\Documents\study-claude-personal-ai-assistant-11xcgh\study-claude-personal-ai-assistant-11xcgh
.\.venv\Scripts\Activate.ps1
python -m scripts.run_portfolio
```
**② 알람봇(스캐너)** (알람봇 창 Ctrl+C 후):
```powershell
cd C:\Users\ghdls\Documents\study-claude-personal-ai-assistant-11xcgh\study-claude-personal-ai-assistant-11xcgh
.\.venv\Scripts\Activate.ps1
python -m scripts.run_scanner
```
**③ 대시보드** (대시보드 창 Ctrl+C 후):
```powershell
cd C:\Users\ghdls\Documents\study-claude-personal-ai-assistant-11xcgh\study-claude-personal-ai-assistant-11xcgh
.\.venv\Scripts\Activate.ps1
python -m scripts.serve_dashboard
```

---

## 0. 커뮤니케이션 규약 (최우선 · 압축되어도 유지)

1. **항상 존댓말을 쓴다.** 사용자에게 보고·설명·질문할 때 반말·구어체 금지.
   대화가 압축되어 말투가 리셋된 것처럼 느껴져도, 이 규칙을 먼저 확인하고 존댓말로 답한다.
2. **중간 진행 상황은 항상 한글로 보고한다.** 작업을 시작할 때·단계가 바뀔 때·끝났을 때
   무엇을 하고 있는지 한글로 짧게 알린다. (코드·커밋 메시지·식별자는 예외)
3. **진행 중인 업무는 압축의 영향을 받지 않게 관리한다.**
   - 큰 작업은 시작 전에 계획을 남기고, 단계마다 커밋해 중간 상태를 디스크에 보존한다.
   - 미완료 작업이 있으면 그 상태(무엇을 어디까지 했고 다음이 무엇인지)를 한글로 명확히 남긴다.
   - 압축 후 이어받을 때는 이 파일 → 최근 커밋 → 코드 상태 순으로 확인하고, 사용자에게
     되묻지 말고 마지막 작업을 이어서 진행한다.
   - **컨텍스트 관리(압축 대비)**: 컨텍스트 사용이 대략 **70%를 넘겼다고 판단되면**, ① 먼저 아래
     「🧭 진행상황 스냅샷」을 현재 상태로 갱신·커밋해 디스크에 보존한 뒤 ② 사용자에게 `/compact`
     실행을 짧게 안내한다(안전한 지점 — 서브에이전트 대기 없고 미커밋 변경 없을 때). 실제 자동
     compact 트리거는 하네스(자동 압축)가 담당하므로, 내가 할 일은 **압축 전에 스냅샷을 최신화**해
     압축돼도 상태가 유실되지 않게 하는 것이다. 큰 사이클(발굴·백테스트 등)을 새로 시작하기 전에도
     스냅샷을 한 번 갱신한다.
4. **`git pull` 안내 시 재구동 코드를 항상 함께 준다.** 코드 변경을 push하고 `git pull`을
   안내할 땐, 어떤 프로세스(①매매봇/②알람봇/③대시보드)를 재시작해야 하는지 유형별로 명시하고
   붙여넣기용 명령 블록을 같이 준다. 상세 규약은 §1의 「재구동 안내 규약」 참조.

---

## 1. 프로젝트 개요

**crypto-trader** — 개인용 자동 암호화폐 트레이딩 봇.
- 사용자 Windows PC에서 로컬 구동, **바이낸스 선물 USDT-M 테스트넷** 대상.
- 자체 완결형 HTML 라이브 대시보드(인라인 SVG 차트·인라인 JS, Pretendard CDN 외 외부 라이브러리 없음).
- **단타 전용 포트폴리오(100%)** — **15m 단독 슬리브(100%)**. 10m은 전 구간 약해 제거(78d874c, 2026-07-13),
  중기·스윙은 손익비 미달로 제외(정의는 git 이력에 있어 복원 가능). 헤지·isolated 모드.
- 시장 스캐너(급등락·거래량/OI 급증·펀딩 극단 감지) → 텔레그램 알림 + 대시보드 갱신.

### 현재 전략·리스크 설정 (2026-07 기준, 바뀌면 여기 갱신)
- **단타 슬리브**: `scalp15m`(15m 진입/1h 확인) **단독**. 볼린저 이탈 강봉+거래량 급증 돌파.
  진입필터 `vol_spike≥5·squeeze≤35%·body≥1.3ATR·regime=False`. 메이커 진입(post-only), 10분할×20초.
  청산: **ATR 트레일링×1.0**(`scalp_exit_mode=trailing`, 신고가−ATR×1.0) + 횡보전환 시 모멘텀 꺾이면 청산.
  SL=신호봉 시가(stop_mult=1.0). (구 split tp1/tp2 청산은 트레일링으로 교체됨 — scalp-exit-mode-ab 백테스트.)
- **레버리지**: 시총상위(major_bases) **30x**, 알트 **10x** (`Settings.leverage_for`).
- **동적 유니버스**: 24h 거래대금 **$10M 이상**(SOL 제외). 사이징은 증거금 기준(`position_margin_pct`).
- **15m은 바이낸스 네이티브** TF라 리샘플 불필요(제거된 옛 10m 슬리브는 5m에서 리샘플했었음, `TF_RULE`).
- 백테스트 검증(교차검증): 3·5분 적자, **15분이 가장 유효(흑자)**, 10분은 국면 의존. 발굴 전략
  ATR-RSI는 우리 프레임워크에서 FAIL(외부 Sharpe 주장 재현 안 됨).

### 백테스트 데이터 소스 (fapi 지역차단 대응 — 중요)
- 이 클라우드 컨테이너에선 **바이낸스 선물 fapi가 451(지역차단)** — klines·ticker 모두 불가.
- **선물 캔들**: `https://data.binance.vision/data/futures/um/{monthly|daily}/klines/<SYM>/<TF>/...zip`
  덤프를 받는다. **선물 전용 알트(XPIN·TAC·EVAA·LAB 등)까지 포함**되므로 실제 유니버스 백테스트 가능.
  (현물 미러 `data-api.binance.vision`는 선물전용 알트가 없어 부적합 — 유니버스는 '선물' 기준이다.)
- **선물 유니버스·24h 거래량**: CoinGecko 파생 API(`/derivatives/exchanges/binance_futures?include_tickers=all`,
  `converted_volume.usd`)로 순위. 10M 이상 ≈ 116종목.
- 라이브 봇은 스캐너/`connectors/universe.py`로 유니버스 선정(fapi→CoinGecko→현물미러 폴백).

### 정기 리서치 루틴 & 최근 반영된 개선
- **정기 루틴 4종**(온체인 트렌딩 조기경보(舊 KOL 하이프워치, kol-watch) 2h·선물 리서치(futures-scout) 2h·시장브리핑 12h·전략발굴 12h)은 **이 상시 세션에 바인딩**
  (`persistent_session_id`)돼 발화 → 이 세션에서 서브에이전트 실행 후 커밋·push. 폰 완료알림은 없음
  (fresh-session 방식은 새 세션에 레포 쓰기권한이 없어 push 403 → 상시세션 바인딩으로 해결).
  결과물: `research/kol/`, `research/market/`, `research/strategies/`, `research/backtests/`.
- **시장브리핑 루틴이 갱신하는 파일 4종**: `research/market/brief.{md,json}` + `research/kol/chartist_views.json`
  (대시보드 '상위 차티스트 현재 뷰' — 인물 고정, 뷰만 갱신) + `research/etf/flows.json`(대시보드
  'ETF Flow' — 과거 이력 보존, 최신일만 append). 이 둘은 원래 자동갱신 루틴이 없어 멈춰 있던 것을
  시장브리핑 루틴에 편입함. 커밋 시 `research/market/ research/kol/chartist_views.json research/etf/` 함께 add.
- **⚠️ 날짜 환각 주의**: kol-watch·market-brief 서브에이전트는 Bash가 없어 현재 날짜를 스스로 못 구해
  ts/날짜를 자주 하루 이상 앞서 환각한다(예: watch.json ts·watch.md 헤더가 미래 날짜로 오기). 이들
  에이전트를 실행할 땐 **반드시 `date -u` 로 현재 UTC 시각을 먼저 확인해 프롬프트에 명시**하고, 완료
  후 커밋 전 저장된 ts/헤더 날짜가 현재와 맞는지 확인한다. 슬롯 판정용으로 어차피 매번 `date -u` 를
  찍으므로 그 값을 그대로 넘기면 된다.
- **최근 수정**(git 이력): 청산 짜바리 방지(분할청산 스텝사이즈 정합), 수동/외부 청산 정확 반영
  (`fetch_realized_close`로 실제 체결가·실현손익), 대시보드 '최근청산' 청산시각 정렬, 일별/누적손익이
  실잔고 이력 부족 시 저널 기준으로 폴백, 고아 슬리브 리컨실(제거·개명된 옛 슬리브로 열린 포지션은
  워커가 안 훑어 영영 '열림'으로 남던 것 → 엔진 `_reconcile_orphan_exits`가 거래소 실체결로 청산 반영).

### 로컬 실행 환경 (사용자 Windows PC)
- 프로젝트 경로(고정): `C:\Users\ghdls\Documents\study-claude-personal-ai-assistant-11xcgh\study-claude-personal-ai-assistant-11xcgh`
- 실행 명령 안내 시 이 경로를 그대로 쓴다(플레이스홀더 `C:\경로\study` 대신).
- PowerShell은 `&&` 미지원 → 줄을 나누거나 `;` 사용. 가상환경: `.\.venv\Scripts\Activate.ps1`.
- 3개 프로세스는 각각 별도 창: ① 매매봇 `python -m scripts.run_portfolio`
  ② 알람봇(스캐너) `python -m scripts.run_scanner` ③ 대시보드 `python -m scripts.serve_dashboard`.

### 재구동 안내 규약 (git pull 안내 시 항상 함께 준다)
코드 변경 후 `git pull`을 안내할 땐 **반드시 어떤 프로세스를 재시작해야 하는지 유형별로 명시**하고
아래 붙여넣기용 블록을 함께 준다. 재시작은 **해당 창에서 Ctrl+C로 멈추고 → 재실행**.
- 어느 프로세스를 재시작할지는 변경 위치로 판단:
  - `portfolio/`·`strategy/`·`risk/`·`connectors/`·`execution/`·`config/` → **① 매매봇**
  - `scanner/`·`monitoring/`(스캐너 경로)·detectors → **② 알람봇**
  - `monitoring/dashboard.py`·`serve_dashboard`·대시보드 API → **③ 대시보드**
  - 대시보드는 저널만 읽으므로, 매매 로직만 바뀌면 매매봇만 재시작하면 새로고침에 반영된다.

**공통(한 번, 아무 창):**
```powershell
cd C:\Users\ghdls\Documents\study-claude-personal-ai-assistant-11xcgh\study-claude-personal-ai-assistant-11xcgh
git pull origin claude/personal-ai-assistant-11xcgh
```
**① 매매봇** / **② 알람봇** / **③ 대시보드** (각 창에서 Ctrl+C 후):
```powershell
cd C:\Users\ghdls\Documents\study-claude-personal-ai-assistant-11xcgh\study-claude-personal-ai-assistant-11xcgh
.\.venv\Scripts\Activate.ps1
python -m scripts.run_portfolio      # ① 매매봇 (또는 run_scanner=② / serve_dashboard=③)
```

### 주요 실행 스크립트
- `python -m scripts.run_scanner` — 시장 스캐너 상시 구동 + `state/dashboard.html` 갱신.
- `python -m scripts.serve_dashboard` — 로컬 대시보드 웹서버(`http://localhost:8787`).
  파생 지표(`/api/derivs`)·캔들(`/api/klines`)·심볼(`/api/symbols`) API는 이 서버 모드에서만 실시간 동작.
- `python -m scripts.recompute_pnl` — 청산 손익 수수료 소급 보정(idempotent).
- `python -m scripts.yt_transcript <url|id> [--meta] [--out f]` — 유튜브 자막(트랜스크립트) 추출.
  **유튜브 영상 분석·전략 발굴은 반드시 이 도구로 트랜스크립트를 먼저 확보한다**(서드파티
  트랜스크립트 사이트는 CAPTCHA로 자주 막힘). yt-dlp 기반, `HTTPS_PROXY` 자동 사용.

---

## 2. 보안 · 상시 제약 (반드시 준수)

- **`.env` 는 절대 커밋하지 않는다** (`.gitignore` 에 포함됨). 테스트넷 키·텔레그램 토큰은
  사용자 본인의 저위험 자격증명이지만 저장소에 올리지 않는다.
- **모델 식별자(`claude-opus-4-8` 등)를 커밋 메시지·PR·코드·주석 등 저장소 산출물에
  절대 넣지 않는다.** 채팅 답변에만 사용.
- 모든 커밋은 지정된 `Co-Authored-By` / `Claude-Session` 푸터로 끝낸다.
- **명시적 요청 없이는 PR을 만들지 않는다.**
- 테스트넷에는 **한 번에 하나의 봇만** 구동한다.
- **Crescent Hook HR 프로젝트는 건드리지 않는다.**

---

## 3. Git

- 개발·푸시 브랜치: **`claude/personal-ai-assistant-11xcgh`** (여기 외 다른 브랜치에 푸시 금지).
- 푸시: `git push -u origin claude/personal-ai-assistant-11xcgh`, 네트워크 실패 시 지수 백오프(2/4/8/16s)로 최대 4회 재시도.
- 커밋 메시지는 한글로 명확하게. 변경이 완결되면 커밋·푸시.

---

## 4. 코드 스타일

- Python 3.11, `from __future__ import annotations`.
- 주석·로그·사용자 노출 문자열은 한글. 넓은 예외 포착에는 `# noqa: BLE001`.
- 대시보드는 외부 의존성 없는 자체 완결형 HTML을 유지한다(인라인 SVG/JS).
- 기존 코드의 관용구·네이밍·주석 밀도를 따른다.

---

## 5. 작업 원칙 (Karpathy 4원칙 — LLM 코딩 함정 방지)

출처: `multica-ai/andrej-karpathy-skills`. Andrej Karpathy가 지적한 LLM 코딩의 흔한 실수
(멋대로 가정·과잉설계·불필요한 수정)를 막기 위한 규약. **속도보다 신중함이 우선.**
사소한 작업엔 판단껏 완화하되, 비트는 판단이 필요할수록 이 원칙을 지킨다.

1. **코딩 전에 생각한다 (Think Before Coding)** — "가정하지 말고, 혼란을 숨기지 말고, 트레이드오프를 드러내라."
   - 요구가 모호하면 **멋대로 정하지 말고** 해석 후보를 제시하고 되묻는다.
   - 리스크·전략 파라미터(레버리지·유니버스·손절 등)는 **사용자 결정 사항**이다. 내가 임의로
     '안전장치'를 바꾸지 않는다. 우려가 있으면 데이터로 **짧게 정보 제공**만 하고 실행은 요청대로.
2. **단순함이 먼저 (Simplicity First)** — "문제를 푸는 최소 코드, 투기적인 것 없이."
   - 요청 안 한 기능·추상화·안 일어날 엣지케이스 방어를 덧붙이지 않는다.
3. **수술적 변경 (Surgical Changes)** — "꼭 필요한 것만 건드리고, 네가 만든 흔적만 치워라."
   - 무관한 코드 리팩터·스타일 변경 금지. 기존 관용구·네이밍 보존. 내가 만든 미사용물만 정리.
4. **목표 기반 실행 (Goal-Driven Execution)** — "성공 기준을 정의하고, 검증될 때까지 반복하라."
   - 작업을 **검증 가능한 성공 기준**으로 바꾸고, 테스트·백테스트·재현으로 확인한 뒤 '완료'라 말한다.
   - 실패·미검증은 정직하게 보고. 예: 백테스트는 단위·정합 버그가 흔하니(ns/ms, 유니버스 소스,
     TWAP 근사) **결과가 이상하면 먼저 계측·의심하고** 수치로 확인한 뒤 결론낸다.
   - **백테스트 결과는 반드시 `backtest-reviewer` 서브에이전트로 한 번 더 검증한다.** 어떤 백테스트든
     (전략 발굴 루틴·수동 스윕·라이브 반영 검토 등) 결과가 나오면, 그 결과를 신뢰·반영·보고하기 전에
     `backtest-reviewer`(정합·단위·룩어헤드·OOS·표본·유니버스편중·수수료·데이터소스·외부주장 재현
     감사)를 돌리고 그 리뷰(VALID/SUSPECT/INVALID)를 세션에 공유한다. INVALID/SUSPECT면 라이브에
     반영하지 않고 재검증한다.

성공의 지표: 불필요한 diff·재작성이 줄고, 구현 전에 확인 질문이 나오고, '완료'가 검증을 동반한다.
