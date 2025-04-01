const double C_0 = -15.59;
const double C_1 = 0.39;
const double C_2 = 11.8;
const std::string sentenceEnd = ".?!";
const std::string syllableCharacters = "aeiouy";
void OpenUserFile(std::ifstream& infile);
void PrintTokens(TokenScanner scanner);
double FleschKincaidGrade(int syllables, int words, int sentences);
void CountTextInformation(TokenScanner scanner, int& syllables,
int& words, int& sentences);
int CountSyllables(std::string word);
void PrintTextInformation(int syllables, int words, int sentences);
int main() {
std::ifstream infile;
OpenUserFile(infile);
TokenScanner scanner(infile);
scanner.ignoreWhitespace();
scanner.addWordCharacters("'");
int syllables, words, sentences;
CountTextInformation(scanner, syllables, words, sentences);
PrintTextInformation(syllables, words, sentences);
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
void PrintTokens(TokenScanner scanner) {
while (scanner.hasMoreTokens()) {
std::string token = scanner.nextToken();
std::cout << "Token: [" << token << "]" << " Type: ("
<< scanner.getTokenType(token) << ")" << std::endl;
}
}
double FleschKincaidGrade(int syllables, int words, int sentences) {
double grade = C_0 + C_1 * (words * 1.0 / sentences) +
C_2 * (syllables * 1.0 / words);
return grade;
}
void CountTextInformation(TokenScanner scanner, int& syllables,
int& words, int& sentences) {
words = 0;
syllables = 0;
sentences = 0;
while (scanner.hasMoreTokens()) {
std::string token = scanner.nextToken();
int syllablesInWord;
TokenType tokenType = scanner.getTokenType(token);
if (tokenType == WORD && isalpha(token[0])) {
syllablesInWord = CountSyllables(token);
words++;
syllables += syllablesInWord;
} else if (tokenType == OPERATOR) {
if (sentenceEnd.find(token) != std::string::npos) {
sentences++;
}
}
}
}
int CountSyllables(std::string token) {
std::vector<std::string> syllables;
token = toLowerCase(token);
int start = -1;
for (int i = 0; i < token.size(); i++) {
if (syllableCharacters.find(token[i]) != std::string::npos) {
if (start == -1) {
start = i;
}
} else {
if (start != -1) {
syllables.push_back(token.substr(start, i-start));
start = -1;
}
}
}
if (start != -1) {
syllables.push_back(token.substr(start));
}
std::string reverseToken = token;
reverse(reverseToken.begin(), reverseToken.end());
if (!syllables.empty() && (syllables.back() == "e") && (reverseToken.find('e') == 0)) {
syllables.pop_back();
}
return syllables.size() == 0 ? 1 : syllables.size();
}
void PrintTextInformation(int syllables, int words, int sentences) {
std::cout << "Words: " << words << std::endl;
std::cout << "Sentences: " << sentences << std::endl;
std::cout << "Syllables: " << syllables << std::endl;
std::cout << "Grade level: " << FleschKincaidGrade(syllables, words, sentences)
<< std::endl;
return;
}