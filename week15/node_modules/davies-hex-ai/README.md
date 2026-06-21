# AI for Hex board game

Developed by Davies, initial project here: https://github.com/DaviesGit/hex_board_game

Forked and adapted. Changes are:

- Translated UI to English, play it here: https://alcalyn.github.io/hex_board_game/
- AI now plays instantly (removed setTimeout)
- added typings for typescript
- made it reusable, can generate a move from a moves history
- made it available through npm
- handle `swap-pieces` and `pass` moves in moves history

Reusable part is in `src/` (and tests in `test/`).

## Install

``` bash
npm install davies-hex-ai
```

## Usage

- Calculate a single move from a game position, from move history

``` js
import { getBestMove, WHO_RED, WHO_BLUE } from 'davies-hex-ai';

// Calculate red move, after d4 f6 (strongest level by default)
getBestMove(WHO_RED, ['d4', 'f6']); // output: "g6"

// Calculate blue move, after d4 f6 g6, at level 5 (min level: 1, max level: 10)
getBestMove(WHO_BLUE, ['d4', 'f6', 'g6'], 5); // output: "g5"
```

- Calculate a single move from a custom position, with stones placed manually

``` js
import { getBestMove, WHO_RED, WHO_BLUE } from 'davies-hex-ai';

// Fill board with red and blue stones manually, and calculate best red move, level 10
getBestMoveCustomPosition(
    WHO_RED,
    [
        // red stones
        ['c1', 'c2', 'd2', 'd3', 'c4', 'b5', 'b6', 'c6', 'c11', 'c10', 'b10', 'c7', 'd9', 'e8', 'e7'],

        // blue stones
        [],
    ],
    10, // level
);
```

## Development

To contribute to this repo, clone it, install dependencies, run tests:

``` bash
# Clone this repo
git clone git@github.com:alcalyn/hex_board_game.git

# Install dependencies
npm install

# Run unit tests
npm test
```

## License

[MIT License](LICENSE.txt)
