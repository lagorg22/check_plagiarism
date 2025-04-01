std::set<int> randomSubsetOf(std::set<int>& s);
void OpenUserFile(std::ifstream& infile);
void printSet(std::set<int>& s);
int main() {
std::set<int> s;
std::ifstream input;
OpenUserFile(input);
copy(std::istream_iterator<int>(input), std::istream_iterator<int>(),
inserter(s, s.begin()));
std::set<int> randomSubset = randomSubsetOf(s);
printSet(randomSubset);
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
std::set<int> randomSubsetOf(std::set<int>& s) {
std::set<int> randomSubset;
if (s.size() == 0) return randomSubset;
auto beginIterator = s.begin();
int element = *beginIterator;
s.erase(beginIterator);
if (randomChance(0.5)) {
randomSubset.insert(element);
}
std::set<int> randomSubsetOfRemaining = randomSubsetOf(s);
randomSubset.insert(randomSubsetOfRemaining.begin(), randomSubsetOfRemaining.end());
return randomSubset;
}
void printSet(std::set<int>& s) {
copy(s.begin(), s.end(), std::ostream_iterator<int>(std::cout, ", "));
std::cout << std::endl;
}