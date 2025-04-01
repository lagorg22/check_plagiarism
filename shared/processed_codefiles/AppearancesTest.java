package assign1;
public class AppearancesTest {
private List<String> stringToList(String s) {
List<String> list = new ArrayList<String>();
for (int i=0; i<s.length(); i++) {
list.add(String.valueOf(s.charAt(i)));
}
return list;
}
@Test
public void testSameCount1() {
List<String> a = stringToList("abbccc");
List<String> b = stringToList("cccbba");
assertEquals(3, Appearances.sameCount(a, b));
}
@Test
public void testSameCount2() {
List<Integer> a = Arrays.asList(1, 2, 3, 1, 2, 3, 5);
assertEquals(1, Appearances.sameCount(a, Arrays.asList(1, 9, 9, 1)));
assertEquals(2, Appearances.sameCount(a, Arrays.asList(1, 3, 3, 1)));
assertEquals(1, Appearances.sameCount(a, Arrays.asList(1, 3, 3, 1, 1)));
}
}