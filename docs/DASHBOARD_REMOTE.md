# 대시보드 외부 접속 (Cloudflare 터널)

로컬 대시보드(`http://localhost:8787`)를 외부(폰·다른 PC)에서 안전하게 보기 위한 설정.
방식: **Cloudflare 터널** — 포트포워딩 없이 공개 HTTPS 주소를 발급하고, 대시보드 자체는
**토큰 인증**으로 보호한다(잔고·포지션이 URL만 아는 사람에게 노출되지 않도록).

> 보안: 터널 URL만으로는 접근 불가하게 `DASHBOARD_TOKEN` 을 반드시 설정한다. 이 토큰은
> `.env` 에만 두고 **절대 커밋하지 않는다**(`.env` 는 `.gitignore` 에 포함).

---

## 1) 토큰 설정 (한 번)

`.env` 파일에 임의의 긴 문자열을 추가한다(예시 값 그대로 쓰지 말고 바꿀 것):

```
DASHBOARD_TOKEN=붙여넣을_임의의_긴_토큰_예_9f3a1c7b2e5d8h
```

- 토큰을 **설정하면** 대시보드는 `?key=<토큰>` 또는 인증 쿠키가 있어야 열린다.
- 토큰을 **비워두면** 기존처럼 인증 없이 로컬 전용으로 동작한다(외부 노출 금지).
- 대시보드를 재시작해야 반영된다(③ 대시보드 창 Ctrl+C 후 재실행).

## 2) cloudflared 설치 (한 번)

PowerShell(관리자):
```powershell
winget install --id Cloudflare.cloudflared
```
(winget 이 없으면 https://github.com/cloudflare/cloudflared/releases 에서
`cloudflared-windows-amd64.exe` 를 받아 PATH 에 둔다.)

## 3) 터널 실행 (접속할 때마다)

대시보드가 켜져 있는 상태에서, **새 PowerShell 창**에서:
```powershell
cloudflared tunnel --url http://127.0.0.1:8787
```
출력에 `https://<무작위>.trycloudflare.com` 주소가 뜬다. 이 창을 열어두는 동안만 터널이 유지된다.

> ⚠️ 반드시 `127.0.0.1` 로 지정한다. `localhost` 로 하면 cloudflared 가 IPv6(`[::1]`)로
> 접속을 시도하는데 서버는 IPv4(`127.0.0.1`)로만 열려 있어, 일부 API·차트 요청이
> `connection refused` 로 간헐 실패한다(로그에 붉은 ERR). `127.0.0.1` 은 IPv4 로 고정돼 이 문제가 없다.

## 4) 외부에서 접속

폰·외부 브라우저에서 **최초 1회** 토큰을 붙여 접속:
```
https://<무작위>.trycloudflare.com/?key=<토큰>
```
통과하면 인증 쿠키가 심겨, 이후엔 `?key=` 없이 접속해도 자동으로 열린다(같은 브라우저 한정).

---

## 주의 / 한계

- **quick 터널 URL 은 실행할 때마다 바뀐다.** `cloudflared` 창을 닫으면 끊긴다.
- API(파생지표·캔들)는 `serve_dashboard` 서버 모드에서만 실시간 동작하므로, 외부에서도
  차트·지표를 실시간으로 보려면 대시보드는 `python -m scripts.serve_dashboard` 로 띄워야 한다
  (스캐너가 생성하는 정적 `state/dashboard.html` 만 볼 거면 터널 대상 포트만 맞추면 된다).

### (선택) 고정 주소 + 이메일 로그인 게이트

Cloudflare 계정에 등록된 도메인이 있으면 **named tunnel + Cloudflare Access** 로
`dash.내도메인.com` 같은 고정 주소를 만들고 이메일 OTP 로그인으로 이중 보호할 수 있다.
자주 쓰게 되면 그때 전환을 권장(설정은 Cloudflare Zero Trust 대시보드에서).
