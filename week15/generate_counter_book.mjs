// Find one-deviation winning lines against deterministic Davies level 10.
import { writeFileSync } from 'node:fs';
import { getBestMoveCustomPosition, WHO_BLUE, WHO_RED } from './vendor/davies-hex-ai/src/index.js';

const E = 0, R = 1, B = 2, N = 11;
const DS = [[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0]];
const notation = (r,c) => String.fromCharCode(97+c)+(r+1);
const parse = s => [Number(s.slice(1))-1,s.charCodeAt(0)-97];
const other = p => p===R?B:R;
const copy = b => b.map(row=>[...row]);
const key = (b,p) => `${p}:`+b.flat().join('');

function won(board,p){
  const q=[];
  if(p===R) for(let c=0;c<N;c++) board[0][c]===p&&q.push([0,c]);
  else for(let r=0;r<N;r++) board[r][0]===p&&q.push([r,0]);
  const seen=new Set(q.map(x=>x.join(',')));
  while(q.length){const [r,c]=q.pop();if((p===R&&r===10)||(p===B&&c===10))return true;
    for(const [dr,dc] of DS){const nr=r+dr,nc=c+dc,k=`${nr},${nc}`;
      if(nr>=0&&nr<N&&nc>=0&&nc<N&&board[nr][nc]===p&&!seen.has(k)){seen.add(k);q.push([nr,nc]);}}
  } return false;
}
function davies(board,p){
  const pos=[[],[]];for(let r=0;r<N;r++)for(let c=0;c<N;c++)if(board[r][c])pos[board[r][c]-1].push(notation(r,c));
  return parse(getBestMoveCustomPosition(p===R?WHO_RED:WHO_BLUE,pos,10));
}
function finish(board,turn,firstMove=null){
  const trace=[];let forced=firstMove;
  while(true){const move=forced??davies(board,turn);forced=null;
    trace.push({board:copy(board),player:turn,move});board[move[0]][move[1]]=turn;
    if(won(board,turn))return {winner:turn,trace};turn=other(turn);
  }
}
function baseline(opening){const b=Array.from({length:N},()=>Array(N).fill(E));const [r,c]=parse(opening);b[r][c]=R;return finish(b,B);}

const requested=process.argv.slice(2);
const openings=requested.length?requested:Array.from({length:N*N},(_,i)=>notation(Math.floor(i/N),i%N));
const book={};
for(const opening of openings){
  const base=baseline(opening), loser=other(base.winner);
  console.log(`${opening}: baseline winner=${base.winner===R?'RED':'BLUE'}, searching ${loser===R?'RED':'BLUE'} counter`);
  let solution=null, tested=0;
  for(let pivot=0;pivot<base.trace.length&&!solution;pivot++){
    const state=base.trace[pivot];if(state.player!==loser)continue;
    for(let idx=0;idx<N*N;idx++){
      const r=Math.floor(idx/N),c=idx%N;if(state.board[r][c]!==E||(r===state.move[0]&&c===state.move[1]))continue;
      tested++;const game=finish(copy(state.board),loser,[r,c]);
      if(game.winner===loser){
        const prefix=base.trace.slice(0,pivot).filter(x=>x.player===loser);
        solution=[...prefix,...game.trace.filter(x=>x.player===loser)];
        console.log(`  found at ply=${pivot+2} move=${notation(r,c)} after ${tested} trials`);break;
      }
    }
  }
  if(!solution){console.log(`  no one-deviation counter after ${tested} trials`);continue;}
  for(const row of solution)book[key(row.board,row.player)]=row.move;
}
writeFileSync('counter_book.json',JSON.stringify(book));
console.log(`wrote ${Object.keys(book).length} counter positions`);
