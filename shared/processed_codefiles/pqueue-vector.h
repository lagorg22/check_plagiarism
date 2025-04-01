class VectorPriorityQueue {
public:
VectorPriorityQueue();
~VectorPriorityQueue();
int size();
bool isEmpty();
void enqueue(std::string value);
std::string peek();
std::string dequeueMin();
private:
std::vector<std::string> priorityQueue;
};