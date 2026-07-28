import java.util.Random;

public class TetrisModel {
    public static final int WIDTH = 10;
    public static final int HEIGHT = 20;

    private int[][] grid = new int[HEIGHT][WIDTH];
    private int[][] currentShape;
    private int currentX = 3;
    private int currentY = 0;

    private final int[][][] SHAPES = {
        {{1, 1, 1, 1}},                // I
        {{1, 1}, {1, 1}},              // O
        {{0, 1, 0}, {1, 1, 1}},        // T
        {{1, 0, 0}, {1, 1, 1}}         // L
    };

    public TetrisModel() {
        spawnPiece();
    }

    public void spawnPiece() {
        Random rand = new Random();
        currentShape = SHAPES[rand.nextInt(SHAPES.length)];
        currentX = WIDTH / 2 - currentShape[0].length / 2;
        currentY = 0;
    }

    public boolean move(int dx, int dy) {
        if (canMove(currentShape, currentX + dx, currentY + dy)) {
            currentX += dx;
            currentY += dy;
            return true;
        }
        return false;
    }

    public boolean canMove(int[][] shape, int newX, int newY) {
        for (int r = 0; r < shape.length; r++) {
            for (int c = 0; c < shape[r].length; c++) {
                if (shape[r][c] != 0) {
                    int targetX = newX + c;
                    int targetY = newY + r;

                    if (targetX < 0 || targetX >= WIDTH || targetY >= HEIGHT) {
                        return false;
                    }
                    if (targetY >= 0 && grid[targetY][targetX] != 0) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    public void lockPiece() {
        for (int r = 0; r < currentShape.length; r++) {
            for (int c = 0; c < currentShape[r].length; c++) {
                if (currentShape[r][c] != 0) {
                    grid[currentY + r][currentX + c] = 1;
                }
            }
        }
        spawnPiece();
    }

    public int[][] getGrid() { return grid; }
    public int[][] getCurrentShape() { return currentShape; }
    public int getCurrentX() { return currentX; }
    public int getCurrentY() { return currentY; }
}