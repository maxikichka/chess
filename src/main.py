board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
         ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
         ["0", "0", "0", "0", "0", "0", "0", "0"],
         ["0", "0", "0", "0", "0", "0", "0", "0"],
         ["0", "0", "0", "0", "0", "0", "0", "0"],
         ["0", "0", "0", "0", "0", "0", "0", "0"],
         ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
         ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

moves = []
possibleMoves = []
otherTurn = {"w": "b", "b": "w"}
inCheck = ("N", (0, 0))
turn = "w"

def giveArrayCoord(coord):
    alphabet = "abcdefgh"
    return (8 - int(coord[1]), alphabet.find(coord[0]))

def emulateBoard(startPos, endPos):
    newBoard = board[:]
    newBoard[endPos[0]][endPos[1]] = newBoard[startPos[0]][startPos[1]][1]
    newBoard[startPos[0]][startPos[1]] = "0"
    return

def tryCastle(turn):
    if turn == "w":
        row = 7
    else:
        row = 0
    if board[row][4][1] == "K" and board[row][7][1] == "R":
        #kingside castle
        if board[row][5] == "0" and board[row][6] == "0":
            possibleMoves.append({"start": (row, 4), "end": (row, 6)})
    elif board[row][0][1] == "R":
        #queenside castle
        if board[row][1] == "0" and board[row][2] == "0" and board[row][3] == "0":
            possibleMoves.append({"start": (row, 4), "end": (row, 2)})

def getPossibleKingMoves(coords, turn):
    opts = [[-1, -1], [1, -1], [1, 1], [-1, 1]]
    for i in range(len(opts)):
        try:
            if board[coords[0] + (1 * opts[i][0])][coords[1] + (1 * opts[i][1])][0] != turn:
                possibleMoves.append({"start": coords, "end": (coords[0] + (1 * opts[i][0]), coords[1] + (1 * opts[i][1]))})
        except IndexError:
            continue
    tryCastle(turn)

def getPossibleQueenMoves(coords, turn):
    getPossibleRookMoves(coords, turn)
    getPossibleBishopMoves(coords, turn)

def getPossibleRookMoves(coords, turn):
    for i in range(3):
        x, y = coords[0], coords[1]
        while True:
            if i == 0:
                x -= 1
            elif i == 1:
                x += 1
            elif i == 2:
                y -= 1
            else:
                y += 1
            try:
                if board[x][y][0] != turn:
                    possibleMoves.append({"start": coords, "end": (x, y)})
                    if board[x][y][0] != "0":
                        break
                else:
                    break
            except IndexError:
                break
            
def getPossibleBishopMoves(coords, turn):
    opts = [[-1, -1], [1, -1], [1, 1], [-1, 1]]
    for i in range(len(opts)):
        x, y = coords[0], coords[1]
        while True:
            x += (1 * opts[i][0])
            y += (1 * opts[i][1])
            try:
                if board[x][y][0] != turn:
                    possibleMoves.append({"start": coords, "end": (x, y)})
                    if board[x][y] != "0":
                        break
                else:
                    break
            except IndexError:
                break

def getPossibleKnightMoves(coords, turn):
    opts = [[-1, -1], [1, -1], [1, 1], [-1, 1]]
    for i in range(len(opts)):
        try:
            if board[coords[0] + (2 * opts[i][0])][coords[1] + (1 * opts[i][1])][0] != turn:
                possibleMoves.append({"start": coords, "end": (coords[0] + (2 * opts[i][0]), coords[0] + (2 * opts[i][0]))})
        except IndexError:
            pass
        try:
            if board[coords[0] + (1 * opts[i][0])][coords[1] + (2 * opts[i][1])][0] != turn:
                possibleMoves.append({"start": coords, "end": (coords[0] + (1 * opts[i][0]), coords[1] + (2 * opts[i][1]))})
        except IndexError:
            continue

def getPossiblePawnMoves(coords, turn):
    #print(coords)
    if board[coords[0] - 1][coords[1]] == "0":
        possibleMoves.append({"start": coords, "end": (coords[0] - 1, coords[1])})
        if coords[0] == 6 and board[coords[0] - 2][coords[1]] == "0":
            possibleMoves.append({"start": coords, "end": (coords[0] - 2, coords[1])})
    if coords[1] < 7 and board[coords[0] - 1][coords[1] + 1][0] == "b":
        possibleMoves.append({"start": coords, "end": (coords[0] - 1, coords[1] + 1)})
    if coords[1] > 0 and board[coords[0] - 1][coords[1] - 1][0] == "b":
        possibleMoves.append({"start": coords, "end": (coords[0] - 1, coords[1] - 1)})
    if (coords[0] == 3 and
        giveArrayCoord(moves[-2]["b"]["move"][:2])[0] == 1 and
        giveArrayCoord(moves[-2]["b"]["move"][3:])[0] == 3):
        if giveArrayCoord(moves[-2]["b"]["move"][3:])[1] == coords[1] + 1:
            possibleMoves.append({"start": coords, "end": (coords[0], coords[1] - 1)})
        if giveArrayCoord(moves[-2]["b"]["move"][3:])[1] == coords[1] - 1:
            possibleMoves.append({"start": coords, "end": (coords[0], coords[1] + 1)})

def getMoves(turn):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j][0] == turn:
                if board[i][j][1] == "p":
                    getPossiblePawnMoves((i, j), turn)
                elif board[i][j][1] == "N":
                    getPossibleKnightMoves((i, j), turn)
                elif board[i][j][1] == "B":
                    getPossibleBishopMoves((i, j), turn)
                elif board[i][j][1] == "R":
                    getPossibleRookMoves((i, j), turn)
                elif board[i][j][1] == "Q":
                    getPossibleQueenMoves((i, j), turn)
                elif board[i][j][1] == "K":
                    getPossibleKingMoves((i, j), turn)

while True:
    getMoves(turn)
    move = input("move: ")
    if turn == "w":
        moves.append({"w": {"move": move}})
    else:
        moves[-1]["b"] = {"move": move}
    for i in range(len(possibleMoves)):
        if possibleMoves[i]["start"] == giveArrayCoord(move[:2]):
            print("yes")
            break
    
    #print(possibleMoves)
