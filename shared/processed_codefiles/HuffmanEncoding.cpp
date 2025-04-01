using namespace std;
Map<ext_char, int> getFrequencyTable(istream& file) {
Map<ext_char, int> frequencyTable;
frequencyTable[PSEUDO_EOF] = 1;
char c;
while (file.get(c)) {
frequencyTable[c]++;
}
return frequencyTable;
}
Node* buildEncodingTree(Map<ext_char, int>& frequencies) {
PriorityQueue<Node*> nodesPQ;
foreach (ext_char character in frequencies) {
Node * node = new Node;
node->character = character;
node->one = NULL;
node->zero = NULL;
node->weight = frequencies[character];
nodesPQ.enqueue(node, node->weight);
}
while (!nodesPQ.isEmpty()) {
Node * node1 = nodesPQ.dequeue();
if (nodesPQ.isEmpty()) return node1;
Node * node2 = nodesPQ.dequeue();
Node * parent = new Node;
parent->zero = node1;
parent->one = node2;
parent->character = NOT_A_CHAR;
parent->weight = node1->weight + node2->weight;
nodesPQ.enqueue(parent, parent->weight);
}
return NULL;
}
void freeTree(Node* root) {
if (root == NULL) return;
freeTree(root->one);
freeTree(root->zero);
delete root;
}
void encodeFile(istream& infile, Node* encodingTree, obstream& outfile) {
Map<ext_char, string> map = getEncodedPatternMap(encodingTree);
char character;
while (infile.get(character)) {
writeBitPattern(outfile, map[character]);
}
writeBitPattern(outfile, map[PSEUDO_EOF]);
}
Map<ext_char, string> getEncodedPatternMap(Node * root) {
Map<ext_char, string> map;
vector<pair<ext_char, string> > pairs = encodedPatterns(root);
for (int i = 0; i < pairs.size(); i++) {
map[pairs[i].first] = pairs[i].second;
}
return map;
}
vector<pair<ext_char, string> > encodedPatterns(Node * encodingTree) {
string pattern;
vector<pair<ext_char, string> > pairs;
encodedPatternUtility(encodingTree, pairs, pattern);
return pairs;
}
void encodedPatternUtility(Node * tree, vector<pair<ext_char, string> >& pairs,
string pattern) {
if (tree == NULL) return;
if (tree->one == NULL && tree->zero == NULL) {
pairs.push_back(make_pair(tree->character, pattern));
}
encodedPatternUtility(tree->one, pairs, pattern + "1" );
encodedPatternUtility(tree->zero, pairs, pattern + "0");
}
void writeBitPattern(obstream& outfile, const string& pattern) {
int bit;
for (int i = 0; i < pattern.size(); i++) {
bit = pattern[i] == '1' ? 1 : 0;
outfile.writeBit(bit);
}
}
void decodeFile(ibstream& infile, Node* encodingTree, ostream& file) {
Map<ext_char, string> encodedMap = getEncodedPatternMap(encodingTree);
Map<string, ext_char> decodeMap;
foreach (ext_char ch in encodedMap) {
decodeMap[encodedMap[ch]] = ch;
}
string pattern;
int bit;
int i = 0;
while (true) {
bit = infile.readBit();
(bit == 1) ? pattern += "1" : pattern += "0";
if (decodeMap.containsKey(pattern)) {
ext_char ch = decodeMap[pattern];
if (ch == PSEUDO_EOF) return;
char ch_ = (char) ch;
file.put(ch_);
pattern = "";
}
}
}
void writeFileHeader(obstream& outfile, Map<ext_char, int>& frequencies) {
if (!frequencies.containsKey(PSEUDO_EOF)) {
error("No PSEUDO_EOF defined.");
}
outfile << frequencies.size() - 1 << ' ';
foreach (ext_char ch in frequencies) {
if (ch == PSEUDO_EOF) continue;
outfile << char(ch) << frequencies[ch] << ' ';
}
}
Map<ext_char, int> readFileHeader(ibstream& infile) {
Map<ext_char, int> result;
int numValues;
infile >> numValues;
infile.get();
for (int i = 0; i < numValues; i++) {
ext_char ch = infile.get();
int frequency;
infile >> frequency;
infile.get();
result[ch] = frequency;
}
result[PSEUDO_EOF] = 1;
return result;
}
void compress(ibstream& infile, obstream& outfile) {
Map<ext_char, int> frequencies = getFrequencyTable(infile);
infile.rewind();
writeFileHeader(outfile, frequencies);
Node* encodingTree = buildEncodingTree(frequencies);
encodeFile(infile, encodingTree, outfile);
freeTree(encodingTree);
}
void decompress(ibstream& infile, ostream& outfile) {
Map<ext_char, int> frequencies = readFileHeader(infile);
Node* encodingTree = buildEncodingTree(frequencies);
decodeFile(infile, encodingTree, outfile);
freeTree(encodingTree);
}