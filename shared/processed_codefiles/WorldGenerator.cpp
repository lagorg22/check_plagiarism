using namespace std;
const double kTerrainShrinkFactor = 0.7;
const double kSigma = 1.0;
const double kPi = 3.1415926535897932384626433;
const int kWindowSize = int(kSigma * 6.0 + 0.5);
static void diamondStep(Grid<double>& heights, int size, double variation);
static double diamondStepAverage(Grid<double>& heights, int size,
int row, int col);
static void squareStep(Grid<double>& heights, int size, double variation);
static double squareStepAverage(Grid<double>& heights, int size,
int row, int col);
static Grid<double> wallsToGrid(Set<Edge>& walls, int numRows, int numCols);
static void smoothTerrain(Grid<double>& toSmooth);
static void normalizeTerrain(Grid<double>& heights);
static void flattenValleys(Grid<double>& heights);
static void diamondSquareGenerate(Grid<double>& heights);
Grid<double> generateRandomTerrain(int numRows, int numCols) {
Grid<double> heights(numRows, numCols);
diamondSquareGenerate(heights);
smoothTerrain(heights);
normalizeTerrain(heights);
flattenValleys(heights);
return heights;
}
Grid<double> generateRandomMaze(int numRows, int numCols) {
Set<Edge> maze = createMaze(numRows, numCols);
return wallsToGrid(maze, numRows, numCols);
}
static void diamondSquareGenerate(Grid<double>& heights) {
int size = (min(heights.numRows(), heights.numCols()) - 1) / 2;
double variation = 1.0;
while (size > 0) {
diamondStep(heights, size, variation);
squareStep(heights, size, variation);
size /= 2;
variation *= kTerrainShrinkFactor;
}
}
static void normalizeTerrain(Grid<double>& heights) {
double maxHeight = -numeric_limits<double>::infinity();
double minHeight = numeric_limits<double>::infinity();
for (int row = 0; row < heights.numRows(); row++) {
for (int col = 0; col < heights.numCols(); col++) {
maxHeight = max(maxHeight, heights[row][col]);
minHeight = min(minHeight, heights[row][col]);
}
}
double range = maxHeight - minHeight;
for (int row = 0; row < heights.numRows(); row++) {
for (int col = 0; col < heights.numCols(); col++) {
heights[row][col] -= minHeight;
heights[row][col] /= range;
}
}
}
static void flattenValleys(Grid<double>& heights) {
for (int row = 0; row < heights.numRows(); row++) {
for (int col = 0; col < heights.numCols(); col++) {
heights[row][col] *= heights[row][col];
}
}
}
static void diamondStep(Grid<double>& heights, int size, double variation) {
int stride = size * 2;
for (int row = size; row < heights.numRows(); row += stride) {
for (int col = size; col < heights.numCols(); col += stride) {
heights[row][col] = diamondStepAverage(heights, size, row, col) +
randomReal(-variation, variation);
}
}
}
static double diamondStepAverage(Grid<double>& heights, int size,
int row, int col) {
double sum = heights[row - size][col - size] +
heights[row - size][col + size] +
heights[row + size][col - size] +
heights[row + size][col + size];
return sum / 4.0;
}
static void squareStep(Grid<double>& heights, int size, double variation) {
int stride = size * 2;
for (int row = size; row < heights.numRows(); row += stride) {
for (int col = 0; col < heights.numCols(); col += stride) {
heights[row][col] = squareStepAverage(heights, size, row, col) +
randomReal(-variation, variation);
}
}
for (int row = 0; row < heights.numRows(); row += stride) {
for (int col = size; col < heights.numCols(); col += stride) {
heights[row][col] = squareStepAverage(heights, size, row, col) +
randomReal(-variation, variation);
}
}
}
static double squareStepAverage(Grid<double>& heights, int size,
int row, int col) {
double sum = 0.0;
int count = 0;
if (row - size >= 0) {
sum += heights[row - size][col];
count++;
}
if (row + size < heights.numRows()) {
sum += heights[row + size][col];
count++;
}
if (col - size >= 0) {
sum += heights[row][col - size];
count++;
}
if (col + size < heights.numCols()) {
sum += heights[row][col + size];
count++;
}
return sum / count;
}
static Grid<double> createGaussianKernel() {
Grid<double> result(kWindowSize, kWindowSize);
for (int i = 0; i < kWindowSize; i++) {
for (int j = 0; j < kWindowSize; j++) {
result[i][j] = exp(-(pow(i - kWindowSize / 2.0, 2.0) +
pow(j - kWindowSize / 2.0, 2.0)) /
(2 * kSigma * kSigma)) /
sqrt(2 * kPi * kSigma);
}
}
return result;
}
static void smoothTerrain(Grid<double>& terrain) {
Grid<double> kernel = createGaussianKernel();
Grid<double> result(terrain.numRows(), terrain.numCols());
for (int i = 0; i < terrain.numRows(); i++) {
for (int j = 0; j < terrain.numCols(); j++) {
double totalWeightUsed = 0.0;
for (int a = 0; a < kernel.numRows(); a++) {
for (int b = 0; b < kernel.numCols(); b++) {
int sampleRow = i + a - kernel.numRows() / 2;
int sampleCol = j + b - kernel.numRows() / 2;
if (!terrain.inBounds(sampleRow, sampleCol)) continue;
totalWeightUsed += kernel[a][b];
result[i][j] += kernel[a][b] * terrain[sampleRow][sampleCol];
}
}
result[i][j] /= totalWeightUsed;
}
}
terrain = result;
}
static Grid<double> wallsToGrid(Set<Edge>& walls, int numRows, int numCols) {
Grid<double> result(2 * numRows - 1, 2 * numCols - 1);
for (int i = 0; i < result.numRows(); i++) {
for (int j = 0; j < result.numCols(); j++) {
result[i][j] = kMazeWall;
}
}
for (int i = 0; i < numRows; i++) {
for (int j = 0; j < numCols; j++) {
result[2 * i][2 * j] = kMazeFloor;
}
}
foreach (Edge wall in walls) {
if (!result.inBounds(wall.start.row, wall.start.col) ||
!result.inBounds(wall.end.row, wall.end.col)) {
error("Edge endpoints are out of range.");
}
int row = 2 * wall.start.row + (wall.end.row - wall.start.row);
int col = 2 * wall.start.col + (wall.end.col - wall.start.col);
result[row][col] = kMazeFloor;
}
return result;
}