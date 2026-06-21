// Round-robin harness: Python hybrid AI versus the actual Davies level 10.
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { getBestMoveCustomPosition, WHO_BLUE, WHO_RED } from './vendor/davies-hex-ai/src/index.js';

const EMPTY = 0, RED = 1, BLUE = 2, SIZE = 11;
const DIRECTIONS = [[-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0]];

const args = Object.fromEntries(process.argv.slice(2).map((item, i, all) =>
    item.startsWith('--') ? [item.slice(2), all[i + 1]?.startsWith('--') ? true : all[i + 1]] : [Symbol(), item]
).filter(([key]) => typeof key === 'string'));
const gamesPerPair = Number(args.games ?? 6);
const timeLimit = Number(args.time ?? 0.15);
const baseSeed = Number(args.seed ?? 20260621);
const allOpenings = process.argv.includes('--all-openings');

const python = spawn('python3', ['engine_server.py'], { stdio: ['pipe', 'pipe', 'inherit'] });
const lines = createInterface({ input: python.stdout });
const replies = [];
lines.on('line', line => replies.shift()?.(JSON.parse(line)));

function pythonMove(board, player, seed) {
    return new Promise((resolve, reject) => {
        replies.push(result => result.error ? reject(new Error(result.error)) : resolve(result));
        python.stdin.write(JSON.stringify({ board, player, time_limit: timeLimit, seed }) + '\n');
    });
}

function notation(row, col) { return String.fromCharCode(97 + col) + (row + 1); }
function parseMove(text) { return [Number(text.slice(1)) - 1, text.charCodeAt(0) - 97]; }
function opponent(player) { return player === RED ? BLUE : RED; }

function hasWon(board, player) {
    const stack = [];
    if (player === RED) {
        for (let col = 0; col < SIZE; col++) if (board[0][col] === RED) stack.push([0, col]);
    } else {
        for (let row = 0; row < SIZE; row++) if (board[row][0] === BLUE) stack.push([row, 0]);
    }
    const seen = new Set(stack.map(([r, c]) => `${r},${c}`));
    while (stack.length) {
        const [row, col] = stack.pop();
        if ((player === RED && row === SIZE - 1) || (player === BLUE && col === SIZE - 1)) return true;
        for (const [dr, dc] of DIRECTIONS) {
            const nr = row + dr, nc = col + dc, key = `${nr},${nc}`;
            if (nr >= 0 && nr < SIZE && nc >= 0 && nc < SIZE && !seen.has(key) && board[nr][nc] === player) {
                seen.add(key); stack.push([nr, nc]);
            }
        }
    }
    return false;
}

function daviesMove(board, player) {
    const position = [[], []];
    for (let row = 0; row < SIZE; row++) for (let col = 0; col < SIZE; col++) {
        if (board[row][col] === RED) position[0].push(notation(row, col));
        if (board[row][col] === BLUE) position[1].push(notation(row, col));
    }
    const who = player === RED ? WHO_RED : WHO_BLUE;
    return parseMove(getBestMoveCustomPosition(who, position, 10));
}

// Deterministic LCG gives reproducible, dependency-free opening positions.
function opening(index) {
    if (allOpenings) return index % (SIZE * SIZE);
    let value = (baseSeed + index * 2654435761) >>> 0;
    value = (1664525 * value + 1013904223) >>> 0;
    return value % (SIZE * SIZE);
}

async function playGame(index, hybridColor) {
    const board = Array.from({ length: SIZE }, () => Array(SIZE).fill(EMPTY));
    const first = opening(index % gamesPerPair);
    board[Math.floor(first / SIZE)][first % SIZE] = RED;
    const moves = [`R:${notation(Math.floor(first / SIZE), first % SIZE)}*`];
    let turn = BLUE;
    let hybridIterations = 0;
    while (moves.length <= SIZE * SIZE) {
        let move;
        if (turn === hybridColor) {
            const result = await pythonMove(board, turn, baseSeed + index * 1000 + moves.length);
            move = [result.row, result.col];
            hybridIterations += result.iterations;
        } else {
            move = daviesMove(board, turn);
        }
        const [row, col] = move;
        if (board[row]?.[col] !== EMPTY) throw new Error(`Illegal move ${notation(row, col)}`);
        board[row][col] = turn;
        moves.push(`${turn === RED ? 'R' : 'B'}:${notation(row, col)}`);
        if (hasWon(board, turn)) return { winner: turn, hybridColor, moves, hybridIterations };
        turn = opponent(turn);
    }
    throw new Error('Hex ended without winner');
}

const results = [];
const started = Date.now();
for (let side = 0; side < 2; side++) {
    const hybridColor = side === 0 ? RED : BLUE;
    for (let game = 0; game < gamesPerPair; game++) {
        const result = await playGame(side * gamesPerPair + game, hybridColor);
        results.push(result);
        const won = result.winner === hybridColor;
        console.log(`${won ? 'WIN ' : 'LOSS'} hybrid=${hybridColor === RED ? 'RED' : 'BLUE'} opening=${result.moves[0]} plies=${result.moves.length}`);
    }
}
python.stdin.end();

const wins = results.filter(result => result.winner === result.hybridColor).length;
const byColor = color => {
    const games = results.filter(result => result.hybridColor === color);
    return `${games.filter(result => result.winner === color).length}/${games.length}`;
};
console.log(JSON.stringify({
    opponent: 'davies-hex-ai 1.2.7 level 10',
    games: results.length,
    timeLimit,
    wins,
    losses: results.length - wins,
    winRate: wins / results.length,
    hybridAsRed: byColor(RED),
    hybridAsBlue: byColor(BLUE),
    elapsedSeconds: (Date.now() - started) / 1000,
    lossesMoves: results.filter(result => result.winner !== result.hybridColor).map(result => result.moves.join(' ')),
}, null, 2));
