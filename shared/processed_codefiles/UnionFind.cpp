UnionFind::UnionFind(int n) {
id = new int[n];
sz = new int[n];
count = n;
for (int i = 0; i < n; i++) {
id[i] = i;
sz[i] = 1;
}
}
UnionFind::~UnionFind() {
delete id;
delete sz;
}
int UnionFind::find(int p) const {
while (p != id[p]) {
id[p] = id[id[p]];
p = id[p];
}
return p;
}
int UnionFind::components() const {
return count;
}
bool UnionFind::connected(int p, int q) const {
if (find(p) == find(q)) return true;
return false;
}
void UnionFind::connect(int p, int q) {
int i = find(p);
int j = find(q);
if (i == j) return;
if (sz[i] < sz[j]) {
id[i] = j;
sz[i] += sz[j];
} else {
id[j] = i;
sz[i] += sz[j];
}
count--;
}