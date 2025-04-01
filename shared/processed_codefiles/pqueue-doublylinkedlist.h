using namespace std;
class DoublyLinkedListPriorityQueue {
public:
DoublyLinkedListPriorityQueue();
~DoublyLinkedListPriorityQueue();
int size();
bool isEmpty();
void enqueue(string value);
string peek();
string dequeueMin();
private:
struct Cell {
string value;
Cell *next;
Cell *prev;
};
Cell *head;
int count;
};