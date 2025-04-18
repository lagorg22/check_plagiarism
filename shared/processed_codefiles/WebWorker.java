package webLoaderAssign;
public class WebWorker extends Thread {
private String urlString;
private int rowToUpdate;
private WebFrame frame;
private String status;
private static final String ERROR = "err";
private static final String INT = "interrupted";
public WebWorker(String u, int r, WebFrame f) {
urlString = u;
rowToUpdate = r;
frame = f;
}
public void run() {
frame.runCount.incrementAndGet();
frame.launcher.showRun();
download();
frame.releaseWorker(status, rowToUpdate);
}
public void download() {
InputStream input = null;
StringBuilder contents = null;
try {
URL url = new URL(urlString);
URLConnection connection = url.openConnection();
connection.setConnectTimeout(5000);
connection.connect();
input = connection.getInputStream();
BufferedReader reader  = new BufferedReader(new InputStreamReader(input));
long startTime = System.currentTimeMillis();
int size = 0;
char[] array = new char[1000];
int len;
contents = new StringBuilder(1000);
while ((len = reader.read(array, 0, array.length)) > 0) {
contents.append(array, 0, len);
if (isInterrupted()) {
status = INT;
break;
}
size += len;
Thread.sleep(100);
}
long finishTime = System.currentTimeMillis();
status = new SimpleDateFormat("HH:mm:ss").format(new Date(finishTime)) + "  " + (finishTime - startTime) + "ms  " + size + "bytes";
}
catch(MalformedURLException ignored) {
status = ERROR;
}
catch(InterruptedException exception) {
status = INT;
}
catch(IOException ignored) {
status = ERROR;
}
finally {
try{
if (input != null) input.close();
}
catch(IOException ignored) {}
}
}
}