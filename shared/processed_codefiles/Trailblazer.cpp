using namespace std;
Vector<Loc>
shortestPath(Loc start,
Loc end,
Grid<double>& world,
double costFn(Loc from, Loc to, Grid<double>& world),
double heuristic(Loc start, Loc end, Grid<double>& world)) {
Grid<BookKeep> bookKeepGrid(world.numRows(), world.numCols());
shortestPathUtility(start, end, world, costFn, heuristic, bookKeepGrid);
Vector<Loc> reversePath;
while (end != NIL) {
reversePath.push_back(end);
end = bookKeepGrid[end.row][end.col].parent;
}
Vector<Loc> path;
for (int i = reversePath.size() - 1; i >= 0; i--) {
path.push_back(reversePath[i]);
}
return path;
}
Set<Edge> createMaze(int numRows, int numCols) {
Set<Edge> edges;
for (int i = 0; i < numRows; i++) {
for (int j = 0; j < numCols; j++) {
Loc locFrom = makeLoc(i, j);
Loc locToRight = makeLoc(i, j + 1);
Loc locToDown = makeLoc(i + 1, j);
if( (locToRight.col >= 0) && (locToRight.col < numCols)
&& (locToRight.row >= 0) && (locToRight.row < numRows) ) {
edges.add(makeEdge(locFrom, locToRight));
}
if( (locToDown.col >= 0) && (locToDown.col < numCols)
&& (locToDown.row >= 0) && (locToDown.row < numRows) ) {
edges.add(makeEdge(locFrom, locToDown));
}
}
}
Set<Edge> spanningTree;
UnionFind nodes(numRows * numCols);
TrailblazerPQueue<Edge> pq;
foreach (Edge edge in edges) {
pq.enqueue(edge, randomInteger(0, 10));
}
Edge edge;
while (nodes.components() > 1) {
edge = pq.dequeueMin();
int startIndex = edge.start.row * numRows + edge.start.col;
int endIndex = edge.end.row * numRows + edge.end.col;
if (!nodes.connected(startIndex, endIndex)) {
nodes.connect(startIndex, endIndex);
spanningTree.add(edge);
}
}
return spanningTree;
}
void
shortestPathUtility(Loc start,
Loc end,
Grid<double>& world,
double costFn(Loc from, Loc to, Grid<double>& world),
double heuristic(Loc start, Loc end, Grid<double>& world),
Grid<BookKeep>& bookKeepGrid) {
for (int i = 0; i < bookKeepGrid.numRows(); i++) {
for (int j = 0; j < bookKeepGrid.numCols(); j++) {
bookKeepGrid[i][j].color = GRAY;
bookKeepGrid[i][j].distance = numeric_limits<double>::infinity();
bookKeepGrid[i][j].parent = NIL;
}
}
bookKeepGrid[start.row][start.col].color = YELLOW;
bookKeepGrid[start.row][start.col].distance = heuristic(start, end, world);
TrailblazerPQueue<Loc> pq;
pq.enqueue(start, 0);
Loc u = start;
while (true) {
u = pq.dequeueMin();
bookKeepGrid[u.row][u.col].color = GREEN;
colorCell(world, u, GREEN);
if (u == end) return;
for (int i = -1; i <= 1; i++) {
for (int j = -1; j <= 1; j++) {
Loc v = makeLoc(u.row + i, u.col + j);
if (world.inBounds(v.row, v.col) && v != u) {
if (bookKeepGrid[v.row][v.col].color == GRAY) {
bookKeepGrid[v.row][v.col].color = YELLOW;
colorCell(world, v, YELLOW);
bookKeepGrid[v.row][v.col].distance =
bookKeepGrid[v.row][v.col].distance +
costFn(u, v, world);
bookKeepGrid[v.row][v.col].parent = u;
pq.enqueue(v,
bookKeepGrid[v.row][v.col].distance +
costFn(u, v, world) + heuristic(v, end, world)
);
}
if ((bookKeepGrid[v.row][v.col].color == YELLOW) &&
(bookKeepGrid[v.row][v.col].distance >
costFn(u, v, world) + bookKeepGrid[u.row][u.col].distance)) {
bookKeepGrid[v.row][v.col].distance =
costFn(u, v, world) + bookKeepGrid[u.row][u.col].distance;
bookKeepGrid[v.row][v.col].parent = u;
pq.decreaseKey(v,
costFn(u, v, world) +
bookKeepGrid[u.row][u.col].distance +
heuristic(v, end, world)
);
}
}
}
}
}
}