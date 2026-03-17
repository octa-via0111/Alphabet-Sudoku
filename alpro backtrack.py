import time
import os

# Database Puzzle (Huruf '.' artinya kosong)
PUZZLE = [
    ['.', '.', '.', 'B', 'F', '.', 'G', '.', 'A'],
    ['F', 'H', '.', '.', 'G', '.', '.', 'I', '.'],
    ['A', 'I', '.', '.', '.', 'D', 'E', '.', '.'],
    ['H', 'B', '.', 'A', '.', '.', '.', 'D', '.'],
    ['.', '.', 'D', 'F', '.', 'B', 'I', '.', '.'],
    ['.', 'E', '.', '.', '.', 'C', '.', 'B', 'H'],
    ['.', '.', 'I', 'C', '.', '.', '.', 'G', 'D'],
    ['.', 'D', '.', '.', 'E', '.', '.', 'C', 'F'],
    ['G', '.', 'C', '.', 'A', 'H', '.', '.', '.'],
]

COLORS = {
    'A': "\033[1;91m", 'B': "\033[1;92m", 'C': "\033[1;93m",
    'D': "\033[1;94m", 'E': "\033[1;95m", 'F': "\033[1;96m",
    'G': "\033[1;31m", 'H': "\033[1;32m", 'I': "\033[1;34m",
    '.': "\033[90m",
}

BG_TABLE = "\033[44;37m"
RESET    = "\033[0m"
BOLD     = "\033[1m"
FOCUS    = "\033[1;103;30m"

HURUF = " ABCDEFGHI"
DELAY = 0.05

def print_board(board, current_pos=None):
    # Header Tabel
    print(f"{BG_TABLE}    ┌───────┬───────┬───────┐{RESET}")
    for r in range(9):
        row_str = f"{BG_TABLE}    │{RESET}"
        for c in range(9):
            val = board[r][c]
            color = COLORS.get(val, RESET)
            
            # Highlight posisi yang sedang dikerjakan
            if (r, c) == current_pos:
                char_disp = f"{FOCUS}{val if val != '.' else '?'}{RESET}"
            else:
                char_disp = f"{color}{val}{RESET}"
            
            row_str += f" {char_disp}"
            if c in (2, 5):
                row_str += f" {BG_TABLE}│{RESET}"
        
        row_str += f" {BG_TABLE}│{RESET}"
        print(row_str)
        if r in (2, 5):
            print(f"{BG_TABLE}    ├───────┼───────┼───────┤{RESET}")
    print(f"{BG_TABLE}    └───────┴───────┴───────┘{RESET}")

def is_valid(board, r, c, char):
    for i in range(9):
        if board[r][i] == char or board[i][c] == char:
            return False
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if board[i][j] == char:
                return False
    return True

def solve(board, initial_time, stats):
    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                for i in range(1, 10):
                    char_coba = HURUF[i]
                    stats['steps'] += 1
                    
                    # Log Status Singkat
                    print(f"\n[STEP {stats['steps']}] Mencoba {char_coba} di ({r+1},{c+1})")

                    if is_valid(board, r, c, char_coba):
                        board[r][c] = char_coba
                        print(f"✅ \033[92mVALID!\033[0m")
                        print_board(board, (r, c))
                        time.sleep(DELAY)

                        if solve(board, initial_time, stats):
                            return True
                        
                        # Proses Backtrack
                        board[r][c] = '.'
                        stats['backtracks'] += 1
                        print(f"❌ \033[91mBACKTRACK!\033[0m Mundur dari {char_coba}")
                        print_board(board, (r, c))
                        time.sleep(DELAY)
                return False
    return True

def main():
    board = [row[:] for row in PUZZLE]
    stats = {'steps': 0, 'backtracks': 0}

    print(f"{BOLD}=" * 45)
    print("   🌈 RAINBOW ALPHABET SUDOKU DETECTIVE")
    print("=" * 45 + RESET)
    print_board(board)
    
    input("\nTekan [ENTER] untuk memulai...")

    start_t = time.time()
    success = solve(board, start_t, stats)
    end_t = time.time() - start_t

    # --- BAGIAN KETERANGAN PALING BAWAH (FINAL REPORT) ---
    print("\n" + "═" * 45)
    if success:
        print(f"🏆 {BOLD}\033[92mHASIL AKHIR: SOLVED!{RESET}")
    else:
        print(f"❌ {BOLD}\033[91mHASIL AKHIR: TIDAK ADA SOLUSI.{RESET}")
    
    print("-" * 45)
    print(f" {BOLD}INFORMASI EKSEKUSI:{RESET}")
    print(f" 📑 Total Langkah (Steps)     : {stats['steps']}")
    print(f" 🔄 Total Mundur (Backtracks) : {stats['backtracks']}")
    print(f" ⏱️  Waktu Proses (Time)       : {end_t:.2f} detik")
    print("═" * 45)

if __name__ == "__main__":
    main()