// Generate supervised positions from Davies-10 self play.
import { writeFileSync, mkdirSync } from 'node:fs';
import { getBestMoveCustomPosition, WHO_BLUE, WHO_RED } from './vendor/davies-hex-ai/src/index.js';

const EMPTY = 0, RED = 1, BLUE = 2, SIZE = 11;
const DIRS = [[-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0]];
const count = Number(process.argv[2] ?? 60);
const notation = (r, c) => String.fromCharCode(97 + c) + (r + 1);
const parse = text => [Number(text.slice(1)) - 1, text.charCodeAt(0) - 97];
const other = p => p === RED ? BLUE : RED;

function won(board, player) {
    const stack = [];
    if (player === RED) for (let c = 0; c < SIZE; c++) board[0][c] === RED && stack.push([0, c]);
    else for (let r = 0; r < SIZE; r++) board[r][0] === BLUE && stack.push([r, 0]);
    const seen = new Set(stack.map(x => x.join(',')));
    while (stack.length) {
        const [r, c] = stack.pop();
        if ((player === RED && r === 10) || (player === BLUE && c === 10)) return true;
        for (const [dr, dc] of DIRS) {
            const nr = r + dr, nc = c + dc, key = `${nr},${nc}`;
            if (nr >= 0 && nr < SIZE && nc >= 0 && nc < SIZE && board[nr][nc] === player && !seen.has(key)) {
                seen.add(key); stack.push([nr, nc]);
            }
        }
    }
    return false;
}

function choose(board, player) {
    const position = [[], []];
    for (let r = 0; r < SIZE; r++) for (let c = 0; c < SIZE; c++) {
        if (board[r][c]) position[board[r][c] - 1].push(notation(r, c));
    }
    return parse(getBestMoveCustomPosition(player === RED ? WHO_RED : WHO_BLUE, position, 10));
}

const rows = [];
for (let game = 0; game < count; game++) {
    const board = Array.from({ length: SIZE }, () => Array(SIZE).fill(EMPTY));
    // Spread openings over all 121 cells instead of clustering pseudo-randomly.
    const opening = (game * 47 + 13) % 121;
    board[Math.floor(opening / 11)][opening % 11] = RED;
    let player = BLUE;
    const gameRows = [];
    while (true) {
        const move = choose(board, player);
        gameRows.push({ board: board.map(values => [...values]), player, move });
        board[move[0]][move[1]] = player;
        if (won(board, player)) {
            for (const row of gameRows) rows.push(JSON.stringify({ ...row, winner: player }));
            break;
        }
        player = other(player);
    }
}
mkdirSync('training', { recursive: true });
writeFileSync('training/davies_positions.jsonl', rows.join('\n') + '\n');
console.log(`wrote ${rows.length} positions from ${count} games`);
