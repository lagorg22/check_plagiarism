const int N_HEADS = 3;
const double P = 0.5;
int SimulateCoinFlipping();
int main() {
int n = SimulateCoinFlipping();
std::cout << "It took " << n << " flips to get " << N_HEADS
<< " consecutive heads." << std::endl;
return 0;
}
int SimulateCoinFlipping() {
int totalTrials = 0;
int consecutiveHeads = 0;
while (true) {
totalTrials++;
if (randomChance(P)) {
std::cout << "heads" << std::endl;
consecutiveHeads++;
if (consecutiveHeads == N_HEADS) break;
} else {
std::cout << "tails" << std::endl;
consecutiveHeads = 0;
}
}
return totalTrials;
}