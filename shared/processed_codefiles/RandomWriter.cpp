void OpenUserFile(std::ifstream& infile);
void generateOccurenceMap(std::ifstream& input,
std::map<std::string, std::vector<char> >& occurenceMap, int order);
int getInteger(std::string prompt);
template <typename T>
void printVector(std::vector<T>& vec, std::string separator);
void generateRandomText(std::map<std::string, std::vector<char> >& occurenceMap,
int numCharacters);
std::string findSeed(std::map<std::string, std::vector<char> >& occurenceMap);
int main() {
std::ifstream input;
OpenUserFile(input);
int order;
while (true) {
order = getInteger("Enter the Markov order[1-10]: ");
if (order >= 1 && order <= 10) break;
};
std::map<std::string, std::vector<char> > occurenceMap;
generateOccurenceMap(input, occurenceMap, order);
generateRandomText(occurenceMap, 2000);
return 0;
}
void OpenUserFile(std::ifstream& infile) {
std::string filename;
while (true) {
std::cout << "Enter the filename: ";
getline(std::cin, filename);
infile.open(filename.c_str());
if (infile.is_open()) return;
std::cout << "Invalid file name. Try again." << std::endl;
infile.clear();
}
}
void generateOccurenceMap(std::ifstream& input,
std::map<std::string, std::vector<char> >& occurenceMap, int order) {
std::string text;
char ch;
for (int i = 0; i < order; i++) {
input.get(ch);
text += ch;
}
while (input.get(ch)) {
occurenceMap[text].push_back(ch);
text = text.substr(1) + ch;
}
}
int getInteger(std::string prompt) {
int result;
while (true) {
std::cout << prompt;
std::stringstream converter;
std::string line;
getline(std::cin, line);
converter << line;
converter >> result;
if (converter.fail()) {
std::cout << "Illegal integer format. Try again." << std::endl;
} else {
char remaining;
if (converter.get(remaining)) {
std::cout << "Illegal integer format. Try again." << std::endl;
} else {
return result;
}
}
}
}
std::string findSeed(std::map<std::string, std::vector<char> >& occurenceMap) {
size_t maxOccurence = 0;
std::vector<std::string> seedVector;
std::string seed = "";
for (auto it = occurenceMap.begin(); it != occurenceMap.end(); ++it) {
if ((it->second).size() > maxOccurence) {
maxOccurence = (it->second).size();
seed = (it->first);
}
}
for (auto it = occurenceMap.begin(); it != occurenceMap.end(); ++it) {
if ((it->second).size() == maxOccurence) {
seedVector.push_back(it->first);
}
}
return seedVector[randomInteger(0, seedVector.size()-1)];
}
void generateRandomText(std::map<std::string, std::vector<char> >& occurenceMap,
int numCharacters) {
std::string seed = findSeed(occurenceMap);
for (int i = 0; i < numCharacters; i++) {
if (occurenceMap[seed].size() == 0) break;
char ch = occurenceMap[seed][randomInteger(0, occurenceMap[seed].size()-1)];
std::cout.put(ch);
seed = seed.substr(1) + ch;
}
std::cout << std::endl;
}
template <typename T>
void printVector(std::vector<T>& vec, std::string separator) {
for (auto it = vec.begin(); it != vec.end(); ++it) {
if (it != vec.begin()) std::cout << separator;
std::cout << *it;
}
}