package tetris;
public class DefaultBrain implements Brain {
public Brain.Move bestMove(Board board, Piece piece, int limitHeight, Brain.Move move) {
if (move==null) move = new Brain.Move();
double bestScore = 1e20;
int bestX = 0;
int bestY = 0;
Piece bestPiece = null;
Piece current = piece;
board.commit();
while (true) {
final int yBound = limitHeight - current.getHeight()+1;
final int xBound = board.getWidth() - current.getWidth()+1;
for (int x = 0; x<xBound; x++) {
int y = board.dropHeight(current, x);
if (y<yBound) {    // piece does not stick up too far
int result = board.place(current, x, y);
if (result <= Board.PLACE_ROW_FILLED) {
if (result == Board.PLACE_ROW_FILLED) board.clearRows();
double score = rateBoard(board);
if (score<bestScore) {
bestScore = score;
bestX = x;
bestY = y;
bestPiece = current;
}
}
board.undo();    // back out that play, loop around for the next
}
}
current = current.fastRotation();
if (current == piece) break;    // break if back to original rotation
}
if (bestPiece == null) return(null);    // could not find a play at all!
else {
move.x = bestX;
move.y = bestY;
move.piece = bestPiece;
move.score = bestScore;
return(move);
}
}
public double rateBoard(Board board) {
final int width = board.getWidth();
final int maxHeight = board.getMaxHeight();
int sumHeight = 0;
int holes = 0;
for (int x=0; x<width; x++) {
final int colHeight = board.getColumnHeight(x);
sumHeight += colHeight;
int y = colHeight - 2;    // addr of first possible hole
while (y>=0) {
if  (!board.getGrid(x,y)) {
holes++;
}
y--;
}
}
double avgHeight = ((double)sumHeight)/width;
return (8*maxHeight + 40*avgHeight + 1.25*holes);
}
}