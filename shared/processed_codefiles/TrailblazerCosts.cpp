using namespace std;
const double kAltitudePenalty = 100;
double terrainCost(Loc from, Loc to, Grid<double>& world) {
if (from == to) return 0.0;
int drow = abs(to.row - from.row);
int dcol = abs(to.col - from.col);
if (drow > 1 || dcol > 1) {
error("Non-adjacent locations passed into cost function.");
}
double distance = sqrt(double(drow * drow + dcol * dcol));
double dheight = fabs(world[to.row][to.col] - world[from.row][from.col]);
return distance + kAltitudePenalty * dheight;
}
double terrainHeuristic(Loc from, Loc to, Grid<double>& world) {
int drow = to.row - from.row;
int dcol = to.col - from.col;
double dheight = fabs(world[to.row][to.col] - world[from.row][from.col]);
return sqrt((double) (drow * drow + dcol * dcol)) + kAltitudePenalty * dheight;
}
double mazeCost(Loc from, Loc to, Grid<double>& world) {
if (from == to) return 0.0;
int drow = abs(to.row - from.row);
int dcol = abs(to.col - from.col);
if (drow > 1 || dcol > 1) {
error("Non-adjacent locations passed into cost function.");
}
if (drow == 1 && dcol == 1)
return numeric_limits<double>::infinity();
if (world[from.row][from.col] == kMazeWall || world[to.row][to.col] == kMazeWall)
return numeric_limits<double>::infinity();
return 1.0;
}
double mazeHeuristic(Loc from, Loc to, Grid<double>& world) {
return abs(from.row - to.row) + abs(from.col - to.col);
}
double zeroHeuristic(Loc, Loc, Grid<double>&) {
return 0.0;
}