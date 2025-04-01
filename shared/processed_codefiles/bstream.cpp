static const int NUM_BITS_IN_BYTE = 8;
inline int GetNthBit(int n, int fromByte) { return ((fromByte & (1 << n)) != 0); }
inline void SetNthBit(int n, int & inByte) { inByte |= (1 << n); }
ibstream::ibstream() : istream(NULL), lastTell(0), curByte(0), pos(NUM_BITS_IN_BYTE) {}
int ibstream::readBit() {
if (!is_open()) error("Cannot read a bit from a stream that is not open.");
if (lastTell != tellg() || pos == NUM_BITS_IN_BYTE) {
if ((curByte = get()) == EOF) // read next single byte from file
return EOF;
pos = 0; // start reading from first bit of new byte
lastTell = tellg();
}
int result = GetNthBit(pos, curByte);
pos++; // advance bit position for next call to readBit
return result;
}
void ibstream::rewind() {
if (!is_open()) error("Cannot rewind stream which is not open.");
clear();
seekg(0, ios::beg);
}
long ibstream::size() {
if (!is_open()) error("Cannot get size of stream which is not open.");
clear();					// clear any error state
streampos cur = tellg();	// save current streampos
seekg(0, ios::end);			// seek to end
streampos end = tellg();	// get offset
seekg(cur);					// seek back to original pos
return long(end);
}
bool ibstream::is_open() {
return true;
}
obstream::obstream() : ostream(NULL), lastTell(0), curByte(0), pos(NUM_BITS_IN_BYTE) {}
void obstream::writeBit(int bit) {
if (bit != 0 && bit != 1) error("writeBit expects argument which can be only 0 or 1.");
if (!is_open()) error("Cannot writeBit to stream which is not open.");
if (lastTell != tellp() || pos == NUM_BITS_IN_BYTE) {
curByte = 0; // zero out byte for next writes
pos = 0;	// start writing to first bit of new byte
}
if (bit) // only need to change if bit needs to be 1 (byte starts already zeroed)
SetNthBit(pos, curByte);
if (pos == 0 || bit) { // only write if first bit in byte or changing 0 to 1
if (pos != 0) seekp(-1, ios::cur); // back up to overwite if pos > 0
put(curByte);
}
pos++; // advance to next bit position for next write
lastTell = tellp();
}
long obstream::size() {
if (!is_open()) error("Cannot get size of stream which is not open.");
clear();					// clear any error state
streampos cur = tellp();	// save current streampos
seekp(0, ios::end);			// seek to end
streampos end = tellp();	// get offset
seekp(cur);					// seek back to original pos
return long(end);
}
bool obstream::is_open() {
return true;
}
ifbstream::ifbstream() {
init(&fb);
}
ifbstream::ifbstream(const char* filename) {
init(&fb);
open(filename);
}
ifbstream::ifbstream(string filename) {
init(&fb);
open(filename);
}
void ifbstream::open(const char* filename) {
if (!fb.open(filename, ios::in | ios::binary))
setstate(ios::failbit);
}
void ifbstream::open(string filename) {
open(filename.c_str());
}
bool ifbstream::is_open() {
return fb.is_open();
}
void ifbstream::close() {
if (!fb.close())
setstate(ios::failbit);
}
ofbstream::ofbstream() {
init(&fb);
}
ofbstream::ofbstream(const char* filename) {
init(&fb);
open(filename);
}
ofbstream::ofbstream(string filename) {
init(&fb);
open(filename);
}
void ofbstream::open(const char* filename) {
if (endsWith(filename, ".cpp") || endsWith(filename, ".h") ||
endsWith(filename, ".hh") || endsWith(filename, ".cc")) {
cerr << "It is potentially extremely dangerous to write to file "
<< filename << ", because that might be your own source code.	"
<< "We're explicitly disallowing this operation.	 Please choose a "
<< "different filename." << endl;
setstate(ios::failbit);
} else {
if (!fb.open(filename, ios::out | ios::binary))
setstate(ios::failbit);
}
}
void ofbstream::open(string filename) {
open(filename.c_str());
}
bool ofbstream::is_open() {
return fb.is_open();
}
void ofbstream::close() {
if (!fb.close())
setstate(ios::failbit);
}
istringbstream::istringbstream(string s) {
init(&sb);
sb.str(s);
}
void istringbstream::str(string s) {
sb.str(s);
}
ostringbstream::ostringbstream() {
init(&sb);
}
string ostringbstream::str() {
return sb.str();
}