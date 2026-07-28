import time
from tetris_logic import Board, Tetromino  # 모듈 import

def render(board: Board, piece: Tetromino) -> None:
    """보드와 현재 떨어지는 블록을 터미널에 시각화하는 함수"""
    # 임시 보드 복사
    temp_grid = [row[:] for row in board.grid]
    
    # 현재 움직이는 블록 그리기
    for r_idx, row in enumerate(piece.shape):
        for c_idx, val in enumerate(row):
            if val:
                py, px = piece.y + r_idx, piece.x + c_idx
                if 0 <= py < board.height and 0 <= px < board.width:
                    temp_grid[py][px] = 2

    print("\033[H\033[J", end="")  # 화면 갱신 (터미널 클리어)
    print("=" * (board.width * 2 + 2))
    for row in temp_grid:
        line = "|" + "".join("■ " if cell else "  " for cell in row) + "|"
        print(line)
    print("=" * (board.width * 2 + 2))

def start_game() -> None:
    board = Board(width=10, height=15)
    current_piece = Tetromino()
    score = 0

    while True:
        render(board, current_piece)
        time.sleep(0.3)  # 블록이 내려오는 속도 조절

        # 아래로 1칸 이동 시도
        if board.is_valid_position(current_piece, offset_x=0, offset_y=1):
            current_piece.y += 1
        else:
            # 더 이상 못 내려가면 고정
            board.lock_piece(current_piece)
            cleared = board.clear_lines()
            score += cleared * 100
            
            # 새 블록 생성
            current_piece = Tetromino()
            
            # 새 블록 생성 위치가 겹치면 게임 오버
            if not board.is_valid_position(current_piece):
                render(board, current_piece)
                print(f"GAME OVER! 최종 점수: {score}")
                break

if __name__ == "__main__":
    start_game()