import { State } from './createState.js';
import { moveToString, WHO_RED, WHO_BLUE } from './utils.js';

export {
    State,
    WHO_RED,
    WHO_BLUE,
};

/**
 * Calculate best move from a real game moves history.
 *
 * @param {Number} who Color of player on which get best move, use WHO_RED or WHO_BLUE from utils.js
 * @param {String[]} movesHistory Moves history played so far, like ['a1', 'swap-pieces', 'pass', ...]
 * @param {Number} level AI level from 1 to 10 (Defaults to 10)
 *
 * @returns {String} Best move as string, like "d4"
 */
export const getBestMove = (who, movesHistory, level) => {
    if (!level) {
        level = 10;
    }

    if (who !== WHO_RED && who !== WHO_BLUE) {
        throw new Error('redOrBlue must be either WHO_RED or WHO_BLUE');
    }

    const state = new State(level);

    if (Array.isArray(movesHistory)) {
        state.replayMovesHistory(movesHistory);
    }

    const bestMove = state.getBestMove(who, level);

    return moveToString(bestMove);
};

/**
 * @param {Number} who Color of player on which get best move, use WHO_RED or WHO_BLUE from utils.js
 * @param {String[][]} position Custom position, like:
 * ``` js
 * [
 *     ['a1', 'd4', 'd5'],   // red cells
 *     ['f6'],         // blue cells
 * ]
 * ```
 *
 * @param {Number} level AI level from 1 to 10 (Defaults to 10)
 *
 * @returns {String} Best move as string, like "d4"
 */
export const getBestMoveCustomPosition = (who, position, level) => {
    if (!level) {
        level = 10;
    }

    if (who !== WHO_RED && who !== WHO_BLUE) {
        throw new Error('redOrBlue must be either WHO_RED or WHO_BLUE');
    }

    const state = new State(level);

    if (Array.isArray(position)) {
        state.resetBoard(position);
    }

    const bestMove = state.getBestMove(who, level);

    return moveToString(bestMove);
};
