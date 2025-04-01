using namespace std;
void docheckCondition(bool expr, string reason, string expression, int lineNumber) {
if (expr) {
cout << "  PASS: " << reason << endl;
} else {
cout << "! FAIL: " << reason << endl;
cout << "     Test failed on line " << lineNumber << " of pqueue-test.cpp" << endl;
cout << "     Specific expression: " << expression << endl;
getLine("     Press ENTER to continue...");
}
}
void beginTest(string testName) {
cout << "================== BEGIN: " << testName << "==================" << endl;
}
void endTest(string testName) {
cout << "=================== END: " << testName << "===================" << endl;
getLine("Press ENTER to continue...");
}
void logInfo(string message) {
cout << "  info: " << message << endl;
}
string randomString(int length = 16) {
string result;
for (int i = 0; i < length; i++) {
result += char(randomInteger('A', 'Z'));
}
return result;
}
template <typename PQueue>
void basicStructuralTests() {
beginTest("Basic Structural Tests");
try {
{
logInfo("These tests will check size() isEmpty() without calling dequeueMin().");
PQueue queue;
checkCondition(queue.isEmpty(), "New priority queue should be empty.");
checkCondition(queue.size() == 0, "New priority queue should have size 0.");
for (int i = 0; i < 5; i++) {
queue.enqueue("Test String");
checkCondition(queue.size() == i + 1, "Queue should have proper size after inserting a value.");
checkCondition(!queue.isEmpty(), "Queue containing elements should not be empty.");
}
}
{
logInfo("We're about to start calling dequeueMin().");
PQueue queue;
for (int i = 0; i < 5; i++) {
queue.enqueue("Test String");
}
for (int i = 5; i > 0; i--) {
checkCondition(queue.size() == i, "Queue should have proper size after dequeues.");
checkCondition(!queue.isEmpty(), "Queue should not be empty before all elements are removed.");
queue.dequeueMin();
}
checkCondition(queue.size() == 0, "After removing all elements, the queue should have size 0.");
checkCondition(queue.isEmpty(), "After removing all elements, the queue should be empty.");
}
{
logInfo("This next test will check whether peek() matches dequeueMin().");
PQueue queue;
for (int i = 0; i < 5; i++) {
queue.enqueue(randomString());
}
while (!queue.isEmpty()) {
string expected = queue.peek();
checkCondition(queue.dequeueMin() == expected, "Value returned by peek() matches value returned by dequeueMin()");
}
}
{
PQueue queue;
bool didThrow = false;
try {
logInfo("About to peek into an empty queue.  This may cause a crash");
logInfo("if your implementation is incorrect.");
queue.peek();
} catch (ErrorException&) {
didThrow = true;
}
checkCondition(didThrow, "Priority queue uses 'error' when peek() called on empty queue.");
}
{
PQueue queue;
bool didThrow = false;
try {
logInfo("About to dequeue from an empty queue.  This may cause a crash");
logInfo("if your implementation is incorrect.");
queue.dequeueMin();
} catch (ErrorException&) {
didThrow = true;
}
checkCondition(didThrow, "Priority queue uses 'error' when dequeueMin() called on empty queue.");
}
} catch (ErrorException& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.getMessage() << endl;
} catch (exception& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.what() << endl;
} catch (...) {
cout << "TEST FAILURE: Unknown exception." << endl;
}
endTest("Basic Structural Tests");
}
template <typename PQueue>
void sortAscendingTests() {
beginTest("Sort Ascending Tests");
try {
{
logInfo("Enqueuing A - H into the queue and confirming it comes back sorted.");
PQueue queue;
for (char ch = 'A'; ch <= 'H'; ch++) {
queue.enqueue(string(1, ch));
}
for (char ch = 'A'; ch <= 'H'; ch++) {
string expected(1, ch);
checkCondition(queue.dequeueMin() == expected, "Queue should yield " + expected + ".");
}
}
{
logInfo("Enqueuing ten sorted random strings and confirming it comes back sorted.");
Vector<string> randomValues;
for (int i = 0; i < 10; i++) {
randomValues += randomString();
}
sort(randomValues.begin(), randomValues.end());
PQueue queue;
foreach (string value in randomValues)
queue.enqueue(value);
for (int i = 0; i < randomValues.size(); i++) {
checkCondition(queue.dequeueMin() == randomValues[i],
"Expecting to get value " + randomValues[i] + " from queue.");
}
}
{
logInfo("Generating 10000 random strings.");
Vector<string> randomValues;
for (int i = 0; i < 10000; i++) {
randomValues += randomString();
}
logInfo("Sorting 10000 random strings.");
sort(randomValues.begin(), randomValues.end());
logInfo("Enqueuing 10000 random strings.");
PQueue queue;
foreach (string value in randomValues)
queue.enqueue(value);
logInfo("Dequeuing 10000 random strings.");
bool isCorrect = true;
for (int i = 0; i < randomValues.size(); i++) {
if (queue.dequeueMin() != randomValues[i]) {
isCorrect = false;
break;
}
}
checkCondition(isCorrect, "Queue correctly sorted 10000 random strings.");
}
} catch (ErrorException& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.getMessage() << endl;
} catch (exception& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.what() << endl;
} catch (...) {
cout << "TEST FAILURE: Unknown exception." << endl;
}
endTest("Sort Ascending Tests");
}
template <typename PQueue>
void sortDescendingTests() {
beginTest("Sort Descending Tests");
try {
{
logInfo("Enqueuing A - H in reverse order and checking that it comes back sorted.");
PQueue queue;
for (char ch = 'H'; ch >= 'A'; ch--) {
queue.enqueue(string(1, ch));
}
for (char ch = 'A'; ch <= 'H'; ch++) {
string expected(1, ch);
checkCondition(queue.dequeueMin() == expected, "Queue should yield " + expected + ".");
}
}
{
logInfo("Enqueuing ten reverse sorted random strings and confirming it comes back sorted.");
Vector<string> randomValues;
for (int i = 0; i < 10; i++) {
randomValues += randomString();
}
sort(randomValues.begin(), randomValues.end(), greater<string>());
PQueue queue;
foreach (string value in randomValues)
queue.enqueue(value);
reverse(randomValues.begin(), randomValues.end());
for (int i = 0; i < randomValues.size(); i++) {
checkCondition(queue.dequeueMin() == randomValues[i],
"Expecting to get value " + randomValues[i] + " from queue.");
}
}
{
logInfo("Generating 10000 random strings.");
Vector<string> randomValues;
for (int i = 0; i < 10000; i++) {
randomValues += randomString();
}
logInfo("Sorting 10000 random strings.");
sort(randomValues.begin(), randomValues.end(), greater<string>());
logInfo("Enqueuing 10000 random strings.");
PQueue queue;
foreach (string value in randomValues)
queue.enqueue(value);
logInfo("Dequeuing 10000 random strings.");
bool isCorrect = true;
reverse(randomValues.begin(), randomValues.end());
for (int i = 0; i < randomValues.size(); i++) {
if (queue.dequeueMin() != randomValues[i]) {
isCorrect = false;
break;
}
}
checkCondition(isCorrect, "Queue correctly sorted 10000 random strings.");
}
} catch (ErrorException& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.getMessage() << endl;
} catch (exception& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.what() << endl;
} catch (...) {
cout << "TEST FAILURE: Unknown exception." << endl;
}
endTest("Sort Descending Tests");
}
template <typename PQueue>
void sortRandomTests() {
beginTest("Sort Random Tests");
try {
{
logInfo("Enqueuing a random permutation of A - H and checking whether it leaves sorted.");
Vector<string> letters;
for (char ch = 'A'; ch <= 'H'; ch++) {
letters += string(1, ch);
}
random_shuffle(letters.begin(), letters.end());
PQueue queue;
foreach (string letter in letters)
queue.enqueue(letter);
for (char ch = 'A'; ch <= 'H'; ch++) {
string expected(1, ch);
checkCondition(queue.dequeueMin() == expected, "Queue should yield " + expected + ".");
}
}
{
logInfo("Enqueuing 10 random strings and checking whether it leaves sorted.");
Vector<string> randomValues;
for (int i = 0; i < 10; i++) {
randomValues += randomString();
}
PQueue queue;
foreach (string value in randomValues)
queue.enqueue(value);
sort(randomValues.begin(), randomValues.end());
for (int i = 0; i < randomValues.size(); i++) {
checkCondition(queue.dequeueMin() == randomValues[i],
"Expecting to get value " + randomValues[i] + " from queue.");
}
}
{
logInfo("Generating 10000 random strings.");
Vector<string> randomValues;
for (int i = 0; i < 10000; i++) {
randomValues += randomString();
}
logInfo("Enqueuing 10000 random strings.");
PQueue queue;
foreach (string value in randomValues)
queue.enqueue(value);
logInfo("Sorting 10000 random strings.");
sort(randomValues.begin(), randomValues.end(), greater<string>());
logInfo("Dequeuing 10000 random strings.");
bool isCorrect = true;
reverse(randomValues.begin(), randomValues.end());
for (int i = 0; i < randomValues.size(); i++) {
if (queue.dequeueMin() != randomValues[i]) {
isCorrect = false;
break;
}
}
checkCondition(isCorrect, "Queue correctly sorted 10000 random strings.");
}
} catch (ErrorException& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.getMessage() << endl;
} catch (exception& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.what() << endl;
} catch (...) {
cout << "TEST FAILURE: Unknown exception." << endl;
}
endTest("Sort Random Tests");
}
template <typename PQueue>
void sortCraftedTests() {
beginTest("Sort Crafted Tests");
try {
{
logInfo("Sorting two sequences that need to be interleaved.");
Vector<string> sequence;
sequence += string(1, 'A');
sequence += string(1, 'C');
sequence += string(1, 'E');
sequence += string(1, 'G');
sequence += string(1, 'B');
sequence += string(1, 'D');
sequence += string(1, 'F');
sequence += string(1, 'H');
PQueue queue;
foreach (string letter in sequence) {
queue.enqueue(letter);
}
for (char ch = 'A'; ch <= 'H'; ch++) {
string expected(1, ch);
checkCondition(queue.dequeueMin() == expected, "Queue should yield " + expected + ".");
}
}
{
logInfo("Sorting two sequences that need to be interleaved, version two.");
Vector<string> sequence;
sequence += string(1, 'B');
sequence += string(1, 'D');
sequence += string(1, 'F');
sequence += string(1, 'H');
sequence += string(1, 'A');
sequence += string(1, 'C');
sequence += string(1, 'E');
sequence += string(1, 'G');
PQueue queue;
foreach (string letter in sequence) {
queue.enqueue(letter);
}
for (char ch = 'A'; ch <= 'H'; ch++) {
string expected(1, ch);
checkCondition(queue.dequeueMin() == expected, "Queue should yield " + expected + ".");
}
}
{
logInfo("Sorting two decreasing sequences that need to be interleaved.");
Vector<string> sequence;
sequence += string(1, 'H');
sequence += string(1, 'F');
sequence += string(1, 'D');
sequence += string(1, 'B');
sequence += string(1, 'G');
sequence += string(1, 'E');
sequence += string(1, 'C');
sequence += string(1, 'A');
PQueue queue;
foreach (string letter in sequence) {
queue.enqueue(letter);
}
for (char ch = 'A'; ch <= 'H'; ch++) {
string expected(1, ch);
checkCondition(queue.dequeueMin() == expected, "Queue should yield " + expected + ".");
}
}
{
logInfo("Sorting two decreasing sequences that need to be interleaved, version 2.");
Vector<string> sequence;
sequence += string(1, 'G');
sequence += string(1, 'E');
sequence += string(1, 'C');
sequence += string(1, 'A');
sequence += string(1, 'H');
sequence += string(1, 'F');
sequence += string(1, 'D');
sequence += string(1, 'B');
PQueue queue;
foreach (string letter in sequence) {
queue.enqueue(letter);
}
for (char ch = 'A'; ch <= 'H'; ch++) {
string expected(1, ch);
checkCondition(queue.dequeueMin() == expected, "Queue should yield " + expected + ".");
}
}
} catch (ErrorException& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.getMessage() << endl;
} catch (exception& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.what() << endl;
} catch (...) {
cout << "TEST FAILURE: Unknown exception." << endl;
}
endTest("Sort Crafted Tests");
}
template <typename PQueue>
void sortDuplicateTests() {
beginTest("Sort Duplicate Tests");
try {
{
logInfo("Loading a sorted sequence containing duplicates.");
PQueue queue;
for (char ch = 'A'; ch <= 'D'; ch++) {
queue.enqueue(string(1, ch));
queue.enqueue(string(1, ch));
}
for (char ch = 'A'; ch <= 'D'; ch++) {
for (int i = 0; i < 2; i++) {
string expected(1, ch);
checkCondition(queue.dequeueMin() == expected, "Queue should yield " + expected + ".");
}
}
}
{
logInfo("Loading a reverse sorted sequence containing duplicates.");
PQueue queue;
for (char ch = 'D'; ch >= 'A'; ch--) {
queue.enqueue(string(1, ch));
queue.enqueue(string(1, ch));
}
for (char ch = 'A'; ch <= 'D'; ch++) {
for (int i = 0; i < 2; i++) {
string expected(1, ch);
checkCondition(queue.dequeueMin() == expected, "Queue should yield " + expected + ".");
}
}
}
{
logInfo("Loading two sorted sequences, one after the other.");
PQueue queue;
for (int i = 0; i < 2; i++) {
for (char ch = 'A'; ch <= 'H'; ch++) {
queue.enqueue(string(1, ch));
}
}
for (char ch = 'A'; ch <= 'H'; ch++) {
for (int i = 0; i < 2; i++) {
string expected(1, ch);
checkCondition(queue.dequeueMin() == expected, "Queue should yield " + expected + ".");
}
}
}
{
logInfo("Loading two reverse sorted sequences, one after the other.");
PQueue queue;
for (int i = 0; i < 2; i++) {
for (char ch = 'H'; ch >= 'A'; ch--) {
queue.enqueue(string(1, ch));
}
}
for (char ch = 'A'; ch <= 'H'; ch++) {
for (int i = 0; i < 2; i++) {
string expected(1, ch);
checkCondition(queue.dequeueMin() == expected, "Queue should yield " + expected + ".");
}
}
}
{
logInfo("Loading a sorted sequence, then repeating the middle.");
PQueue queue;
for (char ch = 'A'; ch <= 'H'; ch++) {
queue.enqueue(string(1, ch));
}
for (char ch = 'C'; ch <= 'F'; ch++) {
queue.enqueue(string(1, ch));
}
for (char ch = 'A'; ch <= 'H'; ch++) {
int numTimes = (ch >= 'C' && ch <= 'F'? 2 : 1);
for (int i = 0; i < numTimes; i++) {
string expected(1, ch);
checkCondition(queue.dequeueMin() == expected, "Queue should yield " + expected + ".");
}
}
}
} catch (ErrorException& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.getMessage() << endl;
} catch (exception& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.what() << endl;
} catch (...) {
cout << "TEST FAILURE: Unknown exception." << endl;
}
endTest("Sort Duplicate Tests");
}
template <typename PQueue>
void reuseTests() {
beginTest("Reuse Tests");
try {
PQueue queue;
bool isSorted = true;
for (int i = 0; i < 5; i++) {
logInfo("Generating 10000 random strings.");
Vector<string> strings;
for (int i = 0; i < 10000; i++) {
strings += randomString();
}
logInfo("Enqueuing 10000 random strings.");
foreach (string str in strings) {
queue.enqueue(str);
}
logInfo("Sorting 10000 random strings.");
sort(strings.begin(), strings.end());
logInfo("Dequeuing 10000 random strings.");
foreach(string str in strings) {
if (queue.dequeueMin() != str) {
isSorted = false;
}
}
if (!isSorted) break;
}
checkCondition(isSorted, "Strings were consistently sorted.");
} catch (ErrorException& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.getMessage() << endl;
} catch (exception& e) {
cout << "TEST FAILURE: Unexpected exception: " << e.what() << endl;
} catch (...) {
cout << "TEST FAILURE: Unknown exception." << endl;
}
endTest("Reuse Tests");
}
template <typename PQueue>
void myVeryOwnTests() {
beginTest("My Very Own Tests");
PQueue queue;
endTest("My Very Own Tests");
}
template <typename PQueue>
void testPriorityQueue() {
basicStructuralTests<PQueue> ();
sortAscendingTests<PQueue> ();
sortDescendingTests<PQueue> ();
sortRandomTests<PQueue> ();
sortCraftedTests<PQueue> ();
sortDuplicateTests<PQueue> ();
reuseTests<PQueue> ();
}
void printReplInstructions() {
cout << "Interactive Priority Queue Test" << endl;
cout << "===============================" << endl;
cout << "This environment allows you to type in commands that will be" << endl;
cout << "executed on your priority queue.  The interpreter knows the" << endl;
cout << "following commands:" << endl;
cout << endl;
cout << "   isEmpty:        Reports whether the priority queue is empty." << endl;
cout << "   size:           Reports the size of the priority queue" << endl;
cout << "   enqueue <str>:  Enqueues the string <str>" << endl;
cout << "   peek:           Peeks at the minimum element of the priority queue." << endl;
cout << "   dequeueMin:     Dequeues the minimum element of the priority queue." << endl;
cout << "   quit:           Quits the interpret and returns to the menu." << endl;
cout << endl;
cout << "The first letter of any command can be used as a substitute" << endl;
cout << "for any command name." << endl;
}
template <typename PQueue>
void replTestPriorityQueue() {
printReplInstructions();
{
PQueue queue;
while (true) {
istringstream command(getLine("Enter command: "));
string action;
command >> action >> ws;
if (!command) {
cout << "Please enter a command." << endl;
} else {
try {
if (action == "peek" || action == "p") {
cout << queue.peek() << endl;
} else if (action == "isEmpty" || action == "i") {
cout << boolalpha << queue.isEmpty() << endl;
} else if (action == "size" || action == "s") {
cout << queue.size() << endl;
} else if (action == "dequeueMin" || action == "d") {
cout << queue.dequeueMin() << endl;
} else if (action == "quit" || action == "q") {
cout << "Leaving test environment...   " << flush;
break;
} else if (action == "enqueue" || action == "e") {
string toEnqueue;
if (!getline(command, toEnqueue)) {
cout << "Must specify a string to enqueue." << endl;
} else {
queue.enqueue(toEnqueue);
cout << "Enqueued string \"" << toEnqueue << "\"." << endl;
}
} else {
cout << "Unknown command." << endl;
}
} catch (ErrorException& e) {
cout << "ERROR: " << e.getMessage() << endl;
} catch (exception& e) {
cout << "ERROR: " << e.what() << endl;
} catch (...) {
cout << "Unknown error." << endl;
}
}
}
}
cout << "success." << endl;
cout << endl;
}
enum {
REPL_VECTOR = 1,
TEST_VECTOR,
REPL_LINKED_LIST,
TEST_LINKED_LIST,
REPL_DOUBLY_LINKED_LIST,
TEST_DOUBLY_LINKED_LIST,
REPL_HEAP,
TEST_HEAP,
REPL_EXTRA,
TEST_EXTRA,
QUIT
};
void displayMenu() {
cout << "CS106B Priority Queue Testing Harness" << endl;
cout << "=====================================" << endl;
cout << REPL_VECTOR << ": Manually test VectorPriorityQueue" << endl;
cout << TEST_VECTOR << ": Automatically test VectorPriorityQueue" << endl;
cout << REPL_LINKED_LIST << ": Manually test LinkedListPriorityQueue" << endl;
cout << TEST_LINKED_LIST << ": Automatically test LinkedListPriorityQueue" << endl;
cout << REPL_DOUBLY_LINKED_LIST << ": Manually test DoublyLinkedListPriorityQueue" << endl;
cout << TEST_DOUBLY_LINKED_LIST << ": Automatically test DoublyLinkedListPriorityQueue" << endl;
cout << REPL_HEAP << ": Manually test HeapPriorityQueue" << endl;
cout << TEST_HEAP << ": Automatically test HeapPriorityQueue" << endl;
cout << REPL_EXTRA << ": Manually test ExtraPriorityQueue" << endl;
cout << TEST_EXTRA << ": Automatically test ExtraPriorityQueue" << endl;
cout << QUIT << ": Quit" << endl;
}
int main() {
while (true) {
displayMenu();
switch (getInteger("Enter choice: ")) {
case TEST_VECTOR:
testPriorityQueue<VectorPriorityQueue> ();
break;
case REPL_VECTOR:
replTestPriorityQueue<VectorPriorityQueue> ();
break;
case TEST_LINKED_LIST:
testPriorityQueue<LinkedListPriorityQueue> ();
break;
case REPL_LINKED_LIST:
replTestPriorityQueue<LinkedListPriorityQueue> ();
break;
case TEST_DOUBLY_LINKED_LIST:
testPriorityQueue<DoublyLinkedListPriorityQueue> ();
break;
case REPL_DOUBLY_LINKED_LIST:
replTestPriorityQueue<DoublyLinkedListPriorityQueue> ();
break;
case TEST_HEAP:
testPriorityQueue<HeapPriorityQueue> ();
break;
case REPL_HEAP:
replTestPriorityQueue<HeapPriorityQueue> ();
break;
case TEST_EXTRA:
testPriorityQueue<ExtraPriorityQueue> ();
break;
case REPL_EXTRA:
replTestPriorityQueue<ExtraPriorityQueue> ();
break;
case QUIT:
return 0;
default:
cout << "Sorry, but I don't know how to do that." << endl;
break;
}
}
return 0;
}