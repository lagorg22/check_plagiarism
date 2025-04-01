package assign1;
public class StringCode {
public static int maxRun(String str) {
int currun=0, maxrun=0;
if (!str.isEmpty()) {
char prechar=str.charAt(0);
currun++;
maxrun++;
for (int i=1; i<str.length(); i++) {
char curchar = str.charAt(i);
if (curchar==prechar) currun++;
else {
if (currun > maxrun) maxrun=currun;
currun=1;
}
prechar=curchar;
}
}
return maxrun;
}
public static String blowup(String str) {
if (str.isEmpty()) return "";
String result = "";
char ch = str.charAt(0);
int i;
for (i=0; i<str.length()-1; i++) {
char nextCh = str.charAt(i+1);
if (ch >= '0' && ch <= '9') result += genChars(str, ch, nextCh);
else result += ch;
ch = nextCh;
}
if (ch < '0' || ch > '9') result += ch;
return result;
}
private static String genChars(String str, char ch, char nextCh) {
String result = "";
int rep = Character.getNumericValue(ch);
for (int i=0; i<rep; i++)
result += nextCh;
return result;
}
public static boolean stringIntersect(String a, String b, int len) {
HashSet<String> strDic = new HashSet<String>();
for (int i=0; i<=a.length()-len; i++) {
String sub = a.substring(i, i+len);
strDic.add(sub);
}
for (int i=0; i<=b.length()-len; i++) {
String sub = b.substring(i, i+len);
if (strDic.contains(sub)) return true;
}
return false;
}
}