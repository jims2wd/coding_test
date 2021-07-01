import random

list1 = ["apple", "bean", "cat", "dead", "elefont", "forests" ]
a = random.randint(0,5)
word = list1[a]

def hangman(word):
    wrong = 0
    stages = ["",
              "__________          ",
              "|                   ",
              "|         |         ",
              "|         ○         ",
              "|        /|\        ",
              "|        / \        ",
              "|                   "
              ]
    rletters = list(word)
    board = ["_"] * len(word)
    win = False

    print("恐怖のハングマンへようこそ！")

# http://tinyurl.com/ztrp5jc

    while wrong < len(stages) - 1:
        print("\n")

        msg = "1文字を予想して入力してください:"
        char = input(msg)

        if char in rletters:
            cind = rletters.index(char)
            board[cind] = char
            rletters[cind] = '$'
        else:
            wrong += 1
    
        print(" ".join(board))

        e = wrong + 1

        print("\n".join(stages[0:e]))

        if "_" not in board:
            print("You win!")
            print(" ".join(board))
            win = True
            break

# http://tinyurl.com/zqklqxo

    if not win:
        print("\n".join(stages[0:wrong+1]))
        print("You lose!answer is {}.".format(word))

hangman(word)
