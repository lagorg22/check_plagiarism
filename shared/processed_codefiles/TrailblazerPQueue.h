template <typename ElemType>
class TrailblazerPQueue {
public:
void enqueue(ElemType elem, double priority);
ElemType dequeueMin();
void decreaseKey(ElemType elem, double newPriority);
bool isEmpty();
int size();
private:
std::multimap<double, ElemType> priorityQueue;
std::map<ElemType, double> elemToPriority;
bool equal(ElemType one, ElemType two) {
return !(one < two || two < one);
}
};
template <typename ElemType>
void TrailblazerPQueue<ElemType>::enqueue(ElemType elem, double priority) {
if (!(priority == priority)) {
error("Attempted to use NaN as a priority.");
}
if (elemToPriority.insert(std::make_pair(elem, priority)).second == false) {
error("Duplicate element in priority queue.");
}
priorityQueue.insert(std::make_pair(priority, elem));
}
template <typename ElemType>
bool TrailblazerPQueue<ElemType>::isEmpty() {
return priorityQueue.empty();
}
template <typename ElemType>
int TrailblazerPQueue<ElemType>::size() {
return int(priorityQueue.size());
}
template <typename ElemType>
ElemType TrailblazerPQueue<ElemType>::dequeueMin() {
if (isEmpty()) {
error("Attempted to dequeue from an empty priority queue.");
}
typename std::multimap<double, ElemType>::iterator toRemove =
priorityQueue.begin();
ElemType result = toRemove->second;
priorityQueue.erase(toRemove);
if (!elemToPriority.erase(result)) {
error("Could not remove element from inverse mapping, because it's not there.");
}
return result;
}
template <typename ElemType>
void TrailblazerPQueue<ElemType>::decreaseKey(ElemType elem, double newPriority) {
if (!(newPriority == newPriority)) {
error("Attempted to use NaN as a priority.");
}
typename std::map<ElemType, double>::iterator itr = elemToPriority.find(elem);
if (itr == elemToPriority.end()) {
error("Cannot call decrease-key on an element not in the priority queue.");
}
if (newPriority > itr->second) {
error("Cannot use decrease-key to increase a key.");
}
typedef typename std::multimap<double, ElemType>::iterator Iterator;
Iterator pItr = priorityQueue.find(itr->second);
while (!equal(pItr->second, elem)) {
pItr++;
}
priorityQueue.erase(pItr);
priorityQueue.insert(std::make_pair(newPriority, elem));
itr->second = newPriority;
}