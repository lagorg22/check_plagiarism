package assign1;
public class TetrisGrid {
private boolean[][] grid;
public TetrisGrid(boolean[][] grid) {
this.grid = grid;
}
public void clearRows() {
int rowLen = grid.length;
int colLen = grid[0].length;
boolean[][] result = new boolean[rowLen][colLen];
int count = 0, resCol = 0;
for (int col=0; col<colLen; col++) {
for (int row=0; row<rowLen; row++) {
result[row][resCol] = grid[row][col];
if (grid[row][col]) count++;
}
if (count != rowLen) resCol++;
count = 0;
}
for (int col=resCol; col<colLen; col++)
for (int row=0; row<rowLen; row++)
result[row][col] = false;
grid = result;
}
boolean[][] getGrid() {
return grid;
}
}