# ai 도움으로 코드 형성
def fractional_knapsack(weights, values, capacity):
    items = []
    
    # (비율, 무게, 가치)
    for i in range(len(weights)):
        items.append((values[i] / weights[i], weights[i], values[i]))
    
    # 비율 기준 내림차순 정렬
    items.sort(reverse=True)
    
    total_value = 0
    
    for ratio, weight, value in items:
        if capacity >= weight:
            # 전체 넣기
            capacity -= weight
            total_value += value
        else:
            # 쪼개서 넣기
            total_value += ratio * capacity
            break
    
    return total_value