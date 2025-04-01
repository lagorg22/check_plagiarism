using namespace std;
enum MenuEntry {
MANUAL_FREQUENCY_TESTS = 1,
AUTOMATIC_FREQUENCY_TESTS,
MANUAL_TREE_TESTS,
AUTOMATIC_TREE_TESTS,
MANUAL_ENCODING_TESTS,
AUTOMATIC_ENCODING_TESTS,
AUTOMATIC_COMPLETE_TESTS,
COMPRESS,
DECOMPRESS,
COMPARE,
QUIT,
};
void doAssertCondition(bool expr, string reason, string expression, int lineNumber) {
if (!expr) {
cout << "! FAIL: " << reason << endl;
cout << "  Test failed on line " << lineNumber << " of HuffmanEncodingTest.cpp" << endl;
cout << "  Specific expression: " << expression << endl;
getLine("  Press ENTER to continue...");
}
}
void doCheckCondition(bool expr, string reason, string expression, int lineNumber) {
if (expr) {
cout << "   PASS: " << reason << endl;
} else {
doAssertCondition(expr, reason, expression, lineNumber);
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
cout << "	 info: " << message << endl;
}
string representationOf(ext_char ch) {
ostringstream representation;
if (ch == PSEUDO_EOF) {
representation << "EOF";
} else if (ch == NOT_A_CHAR) {
representation << "NAC";
}
else if (isgraph(char(ch))) {
representation << char(ch);
}
else if (ch == ' ') {
representation << "\" \"";
} else if (ch == '\t') {
representation << "\\t";
} else if (ch == '\n') {
representation << "\\n";
} else if (ch == '\r') {
representation << "\\r";
}
else {
representation << "0x" << hex << setw(2) << setfill('0') << (int)(unsigned char)ch;
}
return representation.str();
}
void validateFrequencyTable(ibstream& stream, int length) {
const int kMaxDisplayLength = 40;
if (length <= kMaxDisplayLength) {
ostringstream contents;
contents << stream.rdbuf();
stream.rewind();
logInfo("Testing string " + contents.str());
}
Map<ext_char, int> table = getFrequencyTable(stream);
checkCondition(table.containsKey(PSEUDO_EOF),
"Frequency table should contain PSEUDO_EOF");
checkCondition(table[PSEUDO_EOF] == 1,
"Frequency table should record 1 instance of PSEUDO_EOF");
int totalFreq = 0;
bool warnedAboutZero = false; // Prevents warning repeatedly times about zero elements
foreach (ext_char key in table) {
totalFreq += table[key];
assertCondition(table[key] >= 0, "You should never have negative frequencies. "
+ representationOf(key) + " has negative value " + integerToString(table[key]));
if (table[key] == 0 && !warnedAboutZero) {
logInfo("You have a key in your map with frequency 0 ("
+ representationOf(key) + " = 0). Make sure not to put 0-frequency characters in your tree.");
warnedAboutZero = true;
}
}
checkCondition(length + 1 == totalFreq,
"The sum of all frequencies should be equal to the number of characters of input, plus 1 for PSEUDO_EOF");
stream.rewind();
Map<ext_char, int> referenceTable = referenceGetFrequencyTable(stream);
foreach (ext_char key in referenceTable) {
assertCondition(referenceTable[key] == table[key], representationOf(key) + " should be "
+ integerToString(referenceTable[key]) + " but is " + integerToString(table[key]));
}
foreach (ext_char key in table) {
assertCondition(referenceTable[key] == table[key], representationOf(key) + " should be "
+ integerToString(referenceTable[key]) + " but is " + integerToString(table[key]));
}
}
void validateFrequencyTableString(string input, string message) {
logInfo(message);
istringbstream stream (input);
validateFrequencyTable(stream, input.length());
}
void testGetFrequencyTable() {
beginTest("getFrequencyTable Tests");
validateFrequencyTableString("a", "Testing correct table with no content");
validateFrequencyTableString("aaaaaaa", "Testing correct table with only one letter");
validateFrequencyTableString("The quick brown fox jumps over the lazy dog",
"Testing correct table with all of the letters");
validateFrequencyTableString("#66FF33, #CC0099; #FFFF33. #eaa6ea! #c0f7fe?",
"Testing correct table with all of the letters");
{
logInfo("Testing on a file of 10,000 random bytes.");
ifbstream stream("test/input/random_10k.test");
validateFrequencyTable(stream, 10000);
}
endTest("getFrequencyTable Tests");
}
void manualGetFrequencyTable() {
beginTest("Manual getFrequencyTable Test");
cout << "Enter strings below to see the frequency table constructed by your" << endl;
cout << "getFrequencyTable function.	Enter the empty string to quit." << endl;
while (true) {
string text = getLine("Text (enter to stop test): ");
if (text == "") break;
istringstream source(text);
Map<ext_char, int> frequencies = getFrequencyTable(source);
foreach (ext_char ch in frequencies) {
cout << setw(4) << representationOf(ch) << ": " << frequencies[ch] << endl;
}
}
}
int treeCost(Node* root, int depth = 0) {
assertCondition(root != NULL, "NULL tree!  This will almost certainly crash.");
if (root->zero == NULL && root->one == NULL)
return root->weight * depth;
return treeCost(root->zero, depth + 1) + treeCost(root->one, depth + 1);
}
void recCheckTreeCorrectness(Node* root, Map<ext_char, int>& frequencies) {
assertCondition(root != NULL, "Encoding tree should be non-NULL.");
assertCondition((root->zero == NULL && root->one == NULL) ||
(root->zero != NULL && root->one != NULL),
"All nodes should either have 0 or 2 children.");
assertCondition((root->character == NOT_A_CHAR) ==
(root->zero != NULL && root->one != NULL),
"All internal nodes should not store characters.");
assertCondition(root->zero == NULL || root->zero != root->one,
"No internal node should have the same children on both sides.");
assertCondition(root->zero == NULL || root->weight == root->zero->weight + root->one->weight,
"Each interal node should have weight equal to the sum of its children.");
assertCondition(root->character == NOT_A_CHAR ||
frequencies.containsKey(root->character),
"Character not present in the frequency table is in the encoding tree?");
assertCondition(root->character == NOT_A_CHAR ||
frequencies[root->character] == root->weight,
"Weight in the tree should match weight in the table.");
frequencies.remove(root->character);
if (root->zero) recCheckTreeCorrectness(root->zero, frequencies);
if (root->one)	recCheckTreeCorrectness(root->one,	frequencies);
}
bool recCheckTreesEqual(Node* first, Node* second) {
assertCondition((first == NULL) == (second == NULL),
"Both trees must be null or non-null.");
if (first == NULL && second == NULL) return true;
if (first == NULL || second == NULL) return false;
assertCondition(first->weight == second->weight,
"Two encoding trees have different weights.");
assertCondition(first->character == second->character,
"Two encoding trees have different characters.");
return recCheckTreesEqual(first->zero, second->zero) &
recCheckTreesEqual(first->one,  second->one);
}
void testBuildEncodingTree() {
beginTest("buildEncodingTree tests");
{
logInfo("Checking for correct tree on a single letter");
Map<ext_char, int> frequencies;
frequencies[PSEUDO_EOF] = 1;
frequencies['A'] = 1;
Node *tree = buildEncodingTree(frequencies);
checkCondition(tree != NULL, "Tree should be nonempty.");
checkCondition(tree->character == NOT_A_CHAR, "Tree root does not hold a character.");
checkCondition(tree->zero != NULL && tree->one != NULL, "Tree should have two children.");
checkCondition(tree->weight == 2, "Tree should have weight two (one from each child).");
checkCondition(tree->zero->character == PSEUDO_EOF || tree->one->character == PSEUDO_EOF,
"One child should be pseudo-eof.");
checkCondition(tree->zero->character == 'A' || tree->one->character == 'A',
"One child should be A.");
logInfo("If either of the previous tests failed, this is almost certainly going to crash.");
Node*		aChild = (tree->zero->character == 'A'? tree->zero : tree->one);
Node* eofChild = (tree->zero->character == 'A'? tree->one : tree->zero);
checkCondition(aChild->zero == NULL && aChild->one == NULL,
"Singleton node for A should have no children.");
checkCondition(aChild->weight == 1, "Singleton for A should have weight 1.");
checkCondition(eofChild->zero == NULL && eofChild->one == NULL,
"Singleton node for EOF should have no children.");
checkCondition(eofChild->weight == 1, "Singleton for EOF should have weight 1.");
delete aChild;
delete eofChild;
delete tree;
}
{
istringstream stream("ABBCCCCDDDDDDDDEEEEEEEEEEEEEEEE");
Map<ext_char, int> frequencies = referenceGetFrequencyTable(stream);
Node* tree = buildEncodingTree(frequencies);
logInfo("About to recursively check the tree for correctness.");
logInfo("If you don't see any messages here, it means that the tree");
logInfo("is structurally correct (even if it's the wrong tree.)");
recCheckTreeCorrectness(tree, frequencies);
checkCondition(frequencies.isEmpty(), "All letters accounted for.");
}
{
istringstream stream("ABBCCCDDDDDEEEEEEEEFFFFFFFFFFFFF");
Map<ext_char, int> frequencies = referenceGetFrequencyTable(stream);
Node* tree = buildEncodingTree(frequencies);
logInfo("About to recursively check the tree for correctness.");
logInfo("If you don't see any messages here, it means that the tree");
logInfo("is structurally correct (even if it's the wrong tree.)");
recCheckTreeCorrectness(tree, frequencies);
checkCondition(frequencies.isEmpty(), "All letters accounted for.");
}
{
istringstream stream("ABBCCCCDDDDDDDDEEEEEEEEEEEEEEEE");
Map<ext_char, int> frequencies = referenceGetFrequencyTable(stream);
Node* expected = referenceBuildEncodingTree(frequencies);
Node* theirs = buildEncodingTree(frequencies);
checkCondition(treeCost(expected) == treeCost(theirs), "Trees should require proper number of bits for simple text input");
}
{
istringstream stream("ABBCCCDDDDDEEEEEEEEFFFFFFFFFFFFF");
Map<ext_char, int> frequencies = referenceGetFrequencyTable(stream);
Node* expected = referenceBuildEncodingTree(frequencies);
Node* theirs = buildEncodingTree(frequencies);
checkCondition(treeCost(expected) == treeCost(theirs), "Trees should require proper number of bits for harder text input");
}
{
istringstream stream("0123AABBCCDD");
Map<ext_char, int> frequencies = referenceGetFrequencyTable(stream);
Node* expected = referenceBuildEncodingTree(frequencies);
Node* theirs = buildEncodingTree(frequencies);
checkCondition(treeCost(expected) == treeCost(theirs), "Trees should require proper number of bits for even harder text input");
}
{
ifbstream stream("test/input/random_10k.test");
Map<ext_char, int> frequencies = referenceGetFrequencyTable(stream);
Node* expected = referenceBuildEncodingTree(frequencies);
Node* theirs = buildEncodingTree(frequencies);
checkCondition(treeCost(expected) == treeCost(theirs), "Trees should require proper number of bits for random bytes input");
}
{
long disparity = numAllocations() - numDeallocations();
Node* freeMe = new Node;
freeMe->zero = freeMe->one = NULL;
freeMe->character = PSEUDO_EOF;
freeMe->weight = 1;
freeTree(freeMe);
checkCondition(numAllocations() - numDeallocations() == disparity,
"Number of allocations/deallocations matches for a single node.");
}
{
long disparity = numAllocations() - numDeallocations();
ifbstream stream("test/input/random_10k.test");
Map<ext_char, int> frequencies = referenceGetFrequencyTable(stream);
Node* tree = buildEncodingTree(frequencies);
freeTree(tree);
checkCondition(numAllocations() - numDeallocations() == disparity,
"Number of allocations/deallocations matches for a huge tree.");
}
{
istringstream stream("0123AABBCCDD");
Map<ext_char, int> frequencies = referenceGetFrequencyTable(stream);
Node* first = buildEncodingTree(frequencies);
Node* second = buildEncodingTree(frequencies);
Node* third = buildEncodingTree(frequencies);
checkCondition(recCheckTreesEqual(first, second), "Encoding trees should be the same.");
checkCondition(recCheckTreesEqual(second, third), "Encoding trees should be the same.");
checkCondition(recCheckTreesEqual(third, first),  "Encoding trees should be the same.");
}
endTest("buildEncodingTree tests");
}
void printEncodings(Node* root, string code = "") {
if (root == NULL) return;
if (root->character != NOT_A_CHAR) {
cout << setw(4) << representationOf(root->character) << ": " << code << endl;
}
else {
printEncodings(root->zero, code + "0");
printEncodings(root->one, code + "1");
}
}
void manualBuildEncodingTree() {
beginTest("Manual buildEncodingTree Tests");
cout << "You can enter strings below to call your buildEncodingTree function on them." << endl;
cout << "We will display the generated prefix code for the text you've entered." << endl;
while (true) {
string text = getLine("Text (enter to stop test): ");
if (text == "") break;
long difference = numAllocations() - numDeallocations();
istringstream source(text);
Map<ext_char, int> table = getFrequencyTable(source);
Node* tree = buildEncodingTree(table);
printEncodings(tree);
freeTree(tree);
difference = (numAllocations() - numDeallocations()) - difference;
if (difference > 0) {
cout << "Memory leak detected!	Just leaked " << difference << " node(s)." << endl;
} else if (difference < 0) {
cout << "Double free detected!	Freed " << -difference << " too many node(s)." << endl;
}
}
}
void testEncoding() {
beginTest("encodeFile / decodeFile Tests");
Vector<string> files;
files += "singleChar", "nonRepeated", "alphaOnce", "allRepeated", "fibonacci", "poem", "allCharsOnce", "tomSawyer", "dikdik.jpg", "random";
foreach (string file in files) {
logInfo("Testing encoding and decoding on file test/encodeDecode/" + file);
ifbstream input("test/encodeDecode/" + file);
assertCondition(input.is_open(), ("Cannot open file test/encodeDecode/" + file + " for reading!"));
Map<ext_char, int> frequency = getFrequencyTable(input);
input.rewind();
Node* encodingTree = buildEncodingTree(frequency);
int expectedBytes = (treeCost(encodingTree) + 7) / 8;
{
ostringbstream compressed;
encodeFile(input, encodingTree, compressed);
input.rewind();
checkCondition(compressed.size() == expectedBytes,
"Expected " + integerToString(expectedBytes) + " bytes, "
"got " + integerToString(compressed.size()) + " bytes.");
}
{
ostringstream fileContents;
fileContents << input.rdbuf();
input.rewind();
ostringbstream compressed;
encodeFile(input, encodingTree, compressed);
input.rewind();
istringbstream toDecompress(compressed.str());
ostringbstream decompressed;
decodeFile(toDecompress, encodingTree, decompressed);
checkCondition(fileContents.str() == decompressed.str(),
"Encoding then decoding should get back the original file.");
}
}
endTest("encodeFile / decodeFile Tests");
}
void testCompleteStack() {
beginTest("Complete Stack Tests");
Vector<string> files;
files += "singleChar", "nonRepeated", "alphaOnce", "allRepeated", "fibonacci", "poem", "allCharsOnce", "tomSawyer", "dikdik.jpg", "random";
foreach (string file in files) {
logInfo("Testing compress and decompress on file test/encodeDecode/" + file);
long difference = numAllocations() - numDeallocations();
ifbstream input("test/encodeDecode/" + file);
assertCondition(input.is_open(), ("Cannot open file test/encodeDecode/" + file + " for reading!"));
ostringstream originalData;
originalData << input.rdbuf();
input.rewind();
ostringbstream result;
compress(input, result);
istringbstream compressedData(result.str());
ostringbstream decompressedData;
decompress(compressedData, decompressedData);
checkCondition(originalData.str() == decompressedData.str(),
"Compressed/decompressed data matches.");
checkCondition(numAllocations() - numDeallocations() == difference,
"No tree nodes leaked.");
}
endTest("Complete Stack Tests");
}
void printBits(string str, int maxBits) {
istringbstream stream(str);
for (int i = 0; i < maxBits; i++) {
int bit = stream.readBit();
if (bit == EOF) break;
cout << bit;
}
cout << endl;
}
void manualEncodeDecode() {
beginTest("Manual encodeFile / decodeFile Tests");
cout << "Enter text for us to encode and then decode" << endl;
while (true) {
string text = getLine("Text (enter to stop test): ");
if (text == "") break;
istringbstream source(text);
Map<ext_char, int> frequencies = getFrequencyTable(source);
Node* tree = buildEncodingTree(frequencies);
ostringbstream compressed;
source.rewind();
encodeFile(source, tree, compressed);
cout << "Compressed representation: " << endl;
printBits(compressed.str(), treeCost(tree));
istringbstream compressedIn(compressed.str());
ostringstream unpacked;
decodeFile(compressedIn, tree, unpacked);
checkCondition(unpacked.str() == text, "Result of compressing and decompressing should be the original input.");
freeTree(tree);
}
}
template <typename FileStream>
void openFile(FileStream& file, string prompt = "") {
while (true) {
string filename = getLine(prompt);
file.open(filename.c_str());
if (file.is_open()) return;
cout << "Sorry, I couldn't open that file." << endl;
file.clear();
}
}
void runCompress() {
ifbstream infile;
openFile(infile, "File to compress: ");
ofbstream outfile;
openFile(outfile, "Filename for compressed output: ");
cout << "Compressing... " << flush;
compress(infile, outfile);
cout << "done!" << endl << endl;
cout << "Original file size: " << infile.size() << "B" << endl;
cout << "New file size:      " << outfile.size() << "B" << endl;
cout << "Compression ratio:  " << double(outfile.size()) / infile.size() << endl << endl;
getLine("Press ENTER to continue...");
}
void runDecompress() {
ifbstream infile;
openFile(infile, "File to decompress: ");
ofbstream outfile;
openFile(outfile, "Name of file to write result: ");
decompress(infile, outfile);
cout << "Decompressed file written!" << endl;
getLine("Press ENTER to continue...");
}
void compareFiles() {
ifstream one, two;
openFile(one, "First file to compare:  ");
openFile(two, "Second file to compare: ");
ostringstream oneContents, twoContents;
oneContents << one.rdbuf();
twoContents << two.rdbuf();
const string oneString = oneContents.str(), twoString = twoContents.str();
if (oneString.length() != twoString.length()) {
cout << "Files differ!" << endl;
cout << "File one has length " << oneString.length() << "." << endl;
cout << "File two has length " << twoString.length() << "." << endl;
} else {
pair<string::const_iterator, string::const_iterator> diff =
mismatch(oneString.begin(), oneString.end(), twoString.begin());
if (diff.first != oneString.end()) {
cout << "Files differ!" << endl;
ptrdiff_t offset = diff.first - oneString.begin();
cout << "Bytes differ at offset " << offset << "." << endl;
cout << "File one has value " << representationOf(*diff.first) << endl;
cout << "File two has value " << representationOf(*diff.second) << endl;
} else {
cout << "Files match!" << endl;
}
}
getLine("Press ENTER to continue...");
}
void displayMenu() {
cout << "CS106B Huffman Encoding Testing Harness" << endl;
cout << "=====================================" << endl;
cout << setw(2) << MANUAL_FREQUENCY_TESTS << ": Manually test getFrequencyTable" << endl;
cout << setw(2) << AUTOMATIC_FREQUENCY_TESTS << ": Automatically test getFrequencyTable" << endl;
cout << setw(2) << MANUAL_TREE_TESTS << ": Manually test buildEncodingTree" << endl;
cout << setw(2) << AUTOMATIC_TREE_TESTS << ": Automatically test buildEncodingTree" << endl;
cout << setw(2) << MANUAL_ENCODING_TESTS << ": Manually test encodeFile/decodeFile" << endl;
cout << setw(2) << AUTOMATIC_ENCODING_TESTS << ": Automatically test encodeFile/decodeFile" << endl;
cout << setw(2) << AUTOMATIC_COMPLETE_TESTS << ": Automatically test compress/decompress" << endl;
cout << setw(2) << COMPRESS << ": Compress a file" << endl;
cout << setw(2) << DECOMPRESS << ": Decompress a compressed file" << endl;
cout << setw(2) << COMPARE << ": Compare two files for equality" << endl;
cout << setw(2) << QUIT << ": Quit" << endl;
}
void testEnvironment() {
if (std::numeric_limits<char>::is_signed) {
cerr << "============= ENVIRONMENT ERROR =============" << endl;
cerr << "Something is wrong with this project setup." << endl;
cerr << "This is our fault!  Please contact the course" << endl;
cerr << "staff as soon as possible to let them know" << endl;
cerr << "that you're seeing this error." << endl;
cerr << "=============================================" << endl;
cerr << "Error: char is signed in encoding test."  << endl;
cerr << "=============================================" << endl;
getLine("Press ENTER to quit...");
exit(-1);
}
}
int main() {
testEnvironment();
testReferenceSolutionConfiguration();
while (true) {
displayMenu();
switch (getInteger("Enter choice: ")) {
case COMPRESS:
runCompress();
break;
case DECOMPRESS:
runDecompress();
break;
case AUTOMATIC_FREQUENCY_TESTS:
testGetFrequencyTable();
break;
case MANUAL_FREQUENCY_TESTS:
manualGetFrequencyTable();
break;
case AUTOMATIC_TREE_TESTS:
testBuildEncodingTree();
break;
case MANUAL_TREE_TESTS:
manualBuildEncodingTree();
break;
case MANUAL_ENCODING_TESTS:
manualEncodeDecode();
break;
case AUTOMATIC_ENCODING_TESTS:
testEncoding();
break;
case AUTOMATIC_COMPLETE_TESTS:
testCompleteStack();
break;
case COMPARE:
compareFiles();
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