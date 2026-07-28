import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class Main extends JPanel {
    private TetrisModel gameModel;
    private static final int CELL_SIZE = 30;

    public Main() {
        gameModel = new TetrisModel();  // TetrisModel 클래스 호출
        setFocusable(true);

        // 키보드 조작 이벤트 핸들러
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                switch (e.getKeyCode()) {
                    case KeyEvent.VK_LEFT -> gameModel.move(-1, 0);
                    case KeyEvent.VK_RIGHT -> gameModel.move(1, 0);
                    case KeyEvent.VK_DOWN -> gameModel.move(0, 1);
                }
                repaint();
            }
        });

        // 게임 루프 타이머 (400ms마다 아래로 한 칸씩)
        Timer timer = new Timer(400, e -> {
            if (!gameModel.move(0, 1)) {
                gameModel.lockPiece();
            }
            repaint();
        });
        timer.start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // 1. 고정된 보드 그리기
        int[][] grid = gameModel.getGrid();
        for (int r = 0; r < TetrisModel.HEIGHT; r++) {
            for (int c = 0; c < TetrisModel.WIDTH; c++) {
                if (grid[r][c] != 0) {
                    g.setColor(Color.BLUE);
                    g.fillRect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1);
                }
            }
        }

        // 2. 현재 떨어지는 블록 그리기
        int[][] shape = gameModel.getCurrentShape();
        int px = gameModel.getCurrentX();
        int py = gameModel.getCurrentY();
        g.setColor(Color.RED);
        for (int r = 0; r < shape.length; r++) {
            for (int c = 0; c < shape[r].length; c++) {
                if (shape[r][c] != 0) {
                    g.fillRect((px + c) * CELL_SIZE, (py + r) * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1);
                }
            }
        }
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Tetris Game");
        Main gamePanel = new Main();
        
        frame.add(gamePanel);
        frame.setSize(TetrisModel.WIDTH * CELL_SIZE + 15, TetrisModel.HEIGHT * CELL_SIZE + 40);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }
}