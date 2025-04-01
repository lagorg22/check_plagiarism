package assign1;
public class Taboo<T> {
private HashMap<T, HashSet<T>> tabooMap;
public Taboo(List<T> rules) {
tabooMap = new HashMap<T, HashSet<T>>();
T key = null;
for (T rule : rules) {
if (key != null && rule != null) {
if (!tabooMap.containsKey(key))
tabooMap.put(key, new HashSet<T>());
tabooMap.get(key).add(rule);
}
key = rule;
}
}
public Set<T> noFollow(T elem) {
if (tabooMap.containsKey(elem))
return tabooMap.get(elem);
else
return Collections.emptySet();
}
public void reduce(List<T> list) {
Iterator<T> it = list.iterator();
T last = null;
while (it.hasNext()) {
T curr = it.next();
if (last != null && tabooMap.containsKey(last) && tabooMap.get(last).contains(curr))
it.remove();
else last = curr;
}
}
}