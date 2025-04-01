// Test cases for CharGrid -- a few basic tests are provided.
package assign1;

import static org.junit.Assert.*;
import org.junit.Test;

public class CharGridTest {
	
	@Test
	public void testCharArea1() {
		char[][] grid = new char[][] {
				{'a', 'y', ' '},
				{'x', 'a', 'z'},
			};
		
		
		CharGrid cg = new CharGrid(grid);
				
		assertEquals(4, cg.charArea('a'));
		assertEquals(1, cg.charArea('z'));
	}
	
	
	@Test
	public void testCharArea2() {
		char[][] grid = new char[][] {
				{'c', 'a', ' '},
				{'b', ' ', 'b'},
				{' ', ' ', 'a'}
			};
		
		CharGrid cg = new CharGrid(grid);
		
		assertEquals(6, cg.charArea('a'));
		assertEquals(9, cg.charArea(' '));
		assertEquals(1, cg.charArea('c'));
	}
	
	@Test
	public void testCharArea3() {
		char[][] grid = new char[][] {
				{'c'},
				{'b'},
				{' '}
			};
		
		CharGrid cg = new CharGrid(grid);
		
		assertEquals(0, cg.charArea('a'));
		assertEquals(1, cg.charArea('b'));
		assertEquals(1, cg.charArea('c'));
	}	
	
	@Test
	public void testcountPlus() {
		char[][] grid = new char[][] {
			{' ', ' ', ' '},
			{' ', ' ', 'a'},
			{' ', ' ', ' '}
		};
	
		CharGrid cg = new CharGrid(grid);
				
		assertEquals(0, cg.countPlus());
	}
	
    @Test
    public void countPlusTestSimple2CellPlus() {
        char[][] grid = new char[][]{
                {' ', ' ', 'v', ' ', ' '},
                {' ', ' ', 'v', ' ', ' '},
                {'v', 'v', 'v', 'v', 'v'},
                {' ', ' ', 'v', ' ', ' '},
                {' ', ' ', 'v', ' ', ' '}
        };

        CharGrid cg = new CharGrid(grid);

        assertEquals(1, cg.countPlus());
    }

    @Test
    public void countPlusTest2CellAnd1Cell2Pluses() {
        char[][] grid = new char[][]{
                {'c', 'v', ' ', 'a', ' ', 'a', ' ', 'a', ' '},
                {'v', 'v', 'v', 'a', ' ', 'v', ' ', 'a', ' '},
                {' ', 'v', ' ', 'a', ' ', 'v', ' ', 'a', ' '},
                {' ', ' ', ' ', 'v', 'v', 'v', 'v', 'v', ' '},
                {' ', 'a', ' ', 'a', ' ', 'v', ' ', 'a', ' '},
                {' ', 'a', ' ', 'a', ' ', 'v', ' ', 'a', ' '}
        };

        CharGrid cg = new CharGrid(grid);

        assertEquals(2, cg.countPlus());
    }

    @Test
    public void countPlusTestOnlyFirstRow() {
        char[][] grid = new char[][]{
                {'c', 'c', 'c'}
        };

        CharGrid cg = new CharGrid(grid);

        assertEquals(0, cg.countPlus());
    }

    @Test
    public void countPlusTestOnlyFirstCol() {
        char[][] grid = new char[][]{
                {'a'},
                {'a'},
                {'a'}

        };

        CharGrid cg = new CharGrid(grid);

        assertEquals(0, cg.countPlus());
    }

    @Test
    public void countPlusTestOneSideExtraCell() {
        char[][] grid = new char[][]{
                {'c', 'v', ' '},
                {'v', 'v', 'v'},
                {' ', 'v', ' '},
                {' ', 'v', ' '},

        };

        CharGrid cg = new CharGrid(grid);

        assertEquals(0, cg.countPlus());
    }

    @Test
    public void countPlusTestEmptyGrid() {
        char[][] grid = new char[][]{};

        CharGrid cg = new CharGrid(grid);

        assertEquals(0, cg.countPlus());
    }

    @Test
    public void countPlusTestSameLetterFilledGrid() {
        char[][] grid = new char[][]{
                {'v', 'v', 'v'},
                {'v', 'v', 'v'},
                {'v', 'v', 'v'},

        };

        CharGrid cg = new CharGrid(grid);

        assertEquals(1, cg.countPlus());
    }

    @Test
    public void countPlusTestSingleCell() {
        char[][] grid = new char[][]{
                {'c'}
        };

        CharGrid cg = new CharGrid(grid);

        assertEquals(0, cg.countPlus());
    }
}
