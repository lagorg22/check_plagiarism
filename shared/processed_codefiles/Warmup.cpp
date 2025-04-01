using namespace std;
const int HASH_SEED = 5381;
const int HASH_MULTIPLIER = 33;
const int HASH_MASK = unsigned(-1) >> 1;
int hashCode(string key);
int main() {
string name = getLine("Please enter your name: ");
int code = hashCode(name);
cout << "The hash code for your name is " << code << "." << endl;
return 0;
}
int hashCode(string str) {
unsigned hash = HASH_SEED;
int nchars = str.length();
for (int i = 0; i < nchars; i++) {
hash = HASH_MULTIPLIER * hash + str[i];
}
return (hash & HASH_MASK);
}