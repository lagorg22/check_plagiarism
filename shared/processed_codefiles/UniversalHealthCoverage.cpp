bool canOfferUniversalCoverage(std::set<std::string>& cities,
std::vector< std::set<std::string> >& locations,
int numHospitals,
std::vector< std::set<std::string> >& result);
void printSet(std::set<std::string>& s);
int main() {
std::set<std::string> cities;
cities.insert("A");
cities.insert("B");
cities.insert("C");
cities.insert("D");
cities.insert("E");
cities.insert("F");
std::set<std::string> hospital1;
std::set<std::string> hospital2;
std::set<std::string> hospital3;
std::set<std::string> hospital4;
hospital1.insert("A");
hospital1.insert("B");
hospital2.insert("E");
hospital2.insert("C");
hospital2.insert("D");
hospital2.insert("F");
hospital3.insert("D");
hospital3.insert("E");
hospital4.insert("C");
hospital4.insert("E");
hospital4.insert("F");
std::vector<std::set<std::string> > locations;
locations.push_back(hospital1);
locations.push_back(hospital2);
locations.push_back(hospital3);
locations.push_back(hospital4);
std::vector<std::set<std::string> > result;
int numHospitals;
std::cout << "Enter the number of hospitals to provide full coverage: ";
std::cin >> numHospitals;
if (canOfferUniversalCoverage(cities, locations, numHospitals, result)) {
std::cout << "Yes, full coverage can be provided by following hospitals: "
<< std::endl;
for (auto it = result.begin(); it != result.end(); ++it) {
auto s = *it;
printSet(s);
std::cout << std::endl;
}
} else {
std::cout << "It can't provide full coverage." << std::endl;
}
return 0;
}
void printSet(std::set<std::string>& s) {
std::cout << "{";
for (auto it = s.begin(); it != s.end(); ++it) {
if (it == s.begin()) std::cout << *it;
else std::cout << ", " << *it;
}
std::cout << "}";
}
bool canOfferUniversalCoverage(std::set<std::string>& cities,
std::vector< std::set<std::string> >& locations,
int numHospitals,
std::vector< std::set<std::string> >& result) {
if (numHospitals <= 0 && cities.size() > 0) return false;
else if (cities.size() == 0) return true;
else if (cities.size() > 0 && locations.size() == 0) return false;
else {
std::set<std::string> citiesCovered = locations.back();
locations.pop_back();
std::set<std::string> citiesActuallyCovered;
for (auto it = citiesCovered.begin(); it != citiesCovered.end(); ++it) {
std::string city = *it;
if (cities.erase(city)) {
citiesActuallyCovered.insert(city);
}
}
result.push_back(citiesCovered);
if (canOfferUniversalCoverage(cities, locations, numHospitals-1, result)) {
return true;
}
cities.insert(citiesActuallyCovered.begin(), citiesActuallyCovered.end());
result.pop_back();
if (canOfferUniversalCoverage(cities, locations, numHospitals, result)) {
locations.push_back(citiesCovered);
return true;
} else {
locations.push_back(citiesCovered);
return false;
}
}
}