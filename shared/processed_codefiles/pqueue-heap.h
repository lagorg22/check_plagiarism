using namespace std;
class HeapPriorityQueue {
public:
HeapPriorityQueue();
~HeapPriorityQueue();
int size();
bool isEmpty();
void enqueue(string value);
string peek();
string dequeueMin();
private:
static const int INITIAL_CAPACITY = 10;
void expandCapacity();
string *heap;
int count;
int capacity;
void bubbleDown(int index);
void bubbleUp(int index);
};