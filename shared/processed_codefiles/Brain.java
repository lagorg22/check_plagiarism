package tetris;
public interface Brain {
public static class Move {
public int x;
public int y;
public Piece piece;
public double score;    // lower scores are better
}
public Brain.Move bestMove(Board board, Piece piece, int limitHeight, Brain.Move move);
}