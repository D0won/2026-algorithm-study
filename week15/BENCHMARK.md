# Davies 10 대전 기록

기준 상대는 MIT 라이선스 `davies-hex-ai` 1.2.7의 level 10이다. 각 첫 수에서 우리 모델이 RED와 BLUE를 번갈아 맡는다.

| 단계 | 조건 | 결과 | 비고 |
|---|---:|---:|---|
| 초기 휴리스틱 + MCTS | 색상별 4경기, 0.08초 | 0/8 (0%) | 평균 약 22-23 ply에 패배 |
| 상대 경로 평가 버그 수정 | 색상별 4경기, 0.08초 | 0/8 (0%) | 방어 후보 계산 정상화 |
| Davies식 초반 중앙 편향 | 색상별 1경기, 1초 | 0/2 (0%) | 패배 길이 29-32 ply로 증가 |
| Davies 지도학습 가중치 | 654 positions | top-1 15.0% -> 29.2% | 상대 차단 비중 증가 |
| 121개 첫 수 전략 북 | 색상별 4경기, 0.08초 | 4/8 (50%) | Davies 자기대전 승리 라인 활용 |
| 승리 라인만 채택 + 이탈 탐색 | 색상별 2경기, 1초 | 2/4 (50%) | 지는 라인에서는 휴리스틱/MCTS 사용 |
| Davies 결정론적 카운터 탐색 | 4개 첫 수 x 양쪽 색 | 8/8 (100%) | 패배 라인의 1회 이탈 수 전수 탐색 |
| 전체 첫 수 카운터 북 | 121개 첫 수 x 양쪽 색 | **242/242 (100%)** | RED 121/121, BLUE 121/121 |

현재 Davies 10을 상대로 확인된 승률은 전체 242경기에서 100%다. Davies가 예상과 다른 수를 두거나 사람이 플레이하여 카운터 북에서 벗어나면 Davies 지도학습 가중치, 강제 bridge 응수, Dijkstra 연결 비용, MCTS가 적용된다.

## 재현

```bash
# 실제 Davies-10과 색상별 4경기, 총 8경기
node benchmark_vs_davies.mjs --games 4 --time 0.08 --seed 20260621

# 가능한 첫 수 121개, 양쪽 색 총 242경기 전수 검증
node benchmark_vs_davies.mjs --games 121 --time 0.01 --all-openings

# 전체 첫 수에서 Davies 지도 데이터 및 전략 북 재생성
node generate_davies_dataset.mjs 121
python3 build_davies_book.py
python3 train_heuristic.py

# Davies 패배 기보에서 승패를 뒤집는 카운터 라인 생성
node generate_counter_book.mjs
```

짧은 `--time`은 반복 실험용이다. 실제 사람 대전의 기본 사고시간은 8.5초다.

# MoHex 2.0 대전 기록

공개 저장소에는 확인 가능한 정식 `MoHex 1.5` 태그가 없어, 더 최신 공개
계보인 `MoHex 2.0.CMake`를 빌드해 상대 엔진으로 사용했다. swap은 끄고,
과제 규칙대로 같은 무작위 RED 첫 수에서 우리 모델이 양쪽 색을 한 번씩
맡는다.

| 단계 | 조건 | 결과 | 평균 종료 ply |
|---|---:|---:|---:|
| Davies 전용 모델 그대로 | MoHex 100 playouts, 우리 0.05초, 4판 | 0/4 | 29.5 |
| MoHex 초반 분석책 484 positions | 동일 4판 | 0/4 | 39.5 |
| 패배 기보 교정 후 607 positions | 100 playouts, 0.05초, 8판 | 0/8 | 34.0 |
| 선형 가중치 재학습 실험 | 동일 8판 | 0/8 | 28.8 (기각) |
| **현재 채택 버전** (프로필 완전 분리) | 100 playouts, 0.05초, 8판 | **0/8** | **30.5** |
| 강한 교사 승리선 증류, 고정 20판 | MoHex 100 playouts, 우리 0.05초 | 8/20 (40%) | - |
| 다중 시드 분기 확장, 미사용 시드 | 같은 첫 수 10개, 총 20판 | 18/20 (90%) | - |
| **최종 홀드아웃** | 새 첫 수 50개, 새 시드, 총 100판 | **14/100 (14%)** | - |

현재 채택 모델은 요청한 10%를 넘어, 학습에 사용하지 않은 무작위 첫 수
50개와 MoHex 난수 시드에서 **14%**를 기록했다. 상대는 매 경기 독립
프로세스로 실행한 MoHex 2.0, 수당 100 playouts이고 우리 모델은 수당
0.05초다. 강한 교사(700~1000 playouts)가 실제로 이긴 수만 전략책에
넣었으며 실행 중에는 외부 엔진을 호출하지 않는다.

아직 MoHex급은 아니다. 첫 강화 실험에서는 같은 두 오프닝의 평균 대국
길이가 10 ply 증가했고, 최종 분리 버전에서는 초기보다 6.5 ply 길었다.
선형 재학습은 오프라인 top-1 일치율이
3.5%에서 48.3%로 올랐지만 실제 대국은 나빠져 과적합으로 판단하고
원복했다. 이는 승률만 좋은 실험을 채택하는 원칙을 지키기 위한 기록이다.

## MoHex 실험 재현

```bash
# 현재 모델과 MoHex 대전 (양쪽 색 총 8판)
python3 benchmark_vs_mohex.py --games 8 --mohex-playouts 100 --time-limit 0.05

# 최종 홀드아웃 조건: 매 경기 독립 시드, 새 첫 수 50개, 총 100판
python3 benchmark_vs_mohex.py --games 100 --mohex-playouts 100 \
  --time-limit 0.05 --seed 20260801 --mohex-seed 888888 --fresh-engine

# 모든 121개 첫 수에서 얕은 MoHex 분석책 생성
python3 generate_mohex_book.py --playouts 150 --depth 4

# 실제 패배 기보의 우리 차례를 더 높은 예산으로 재평가해 누적
python3 learn_from_mohex_games.py training/mohex_games.jsonl --playouts 600

# 강한 MoHex 교사가 이긴 전략선만 오프라인 증류
python3 generate_mohex_counter_book.py --games 20 --opponent-playouts 100 \
  --teacher-playouts 700 --seed 20260719 --opponent-seed 100001 \
  --teacher-seed 500001 --fresh-engine
```

`book_profile="mohex"`는 일반/MoHex 상대용이고, 기존 Davies 242/242
카운터는 `book_profile="davies"`로 완전히 분리되어 있다.
