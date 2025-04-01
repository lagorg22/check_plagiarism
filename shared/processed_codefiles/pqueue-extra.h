using namespace std;
struct Cell {
Cell * parent, * sibling, * child;
int degree;
string key;
};
class ExtraPriorityQueue {
public:
ExtraPriorityQueue();
~ExtraPriorityQueue();
int size();
bool isEmpty();
void enqueue(string value);
string peek();
string dequeueMin();
private:
Cell * head;
int count;
void binomialLink(Cell * & binomialTreeY, Cell * & binomialTreeZ);
Cell * binomialHeapMerge(Cell * & bHx, Cell * & bHy);
Cell * binomialHeapUnion(Cell * & bHx, Cell * & bHy);
};