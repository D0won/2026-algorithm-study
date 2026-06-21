// Persistent JSON-lines adapter around the unmodified davies-hex-ai 1.2.7.
import readline from 'node:readline';
import { getBestMove, WHO_RED, WHO_BLUE } from 'davies-hex-ai';

const input = readline.createInterface({ input: process.stdin, terminal: false });
input.on('line', line => {
  try {
    const request = JSON.parse(line);
    const who = request.player === 1 ? WHO_RED : WHO_BLUE;
    const move = getBestMove(who, request.history, 10);
    process.stdout.write(JSON.stringify({ move }) + '\n');
  } catch (error) {
    process.stdout.write(JSON.stringify({ error: String(error) }) + '\n');
  }
});
