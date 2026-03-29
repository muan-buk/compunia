import random

def print_board(board, revealed):
    size = len(board)
    # 열 번호 출력
    print("   " + " ".join(str(i) for i in range(size)))
    print("  " + "-" * (size * 2 + 1))
    
    for r in range(size):
        row_str = f"{r} |" # 행 번호
        for c in range(size):
            if revealed[r][c]:
                # 지뢰가 없는 빈 공간(0)은 빈칸으로 표시
                row_str += ("  " if board[r][c] == 0 else str(board[r][c]) + " ")
            else:
                row_str += "■ " # 아직 안 열어본 칸
        print(row_str)
    print()

def place_mines(size, num_mines):
    board = [[0 for _ in range(size)] for _ in range(size)]
    # 지뢰 랜덤 배치
    mines = random.sample([(r, c) for r in range(size) for c in range(size)], num_mines)
    
    for r, c in mines:
        board[r][c] = '*'
        # 주변 8칸에 숫자 1씩 증가
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if 0 <= r+dr < size and 0 <= c+dc < size and board[r+dr][c+dc] != '*':
                    board[r+dr][c+dc] += 1
    return board, mines

def reveal(board, revealed, r, c):
    # 보드 밖을 벗어나거나 이미 열린 칸이면 중단
    if r < 0 or r >= len(board) or c < 0 or c >= len(board) or revealed[r][c]: 
        return
    
    revealed[r][c] = True
    
    # 빈칸(0)이면 주변 8칸도 연쇄적으로 열기
    if board[r][c] == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                reveal(board, revealed, r+dr, c+dc)

def play_minesweeper(size=8, num_mines=10):
    board, mines = place_mines(size, num_mines)
    revealed = [[False for _ in range(size)] for _ in range(size)]
    safe_cells = size * size - num_mines # 지뢰가 아닌 안전한 칸의 수

    print("\n=== 터미널 지뢰찾기 게임에 오신 것을 환영합니다! ===")
    
    while True:
        print_board(board, revealed)
        
        # 승리 조건 체크
        revealed_count = sum(row.count(True) for row in revealed)
        if revealed_count == safe_cells:
            print("🎉 축하합니다! 모든 지뢰를 피했습니다! 🎉")
            break

        try:
            user_input = input("열어볼 좌표를 입력하세요 (행 열, 예: 2 3) : ")
            r, c = map(int, user_input.split())
            if not (0 <= r < size and 0 <= c < size):
                print("⚠️ 보드 밖의 좌표입니다. 다시 입력해주세요.\n")
                continue
        except ValueError:
            print("⚠️ 숫자 두 개를 띄어쓰기로 입력해주세요. (예: 2 3)\n")
            continue

        if (r, c) in mines:
            # 지뢰를 밟았을 때 모든 지뢰 공개
            for mr, mc in mines:
                revealed[mr][mc] = True
            print_board(board, revealed)
            print("💥 앗! 지뢰를 밟았습니다! 게임 오버. 💥")
            break

        if not revealed[r][c]:
            reveal(board, revealed, r, c)

if __name__ == "__main__":
    play_minesweeper()
