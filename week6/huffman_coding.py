# ai 도움으로 코드 형성
class Node:
    def __init__(self, char, freq):
        self.char = char      # 문자
        self.freq = freq      # 빈도수
        self.left = None
        self.right = None


def huffman_tree(freq_dict):
    # 1. 초기 노드 리스트 생성
    nodes = []
    for char, freq in freq_dict.items():
        nodes.append(Node(char, freq))

    # 2. 노드가 1개 남을 때까지 반복
    while len(nodes) > 1:
        # 빈도수 기준 정렬
        nodes.sort(key=lambda x: x.freq)

        # 가장 작은 2개 선택
        left = nodes.pop(0)
        right = nodes.pop(0)

        # 새로운 노드 생성
        new_node = Node(None, left.freq + right.freq)
        new_node.left = left
        new_node.right = right

        # 다시 리스트에 추가
        nodes.append(new_node)

    # 루트 반환
    return nodes[0]


# 코드 출력용 함수
def print_codes(node, code=""):
    if node is None:
        return

    # leaf node면 출력
    if node.char is not None:
        print(f"{node.char}: {code}")
        return

    print_codes(node.left, code + "0")
    print_codes(node.right, code + "1")