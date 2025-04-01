std::set<std::string> listAllRNAStrandsFor(std::string protein,
std::map<char, std::set<std::string> >& codons);
std::map<char, std::set<std::string> > loadCodonMap();
static int x = 0;
int main() {
std::map<char, std::set<std::string> > codons = loadCodonMap();
std::cout << "Enter the input protein: ";
std::string inputProtein;
getline(std::cin, inputProtein);
std::set<std::string> rnaStrands =
listAllRNAStrandsFor(inputProtein, codons);
for (auto it = rnaStrands.begin(); it != rnaStrands.end(); ++it) {
std::cout << *it << std::endl;
}
return 0;
}
std::set<std::string> listAllRNAStrandsFor(std::string protein,
std::map<char, std::set<std::string> >& codons) {
std::set<std::string> rnaStrands;
if (protein.size() == 1) {
for (auto it = codons[protein[0]].begin();
it != codons[protein[0]].end();
++it) {
rnaStrands.insert(*it);
}
return rnaStrands;
}
std::set<std::string> rnaStrandsRemaining =
listAllRNAStrandsFor(protein.substr(1), codons);
for (auto it = codons[protein[0]].begin();
it != codons[protein[0]].end();
++it) {
for (auto it_ = rnaStrandsRemaining.begin();
it_ != rnaStrandsRemaining.end();
++it_) {
rnaStrands.insert((*it) + (*it_));
}
}
return rnaStrands;
}
std::map<char, std::set<std::string> > loadCodonMap() {
std::ifstream input("codons.txt");
std::map<char, std::set<std::string> > result;
std::string codon;
char protein;
while (input >> codon >> protein) {
result[protein].insert(codon);
}
return result;
}