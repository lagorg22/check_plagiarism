std::string intToString(int n);
int stringToInt(std::string str);
int main() {
int n = -1729;
std::cout << intToString(n) + "1" << std::endl;
std::cout << stringToInt("-1729") + 1 << std::endl;
return 0;
}
std::string intToString(int n) {
std::stringstream converter;
converter << n;
std::string result;
converter >> result;
return result;
}
int stringToInt(std::string str) {
std::stringstream converter;
converter << str;
int n;
converter >> n;
return n;
}