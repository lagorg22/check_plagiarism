package tetris;
public class TPoint implements Comparable<TPoint> {
public int x;
public int y;
public TPoint(int x, int y) {
this.x = x;
this.y = y;
}
public TPoint(TPoint point) {
this.x = point.x;
this.y = point.y;
}
public boolean equals(Object other) {
if (this == other) return true;
if (!(other instanceof TPoint)) return false;
TPoint pt = (TPoint)other;
return(x==pt.x && y==pt.y);
}
public int compareTo(TPoint other) {
if (!(x == other.x)) return(x-other.x);
else return(y-other.y);
}
public String toString() {
return "(" + x + "," + y + ")";
}
}