typedef int ext_char;
const ext_char PSEUDO_EOF = 256;
const ext_char NOT_A_CHAR = 257;
struct Node {
ext_char character;
Node *zero;
Node *one;
int weight;
void* operator new	 (size_t bytesNeeded);
void	operator delete(void* toDelete);
};