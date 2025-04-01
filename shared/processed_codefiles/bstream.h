using namespace std;
class ibstream: public istream {
public:
ibstream();
int readBit();
void rewind();
long size();
virtual bool is_open();
private:
int pos, curByte;
streampos lastTell;
};
class obstream: public ostream {
public:
obstream();
void writeBit(int bit);
long size();
virtual bool is_open();
private:
int pos, curByte;
streampos lastTell;
};
class ifbstream: public ibstream {
public:
ifbstream();
ifbstream(const char* filename);
ifbstream(string filename);
void open(const char* filename);
void open(string filename);
bool is_open();
void close();
private:
filebuf fb;
};
class ofbstream: public obstream {
public:
ofbstream();
ofbstream(const char* filename);
ofbstream(string filename);
void open(const char* filename);
void open(string filename);
bool is_open();
void close();
private:
filebuf fb;
};
class istringbstream: public ibstream {
public:
istringbstream(string s = "");
void str(string s);
private:
stringbuf sb;
};
class ostringbstream: public obstream {
public:
ostringbstream();
string str();
private:
stringbuf sb;
};