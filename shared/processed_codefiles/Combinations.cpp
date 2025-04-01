int choose(int n, int k);
int main() {
std::cout << "Calculate the value of n choose k." << std::endl;
int n = getInteger("Enter the value of n: ");
int k = getInteger("Enter the value of k: ");
std::cout << "The value of choose(n, k) is " << choose(n, k) << std::endl;
return 0;
}
int choose(int n, int k) {
if (k == 0 || k == n) return 1;
else return choose(n-1, k-1) + choose(n-1, k);
}