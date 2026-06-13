import random

""" AI 도움으로 작성

    유전자 알고리즘 (Genetic Algorithm)

    다윈의 진화론에 기반한 최적화 알고리즘. 후보해 집합(Population)을 만들고,
    적합도가 높은 우수한 해를 선택(Selection), 교차(Crossover), 돌연변이(Mutation) 시키며
    진화적으로 최적해에 수렴해 나감.

    주요 단계:
    1. 초기화: 랜덤한 후보해(염색체) 집합 생성
    2. 적합도 평가: 후보해가 정답에 얼마나 가까운지 점수 매김
    3. 선택: 룰렛 휠 방식을 통해 우수한 해를 높은 확률로 복사
    4. 교차 및 돌연변이: 유전자를 섞고 돌발 변형을 주어 새로운 세대 생성
    5. 반복: 종료 조건(최대 세대 도달 등) 충족 시까지 2~4단계 반복

    시간 복잡도: O(Generations * Population_Size * Chromosome_Length) — 문제/파라미터별 상이
    공간 복잡도: O(Population_Size * Chromosome_Length) — 세대별 모집단 유지 공간
"""

def evaluate_fitness(x: int) -> int:
    """적합도 함수 (Fitness Function): f(x) = -x² + 38x + 80"""
    return -x**2 + 38 * x + 80


def decode_chromosome(chrom: list) -> int:
    """5비트 이진수 리스트를 10진수 정수 X로 변환 (0 ~ 31)"""
    binary_str = "".join(map(str, chrom))
    return int(binary_str, 2)


def genetic_algorithm(pop_size: int = 4, generations: int = 20, crossover_rate: float = 0.8, mutation_rate: float = 0.1) -> int:
    # 1. 초기 후보해 집합(Population) 생성 (5비트 염색체 4개)
    # 예: [[0, 0, 0, 0, 1], [1, 1, 1, 0, 1], ...]
    chrom_len = 5
    population = [[random.randint(0, 1) for _ in range(chrom_len)] for _ in range(pop_size)]

    for generation in range(generations):
        # 2. 적합도 평가 (Evaluation)
        decoded_values = [decode_chromosome(chrom) for chrom in population]
        fitness_scores = [evaluate_fitness(x) for x in decoded_values]

        # 3. 선택 연산 (Selection) — 룰렛 휠 방식
        total_fitness = sum(fitness_scores)
        if total_fitness == 0:
            probabilities = [1 / pop_size] * pop_size
        else:
            probabilities = [score / total_fitness for score in fitness_scores]
        
        # 확률에 따라 다음 세대가 될 부모 후보들을 선택 (중복 허용)
        selected_population = random.choices(population, weights=probabilities, k=pop_size)

        # 4. 차세대 생성을 위한 교차 및 돌연변이 연산
        next_generation = []
        for i in range(0, pop_size, 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i + 1] if i + 1 < pop_size else selected_population[0]

            # 4-1. 교차 연산 (Crossover) — 1점 교차
            if random.random() < crossover_rate:
                # 1부터 크기-1 사이의 임의의 교차점 선택
                cut = random.randint(1, chrom_len - 1)
                child1 = parent1[:cut] + parent2[cut:]
                child2 = parent2[:cut] + parent1[cut:]
            else:
                child1, child2 = parent1[:], parent2[:]  # 교차 안 됨

            # 4-2. 돌연변이 연산 (Mutation) — 비트 반전
            for child in [child1, child2]:
                for gene_idx in range(chrom_len):
                    if random.random() < mutation_rate:
                        child[gene_idx] = 1 - child[gene_idx]  # 0은 1로, 1은 0으로 반전
                
                if len(next_generation) < pop_size:
                    next_generation.append(child)

        population = next_generation

    # 모든 세대가 끝난 후 최적의 해 찾기 및 반환
    final_decoded = [decode_chromosome(chrom) for chrom in population]
    final_fitness = [evaluate_fitness(x) for x in final_decoded]
    best_idx = final_fitness.index(max(final_fitness))

    return final_decoded[best_idx]