using namespace std;
enum WorldType {
TERRAIN_WORLD,
MAZE_WORLD
};
enum WorldSize {
SMALL_WORLD, MEDIUM_WORLD, LARGE_WORLD, HUGE_WORLD
};
enum AlgorithmType {
DIJKSTRA, A_STAR
};
enum UIState {
FRESH, MARKED, DRAWN
};
struct State {
Grid<double> world;  // The world.
WorldType worldType; // The type of world.
UIState uiState;       // Which state we're in.
};
const int kMaxRows = 400;
const int kMaxCols = 400;
const string kNewWorldLabel("New World");
const string kRerunLabel("Rerun");
const string kClearLabel("Clear");
const string kQuitLabel("Quit");
const string kRandomTerrainLabel("Random Terrain		");
const string kRandomMazeLabel("Random Maze		 ");
const string kLoadWorldLabel("Load World");
const string kSmallWorldLabel("Small World		 ");
const string kMediumWorldLabel("Medium World		");
const string kLargeWorldLabel("Large World		 ");
const string kHugeWorldLabel("Huge World       ");
const string kDijkstraLabel("Dijkstra's Algorithm			");
const string kAStarLabel("A* Search	 ");
const string kSelectedLocationColor("RED");
const string kPathColor("RED");
const string kBackgroundColor("Black");
const int kDisplayWidth = 600;
const int kDisplayHeight = 600;
const int kTerrainNumRows[] = { 33, 65, 129, 257 };
const int kTerrainNumCols[] = { 33, 65, 129, 257 };
const int kMazeNumRows[] = { 10, 30, 80, 160 };
const int kMazeNumCols[] = { 10, 30, 80, 160 };
const int kMargin = 5;
const int kWidthAdjustment = 0;
const int kHeightAdjustment = 75;
const int kColorMultipliers[3][3] = {
{ 255, 255, 255 },
{ 255, 255, 0 },
{ 0, 255, 0 }
};
static void removeOverlays();
static void removeMarkedSquares();
static void locToCoord(Loc loc, double& x, double& y);
static string valueToColor(double value, Color locColor);
static void colorLocation(Loc loc, double value, Color locColor);
static void removeAndDelete(GObject* object);
static Loc coordToLoc(double x, double y);
static GRect* makeSelectionRectangle(Loc loc, string color);
static void findMidpoint(Loc loc, double& xc, double& yc);
static WorldSize getWorldSize(string sizeLabel);
static double runShortestPath(Grid<double>& world,
WorldType worldType,
Loc start, Loc end);
static
Vector<Loc> invoke(Vector<Loc> pathFn(Loc start,
Loc end,
Grid<double>& world,
double costFn(Loc, Loc, Grid<double>&)),
Loc start,
Loc end,
Grid<double>& world,
double costFn(Loc from, Loc to, Grid<double>& world),
double heuristicFn(Loc from, Loc to, Grid<double>& world));
static
Vector<Loc> invoke(Vector<Loc> pathFn(Loc start,
Loc end,
Grid<double>& world,
double costFn(Loc, Loc, Grid<double>&),
double heuristicFn(Loc, Loc, Grid<double>&)),
Loc start,
Loc end,
Grid<double>& world,
double costFn(Loc from, Loc to, Grid<double>& world),
double heuristicFn(Loc from, Loc to, Grid<double>& world));
static GWindow* gWindow = NULL;
static GChooser* gTypeList = NULL;
static GChooser* gSizeList = NULL;
static GChooser* gAlgorithmList = NULL;
static double gPixelsPerWidth;
static double gPixelsPerHeight;
static GRect* gFirstSelected = NULL;
static GRect* gSecondSelected = NULL;
static Loc gStartLocation;
static Loc gEndLocation;
static Vector<GLine*> gHighlightedPath;
static Grid<bool> gMarked;
static Grid<double> gMarkedValues;
static void fillRect(int x, int y, int width, int height, string color) {
gWindow->setColor(color);
gWindow->fillRect(x, y, width, height);
}
static void drawWorld(Grid<double>& world) {
if (gWindow == NULL) error("Cannot draw world before window is set up.");
removeMarkedSquares();
removeOverlays();
gPixelsPerWidth = (double) kDisplayWidth / world.numCols();
gPixelsPerHeight = (double) kDisplayHeight / world.numRows();
fillRect(0, 0, kDisplayWidth + 2 * kMargin, kDisplayHeight + 2 * kMargin,
kBackgroundColor);
gMarked.resize(world.numRows(), world.numCols());
gMarkedValues = world;
for (int row = 0; row < world.numRows(); row++) {
for (int col = 0; col < world.numCols(); col++) {
Loc loc = { row, col };
double x, y;
locToCoord(loc, x, y);
fillRect(x, y, gPixelsPerWidth, gPixelsPerHeight,
valueToColor(world[row][col], GRAY));
}
}
gWindow->repaint();
}
static void uncolorSquares() {
for (int row = 0; row < gMarked.numRows(); row++) {
for (int col = 0; col < gMarked.numCols(); col++) {
if (gMarked[row][col]) {
Loc loc = { row, col };
colorLocation(loc, gMarkedValues[row][col], GRAY);
gMarked[row][col] = false;
}
}
}
}
static void removeMarkedSquares() {
removeAndDelete(gFirstSelected);
removeAndDelete(gSecondSelected);
gFirstSelected = gSecondSelected = NULL;
}
static void removeOverlays() {
for (int i = 0; i < gHighlightedPath.size(); i++) {
removeAndDelete(gHighlightedPath[i]);
}
gHighlightedPath.clear();
}
static void restoreWorldDisplay() {
if (gWindow == NULL)
error("Window has not yet been initialized.");
uncolorSquares();
removeMarkedSquares();
removeOverlays();
gWindow->repaint();
}
static bool registerClick(Grid<double>& world, double x, double y,
WorldType worldType) {
if (gWindow == NULL)
error("Window has not yet been initialized.");
if (gFirstSelected != NULL && gSecondSelected != NULL)
error("Two tiles have already been selected.");
Loc loc = coordToLoc(x, y);
if (!world.inBounds(loc.row, loc.col) ||
(worldType == MAZE_WORLD && world[loc.row][loc.col] == kMazeWall)) {
return false;
}
GRect* selection = makeSelectionRectangle(loc, kSelectedLocationColor);
gWindow->add(selection);
if (gFirstSelected == NULL) {
gFirstSelected = selection;
gStartLocation = loc;
} else {
gSecondSelected = selection;
gEndLocation = loc;
}
return true;
}
void colorCell(Grid<double>& world, Loc loc, Color locColor) {
colorLocation(loc, world[loc.row][loc.col], locColor);
gMarked[loc.row][loc.col] = true;
}
static void highlightConnection(Loc from, Loc to) {
double srcX, srcY, dstX, dstY;
findMidpoint(from, srcX, srcY);
findMidpoint(to, dstX, dstY);
GLine* connection = new GLine(srcX, srcY, dstX, dstY);
connection->setColor(kPathColor);
connection->setLineWidth(3.0);
gWindow->add(connection);
gHighlightedPath.add(connection);
}
static void initializeWindow() {
int windowWidth = kDisplayWidth + 2 * kMargin + kWidthAdjustment;
int windowHeight = kDisplayHeight + 2 * kMargin + kHeightAdjustment;
gWindow = new GWindow(windowWidth, windowHeight);
gWindow->setWindowTitle("Trailblazer");
pause(500);
gTypeList = new GChooser();
gTypeList->addItem(kRandomTerrainLabel);
gTypeList->addItem(kRandomMazeLabel);
gTypeList->setSelectedItem(kRandomTerrainLabel);
gWindow->addToRegion(gTypeList, "SOUTH");
gSizeList = new GChooser();
gSizeList->addItem(kSmallWorldLabel);
gSizeList->addItem(kMediumWorldLabel);
gSizeList->addItem(kLargeWorldLabel);
gSizeList->addItem(kHugeWorldLabel);
gSizeList->setSelectedItem(kMediumWorldLabel);
gWindow->addToRegion(gSizeList, "SOUTH");
gAlgorithmList = new GChooser();
gAlgorithmList->addItem(kDijkstraLabel);
gAlgorithmList->addItem(kAStarLabel);
gWindow->addToRegion(gAlgorithmList, "NORTH");
gWindow->addToRegion(new GButton(kNewWorldLabel), "SOUTH");
gWindow->addToRegion(new GButton(kLoadWorldLabel), "SOUTH");
gWindow->addToRegion(new GButton(kRerunLabel), "NORTH");
gWindow->addToRegion(new GButton(kClearLabel), "NORTH");
gWindow->addToRegion(new GButton(kQuitLabel), "NORTH");
pause(500);
}
static bool regenerateWorld(Grid<double>& world, WorldType& worldType) {
string typeLabel = gTypeList->getSelectedItem();
WorldSize worldSize = getWorldSize(gSizeList->getSelectedItem());
Grid<double> newWorld;
WorldType newType;
if (typeLabel == kRandomTerrainLabel) {
int numRows = kTerrainNumRows[worldSize];
int numCols = kTerrainNumCols[worldSize];
newWorld = generateRandomTerrain(numRows, numCols);
newType = TERRAIN_WORLD;
} else if (typeLabel == kRandomMazeLabel) {
int numRows = kMazeNumRows[worldSize];
int numCols = kMazeNumCols[worldSize];
try {
newWorld = generateRandomMaze(numRows / 2 + 1, numCols / 2 + 1);
newType = MAZE_WORLD;
} catch (const ErrorException& e) {
cout << e.what() << endl;
return false;
}
} else {
error("Invalid world type provided.");
}
world = newWorld;
worldType = newType;
return true;
}
static WorldSize getWorldSize(string sizeLabel) {
if (sizeLabel == kSmallWorldLabel) {
return SMALL_WORLD;
} else if (sizeLabel == kMediumWorldLabel) {
return MEDIUM_WORLD;
} else if (sizeLabel == kLargeWorldLabel) {
return LARGE_WORLD;
} else if (sizeLabel == kHugeWorldLabel) {
return HUGE_WORLD;
} else {
error("Invalid world size provided.");
}
}
static AlgorithmType getAlgorithmType() {
if (gWindow == NULL) error("Window has not yet been initialized.");
string algorithmLabel = gAlgorithmList->getSelectedItem();
if (algorithmLabel == kDijkstraLabel) {
return DIJKSTRA;
} else if (algorithmLabel == kAStarLabel) {
return A_STAR;
} else {
error("Invalid algorithm provided.");
}
}
static string valueToColor(double value, Color locColor) {
if (locColor != GRAY) {
value = 0.8 * value + 0.2;
}
stringstream hexValue;
hexValue << "#" << hex << setfill('0');
for (int i = 0; i < 3; i++) {
int intensity = int(value * kColorMultipliers[locColor][i]);
hexValue << setw(2) << intensity;
}
return hexValue.str();
}
static void removeAndDelete(GObject* object) {
if (object != NULL) {
gWindow->remove(object);
delete object;
}
}
static Loc coordToLoc(double x, double y) {
Loc loc;
loc.row = (int) ((y - kMargin) / gPixelsPerHeight);
loc.col = (int) ((x - kMargin) / gPixelsPerWidth);
return loc;
}
static void locToCoord(Loc loc, double& x, double& y) {
x = loc.col * gPixelsPerWidth + kMargin;
y = loc.row * gPixelsPerHeight + kMargin;
}
static GRect* makeSelectionRectangle(Loc loc, string color) {
double x, y;
locToCoord(loc, x, y);
GRect* selection = new GRect(x, y, gPixelsPerWidth, gPixelsPerHeight);
selection->setLineWidth(2.0);
selection->setColor(color);
return selection;
}
static void colorLocation(Loc loc, double value, Color locColor) {
double x, y;
locToCoord(loc, x, y);
fillRect(x, y, gPixelsPerWidth, gPixelsPerHeight,
valueToColor(value, locColor));
}
static void findMidpoint(Loc loc, double& xc, double& yc) {
locToCoord(loc, xc, yc);
xc += gPixelsPerWidth / 2;
yc += gPixelsPerHeight / 2;
}
static bool readWorldFile(ifstream& input, Grid<double>& world,
WorldType& worldType) try {
input.exceptions(ios::failbit | ios::badbit);
string type;
input >> type;
if (type == "terrain") {
worldType = TERRAIN_WORLD;
} else if (type == "maze") {
worldType = MAZE_WORLD;
} else return false;
int numRows, numCols;
input >> numRows >> numCols;
if (numRows <= 0 || numCols <= 0 ||
numRows >= kMaxRows || numRows >= kMaxCols) {
return false;
}
world.resize(numRows, numCols);
for (int row = 0; row < numRows; row++) {
for (int col = 0; col < numCols; col++) {
double value;
input >> value;
if (worldType == MAZE_WORLD) {
if (value != kMazeWall && value != kMazeFloor) {
return false;
}
} else  {
if (value < 0.0 || value > 1.0) {
return false;
}
}
world[row][col] = value;
}
}
return true;
} catch (...) {
return false;
}
static bool tryLoadWorld(Grid<double>& world, WorldType& worldType) {
ifstream input;
string filename = promptUserForFile(input, "Choose world file: ");
Grid<double> newWorld;
WorldType newWorldType;
if (!readWorldFile(input, newWorld, newWorldType)) {
cout << filename << " is not a world file." << endl;
return false;
}
world = newWorld;
worldType = newWorldType;
return true;
}
static void initializeState(State& state) {
if (!regenerateWorld(state.world, state.worldType)) {
error("Cannot set up initial world properly!");
}
state.uiState = FRESH;
}
static void runSearch(State& state) {
try {
double pathCost = runShortestPath(state.world,
state.worldType,
gStartLocation,
gEndLocation);
cout << "Path cost: " << pathCost << endl;
} catch (const ErrorException& e) {
cout << e.what() << endl;
}
}
static void processMouseEvent(State& state, GMouseEvent e) {
switch (state.uiState) {
case DRAWN:
restoreWorldDisplay();
state.uiState = FRESH;
case FRESH:
if (registerClick(state.world, e.getX(), e.getY(),
state.worldType)) {
state.uiState = MARKED;
}
break;
case MARKED:
if (registerClick(state.world, e.getX(), e.getY(),
state.worldType)) {
runSearch(state);
state.uiState = DRAWN;
}
}
}
static void processActionEvent(State& state, GActionEvent e) {
string cmd = e.getActionCommand();
if (cmd == kNewWorldLabel) {
if (regenerateWorld(state.world, state.worldType)) {
drawWorld(state.world);
state.uiState = FRESH;
}
}
else if (cmd == kLoadWorldLabel) {
if (tryLoadWorld(state.world, state.worldType)) {
drawWorld(state.world);
state.uiState = FRESH;
}
}
else if (cmd == kRerunLabel) {
if (state.uiState == DRAWN) {
uncolorSquares();
removeOverlays();
runSearch(state);
} else {
cout << "Cannot rerun a search; no search has been done." << endl;
}
}
else if (cmd == kClearLabel) {
restoreWorldDisplay();
state.uiState = FRESH;
}
else if (cmd == kQuitLabel) {
exitGraphics();
}
}
static void drawPath(Vector<Loc>& path) {
for (int i = 1; i < path.size(); i++) {
highlightConnection(path[i - 1], path[i]);
}
}
static double costOf(Vector<Loc>& path,
Grid<double>& world,
double costFn(Loc, Loc, Grid<double>&)) {
double result = 0.0;
for (int i = 1; i < path.size(); i++) {
result += costFn(path[i - 1], path[i], world);
}
return result;
}
static double runShortestPath(Grid<double>& world,
WorldType worldType,
Loc start, Loc end) {
AlgorithmType algType = getAlgorithmType();
Vector<Loc> path;
double (*costFn)(Loc, Loc, Grid<double>&);
double (*hFn)(Loc, Loc, Grid<double>&);
if (worldType == TERRAIN_WORLD) {
costFn = terrainCost;
hFn = terrainHeuristic;
} else if (worldType == MAZE_WORLD) {
costFn = mazeCost;
hFn = mazeHeuristic;
} else error("Unknown world type.");
path = invoke(shortestPath, start, end, world, costFn,
algType == A_STAR ? hFn : zeroHeuristic);
if (path.isEmpty()) {
cout << "Warning: Returned path is empty." << endl;
} else if (path[0] != start) {
cout << "Warning: Start of path is not the start location." << endl;
} else if (path[path.size() - 1] != end) {
cout << "Warning: End of path is not the end location." << endl;
}
drawPath(path);
return costOf(path, world, costFn);
}
static
Vector<Loc> invoke(Vector<Loc> pathFn(Loc start,
Loc end,
Grid<double>& world,
double costFn(Loc, Loc, Grid<double>&)),
Loc start,
Loc end,
Grid<double>& world,
double costFn(Loc from, Loc to, Grid<double>& world),
double heuristicFn(Loc from, Loc to, Grid<double>& world)) {
return pathFn(start, end, world, costFn);
}
static
Vector<Loc> invoke(Vector<Loc> pathFn(Loc start,
Loc end,
Grid<double>& world,
double costFn(Loc, Loc, Grid<double>&),
double heuristicFn(Loc, Loc, Grid<double>&)),
Loc start,
Loc end,
Grid<double>& world,
double costFn(Loc from, Loc to, Grid<double>& world),
double heuristicFn(Loc from, Loc to, Grid<double>& world)) {
return pathFn(start, end, world, costFn, heuristicFn);
}
int main() {
State state;
initializeWindow();
initializeState(state);
drawWorld(state.world);
while (true) {
GEvent e = waitForEvent(ACTION_EVENT | MOUSE_EVENT);
if (e.getEventType() == MOUSE_CLICKED) {
processMouseEvent(state, GMouseEvent(e));
} else if (e.getEventClass() == ACTION_EVENT) {
processActionEvent(state, GActionEvent(e));
}
}
}