using namespace std;
Map<ext_char, int> getFrequencyTable(istream& file);
Node* buildEncodingTree(Map<ext_char, int>& frequencies);
void freeTree(Node* root);
void encodeFile(istream& infile, Node* encodingTree, obstream& outfile);
void decodeFile(ibstream& infile, Node* encodingTree, ostream& file);
void writeFileHeader(obstream& outfile, Map<ext_char, int>& frequencies);
Map<ext_char, int> readFileHeader(ibstream& infile);
void compress(ibstream& infile, obstream& outfile);
void decompress(ibstream& infile, ostream& outfile);
vector<pair<ext_char, string> > encodedPatterns(Node * encodingTree);
void writeBitPattern(obstream & outfile, const string& pattern);
Map<ext_char, string> getEncodedPatternMap(Node * root);
void encodedPatternUtility(Node * tree, vector<pair<ext_char, string> >& pairs,
string pattern);