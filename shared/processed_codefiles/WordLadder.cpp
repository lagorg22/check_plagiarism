const std::string alphabets = "abcdefghijklmnopqrstuvwxyz";
std::vector<std::string> findLadder(std::string source, std::string destination,
Lexicon& lexicon);
template <typename T>
void printVector(std::vector<T>& vec, std::string separator);
std::set<std::string> oneDistanceWords(std::string word, Lexicon& lexicon);
int main() {
Lexicon english("EnglishWords.txt");
while (true) {
std::string source, destination;
std::cout << "Enter start word (RETURN to quit): ";
getline(std::cin, source);
if (source.size() == 0) {	 // RETURN has been entered
std::cout << "GoodBye !" << std::endl;
break;
}
std::cout << "Enter the ending word: ";
getline(std::cin, destination);
std::cout << "Searching..." << std::endl;
std::vector<std::string> ladder;
if (english.contains(source) && english.contains(destination)) {
ladder = findLadder(source, destination,
english);
}
if (ladder.size() > 0) {
std::cout << "Ladder found: ";
printVector(ladder, " -> ");
std::cout << std::endl;
} else {
std::cout << "No word ladder could be find." << std::endl;
}
std::cout << std::endl;
}
std::cout << std::endl;
return 0;
}
std::vector<std::string> findLadder(std::string source, std::string destination,
Lexicon& lexicon) {
std::vector<std::string> ladder;
std::queue<std::vector<std::string> > bfsQueue;
ladder.push_back(source);
std::set<std::string> wordsSeen;
bfsQueue.push(ladder);
vector<std::string> currentLadder;
wordsSeen.insert(source);
while (!bfsQueue.empty()) {
currentLadder = bfsQueue.front();
bfsQueue.pop();
if (currentLadder.back() == destination) {
return currentLadder;
}
std::set<std::string> wordsOneDistanceAway;
wordsOneDistanceAway = oneDistanceWords(currentLadder.back(),
lexicon);
for (auto it = wordsOneDistanceAway.begin();
it != wordsOneDistanceAway.end();
++it) {
if (wordsSeen.count(*it) == 0) {
std::vector<std::string> nextLadder(currentLadder);
nextLadder.push_back(*it);
wordsSeen.insert(*it);
bfsQueue.push(nextLadder);
}
}
}
ladder.clear();
return ladder;
}
std::set<std::string> oneDistanceWords(std::string word, Lexicon& lexicon) {
std::set<std::string> words;
std::string wordCopy = word;
for (size_t i = 0; i < word.size(); i++) {
for (size_t j = 0; j < alphabets.size(); j++) {
word[i] = alphabets[j];
if (word != wordCopy && lexicon.contains(word)) {
words.insert(word);
}
}
word = wordCopy;
}
return words;
}
template <typename T>
void printVector(std::vector<T>& vec, std::string separator) {
for (auto it = vec.begin(); it != vec.end(); ++it) {
if (it != vec.begin()) std::cout << separator;
std::cout << *it;
}
}