int numPathsHome(int street, int avenue);
int main() {
int street, avenue;
street = getInteger("Enter the street number: ");
avenue = getInteger("Enter the avenue number: ");
std::cout << "Number of optimal paths to take back home: " <<
numPathsHome(street, avenue) << std::endl;
return 0;
}
int numPathsHome(int street, int avenue) {
if (street == 1 && avenue == 1) return 1;
else if (street < 0 || avenue < 0) return 0;
else return numPathsHome(street-1, avenue) + numPathsHome(street, avenue-1);
}