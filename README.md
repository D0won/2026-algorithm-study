# Pusan National University (PNU) Algorithm Course Study — Spring 2026

This repository contains study materials, source code implementations, weekly programming assignments, and tournament project files for the **Algorithm** course (Spring Semester 2026) in the **Department of Biomedical Convergence Engineering (Data Science Major)** at **Pusan National University (PNU)**.

Coding assignments and online judge problems are solved primarily on PNU's official platform: **[Codeplace](https://code.pusan.ac.kr/)**.

---

## 📅 Weekly Curriculum & Coursework

| Week | Core Topics & Algorithms | Assignments & Implementations | Codeplace Problems |
|:---:|---|---|---|
| **Week 1** | Introduction & Complexity Analysis | • Sum of integers using Gauss's formula (O(1)) in [assignment1_202355699.py](week1%20/assignment1_202355699.py) | • [1160.py](week1%20/1160.py)<br>• [1509.py](week1%20/1509.py) |
| **Week 2** | Sieve of Eratosthenes & Prime Numbers | • License plate prime number checker in [assignment2_202355699.py](week2/assignment2_202355699.py) | • [3164.py](week2/3164.py)<br>• [3199.py](week2/3199.py)<br>• [4010.py](week2/4010.py) |
| **Week 3** | Divide & Conquer (Part I) | • Tower of Hanoi path tracker in [assignment3_202355699.py](week3/assignment3_202355699.py)<br>• Merge Sort in [merge_sort.py](week3/merge_sort.py) | • [1053.py](week3/1053.py) |
| **Week 4** | Divide & Conquer (Part II) & Disjoint Set | • Quick Sort (Hoare / Lomuto partition) & Quick Select<br>• Kruskal's MST (Union-Find) in [assignment4_202355699.py](week4/assignment4_202355699.py) | • [1018.py](week4/1018.py)<br>• [1076.py](week4/1076.py)<br>• [3234.py](week4/3234.py) |
| **Week 5** | Greedy Algorithms & Graphs | • Greedy Candy Distribution in [assignment5_202355699.py](week5/assignment5_202355699.py)<br>• MST (Prim & Kruskal)<br>• Dijkstra's Shortest Path<br>• Fractional Knapsack<br>• Greedy Job Scheduling | • [2129.py](week5/2129.py) |
| **Week 6** | Greedy Algorithms & Dynamic Programming | • Huffman Coding<br>• 0-1 Knapsack (DP)<br>• Coin Change (DP) | • [3202.py](week6/3202.py)<br>• [5444.py](week6/5444.py) |
| **Week 7** | Dynamic Programming | • Matrix Chain Multiplication (DP)<br>• Edit Distance (DP) | • [1044.py](week7/1044.py)<br>• [1141.py](week7/1141.py) |
| **Week 8** | **Midterm Examination Week** | *No new algorithms* | *(N/A)* |
| **Week 9** | Sorting Algorithms & DP Extensions | • Elementary Sorts (Bubble, Insertion, Selection, Shell)<br>• Edit Distance with custom penalty (DP) in [assignment9_202355699.py](week9/assignment9_202355699.py) | • [1066.py](week9/1066.py)<br>• [1133.py](week9/1133.py)<br>• [4006.py](week9/4006.py) |
| **Week 10**| Heap Sort & Metric TSP Approximation | • Heap Sort<br>• MST-based 2-Approximation for Metric TSP<br>• Lexicographical Rank computation in [assignment10_202355699.py](week10/assignment10_202355699.py) | • [1007.py](week10/1007.py) |
| **Week 11**| Backtracking & Approximation Algorithms | • TSP via Backtracking<br>• Vertex Cover 2-Approximation via Matching<br>• Mutation Gene Detection in [assignment11_202355699.py](week11/assignment11_202355699.py) | • [1072.py](week11/1072.py)<br>• [1122.py](week11/1122.py) |
| **Week 12**| Branch & Bound & Advanced DP | • TSP via Branch & Bound<br>• Interleaving String Validation (DP) in [assignment12_202355699.py](week12/assignment12_202355699.py) | • [1109.py](week12/1109.py)<br>• [1110.py](week12/1110.py) |
| **Week 13**| Heuristic Optimization & Genetic Algorithms | • Genetic Algorithm for TSP<br>• 3D Block Projection Stacking in [assignment13_202355699.py](week13/assignment13_202355699.py) | • [1067.py](week13/1067.py) |
| **Week 14**| Number Theory | • Finding original numbers from proper divisors | • [3064.py](week14/3064.py) |
| **Week 15**| **Final Examination Week** | *No new algorithms* | *(N/A)* |
| **Week 16**| **Term Project: Hex AI Playing Agent** | • Strategic board game engine & playing AI agent using minimax search, alpha-beta pruning, and heuristics in [week16/](week16/) | *(Term Project)* |

---

## 📁 Repository Directory Structure

```directory
.
├── week1 /                   # Gauss formula & basic time complexity tasks
├── week2/                    # License plate prime check (Sieve of Eratosthenes)
├── week3/                    # Hanoi Tower recursion & Merge Sort
├── week4/                    # Quick Sort (Lomuto/Hoare), Quick Select & Kruskal's MST
├── week5/                    # Greedy Algorithms (Fractional Knapsack, Prim, Dijkstra)
├── week6/                    # Huffman coding, Knapsack DP, Coin Change DP
├── week7/                    # Matrix Chain Multiplication & Edit Distance
├── week9/                    # Basic Sorting Algorithms & Edit Distance with Penalty
├── week10/                   # Heap Sort & TSP Approximation (MST-based)
├── week11/                   # Backtracking TSP, Vertex Cover Approx, Gene mutation search
├── week12/                   # Branch & Bound TSP, Interleaving String check
├── week13/                   # Genetic TSP, 3D Block projection stacking
├── week14/                   # Proper divisors number theory problem
└── week16/                   # Week 16 Term Project: Hex AI Board Game Agent
```

---

## 🏆 Week 16 Term Project: Hex AI Agent (`week16`)

The term project focuses on constructing an intelligent game agent to compete in **Hex**, a mathematical connection board game. 

The AI agent ([hex_ai.py](week16/hex_ai.py)) implements:
- **Search Strategy**: Depth-limited alpha-beta search with iterative deepening.
- **Tactical Patterns**: Explicit identification of two-cell bridge structures to maintain connections or disrupt opponent routes.
- **Shortest Path Heuristic**: Evaluates the board's state by calculating shortest-path connectivity distances for each player's boundaries using custom weights.

---

## 🔗 Links & References
- **University Platform**: [Pusan National University Codeplace](https://code.pusan.ac.kr/)
- **Course**: Pusan National University (PNU) Data Science Major / CSE - Algorithm (2026-1)
