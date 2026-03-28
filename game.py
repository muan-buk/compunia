from random import randrange

def game_loop():
    tmp = randrange(2, 10)
    tmp2 = randrange(1, 10)
    answer = tmp * tmp2

    while True:
        try:
            player_input = int(input(f"{tmp} × {tmp2}: "))
            break
        except ValueError:
            print("숫자를 입력하세요.")

    return player_input == answer


if __name__ == "__main__":
    count = 0
    while game_loop():
        count += 1
    print(f"{count}번 정답!")
