Vector<Loc>
shortestPath(Loc start,
Loc end,
Grid<double>& world,
double costFn(Loc from, Loc to, Grid<double>& world),
double heuristic(Loc start, Loc end, Grid<double>& world));
Set<Edge> createMaze(int numRows, int numCols);
struct BookKeep {
double distance;
Loc parent;
Color color;
};
void
shortestPathUtility(Loc start,
Loc end,
Grid<double>& world,
double costFn(Loc from, Loc to, Grid<double>& world),
double heuristic(Loc start, Loc end, Grid<double>& world),
Grid<BookKeep>& bookKeepGrid);
static const Loc NIL = makeLoc(-1, -1);