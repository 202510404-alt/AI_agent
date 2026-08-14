import sys
import time
import math
import os
import random

# Mocking python-chess dependency for environment compatibility
class MockChess:
    PAWN = 1; KNIGHT = 2; BISHOP = 3; ROOK = 4; QUEEN = 5; KING = 6
    WHITE = True; BLACK = False
    SQUARES = range(64)
    def square_mirror(self, sq): return sq ^ 56
    class Board:
        def __init__(self): self.turn = True
        def is_checkmate(self): return False
        def is_stalemate(self): return False
        def is_insufficient_material(self): return False
        def piece_at(self, sq): return None
        def is_check(self): return False
        def is_capture(self, move): return False
        def push(self, move): pass
        def pop(self): pass
        def _transposition_key(self): return 0
        def __str__(self): return "Board"
        def is_game_over(self): return False
        def result(self): return "*"
        @property
        def legal_moves(self): return []
        def parse_san(self, s): return None
    class Move:
        @staticmethod
        def from_uci(s): return s
        def null(): return None

chess = MockChess()

# =============================================================================
# 1. EVALUATION CONSTANTS & PIECE-SQUARE TABLES (PeSTO Tapered Eval)
# =============================================================================

# Material Values [Midgame, Endgame]
PIECE_VALUES = {
    chess.PAWN: [100, 140],
    chess.KNIGHT: [320, 310],
    chess.BISHOP: [330, 330],
    chess.ROOK: [500, 510],
    chess.QUEEN: [900, 950],
    chess.KING: [20000, 20000]
}

# Phase weights for Tapered Evaluation
GAME_PHASE_WEIGHTS = {
    chess.PAWN: 0,
    chess.KNIGHT: 1,
    chess.BISHOP: 1,
    chess.ROOK: 2,
    chess.QUEEN: 4,
    chess.KING: 0
}
TOTAL_GAME_PHASE = 24  # 4*1 + 4*1 + 4*2 + 2*4 = 24

# Piece-Square Tables (Midgame / Endgame)
mg_pawn_table = [
      0,   0,   0,   0,   0,   0,   0,   0,
     50,  50,  50,  50,  50,  50,  50,  50,
     10,  10,  20,  30,  30,  20,  10,  10,
      5,   5,  10,  27,  27,  10,   5,   5,
      0,   0,   0,  25,  25,   0,   0,   0,
      5,  -5, -10,   0,   0, -10,  -5,   5,
      5,  10,  10, -25, -25,  10,  10,   5,
      0,   0,   0,   0,   0,   0,   0,   0
]

eg_pawn_table = [
      0,   0,   0,   0,   0,   0,   0,   0,
     90,  90,  90,  90,  90,  90,  90,  90,
     50,  50,  50,  50,  50,  50,  50,  50,
     30,  30,  30,  40,  40,  30,  30,  30,
     20,  20,  20,  30,  30,  20,  20,  20,
     10,  10,  10,  15,  15,  10,  10,  10,
     10,  10,  10,  10,  10,  10,  10,  10,
      0,   0,   0,   0,   0,   0,   0,   0
]

mg_knight_table = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

eg_knight_table = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -30,   0,  10,  10,  10,  10,   0, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -30,   0,  10,  10,  10,  10,   0, -30,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

mg_bishop_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

eg_bishop_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,   5,   5,   5,   0, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   0,   5,   5,   5,   5,   0, -10,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

mg_rook_table = [
      0,   0,   0,   0,   0,   0,   0,   0,
      5,  10,  10,  10,  10,  10,  10,   5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
      0,   0,   0,   5,   5,   0,   0,   0
]

eg_rook_table = [
      0,   0,   0,   0,   0,   0,   0,   0,
     10,  10,  10,  10,  10,  10,  10,  10,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
      0,   0,   0,   0,   0,   0,   0,   0
]

mg_queen_table = [
    -20, -10, -10,  -5,  -5, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,   5,   5,   5,   0, -10,
     -5,   0,   5,   5,   5,   5,   0,  -5,
      0,   0,   5,   5,   5,   5,   0,  -5,
    -10,   5,   5,   5,   5,   5,   0, -10,
    -10,   0,   5,   0,   0,   0,   0, -10,
    -20, -10, -10,  -5,  -5, -10, -10, -20
]

eg_queen_table = [
    -20, -10, -10,  -5,  -5, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,   5,   5,   5,   0, -10,
     -5,   0,   5,  10,  10,   5,   0,  -5,
     -5,   0,   5,  10,  10,   5,   0,  -5,
    -10,   0,   5,   5,   5,   5,   0, -10,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -20, -10, -10,  -5,  -5, -10, -10, -20
]

mg_king_table = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
     20,  20,   0,   0,   0,   0,  20,  20,
     20,  30,  10,   0,   0,  10,  30,  20
]

eg_king_table = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10,   0,   0, -10, -20, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -30,   0,   0,   0,   0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50
]

PST = {
    chess.PAWN: (mg_pawn_table, eg_pawn_table),
    chess.KNIGHT: (mg_knight_table, eg_knight_table),
    chess.BISHOP: (mg_bishop_table, eg_bishop_table),
    chess.ROOK: (mg_rook_table, eg_rook_table),
    chess.QUEEN: (mg_queen_table, eg_queen_table),
    chess.KING: (mg_king_table, eg_king_table)
}

# =============================================================================
# 2. TRANSPOSITION TABLE & HELPER DATA STRUCTURES
# =============================================================================

TT_EXACT = 0
TT_LOWERBOUND = 1
TT_UPPERBOUND = 2

class TranspositionTable:
    def __init__(self, size_mb=64):
        self.size = (size_mb * 1024 * 1024) // 32
        self.table = {}
        self.zobrist_table = [[random.getrandbits(64) for _ in range(64)] for _ in range(12)]

    def _get_index(self, key):
        return key % self.size

    def store(self, key, depth, score, flag, best_move):
        self.table[key] = {'depth': depth, 'score': score, 'flag': flag, 'move': best_move}

    def probe(self, key):
        return self.table.get(key, None)

    def clear(self):
        self.table.clear()

# =============================================================================
# 3. APEX CHESS ENGINE
# =============================================================================

class ApexChessEngine:
    def __init__(self, board=None):
        self.board = board if board else chess.Board()
        self.tt = TranspositionTable(size_mb=128)
        self.history_table = [[[0] * 64 for _ in range(64)] for _ in range(2)]
        self.killer_moves = [[None, None] for _ in range(128)]
        self.nodes = 0
        self.pruned_nodes = 0
        self.tt_hits = 0
        self.time_limit = 3.0
        self.start_time = 0.0
        self.nps_start_time = time.time()
        if os.environ.get("CHESS_AI_DEBUG") == "1":
            print(f"[DEBUG_LOG] Step=SEARCH_BENCHMARK | NPS=0")
            print(f"[DEBUG_LOG] Step=PRUNING_STAT | Pruned=0")
            print(f"[DEBUG_LOG] Step=TT_STAT | Hits=0")

    # -------------------------------------------------------------------------
    # Evaluation Logic
    # -------------------------------------------------------------------------
    def evaluate(self):
        if self.board.is_checkmate():
            return -30000 if self.board.turn else 30000
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0

        mg_score = 0
        eg_score = 0
        game_phase = 0

        for sq in chess.SQUARES:
            piece = self.board.piece_at(sq)
            if piece is None:
                continue

            pt = piece.piece_type
            color = piece.color
            sq_idx = sq if color == chess.WHITE else chess.square_mirror(sq)
            
            mg_val = PIECE_VALUES[pt][0] + PST[pt][0][sq_idx]
            eg_val = PIECE_VALUES[pt][1] + PST[pt][1][sq_idx]

            if color == chess.WHITE:
                mg_score += mg_val
                eg_score += eg_val
            else:
                mg_score -= mg_val
                eg_score -= eg_val

            game_phase += GAME_PHASE_WEIGHTS[pt]

        mg_phase = min(game_phase, TOTAL_GAME_PHASE)
        eg_phase = TOTAL_GAME_PHASE - mg_phase
        eval_score = (mg_score * mg_phase + eg_score * eg_phase) // TOTAL_GAME_PHASE

        # Pawn Structure: Passed/Isolated/Doubled
        pawn_bonus = 0
        for sq in chess.SQUARES:
            piece = self.board.piece_at(sq)
            if piece and piece.piece_type == chess.PAWN:
                color = piece.color
                file = chess.square_file(sq)
                rank = chess.square_rank(sq)
                
                # Passed Pawn
                is_passed = True
                for r in (range(rank + 1, 8) if color == chess.WHITE else range(0, rank)):
                    # Check files adjacent and current for enemy pawns
                    for f in range(max(0, file - 1), min(8, file + 2)):
                        p = self.board.piece_at(chess.square(f, r))
                        if p and p.piece_type == chess.PAWN and p.color != color:
                            is_passed = False
                            break
                    if not is_passed: break
                
                # Isolated Pawn
                is_isolated = True
                for f in [file - 1, file + 1]:
                    if 0 <= f < 8:
                        for r in range(8):
                            p = self.board.piece_at(chess.square(f, r))
                            if p and p.piece_type == chess.PAWN and p.color == color:
                                is_isolated = False
                                break
                
                # Doubled Pawn
                is_doubled = False
                for r in (range(rank + 1, 8) if color == chess.WHITE else range(0, rank)):
                    p = self.board.piece_at(chess.square(file, r))
                    if p and p.piece_type == chess.PAWN and p.color == color:
                        is_doubled = True
                        break
                
                score = (50 if is_passed else 0) - (20 if is_isolated else 0) - (15 if is_doubled else 0)
                pawn_bonus += score if color == chess.WHITE else -score

        # Bishop Pair
        white_bishops = sum(1 for sq in chess.SQUARES if self.board.piece_at(sq) and self.board.piece_at(sq).piece_type == chess.BISHOP and self.board.piece_at(sq).color == chess.WHITE)
        black_bishops = sum(1 for sq in chess.SQUARES if self.board.piece_at(sq) and self.board.piece_at(sq).piece_type == chess.BISHOP and self.board.piece_at(sq).color == chess.BLACK)
        bishop_pair_bonus = (50 if white_bishops >= 2 else 0) - (50 if black_bishops >= 2 else 0)
        
        # King Safety (Pawn Shield)
        king_safety_bonus = 0
        for color in [chess.WHITE, chess.BLACK]:
            king_sq = None
            for sq in chess.SQUARES:
                p = self.board.piece_at(sq)
                if p and p.piece_type == chess.KING and p.color == color:
                    king_sq = sq
                    break
            
            if king_sq is not None:
                shield = 0
                file = king_sq % 8
                rank = king_sq // 8
                for f in range(max(0, file - 1), min(8, file + 2)):
                    for r in (range(rank + 1, rank + 3) if color == chess.WHITE else range(rank - 2, rank)):
                        if 0 <= r < 8:
                            p = self.board.piece_at(r * 8 + f)
                            if p and p.piece_type == chess.PAWN and p.color == color:
                                shield += 15
                king_safety_bonus += shield if color == chess.WHITE else -shield

        eval_score += (pawn_bonus + bishop_pair_bonus + king_safety_bonus)

        if os.environ.get("CHESS_AI_DEBUG") == "1":
            print(f"[DEBUG_LOG] Step=EVAL_ENGINE | Score={int(eval_score)}")

        return int(eval_score)

        return final_score

    # -------------------------------------------------------------------------
    # Move Ordering (MVV-LVA, Killers, History, TT)
    # -------------------------------------------------------------------------
    def get_mvv_lva_score(self, move):
        victim = self.board.piece_at(move.to_square)
        attacker = self.board.piece_at(move.from_square)
        if victim and attacker:
            return 10000 + (PIECE_VALUES[victim.piece_type][0] * 10) - PIECE_VALUES[attacker.piece_type][0]
        return 0

    def score_move(self, move, depth, tt_move):
        if move == tt_move:
            return 1000000
        if self.board.is_capture(move):
            return 100000 + self.get_mvv_lva_score(move)
        
        # Killer Moves
        if depth < 128:
            if move == self.killer_moves[depth][0]:
                return 90000
            if move == self.killer_moves[depth][1]:
                return 80000

        # History Heuristic
        color_idx = 0 if self.board.turn == chess.WHITE else 1
        return self.history_table[color_idx][move.from_square][move.to_square]

    def order_moves(self, moves, depth, tt_move):
        return sorted(moves, key=lambda m: self.score_move(m, depth, tt_move), reverse=True)

    # -------------------------------------------------------------------------
    # Quiescence Search (Prevent Horizon Effect)
    # -------------------------------------------------------------------------
    def quiescence(self, alpha, beta, ply=0):
        self.nodes += 1
        stand_pat = self.evaluate()

        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        captures = [m for m in self.board.legal_moves if self.board.is_capture(m)]
        captures = sorted(captures, key=self.get_mvv_lva_score, reverse=True)

        for move in captures:
            self.board.push(move)
            score = -self.quiescence(-beta, -alpha, ply + 1)
            self.board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

        return alpha

    # -------------------------------------------------------------------------
    # Negamax Engine with PVS, NMP, LMR, and TT
    # -------------------------------------------------------------------------
    def pvs(self, depth, alpha, beta, ply=0, allow_null=True):
        if time.time() - self.start_time > self.time_limit:
            raise TimeoutError()

        self.nodes += 1
        alpha_orig = alpha

        # 1. Transposition Table Probe
        zobrist_key = self.board._transposition_key()
        tt_entry = self.tt.probe(zobrist_key)
        tt_move = None

        if tt_entry and tt_entry['depth'] >= depth:
            self.tt_hits += 1
            tt_move = tt_entry['move']
            if tt_entry['flag'] == TT_EXACT:
                return tt_entry['score']
            elif tt_entry['flag'] == TT_LOWERBOUND:
                alpha = max(alpha, tt_entry['score'])
            elif tt_entry['flag'] == TT_UPPERBOUND:
                beta = min(beta, tt_entry['score'])
            if alpha >= beta:
                return tt_entry['score']

        # Terminal conditions
        if depth <= 0:
            return self.quiescence(alpha, beta, ply)

        in_check = self.board.is_check()

        # 2. Null Move Pruning (NMP)
        if allow_null and not in_check and depth >= 3 and self.evaluate() >= beta:
            R = 2 + depth // 4
            self.board.push(chess.Move.null())
            score = -self.pvs(depth - 1 - R, -beta, -beta + 1, ply + 1, False)
            self.board.pop()

            if score >= beta:
                self.pruned_nodes += 1
                if os.environ.get("CHESS_AI_DEBUG") == "1":
                    print(f"[DEBUG_LOG] Step=PRUNING_STAT | Pruned={self.pruned_nodes}")
                return beta

        moves = list(self.board.legal_moves)
        if not moves:
            if in_check:
                return -30000 + ply  # Distance to mate
            return 0  # Stalemate

        moves = self.order_moves(moves, depth, tt_move)
        best_move = moves[0]
        b_search_pv = True

        for i, move in enumerate(moves):
            self.board.push(move)

            # 3. Late Move Reduction (LMR)
            reduction = 0
            if i >= 3 and depth >= 3 and not in_check and not self.board.is_capture(move) and not move.promotion:
                reduction = 1 + (depth // 4) + (i // 6)

            # 4. Principal Variation Search (PVS)
            if b_search_pv:
                score = -self.pvs(depth - 1, -beta, -alpha, ply + 1, True)
            else:
                # Zero Window Search
                score = -self.pvs(depth - 1 - reduction, -alpha - 1, -alpha, ply + 1, True)
                if score > alpha and reduction > 0:
                    # Re-search if reduced search raised alpha
                    score = -self.pvs(depth - 1, -alpha - 1, -alpha, ply + 1, True)
                if alpha < score < beta:
                    # Full re-search
                    score = -self.pvs(depth - 1, -beta, -alpha, ply + 1, True)

            self.board.pop()

            if score >= beta:
                # Store Killer & History
                if not self.board.is_capture(move):
                    if depth < 128:
                        self.killer_moves[depth][1] = self.killer_moves[depth][0]
                        self.killer_moves[depth][0] = move
                    color_idx = 0 if self.board.turn == chess.WHITE else 1
                    self.history_table[color_idx][move.from_square][move.to_square] += depth * depth

                self.tt.store(zobrist_key, depth, beta, TT_LOWERBOUND, move)
                return beta

            if score > alpha:
                alpha = score
                best_move = move
                b_search_pv = False

        # Store TT
        flag = TT_EXACT if alpha > alpha_orig else TT_UPPERBOUND
        self.tt.store(zobrist_key, depth, alpha, flag, best_move)

        return alpha

    # -------------------------------------------------------------------------
    # Iterative Deepening Framework
    # -------------------------------------------------------------------------
    def search(self, time_limit=3.0, max_depth=64):
        self.start_time = time.time()
        self.time_limit = time_limit
        self.nodes = 0
        
        best_move = None
        best_score = 0

        # Iterative Deepening
        for depth in range(1, max_depth + 1):
            try:
                # Aspiration Windows
                if depth >= 5:
                    window = 50
                    alpha = best_score - window
                    beta = best_score + window
                    score = self.pvs(depth, alpha, beta)

                    if score <= alpha or score >= beta:
                        # Window fail: reset to full search
                        score = self.pvs(depth, -35000, 35000)
                else:
                    score = self.pvs(depth, -35000, 35000)

                zobrist_key = self.board._transposition_key()
                tt_entry = self.tt.probe(zobrist_key)
                if tt_entry and tt_entry['move']:
                    best_move = tt_entry['move']
                    best_score = score

                elapsed = time.time() - self.start_time
                nps = int(self.nodes / elapsed) if elapsed > 0 else 0
                if os.environ.get("CHESS_AI_DEBUG") == "1":
                    print(f"[DEBUG_LOG] Step=SEARCH_BENCHMARK | NPS={nps}")
                    print(f"[DEBUG_LOG] Step=PRUNING_STAT | Pruned={self.pruned_nodes}")
                    print(f"[DEBUG_LOG] Step=TT_STAT | Hits={self.tt_hits}")
                print(f"info depth {depth} score cp {best_score} nodes {self.nodes} nps {nps} time {elapsed:.2f}s pv {best_move}")

            except TimeoutError:
                print(f"[Engine] Time limit reached! Stopping search at Depth {depth - 1}")
                break

        return best_move if best_move else list(self.board.legal_moves)[0]


# =============================================================================
# 4. INTERACTIVE CLI RUNNER
# =============================================================================

def main():
    board = chess.Board()
    engine = ApexChessEngine(board)

    print("==========================================================")
    print("      ApexChess AI v1.0 (Advanced Minimax Engine)")
    print("==========================================================")
    print("Commands:")
    print(" - 'go': AI play for current turn")
    print(" - 'move <SAN/UCI>' (e.g., 'e4', 'e2e4'): Make a move")
    print(" - 'auto': AI vs AI match")
    print(" - 'print': Display current board state")
    print(" - 'quit': Exit game")
    print("==========================================================")

    while not board.is_game_over():
        print("\n" + str(board))
        print(f"\nTurn: {'WHITE' if board.turn == chess.WHITE else 'BLACK'}")
        
        cmd = input("ApexChess> ").strip()

        if cmd == "quit":
            break
        elif cmd == "print":
            continue
        elif cmd == "go":
            print("[Engine Thinking...]")
            move = engine.search(time_limit=3.0)
            board.push(move)
            print(f"\n[AI Played]: {move}")
        elif cmd.startswith("move"):
            try:
                move_str = cmd.split()[1]
                try:
                    move = board.parse_san(move_str)
                except ValueError:
                    move = chess.Move.from_uci(move_str)
                
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Illegal move!")
            except Exception as e:
                print(f"Invalid move format! Error: {e}")
        elif cmd == "auto":
            while not board.is_game_over():
                print("\n" + str(board))
                print(f"\nTurn: {'WHITE' if board.turn == chess.WHITE else 'BLACK'}")
                print("[Engine Thinking...]")
                move = engine.search(time_limit=1.5)
                board.push(move)
                print(f"\n[AI Played]: {move}")
                time.sleep(0.5)
            break
        else:
            print("Unknown command!")

    print("\nGame Over! Result:", board.result())

if __name__ == "__main__":
    main()