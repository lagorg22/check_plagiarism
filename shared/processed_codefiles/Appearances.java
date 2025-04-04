package assign1;
public class Appearances {
public static <T> int sameCount(Collection<T> a, Collection<T> b) {
int result = 0;
HashMap<T, Integer> aMap = new HashMap<T, Integer>();
HashMap<T, Integer> bMap = new HashMap<T, Integer>();
calAppearances(a, aMap);
calAppearances(b, bMap);
for (T key : aMap.keySet())
if (bMap.containsKey(key) && bMap.get(key).equals(aMap.get(key)))
result++;
return result;
}
private static <T> void calAppearances(Collection<T> items, HashMap<T, Integer> map) {
for (T item : items) {
if (map.containsKey(item)) map.put(item, map.get(item)+1);
else map.put(item, 1);
}
}
}