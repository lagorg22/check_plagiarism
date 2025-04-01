class Boggle {
public:
Boggle();
void play();
private:
void drawBoard() const;
void giveInstructions() const;
void welcome() const;
void askBoardSize();
void setBoardCharacters();
void showScore() const;
void loadLexicon();
void setUserString();
void setComputerGeneratedBoard();
void humanTurn();
void computerTurn();
void showScoreForPlayer(const std::vector<std::string>& words) const;
bool isValidWord(std::string word);
bool isWordOnBoard(std::string word, int row, int col);
bool inBounds(int row, int col) const;
void resetUsed();
int calculateScore(const std::vector<std::string>& vec) const;
void findWords(std::string& tillNow, int& row, int& col);
std::vector<std::vector<char> > board;
std::vector<std::vector<bool> > used;
std::vector<std::string> wordsByHuman;
std::vector<std::string> wordsByComputer;
static Lexicon lexicon;
static const std::string STANDARD_CUBES[16];
static const std::string BIG_BOGGLE_CUBES[25];
const std::string kClearCommand = "clear";
const size_t kRegularBoggleSize = 4;
const size_t kBigBoggleSize = 5;
const std::vector<std::pair<int, int> > dp = {
std::make_pair(-1, -1), std::make_pair(-1, 0), std::make_pair(-1, 1),
std::make_pair( 0, -1),                        std::make_pair( 0, 1),
std::make_pair( 1, -1), std::make_pair( 1, 0), std::make_pair( 1, 1)
};
const int kMinWordLength = 4;
};