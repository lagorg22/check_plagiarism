using namespace std;
class LinkedListPriorityQueue {
public:
LinkedListPriorityQueue();
~LinkedListPriorityQueue();
int size();
bool isEmpty();
void enqueue(string value);
string peek();
string dequeueMin();
private:
struct Cell {
string value;
Cell *link;
};
int count;
Cell *head;
};