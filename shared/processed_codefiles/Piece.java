package tetris;
public class Piece {
private TPoint[] body;
private int[] skirt;
private int width;
private int height;
private Piece next; // "next" rotation
static private Piece[] pieces;	// singleton static array of first rotations
public Piece(TPoint[] points) {
body = points;
Arrays.sort(body);
width = 1;
height = 1;
for (TPoint p: body) {
if (p.x >= width) width = p.x + 1;
if (p.y >= height) height = p.y + 1;
}
skirt = new int[width];
Arrays.fill(skirt, height);
for (TPoint p: body) {
if (skirt[p.x] > p.y) skirt[p.x] = p.y;
}
}
public Piece(String points) {
this(parsePoints(points));
}
public int getWidth() {
return width;
}
public int getHeight() {
return height;
}
public TPoint[] getBody() {
return body;
}
public int[] getSkirt() {
return skirt;
}
public Piece computeNextRotation() {
TPoint[] nextBody = new TPoint[body.length];
for (int i = 0; i < body.length; i++)
nextBody[i] = new TPoint(height-body[i].y-1, body[i].x);
return new Piece(nextBody);
}
public Piece fastRotation() {
return next;
}
public boolean equals(Object obj) {
if (obj == this) return true;
if (!(obj instanceof Piece)) return false;
Piece other = (Piece)obj;
return  Arrays.equals(body, other.body);
}
public static final String STICK_STR	= "0 0	0 1	 0 2  0 3";
public static final String L1_STR		= "0 0	0 1	 0 2  1 0";
public static final String L2_STR		= "0 0	1 0 1 1	 1 2";
public static final String S1_STR		= "0 0	1 0	 1 1  2 1";
public static final String S2_STR		= "0 1	1 1  1 0  2 0";
public static final String SQUARE_STR	= "0 0  0 1  1 0  1 1";
public static final String PYRAMID_STR	= "0 0  1 0  1 1  2 0";
public static final int STICK = 0;
public static final int L1	  = 1;
public static final int L2	  = 2;
public static final int S1	  = 3;
public static final int S2	  = 4;
public static final int SQUARE	= 5;
public static final int PYRAMID = 6;
public static Piece[] getPieces() {
if (Piece.pieces==null) {
Piece.pieces = new Piece[] {
makeFastRotations(new Piece(STICK_STR)),
makeFastRotations(new Piece(L1_STR)),
makeFastRotations(new Piece(L2_STR)),
makeFastRotations(new Piece(S1_STR)),
makeFastRotations(new Piece(S2_STR)),
makeFastRotations(new Piece(SQUARE_STR)),
makeFastRotations(new Piece(PYRAMID_STR)),
};
}
return Piece.pieces;
}
private static Piece makeFastRotations(Piece root) {
Piece pre = root;
Piece curr = root.computeNextRotation();
root.next = curr;
while (!root.equals(curr)) {
pre = curr;
curr.next = curr.computeNextRotation();
curr = curr.next;
}
pre.next = root;
return root;
}
private static TPoint[] parsePoints(String string) {
List<TPoint> points = new ArrayList<TPoint>();
StringTokenizer tok = new StringTokenizer(string);
try {
while(tok.hasMoreTokens()) {
int x = Integer.parseInt(tok.nextToken());
int y = Integer.parseInt(tok.nextToken());
points.add(new TPoint(x, y));
}
}
catch (NumberFormatException e) {
throw new RuntimeException("Could not parse x,y string:" + string);
}
TPoint[] array = points.toArray(new TPoint[0]);
return array;
}
}