static long gTotalAllocs = 0;
static long gTotalFrees = 0;
void* Node::operator new (size_t bytesNeeded) {
++gTotalAllocs;
return ::operator new(bytesNeeded);
}
void	Node::operator delete(void* toDelete) {
++gTotalFrees;
return ::operator delete(toDelete);
}
long numAllocations() {
return gTotalAllocs;
}
long numDeallocations() {
return gTotalFrees;
}