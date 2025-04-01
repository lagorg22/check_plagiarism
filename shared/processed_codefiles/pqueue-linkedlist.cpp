using namespace std;
LinkedListPriorityQueue::LinkedListPriorityQueue() {
head = NULL;
count = 0;
}
LinkedListPriorityQueue::~LinkedListPriorityQueue() {
Cell *cp = head;
while (cp != NULL) {
Cell *oldCp = cp;
cp = cp->link;
delete oldCp;
}
}
int LinkedListPriorityQueue::size() {
return count;
}
bool LinkedListPriorityQueue::isEmpty() {
return count == 0;
}
void LinkedListPriorityQueue::enqueue(string value) {
Cell *cp = new Cell;
cp->value = value;
cp->link = NULL;
Cell **cpp = &head;
while ((*cpp) != NULL && (*cpp)->value < value) {
cpp = &((*cpp)->link);
}
cp->link = *cpp;
*cpp = cp;
count++;
}
string LinkedListPriorityQueue::peek() {
if (isEmpty()) error("peek: Attempting to peek at an empty queue");
return head->value;
}
string LinkedListPriorityQueue::dequeueMin() {
if (isEmpty()) error("dequeueMin: Attempting to dequeue at an empty queue");
Cell *cp = head;
head = head->link;
string value = cp->value;
delete cp;
count--;
return value;
}