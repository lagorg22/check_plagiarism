package tetris;
public class PieceTest {
private Piece pyr1, pyr2, pyr3, pyr4, pyrInitialAfterRotations;
private Piece s, sRotated, sInitialAfterRotations;
private Piece s2, s2Rotated, s2InitialAfterRotations;
private Piece l, lRotated1, lRotated2, lRotated3, LInitialAfterRotations;
private Piece l2, l2Rotated1, l2Rotated2, l2Rotated3,  L2InitialAfterRotations;
private Piece stick, stickRotated, stickInitialAfterRotations;
private Piece square, squareInitialAfterRotations;
@Before
public void setUp() throws Exception {
pyr1 = new Piece(Piece.PYRAMID_STR);
pyr2 = pyr1.computeNextRotation();
pyr3 = pyr2.computeNextRotation();
pyr4 = pyr3.computeNextRotation();
pyrInitialAfterRotations = pyr4.computeNextRotation();
s = new Piece(Piece.S1_STR);
sRotated = s.computeNextRotation();
sInitialAfterRotations = sRotated.computeNextRotation();
s2 = new Piece(Piece.S2_STR);
s2Rotated = s2.computeNextRotation();
s2InitialAfterRotations = s2Rotated.computeNextRotation();
l = new Piece(Piece.L1_STR);
lRotated1 = l.computeNextRotation();
lRotated2 = lRotated1.computeNextRotation();
lRotated3 = lRotated2.computeNextRotation();
LInitialAfterRotations = lRotated3.computeNextRotation();
l2 = new Piece(Piece.L2_STR);
l2Rotated1 = l2.computeNextRotation();
l2Rotated2 = l2Rotated1.computeNextRotation();
l2Rotated3 = l2Rotated2.computeNextRotation();
L2InitialAfterRotations = l2Rotated3.computeNextRotation();
stick = new Piece(Piece.STICK_STR);
stickRotated = stick.computeNextRotation();
stickInitialAfterRotations = stickRotated.computeNextRotation();
square = new Piece(Piece.SQUARE_STR);
squareInitialAfterRotations = square.computeNextRotation();
}
@Test
public void testSampleSize() {
assertEquals(3, pyr1.getWidth());
assertEquals(2, pyr1.getHeight());
assertEquals(2, pyr2.getWidth());
assertEquals(3, pyr2.getHeight());
assertEquals(4, stickRotated.getWidth());
assertEquals(1, stickRotated.getHeight());
assertEquals(2, square.getWidth());
assertEquals(2, square.getHeight());
assertEquals(2, l.getWidth());
assertEquals(3, l.getHeight());
assertEquals(2, L2InitialAfterRotations.getWidth());
assertEquals(3, L2InitialAfterRotations.getHeight());
assertEquals(2, sRotated.getWidth());
assertEquals(3, sRotated.getHeight());
}
@Test
public void testSampleSkirt() {
assertTrue(Arrays.equals(new int[] {0, 0, 0}, pyr1.getSkirt()));
assertTrue(Arrays.equals(new int[] {1, 0, 1}, pyr3.getSkirt()));
assertTrue(Arrays.equals(new int[] {0, 0, 1}, s.getSkirt()));
assertTrue(Arrays.equals(new int[] {1, 0}, sRotated.getSkirt()));
}
@Test
public void testEquals(){
assertTrue(l.equals(LInitialAfterRotations));
assertTrue(l2.equals(L2InitialAfterRotations));
assertTrue(square.equals(squareInitialAfterRotations));
assertTrue(pyr1.equals(pyrInitialAfterRotations));
assertTrue(s2.equals(s2InitialAfterRotations));
assertFalse(s.equals(sRotated));
assertFalse(stick.equals(stickRotated));
}
@Test
public void testGetPieces(){
Piece[] pieces =  Piece.getPieces();
assertTrue(pieces[Piece.L1].equals(l));
assertTrue(pieces[Piece.S1].equals(s));
assertTrue(pieces[Piece.L2].equals(l2));
assertTrue(pieces[Piece.SQUARE].equals(square));
assertTrue(pieces[Piece.PYRAMID].equals(pyr1));
assertTrue(pieces[Piece.L1].fastRotation().fastRotation().fastRotation().fastRotation().fastRotation().equals(pieces[Piece.L1].fastRotation()));
assertTrue(pieces[Piece.S1].fastRotation().equals(sRotated));
assertFalse(pieces[Piece.S1].fastRotation().equals(s));
assertFalse(pieces[Piece.S1].equals(sRotated));
}
}