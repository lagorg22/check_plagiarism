bool isSubsequence(std::string text, std::string subsequence);
int main() {
std::string text, subsequence;
std::cout << "Enter the text: ";
getline(std::cin, text);
std::cout << "Enter the subsequence to search for: ";
getline(std::cin, subsequence);
std::cout << "Is \"" << subsequence << "\" a subsequence of \"" << text
<< "\" ? : " << std::boolalpha << isSubsequence(text, subsequence);
std::cout << std::endl;
}
bool isSubsequence(std::string text, std::string subsequence) {
if (subsequence.size() == 0) return true;
if (text.size() == 0 && subsequence.size() != 0) return false;
if (text[0] == subsequence[0]) {
return isSubsequence(text.substr(1), subsequence.substr(1));
}
else {
return isSubsequence(text.substr(1), subsequence);
}
}