export const WHO_RED: 1;
export const WHO_BLUE: 2;

type WHO = typeof WHO_RED | typeof WHO_BLUE;

/**
 * @param who Color of player on which get best move, use WHO_RED or WHO_BLUE from utils.js
 * @param movesHistory Moves history played so far, like ['a1', 'swap-pieces', 'pass', ...]
 * @param level AI level from 1 to 10 (Defaults to 10)
 *
 * @returns {String} Best move as string, like "d4"
 */
export function getBestMove(
    redOrBlue: WHO,
    movesHistory: string[],
    level: number,
): string;

/**
 * @param who Color of player on which get best move, use WHO_RED or WHO_BLUE from utils.js
 * @param position Custom position, like:
 * ``` js
 * [
 *     ['a1', 'd4', 'd5'],  // red cells
 *     ['f6'],              // blue cells
 * ]
 * ```
 *
 * @param level AI level from 1 to 10 (Defaults to 10)
 *
 * @returns Best move as string, like "d4"
 */
export function getBestMoveCustomPosition(
    redOrBlue: WHO,
    position: [string[], string[]],
    level: number,
): string;

export class State {
    constructor(level: number);

    /**
     * Update AI level, from 1 to 10.
     */
    setLevel(level: number): void;

    /**
     * Calculate next move.
     */
    getBestMove(who: WHO, theLevel?: number): [number, number];

    /**
     * Add a move from i and j coords.
     * Does not support swap and pass.
     * Use replayMovesHistory() to initialize board with a moves history containing swap-pieces and pass moves.
     *
     * @param who WHO_RED or WHO_BLUE
     *
     * @returns Number of total moves played. False if this cell is already played.
     */
    makeMove(who: WHO, i: number, j: number): false | number;

    /**
     * Recreate a game state from history.
     * Handles "swap-pieces" and "pass".
     */
    replayMovesHistory(movesHistory: string[]): void;

    /**
     * Reset and set a board position from red and blue cells, like:
     *
     * ```
     * [
     *  ['a1', 'd4'],   // red cells
     *  ['f6'],         // blue cells
     * ]
     * ```
     */
    resetBoard(cells: [string[], string[]]): void;
}
