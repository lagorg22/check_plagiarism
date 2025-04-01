package tetris;
public class Board	{
private int width;
private int height;
private boolean[][] grid;
private boolean DEBUG = true;
boolean committed;
private int[] heights;
private int[] widths;
private int maxHeight;
private boolean hasPlaced = false;
private boolean[][] xGrid;
private int[] xHeights;
private int[] xWidths;
private int xMaxHeight;
public Board(int width, int height) {
this.width = width;
this.height = height;
grid = new boolean[width][height];
committed = true;
widths = new int[height];
heights = new int[width];
maxHeight = 0;
xGrid = new boolean[width][height];
xHeights = new int[width];
xWidths = new int[height];
}
public int getWidth() {
return width;
}
public int getHeight() {
return height;
}
public int getMaxHeight() {
return maxHeight;
}
public void sanityCheck() {
if (DEBUG) {
int[] yHeights = new int[width];
int[] yWidths = new int[height];
int yMaxHeight = 0;
for (int j = 0; j < height; j++)
for (int i = 0; i < width; i++)
if (grid[i][j]) {
yWidths[j]++;
if (j + 1 > yHeights[i]) yHeights[i] = j + 1;
if (yHeights[i] > yMaxHeight) yMaxHeight = yHeights[i];
}
if (!Arrays.equals(heights, yHeights) || !Arrays.equals(widths, yWidths) || !(maxHeight == yMaxHeight))
throw new RuntimeException("insane board problem");
}
}
public int dropHeight(Piece piece, int x) {
int y = 0;
int[] skirt = piece.getSkirt();
for (int i = 0; i < piece.getWidth(); i++) {
int h = heights[x + i] - skirt[i];
if (h >= 0 && h > y) y = h;
}
return y;
}
public int getColumnHeight(int x) {
return heights[x];
}
public int getRowWidth(int y) {
return widths[y];
}
public boolean getGrid(int x, int y) {
return (x >= width || y >= height || y < 0 || x < 0 || grid[x][y]);
}
public static final int PLACE_OK = 0;
public static final int PLACE_ROW_FILLED = 1;
public static final int PLACE_OUT_BOUNDS = 2;
public static final int PLACE_BAD = 3;
public int place(Piece piece, int x, int y) {
if (!committed) throw new RuntimeException("place commit problem");
hasPlaced = true;
committed = false;
backup();
int result = PLACE_OK;
if (x + piece.getWidth() > width || y + piece.getHeight() > height || x < 0 || y < 0)
return PLACE_OUT_BOUNDS;
for (TPoint p: piece.getBody()) {
int curX = p.x + x;
int curY = p.y + y;
if (grid[curX][curY]) return PLACE_BAD;
grid[curX][curY] = true;
widths[curY]++;
if (widths[curY] == width) result = PLACE_ROW_FILLED;
if (heights[curX] < curY + 1) heights[curX] = curY + 1;
if (heights[curX] > maxHeight) maxHeight = heights[curX];
}
sanityCheck();
return result;
}
public int clearRows() {
if (!hasPlaced) {
committed = false;
backup();
}
int rowsCleared = 0;
int toRow = 0;
for (int row = 0; row < maxHeight; row++) {
while (widths[row] == width) {
row++;
rowsCleared++;
}
for (int col = 0; col < width; col++)
grid[col][toRow] = grid[col][row];
widths[toRow] = widths[row];
toRow++;
}
while(toRow < maxHeight){
widths[toRow] = 0;
for(int col = 0; col < width; col++)
grid[col][toRow] = false;
toRow++;
}
maxHeight -= rowsCleared;
Arrays.fill(heights, 0);
for (int j = maxHeight - 1; j >= 0; j--) {
for (int i = 0; i < width; i++) {
if (grid[i][j]) {
if (j + 1 > heights[i]) heights[i] = j + 1;
}
}
}
sanityCheck();
return rowsCleared;
}
private void backup() {
for(int i = 0; i < width; i++)
System.arraycopy(grid[i], 0, xGrid[i], 0, height);
System.arraycopy(heights, 0, xHeights, 0, width);
System.arraycopy(widths, 0, xWidths, 0, height);
xMaxHeight = maxHeight;
}
public void undo() {
if (!committed) {
boolean[][] temp = grid;
grid = xGrid;
xGrid = temp;
int[] tempX = heights;
heights = xHeights;
xHeights = tempX;
int[] tempY = widths;
widths = xWidths;
xWidths = tempY;
maxHeight = xMaxHeight;
hasPlaced = false;
committed = true;
sanityCheck();
}
}
public void commit() {
hasPlaced = false;
committed = true;
}
public String toString() {
StringBuilder buff = new StringBuilder();
for (int y = height-1; y>=0; y--) {
buff.append('|');
for (int x=0; x<width; x++) {
if (getGrid(x,y)) buff.append('+');
else buff.append(' ');
}
buff.append("|\n");
}
for (int x=0; x<width+2; x++) buff.append('-');
return(buff.toString());
}
}