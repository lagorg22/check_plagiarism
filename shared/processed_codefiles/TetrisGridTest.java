package assign1;
public class TetrisGridTest {
@Test
public void testClear1() {
boolean[][] before =
{
{true, true, false, },
{false, true, true, }
};
boolean[][] after =
{
{true, false, false},
{false, true, false}
};
TetrisGrid tetris = new TetrisGrid(before);
tetris.clearRows();
assertTrue( Arrays.deepEquals(after, tetris.getGrid()) );
}
@Test
public void testClear2() {
boolean[][] before =
{
{true, false, false, },
{false, true, true, },
{false, true, true, }
};
boolean[][] after =
{
{true, false, false },
{false, true, true },
{false, true, true, }
};
TetrisGrid tetris = new TetrisGrid(before);
tetris.clearRows();
assertTrue( Arrays.deepEquals(after, tetris.getGrid()) );
}
@Test
public void testClear3() {
boolean[][] before =
{
{true, true, false, },
{true, true, true, },
{true, true, true, }
};
boolean[][] after =
{
{false, false, false },
{true, false, false },
{true, false, false, }
};
TetrisGrid tetris = new TetrisGrid(before);
tetris.clearRows();
assertTrue( Arrays.deepEquals(after, tetris.getGrid()) );
}
}