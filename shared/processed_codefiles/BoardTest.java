package tetris;
public class BoardTest {
Board b;
Piece pyr1, pyr2, pyr3, pyr4, s, sRotated;
Piece l;
@Before
public void setUp() throws Exception {
b = new Board(3, 6);
pyr1 = new Piece(Piece.PYRAMID_STR);
pyr2 = pyr1.computeNextRotation();
pyr3 = pyr2.computeNextRotation();
pyr4 = pyr3.computeNextRotation();
s = new Piece(Piece.S1_STR);
sRotated = s.computeNextRotation();
b.place(pyr1, 0, 0);
}
@Test
public void testSample1() {
assertEquals(1, b.getColumnHeight(0));
assertEquals(2, b.getColumnHeight(1));
assertEquals(2, b.getMaxHeight());
assertEquals(3, b.getRowWidth(0));
assertEquals(1, b.getRowWidth(1));
assertEquals(0, b.getRowWidth(2));
}
@Test
public void testSample2() {
b.commit();
int result = b.place(sRotated, 1, 1);
assertEquals(Board.PLACE_OK, result);
assertEquals(1, b.getColumnHeight(0));
assertEquals(4, b.getColumnHeight(1));
assertEquals(3, b.getColumnHeight(2));
assertEquals(4, b.getMaxHeight());
}
@Test
public void testClearRows() {
b.clearRows();
assertEquals(0, b.getColumnHeight(0));
assertEquals(1, b.getColumnHeight(1));
assertEquals(1, b.getMaxHeight());
assertEquals(1, b.getRowWidth(0));
assertEquals(0, b.getRowWidth(1));
b.commit();
b.place(pyr2, 1, 0);
b.clearRows();
Piece[] pieces = Piece.getPieces();
l = pieces[Piece.L2];
l = l.fastRotation();
l = l.fastRotation();
b.commit();
b.place(l,0, b.dropHeight(l,0));
b.clearRows();
assertEquals(0, b.getColumnHeight(1));
assertEquals(0, b.getMaxHeight());
assertEquals(0, b.getRowWidth(0));
}
@Test
public void testUndo(){
b.undo();
assertEquals(0, b.getColumnHeight(1));
assertEquals(0, b.getMaxHeight());
assertEquals(0, b.getRowWidth(0));
}
@Test
public void testDropPiece(){
b = new Board(10, 10);
int y = 3;
while (b.place(sRotated, 5, b.dropHeight(sRotated, 5)) != Board.PLACE_OUT_BOUNDS) {
assertEquals(y, b.getMaxHeight());
y += 2;
b.commit();
}
}
@Test
public void testCommits(){
b = new Board(3, 6);
b.commit();
b.place(s, 0, b.dropHeight(s,0));
b.clearRows();
b.clearRows();
b.commit();
b.place(s,0,b.dropHeight(s,0));
b.clearRows();
b.commit();
b.place(s,0,b.dropHeight(s,0));
b.clearRows();
b.commit();
assertEquals(5, b.getColumnHeight(0));
assertEquals(6, b.getColumnHeight(1));
assertEquals(6, b.getMaxHeight());
assertEquals(2, b.getRowWidth(0));
assertEquals(2, b.getRowWidth(1));
assertEquals(2, b.getRowWidth(2));
}
}