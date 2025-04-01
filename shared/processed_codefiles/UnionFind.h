class UnionFind {
public:
UnionFind(int n);
~UnionFind();
bool connected(int p, int q) const;
void connect(int p, int q);
int components() const;
int find(int p) const;
private:
int *sz;
int *id;
int count;
};