# Third-party references

This implementation was written from scratch, but its design was informed by:

- `davies-hex-ai` 1.2.7, MIT License, Copyright (c) 2020 Davies.
  Source: https://github.com/alcalyn/hex_board_game
- B. Arneson, R. Hayward, and P. Henderson, "Monte Carlo Tree Search in Hex".
- S.-C. Huang et al., "MoHex 2.0: a pattern-based MCTS Hex player".

For local strength benchmarking, the repository also contains
`vendor/benzene-vanilla-cmake`, a CMake port of Benzene/MoHex distributed under
the GNU Lesser General Public License. It is an external opponent and offline
analysis tool; `play.py`, `main.py`, and `hex_ai.py` do not load or execute it.
Source: https://github.com/cgao3/benzene-vanilla-cmake
