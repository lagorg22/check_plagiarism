struct Loc {
int row;
int col;
};
Loc makeLoc(int row, int col);
enum Color {
GRAY, YELLOW, GREEN
};
struct Edge {
Loc start;
Loc end;
};
Edge makeEdge(Loc start, Loc end);
bool operator <	 (Loc lhs, Loc rhs);
bool operator >	 (Loc lhs, Loc rhs);
bool operator == (Loc lhs, Loc rhs);
bool operator != (Loc lhs, Loc rhs);
bool operator <= (Loc lhs, Loc rhs);
bool operator >= (Loc lhs, Loc rhs);
bool operator <	 (Edge lhs, Edge rhs);
bool operator >	 (Edge lhs, Edge rhs);
bool operator == (Edge lhs, Edge rhs);
bool operator != (Edge lhs, Edge rhs);
bool operator <= (Edge lhs, Edge rhs);
bool operator >= (Edge lhs, Edge rhs);
int hashCode(Loc l);
int hashCode(Edge e);