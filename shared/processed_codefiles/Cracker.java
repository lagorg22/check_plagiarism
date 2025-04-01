package crackerAssign;
public class Cracker {
public static final char[] CHARS = "abcdefghijklmnopqrstuvwxyz0123456789.,-!".toCharArray();
public static final int MAX_WORKERS = CHARS.length;
public static String hexToString(byte[] bytes) {
StringBuffer buff = new StringBuffer();
for (int i=0; i<bytes.length; i++) {
int val = bytes[i];
val = val & 0xff;  // remove higher bits, sign
if (val<16) buff.append('0'); // leading 0
buff.append(Integer.toString(val, 16));
}
return buff.toString();
}
public static byte[] hexToArray(String hex) {
byte[] result = new byte[hex.length()/2];
for (int i=0; i<hex.length(); i+=2) {
result[i/2] = (byte) Integer.parseInt(hex.substring(i, i+2), 16);
}
return result;
}
public static byte[] genHash(String pw) {
MessageDigest md;
try {
md = MessageDigest.getInstance("SHA");
md.update(pw.getBytes());
return md.digest();
} catch (NoSuchAlgorithmException e) {
e.printStackTrace();
}
return null;
}
public static class Worker extends Thread {
int step;
int index;
int length;
byte[] hashBytes;
public Worker(int i, int s, int l, String hash, byte[] hb) {
index = i;
step = s;
length = l;
hashBytes = hb;
}
@Override
public void run() {
int start = index * step;
int tmp = (index + 1) * step;
int end = (tmp+step > MAX_WORKERS) ? MAX_WORKERS : tmp;
for (int i = start; i < end; i++)
crackHash("" + CHARS[i]);
latch.countDown();
}
public void crackHash(String result) {
if (result.length() <= length) {
if (Arrays.equals(hashBytes, genHash(result)))
System.out.println(result);
for (char ch : CHARS)
crackHash(result + ch);
}
}
}
static CountDownLatch latch;
public static void main(String[] args) {
if (args.length == 1) {
System.out.println(hexToString(genHash(args[0])));
} else if (args.length == 3) {
try {
int maxLength = Integer.parseInt(args[1]);
int numOfWorkers = Integer.parseInt(args[2]);
byte[] hashBytes = hexToArray(args[0]);
latch = new CountDownLatch(numOfWorkers);
int step = MAX_WORKERS / numOfWorkers;
for (int i = 0; i < numOfWorkers; i++)
new Worker(i, step, maxLength, args[0], hashBytes).start();
try { latch.await(); }
catch (InterruptedException ignored) {}
System.out.println("All done");
} catch (Exception ignored) { hintAndExit(); }
} else {
hintAndExit();
}
}
private static void hintAndExit() {
System.out.println("Usage: Cracker password / Cracker pwHash max_length num_of_thread");
System.exit(1);
}
}