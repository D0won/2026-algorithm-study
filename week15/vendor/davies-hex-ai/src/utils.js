export const WHO_NONE = 0;
export const WHO_RED = 1;
export const WHO_BLUE = 2;

export const sign = (xx) => {
    if (xx < 0) return (-1);
    if (xx > 0) return (1);
    return (0);
};

/**
 * Converts "a1" to [0, 0]
 *
 * @param {String} moveStr E.g "a1"
 *
 * @returns {[Number, Number]} E.g [0, 0]
 */
export const parseMove = (moveStr) => {
    const matches = moveStr.match(/^([a-z])(\d+)$/);

    if (!matches) {
        throw new Error('Expected move like "a1", got: ' + moveStr);
    }

    const [_, letterStr, numberStr] = matches;

    return [
        letterStr.charCodeAt(0) - 97,
        parseInt(numberStr, 10) - 1,
    ];
};

/**
 * Converts (0, 0) to "a1"
 *
 * @param {[Number, Number]} ij
 *
 * @returns {String} E.g "a1"
 */
export const moveToString = ([i, j]) => {
    return String.fromCharCode(i + 97) + (j + 1);
};

/**
 * Mirror a move
 *
 * @param {String} moveStr E.g "b1"
 *
 * @returns {String} E.g "a2"
 */
export const mirrorMove = (moveStr) => {
    const [i, j] = parseMove(moveStr);

    return moveToString([j, i]);
};



/**
 * Converts ['a2', 'swap-pieces', 'd4', 'pass']
 * to: [['d4'], ['b1']]
 *
 * Handles swap-pieces and pass, make a "normalized" moves list
 *
 * @param {String[]} movesHistory
 *
 * @returns {[String[], String[]]}
 */
export const convertMovesHistoryToCells = movesHistory => {
    if (!Array.isArray(movesHistory)) {
        throw new Error('Expected movesHistory to be an array');
    }

    /** @type {[String[], String[]]} */
    const cells = [[], []];
    const RED = 0;
    const BLUE = 1;

    if (movesHistory.length === 0) {
        return cells;
    }

    const [firstMove, secondMove] = movesHistory;

    if (secondMove === undefined) {
        if (firstMove !== 'pass') {
            cells[RED].push(firstMove);
        }

        return cells;
    }

    if (secondMove === 'swap-pieces') {
        if (firstMove !== 'pass') {
            cells[BLUE].push(mirrorMove(firstMove));
        }
    } else {
        if (firstMove !== 'pass') {
            cells[RED].push(firstMove);
        }

        if (secondMove !== 'pass') {
            cells[BLUE].push(secondMove);
        }
    }

    for (let i = 2; i < movesHistory.length; ++i) {
        const moveStr = movesHistory[i];

        if (moveStr === 'pass') {
            continue;
        }

        cells[i % 2].push(moveStr);
    }

    return cells;
};
