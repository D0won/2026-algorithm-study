# Davies 10 기반 11x11 Hex AI

과제 PDF의 규칙을 따르는 콘솔 Hex 게임과 규칙 기반 AI입니다.

- 11x11, 빨강은 위-아래, 파랑은 왼쪽-오른쪽 연결
- 선공 빨강의 첫 돌은 무작위 배치
- Python 기본 라이브러리만 사용
- 한 수의 탐색 시간은 최대 9.5초로 제한
- 학습 모델 및 사전 학습 가중치 없음

## 출발점: 원본 Davies 10

PlayHex의 Davies 10은 `davies-hex-ai@1.2.7`의 레벨 10입니다. 원본은
네 방향(각 색의 두 목표 변)의 potential field를 반복 전파하고, 두 경로가
겹치는 bridge 후보에 보너스를 주어 가장 낮은 점수의 빈 칸을 선택합니다.
레벨 1-9는 평가에 난수 오차를 넣지만 레벨 10은 오차가 0이라 결정적입니다.

`davies_port.py`는 이 potential/bridge 계산을 Python으로 옮긴 기준 모델입니다.
`original_davies_runner.mjs`는 Python 포트가 아니라 npm의 원본 Davies 10을
그대로 실행합니다. 따라서 벤치마크 상대는 자기 복제품이 아니라 실제 원본입니다.

## 강화한 부분

`EnhancedDaviesAI`는 Davies 평가를 수순 정렬에 유지하면서 다음을 추가합니다.

1. 놓자마자 이기는 수를 최우선으로 선택
2. 상대의 1수 승리를 즉시 차단
3. Dijkstra식 최소 빈칸 연결 비용으로 양쪽의 실제 연결 난도를 평가
4. 연결 span과 인접 연결을 보조 점수로 사용
5. 확실히 증명되는 2수 포크만 Davies의 positional 수보다 우선
6. Davies 상위 후보별로 양쪽의 Davies 10 정책을 끝까지 시뮬레이션하고,
   실제 승리로 끝날 것으로 예측되는 후보만 override
7. 실험 옵션으로 Davies 상위 후보에 iterative-deepening negamax/alpha-beta 적용 가능
8. 모든 탐색 단계에서 monotonic clock을 확인해 10초 실격을 방지

## 설치와 실행

```bash
npm install
python3 -m unittest -v
python3 hex_game.py --human blue --time 9
```

옵션 없이 `python3 hex_game.py`를 실행하면 먼저 사람의 선공/후공을 묻고,
중계 화면에서 랜덤 배치된 빨강 첫 수를 입력받습니다. 빠르게 실행하려면
`--human blue --opening f6`처럼 지정할 수 있습니다. 첫 수 입력에서 Enter만
누르면 연습용 무작위 위치를 프로그램이 생성합니다.

원본 Davies 10과 자동 대국:

```bash
python3 benchmark.py --games 20 --time 9 --seed 99173
```

같은 랜덤 첫 수로 두 판을 두되 강화 AI의 색을 맞바꾸는 paired opening을
사용합니다. Davies counter-search를 사용할 때는 `--time 9`와 충분한 판수를
권장합니다. 10초 제한에 안전 여유를 두기 위해 코드상 상한은 9.5초입니다.

현재 실제 JavaScript Davies 10을 상대로 서로 다른 두 seed에서 paired-opening
30판을 실행해 30승 0패를 기록했습니다. 두 모델은 같은 랜덤 첫 수에서 레드와
블루를 한 번씩 맡았고, 측정된 최장 한 수는 9.02초였습니다. 이는 검증 표본의
승률 100%이지 모든 가능한 대국에 대한 수학적 보장은 아닙니다. 벤치마크는 한
수라도 10초 이상 걸리면 실패 처리합니다.

## 파일

- `hex_board.py`: 보드, 착수, 승리 판정, 좌표 변환
- `davies_port.py`: Davies 10의 Python potential/bridge 기준 모델
- `enhanced_ai.py`: 전술 + 연결 비용 + 제한시간 탐색 강화 모델
- `hex_game.py`: 사람 대 AI 콘솔 게임
- `benchmark.py`: 원본 JavaScript Davies 10과 자동 대국
- `original_davies_runner.mjs`: 원본 npm 패키지 JSON-lines 어댑터
- `test_hex.py`: 규칙, 합법 수, 즉시 승리/방어 테스트
- `THIRD_PARTY_NOTICES.md`: 원본 출처와 MIT 라이선스 고지
