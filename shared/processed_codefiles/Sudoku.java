package assign3;
public class Sudoku {
private int[][] grid;
private int[][] gridSol;
private boolean isSolved;
private int solCount;
private long timeElapsed;
private List<Spot> spots;
public static final int[][] easyGrid = Sudoku.stringsToGrid(
"1 6 4 0 0 0 0 0 2",
"2 0 0 4 0 3 9 1 0",
"0 0 5 0 8 0 4 0 7",
"0 9 0 0 0 6 5 0 0",
"5 0 0 1 0 2 0 0 8",
"0 0 8 9 0 0 0 3 0",
"8 0 9 0 4 0 2 0 0",
"0 7 3 5 0 9 0 0 1",
"4 0 0 0 0 0 6 7 9");
public static final int[][] mediumGrid = Sudoku.stringsToGrid(
"530070000",
"600195000",
"098000060",
"800060003",
"400803001",
"700020006",
"060000280",
"000419005",
"000080079");
public static final int[][] hardGrid = Sudoku.stringsToGrid(
"3 7 0 0 0 0 0 8 0",
"0 0 1 0 9 3 0 0 0",
"0 4 0 7 8 0 0 0 3",
"0 9 3 8 0 0 0 1 2",
"0 0 0 0 4 0 0 0 0",
"5 2 0 0 0 6 7 9 0",
"6 0 0 0 2 1 0 4 0",
"0 0 0 5 3 0 9 0 0",
"0 3 0 0 0 0 0 5 1");
public static final int SIZE = 9;  // size of the whole 9x9 puzzle
public static final int PART = 3;  // size of each 3x3 part
public static final int MAX_SOLUTIONS = 100;
public static int[][] stringsToGrid(String... rows) {
int[][] result = new int[rows.length][];
for (int row = 0; row<rows.length; row++) {
result[row] = stringToInts(rows[row]);
}
return result;
}
public static int[][] textToGrid(String text) {
int[] nums = stringToInts(text);
if (nums.length != SIZE*SIZE) {
throw new RuntimeException("Needed 81 numbers, but got:" + nums.length);
}
int[][] result = new int[SIZE][SIZE];
int count = 0;
for (int row = 0; row<SIZE; row++) {
for (int col=0; col<SIZE; col++) {
result[row][col] = nums[count];
count++;
}
}
return result;
}
public static int[] stringToInts(String string) {
int[] a = new int[string.length()];
int found = 0;
for (int i=0; i<string.length(); i++) {
if (Character.isDigit(string.charAt(i))) {
a[found] = Integer.parseInt(string.substring(i, i+1));
found++;
}
}
int[] result = new int[found];
System.arraycopy(a, 0, result, 0, found);
return result;
}
public static void main(String[] args) {
Sudoku sudoku;
sudoku = new Sudoku(hardGrid);
System.out.println(sudoku); // print the raw problem
int count = sudoku.solve();
System.out.println("solutions:" + count);
System.out.println("elapsed:" + sudoku.getElapsed() + "ms");
System.out.println(sudoku.getSolutionText());
}
private class Spot implements Comparable<Spot> {
private int row;
private int col;
private int legalCount;
public Spot(int r, int c) {
row = r;
col = c;
legalCount = getLegal().size();
}
public void set(int val) {
grid[row][col] = val;
}
private HashSet<Integer> getLegal() {
HashSet<Integer> lvs = new HashSet<Integer>(Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9));
for (int i=0; i<SIZE; i++) {
lvs.remove(grid[row][i]);
lvs.remove(grid[i][col]);
lvs.remove(grid[(row/PART)*PART + i / PART][(col/PART)*PART + i % PART]);
}
return lvs;
}
@Override
public int compareTo(Spot other) {
return legalCount - other.legalCount;
}
}
public Sudoku(int[][] ints) {
grid = ints;
gridSol = new int[SIZE][SIZE];
isSolved = false;
}
public Sudoku(String text) {
this(textToGrid(text));
}
@Override
public String toString() {
return gridToText(grid);
}
private static String gridToText(int[][] grid) {
StringBuilder gridTxt = new StringBuilder();
for(int i = 0; i < SIZE; i++) {
for (int j = 0; j < SIZE; j++) {
gridTxt.append(grid[i][j]);
gridTxt.append(' ');
}
gridTxt.append('\n');
}
return gridTxt.toString();
}
private void makeSpots() {
spots = new ArrayList<Spot>();
for (int i = 0; i < SIZE; i++)
for (int j = 0; j < SIZE; j++)
if (grid[i][j] == 0) spots.add(new Spot(i,j));
Collections.sort(spots);
}
public int solve() {
long startTime = System.currentTimeMillis();
makeSpots();
solCount = 0;
recSolve(0);
long endTime = System.currentTimeMillis();
timeElapsed = endTime - startTime;
return solCount;
}
private void recSolve(int pos) {
if (solCount >= MAX_SOLUTIONS) return;
if (pos == spots.size()) {
if (solCount == 0) {
isSolved = true;
saveSolution();
}
solCount++;
return;
}
Spot curSpot = spots.get(pos);
for (int val : curSpot.getLegal()) {
curSpot.set(val);
recSolve(pos + 1);
}
curSpot.set(0);
return;
}
private void saveSolution() {
for (int i = 0; i < SIZE; i++)
System.arraycopy(grid[i], 0, gridSol[i], 0, SIZE);
}
public String getSolutionText() {
if (!isSolved) solve();
if (solCount == 0) return "";
else return gridToText(gridSol);
}
public long getElapsed() {
if (!isSolved) solve();
return timeElapsed;
}
}