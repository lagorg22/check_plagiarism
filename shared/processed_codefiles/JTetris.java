package tetris;
public class JTetris extends JComponent {
public static final int WIDTH = 10;
public static final int HEIGHT = 20;
public static final int TOP_SPACE = 4;
protected boolean testMode = false;
public final int TEST_LIMIT = 100;
protected boolean DRAW_OPTIMIZE = false;
protected Board board;
protected Piece[] pieces;
protected Piece currentPiece;
protected int currentX;
protected int currentY;
protected boolean moved;	// did the player move the piece
protected Piece newPiece;
protected int newX;
protected int newY;
protected boolean gameOn;	// true if we are playing
protected int count;		 // how many pieces played so far
protected long startTime;	// used to measure elapsed time
protected Random random;	 // the random generator for new pieces
protected JLabel countLabel;
protected JLabel scoreLabel;
protected int score;
protected JLabel timeLabel;
protected JButton startButton;
protected JButton stopButton;
protected javax.swing.Timer timer;
protected JSlider speed;
protected JCheckBox testButton;
public final int DELAY = 400;	// milliseconds per tick
JTetris(int pixels) {
super();
setPreferredSize(new Dimension((WIDTH * pixels)+2,
(HEIGHT+TOP_SPACE)*pixels+2));
gameOn = false;
pieces = Piece.getPieces();
board = new Board(WIDTH, HEIGHT + TOP_SPACE);
registerKeyboardAction(
new ActionListener() {
public void actionPerformed(ActionEvent e) {
tick(LEFT);
}
}, "left", KeyStroke.getKeyStroke('4'), WHEN_IN_FOCUSED_WINDOW
);
registerKeyboardAction(
new ActionListener() {
public void actionPerformed(ActionEvent e) {
tick(LEFT);
}
}, "left", KeyStroke.getKeyStroke('j'), WHEN_IN_FOCUSED_WINDOW
);
registerKeyboardAction(
new ActionListener() {
public void actionPerformed(ActionEvent e) {
tick(RIGHT);
}
}, "right", KeyStroke.getKeyStroke('6'), WHEN_IN_FOCUSED_WINDOW
);
registerKeyboardAction(
new ActionListener() {
public void actionPerformed(ActionEvent e) {
tick(RIGHT);
}
}, "right", KeyStroke.getKeyStroke('l'), WHEN_IN_FOCUSED_WINDOW
);
registerKeyboardAction(
new ActionListener() {
public void actionPerformed(ActionEvent e) {
tick(ROTATE);
}
}, "rotate", KeyStroke.getKeyStroke('5'), WHEN_IN_FOCUSED_WINDOW
);
registerKeyboardAction(
new ActionListener() {
public void actionPerformed(ActionEvent e) {
tick(ROTATE);
}
}, "rotate", KeyStroke.getKeyStroke('k'), WHEN_IN_FOCUSED_WINDOW
);
registerKeyboardAction(
new ActionListener() {
public void actionPerformed(ActionEvent e) {
tick(DROP);
}
}, "drop", KeyStroke.getKeyStroke('0'), WHEN_IN_FOCUSED_WINDOW
);
registerKeyboardAction(
new ActionListener() {
public void actionPerformed(ActionEvent e) {
tick(DROP);
}
}, "drop", KeyStroke.getKeyStroke('n'), WHEN_IN_FOCUSED_WINDOW
);
timer = new javax.swing.Timer(DELAY, new ActionListener() {
public void actionPerformed(ActionEvent e) {
tick(DOWN);
}
});
requestFocusInWindow();
}
public void startGame() {
board = new Board(WIDTH, HEIGHT + TOP_SPACE);
repaint();
count = 0;
score = 0;
updateCounters();
gameOn = true;
testMode = testButton.isSelected();
if (testMode) random = new Random(0);	// same seq every time
else random = new Random(); // diff seq each game
enableButtons();
timeLabel.setText(" ");
addNewPiece();
timer.start();
startTime = System.currentTimeMillis();
}
private void enableButtons() {
startButton.setEnabled(!gameOn);
stopButton.setEnabled(gameOn);
}
public void stopGame() {
gameOn = false;
enableButtons();
timer.stop();
long delta = (System.currentTimeMillis() - startTime)/10;
timeLabel.setText(Double.toString(delta/100.0) + " seconds");
}
public int setCurrent(Piece piece, int x, int y) {
int result = board.place(piece, x, y);
if (result <= Board.PLACE_ROW_FILLED) { // SUCESS
if (currentPiece != null) repaintPiece(currentPiece, currentX, currentY);
currentPiece = piece;
currentX = x;
currentY = y;
repaintPiece(currentPiece, currentX, currentY);
}
else {
board.undo();
}
return(result);
}
public Piece pickNextPiece() {
int pieceNum;
pieceNum = (int) (pieces.length * random.nextDouble());
Piece piece	 = pieces[pieceNum];
return(piece);
}
public void addNewPiece() {
count++;
score++;
if (testMode && count == TEST_LIMIT+1) {
stopGame();
return;
}
board.commit();
currentPiece = null;
Piece piece = pickNextPiece();
int px = (board.getWidth() - piece.getWidth())/2;
int py = board.getHeight() - piece.getHeight();
int result = setCurrent(piece, px, py);
if (result>Board.PLACE_ROW_FILLED) {
stopGame();
}
updateCounters();
}
private void updateCounters() {
countLabel.setText("Pieces " + count);
scoreLabel.setText("Score " + score);
}
public void computeNewPosition(int verb) {
newPiece = currentPiece;
newX = currentX;
newY = currentY;
switch (verb) {
case LEFT: newX--; break;
case RIGHT: newX++; break;
case ROTATE:
newPiece = newPiece.fastRotation();
newX = newX + (currentPiece.getWidth() - newPiece.getWidth())/2;
newY = newY + (currentPiece.getHeight() - newPiece.getHeight())/2;
break;
case DOWN: newY--; break;
case DROP:
newY = board.dropHeight(newPiece, newX);
if (newY > currentY) {
newY = currentY;
}
break;
default:
throw new RuntimeException("Bad verb");
}
}
public static final int ROTATE = 0;
public static final int LEFT = 1;
public static final int RIGHT = 2;
public static final int DROP = 3;
public static final int DOWN = 4;
public void tick(int verb) {
if (!gameOn) return;
if (currentPiece != null) {
board.undo();	// remove the piece from its old position
}
computeNewPosition(verb);
int result = setCurrent(newPiece, newX, newY);
if (result ==  Board.PLACE_ROW_FILLED) {
repaint();
}
boolean failed = (result >= Board.PLACE_OUT_BOUNDS);
if (failed) {
if (currentPiece != null) board.place(currentPiece, currentX, currentY);
repaintPiece(currentPiece, currentX, currentY);
}
if (failed && verb==DOWN && !moved) {	// it's landed
int cleared = board.clearRows();
if (cleared > 0) {
switch (cleared) {
case 1: score += 5;	 break;
case 2: score += 10;  break;
case 3: score += 20;  break;
case 4: score += 40; Toolkit.getDefaultToolkit().beep(); break;
default: score += 50;  // could happen with non-standard pieces
}
updateCounters();
repaint();	// repaint to show the result of the row clearing
}
if (board.getMaxHeight() > board.getHeight() - TOP_SPACE) {
stopGame();
}
else {
addNewPiece();
}
}
moved = (!failed && verb!=DOWN);
}
public void repaintPiece(Piece piece, int x, int y) {
if (DRAW_OPTIMIZE) {
int px = xPixel(x);
int py = yPixel(y + piece.getHeight() - 1);
int pwidth = xPixel(x+piece.getWidth()) - px;
int pheight = yPixel(y-1) - py;
repaint(px, py, pwidth, pheight);
}
else {
repaint();
}
}
private final float dX() {
return( ((float)(getWidth()-2)) / board.getWidth() );
}
private final float dY() {
return( ((float)(getHeight()-2)) / board.getHeight() );
}
private final int xPixel(int x) {
return(Math.round(1 + (x * dX())));
}
private final int yPixel(int y) {
return(Math.round(getHeight() -1 - (y+1)*dY()));
}
public void paintComponent(Graphics g) {
g.drawRect(0, 0, getWidth()-1, getHeight()-1);
int spacerY = yPixel(board.getHeight() - TOP_SPACE - 1);
g.drawLine(0, spacerY, getWidth()-1, spacerY);
Rectangle clip = null;
if (DRAW_OPTIMIZE) {
clip = g.getClipBounds();
}
final int dx = Math.round(dX()-2);
final int dy = Math.round(dY()-2);
final int bWidth = board.getWidth();
int x, y;
for (x=0; x<bWidth; x++) {
int left = xPixel(x);	// the left pixel
int right = xPixel(x+1) -1;
if (DRAW_OPTIMIZE && clip!=null) {
if ((right<clip.x) || (left>=(clip.x+clip.width))) continue;
}
final int yHeight = board.getColumnHeight(x);
for (y=0; y<yHeight; y++) {
if (board.getGrid(x, y)) {
boolean filled = (board.getRowWidth(y)==bWidth);
if (filled) g.setColor(Color.green);
g.fillRect(left+1, yPixel(y)+1, dx, dy);	// +1 to leave a white border
if (filled) g.setColor(Color.black);
}
}
}
}
public void updateTimer() {
double value = ((double)speed.getValue())/speed.getMaximum();
timer.setDelay((int)(DELAY - value*DELAY));
}
public JComponent createControlPanel() {
JPanel panel = new JPanel();
panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
countLabel = new JLabel("0");
panel.add(countLabel);
scoreLabel = new JLabel("0");
panel.add(scoreLabel);
timeLabel = new JLabel(" ");
panel.add(timeLabel);
panel.add(Box.createVerticalStrut(12));
startButton = new JButton("Start");
panel.add(startButton);
startButton.addActionListener( new ActionListener() {
public void actionPerformed(ActionEvent e) {
startGame();
}
});
stopButton = new JButton("Stop");
panel.add(stopButton);
stopButton.addActionListener( new ActionListener() {
public void actionPerformed(ActionEvent e) {
stopGame();
}
});
enableButtons();
JPanel row = new JPanel();
panel.add(Box.createVerticalStrut(12));
row.add(new JLabel("Speed:"));
speed = new JSlider(0, 200, 75);	// min, max, current
speed.setPreferredSize(new Dimension(100, 15));
updateTimer();
row.add(speed);
panel.add(row);
speed.addChangeListener( new ChangeListener() {
public void stateChanged(ChangeEvent e) {
updateTimer();
}
});
testButton = new JCheckBox("Test sequence");
panel.add(testButton);
return panel;
}
public static JFrame createFrame(JTetris tetris) {
JFrame frame = new JFrame("Stanford Tetris");
JComponent container = (JComponent)frame.getContentPane();
container.setLayout(new BorderLayout());
container.add(tetris, BorderLayout.CENTER);
JComponent controls = tetris.createControlPanel();
container.add(controls, BorderLayout.EAST);
controls.add(Box.createVerticalStrut(12));
JButton quit = new JButton("Quit");
controls.add(quit);
quit.addActionListener( new ActionListener() {
public void actionPerformed(ActionEvent e) {
System.exit(0);
}
});
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
frame.pack();
return frame;
}
public static void main(String[] args) {
try {
UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
} catch (Exception ignored) { }
JTetris tetris = new JTetris(16);
JFrame frame = JTetris.createFrame(tetris);
frame.setVisible(true);
}
}