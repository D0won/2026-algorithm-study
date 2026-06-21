# Hex AI - Davies 10 + MoHex heuristic hybrid

과제 PDF의 조건에 맞춘 11x11 Hex AI입니다.

- 빨강(`1`): 위-아래 연결
- 파랑(`2`): 왼쪽-오른쪽 연결
- 빈 칸: `0`
- Python 표준 라이브러리만 사용
- 기본 사고 시간 8.5초(과제 제한 10초보다 여유 있게 설정)

## 전략

1. 즉시 이기는 수와 상대의 즉시 승리 수를 먼저 검사합니다.
2. Davies 10처럼 양쪽 목표 변까지의 연결 잠재력을 계산합니다. 구현에서는 자기 돌 비용 `0`, 빈 칸 `1`, 상대 돌은 통과 불가로 둔 Dijkstra 연결 비용을 사용합니다.
3. 가상 연결의 기본 형태인 bridge 완성/차단, 이웃 돌, 중앙 및 대각선 방향성을 휴리스틱에 반영합니다.
4. 상위 후보에 MoHex 계열의 UCT Monte Carlo Tree Search와 패턴 기반 rollout을 수행합니다.
5. 일반/사람 상대에서는 121개 랜덤 첫 수의 MoHex 2.0 초반 분석과, 강한 MoHex 교사가 약한 MoHex를 실제로 이긴 전략선만 오프라인 증류한 책을 사용합니다.
6. Davies 프로필에서는 Davies 자가대전 전략 북과 한 수 이탈 전수 탐색으로 찾은 전용 카운터 북을 사용합니다.
7. 시간이 끝나면 가장 많이 탐색한 수를 선택합니다.

Davies 원본을 그대로 복사한 것이 아니라 핵심 평가 아이디어를 Python으로 다시 설계했고, MoHex의 MCTS/bridge 아이디어를 합친 모델입니다.

## 사용법

### 사람과 AI가 터미널에서 대전

실행 후 레드/블루를 직접 선택:

```bash
python3 play.py
```

실행 시 색상을 미리 지정할 수도 있습니다:

```bash
python3 play.py --human red --time 2
python3 play.py --human blue --time 2
python3 play.py --human blue --profile mohex
```

실행 직후 과제에서 무작위로 정해진 빨강 첫 돌의 좌표를 먼저 입력합니다. 이후 보드가 나오면 `a 1`, `f 6`, `h 10` 형태로 수를 입력하고, `q`로 종료합니다. 붙여 쓴 `f6` 형식도 사용할 수 있습니다.

AI는 기본적으로 제한시간에 여유를 둔 8.5초 동안 생각합니다. 빠른 연습 게임은 `--time 2`, 가장 강한 기본 설정은 별도 옵션 없이 실행하면 됩니다.

프로그램이 첫 돌까지 자동 추첨하게 하려면 `--auto-opening`, 일반적인 Hex처럼 빨강 플레이어가 첫 수부터 두게 하려면 `--normal-opening`을 추가하세요.

### Python 코드에서 호출

```python
from hex_ai import RED, BLUE, get_best_move

board = [[0] * 11 for _ in range(11)]
board[5][5] = RED  # 과제 규칙에 따라 선공 첫 돌은 외부에서 랜덤 배치

row, col = get_best_move(board, BLUE, time_limit=8.5, book_profile="mohex")
print(row, col)
```

반환 좌표는 0부터 시작하는 `(행, 열)`입니다. 중계 프로그램이 `a1`, `f6` 표기를 요구하면 `move_to_notation()`을 사용하세요.

JSON 표준입출력 어댑터:

```bash
python3 main.py <<'EOF'
{"board":[[0,0,0],[0,1,0],[0,0,0]],"player":2,"time_limit":0.2,"seed":1}
EOF
```

## 테스트

```bash
python3 -m unittest -v
```

Davies 10과 양쪽 색을 번갈아 맡는 벤치마크:

```bash
node benchmark_vs_davies.mjs --games 6 --time 0.15

# 빌드한 MoHex 2.0과 총 8경기
python3 benchmark_vs_mohex.py --games 8 --mohex-playouts 100 --time-limit 0.05
```

현재 홀드아웃 성적은 학습에 쓰지 않은 무작위 첫 수 50개와 MoHex 시드,
양쪽 색 총 100판에서 **14/100(14%)**입니다. 대국 중에는 MoHex 실행
파일을 호출하지 않으며 `hex_ai.py`와 `mohex_book.json`만 사용합니다.

`--games`는 색상별 경기 수이며 위 명령은 총 12경기를 실행합니다. 짧은 사고시간으로 후보 가중치를 빠르게 비교한 뒤, 최종 설정은 8.5초로 검증하는 용도입니다.

학습 과정과 단계별 승률은 `BENCHMARK.md`에 기록되어 있습니다.

## 제출 전 연결할 부분

교수님이 제공하는 중계 코드의 함수명/입력 형식이 정해져 있다면, 그 함수에서 `get_best_move(board, player)`만 호출하면 됩니다. 선공의 첫 돌 랜덤 배치는 게임 진행 측 규칙이므로 AI가 빈 보드에서 임의로 만들지 않습니다.

## 참고

- PlayHex의 Davies 봇은 `davies-hex-ai` 패키지를 사용하며 11x11 전용, 레벨 범위는 1-10입니다.
- Davies 패키지: MIT License, Copyright (c) 2020 Davies.
- MoHex의 핵심 공개 아이디어: UCT/AMAF 기반 MCTS, bridge pattern, virtual connection 및 inferior-cell 분석.
