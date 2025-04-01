package tetris;
public class BadBrain extends DefaultBrain {
public double rateBoard(Board board) {
double score = super.rateBoard(board);
return(10000 - score);
}
}