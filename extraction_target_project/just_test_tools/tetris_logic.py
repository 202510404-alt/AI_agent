import random

class Tetromino:
    """테트리스 블록 데이터 및 회전 로직 관리"""
    SHAPES = [
        [[1, 1, 1, 1]],                  # I
        [[1, 1], [1, 1]],                # O
        [[0, 1, 0], [1, 1, 1]],          # T
        [[1, 0, 0], [1, 1, 1]],          # L
        [[0, 0, 1], [1, 1, 1]],          # J
        [[0, 1, 1], [1, 0, 0]],          # S
        [[1, 1, 0], [0, 1, 1]]           # Z
    ]

    def __init__(self, x: int = 3, y: int = 0):
        self.x = x
        self.y = y
        self.shape = random.choice(self.SHAPES)

    def rotate(self) -> None:
        """블록을 시계 방향으로 90도 회전"""
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


class Board:
    """테트리스 판 및 이동/충돌 감지 로직"""
    def __init__(self, width: int = 10, height: int = 20):
        self.width = width
        self.height = height
        self.grid = [[0] * width for _ in range(height)]

    def is_valid_position(self, piece: Tetromino, offset_x: int = 0, offset_y: int = 0) -> bool:
        """해당の位置로 이동이 가능한지 확인 (인자: piece 객체, 오프셋 값)"""
        for r_idx, row in enumerate(piece.shape):
            for c_idx, val in enumerate(row):
                if val:
                    new_x = piece.x + c_idx + offset_x
                    new_y = piece.y + r_idx + offset_y
                    
                    # 경계선 체크
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return False
                    # 기존에 쌓인 블록과 충돌 체크
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True

    def lock_piece(self, piece: Tetromino) -> None:
        """블록을 보드판에 고정"""
        for r_idx, row in enumerate(piece.shape):
            for c_idx, val in enumerate(row):
                if val:
                    self.grid[piece.y + r_idx][piece.x + c_idx] = 1

    def clear_lines(self) -> int:
        """꽉 찬 줄을 지우고 획득한 줄 수를 반환"""
        lines_cleared = 0
        new_grid = []
        for row in self.grid:
            if all(cell == 1 for cell in row):
                lines_cleared += 1
            else:
                new_grid.append(row)
        
        # 지워진 줄만큼 위에 빈 줄 추가
        for _ in range(lines_cleared):
            new_grid.insert(0, [0] * self.width)
            
        self.grid = new_grid
        return lines_cleared
    