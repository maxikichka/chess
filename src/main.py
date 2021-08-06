board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
         ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
         ["0", "0", "0", "0", "0", "0", "0", "0"],
         ["0", "0", "0", "0", "0", "0", "0", "0"],
         ["0", "0", "0", "0", "0", "0", "0", "0"],
         ["0", "0", "0", "0", "0", "0", "0", "0"],
         ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
         ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

check = "n"
moves = []
otherTurn = {"w": "b", "b": "w"}

'''
TODO:
castling
king move
checkmate
ways to draw:
threefold repetition
stalemate
insufficient material
perpetual check
'''

def drawBoard():
    for i in range(len(board)):
        strToPrint = ""
        for j in range(len(board[i])):
            if board[i][j] != "0":
                strToPrint += board[i][j][1] + " "
            else:
                strToPrint += board[i][j] + " "
        print(strToPrint)

def getKingPos(turn):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == turn + "K":
                return (i, j)

def makeMove(piece, startCoords, endCoords, turn):
    originalSquare = board[endCoords[0]][endCoords[1]]
    board[startCoords[0]][startCoords[1]] = "0"
    board[endCoords[0]][endCoords[1]] = turn + piece
    if checkForCheck(getKingPos(turn), board) == False:
        return True
    board[startCoords[0]][startCoords[1]] = turn + piece
    board[endCoords[0]][endCoords[1]] = originalSquare
    return False

def checkForCheck(kingCoords, tempBoard):
    whosChecking = otherTurn[tempBoard[kingCoords[0]][kingCoords[1]][0]]
    for i in range(len(tempBoard)):
        for j in range(len(tempBoard[i])):
            if tempBoard[i][j] != "0":
                if tempBoard[i][j] == whosChecking + "p":
                    if checkForMovePawn((i, j), kingCoords, whosChecking, "isCheck") == True:
                        print("check!")
                        check = tempBoard[kingCoords[0]][kingCoords[1]][0]
                        return True
                elif tempBoard[i][j] == whosChecking + "N":
                    if checkForMoveKnight((i, j), kingCoords, whosChecking) == True:
                        print("check!")
                        check = tempBoard[kingCoords[0]][kingCoords[1]][0]
                        return True
                elif tempBoard[i][j] == whosChecking + "B":
                    if checkForMoveBishop((i, j), kingCoords, whosChecking) == True:
                        print("check!")
                        check = tempBoard[kingCoords[0]][kingCoords[1]][0]
                        return True
                elif tempBoard[i][j] == whosChecking + "R":
                    if checkForMoveRook((i, j), kingCoords, whosChecking) == True:
                        print("check!")
                        check = tempBoard[kingCoords[0]][kingCoords[1]][0]
                        return True
                elif tempBoard[i][j] == whosChecking + "Q":
                    if checkForMoveQueen((i, j), kingCoords, whosChecking) == True:
                        print("check!")
                        check = tempBoard[kingCoords[0]][kingCoords[1]][0]
                        return True
    return False

def giveArrayCoord(coord):
    alphabet = "abcdefgh"
    return (8 - int(coord[1]), alphabet.find(coord[0]))

def checkForMoveKing(kingCoordinates, destinationCoordinates, turn):
    if abs(kingCoordinates[0] - destinationCoordinates[0]) <= 1 and abs(kingCoordinates[1] - destinationCoordinates[1]) <= 1 and board[destinationCoordinates[0]][destinationCoordinates[1]][0] != turn:
        return True
    return False

def checkForMoveQueen(queenCoordinates, destinationCoordinates, turn):
    #just rook and bishop combined
    if checkForMoveRook(queenCoordinates, destinationCoordinates, turn) == False:
        return checkForMoveBishop(queenCoordinates, destinationCoordinates, turn)
    return True

def checkForMoveRook(rookCoordinates, destinationCoordinates, turn):
    if rookCoordinates[0] == destinationCoordinates[0]:
        sameI = 0
        diffI = 1
    elif rookCoordinates[1] == destinationCoordinates[1]:
        sameI = 1
        diffI = 0
    else:
        return False

    start = min(rookCoordinates[diffI], destinationCoordinates[diffI]) + 1
    end = max(rookCoordinates[diffI], destinationCoordinates[diffI])

    for i in range(start, end + 1):
        if i == end and board[destinationCoordinates[0]][destinationCoordinates[1]][0] != turn:
            return True
        if (sameI == 0 and board[rookCoordinates[sameI]][i] != "0") or (sameI == 1 and board[i][rookCoordinates[sameI]] != "0"):
            return False

def checkForMoveBishop(bishopCoordinates, destinationCoordinates, turn):
    #first check if squares lineup diagonally
    if abs(bishopCoordinates[0] - destinationCoordinates[0]) != abs(bishopCoordinates[1] - destinationCoordinates[1]):
        return False
    x = bishopCoordinates[0]
    y = bishopCoordinates[1]
    while True:
        print(x, y)
        x += (bishopCoordinates[0] - destinationCoordinates[0]) // abs(bishopCoordinates[0] - destinationCoordinates[0]) * -1
        y += (bishopCoordinates[1] - destinationCoordinates[1]) // abs(bishopCoordinates[1] - destinationCoordinates[1]) * -1
        if (x, y) == (destinationCoordinates[0], destinationCoordinates[1]) and board[destinationCoordinates[0]][destinationCoordinates[1]][0] != turn:
            return True
        if board[x][y] != "0":
            return False

def checkForMoveKnight(knightCoordinates, destinationCoordinates, turn):
    if (abs(knightCoordinates[0] - destinationCoordinates[0]) == 2 and abs(knightCoordinates[1] - destinationCoordinates[1]) == 1) or (abs(knightCoordinates[0] - destinationCoordinates[0]) == 1 and abs(knightCoordinates[1] - destinationCoordinates[1]) == 2) and board[destinationCoordinates[0]][destinationCoordinates[1]][0] != turn:
        return True
    return False

def checkForMovePawn(pawnCoordinates, destinationCoordinates, turn, purpose):
    if turn == "w":
        if pawnCoordinates[0] - 1 == destinationCoordinates[0] and pawnCoordinates[1] == destinationCoordinates[1] and purpose == "move":
            return True
        elif pawnCoordinates[0] == 6 and pawnCoordinates[0] - 2 == destinationCoordinates[0] and pawnCoordinates[1] == destinationCoordinates[1] and purpose == "move":
            return True
        elif pawnCoordinates[0] - 1 == destinationCoordinates[0] and (pawnCoordinates[1] + 1 == destinationCoordinates[1] or pawnCoordinates[1] - 1 == destinationCoordinates[1]) and board[destinationCoordinates[0]][destinationCoordinates[1]][0] == "b":
            return True
        elif pawnCoordinates[0] == 3 and giveArrayCoord(moves[-2]["b"][3:])[0] == 3 and abs(giveArrayCoord(moves[-2]["b"][3:])[1] - pawnCoordinates[1]) == 1 and giveArrayCoord(moves[-2]["b"][:2])[0] == 1:
            board[giveArrayCoord(moves[-2]["b"][3:])[0]][giveArrayCoord(moves[-2]["b"][3:])[1]] = "0"
            return True
    else:
        if pawnCoordinates[0] + 1 == destinationCoordinates[0] and pawnCoordinates[1] == destinationCoordinates[1] and purpose == "move":
            return True
        elif pawnCoordinates[0] == 1 and pawnCoordinates[0] + 2 == destinationCoordinates[0] and pawnCoordinates[1] == destinationCoordinates[1] and purpose == "move":
            return True
        elif pawnCoordinates[0] + 1 == destinationCoordinates[0] and (pawnCoordinates[1] + 1 == destinationCoordinates[1] or pawnCoordinates[1] - 1 == destinationCoordinates[1]) and board[destinationCoordinates[0]][destinationCoordinates[1]][0] == "w":
            return True
        elif pawnCoordinates[0] == 4 and giveArrayCoord(moves[-1]["w"][3:])[0] == 4 and abs(giveArrayCoord(moves[-1]["w"][3:])[1] - pawnCoordinates[1]) == 1 and giveArrayCoord(moves[-1]["w"][:2])[0] == 6:
            board[giveArrayCoord(moves[-1]["w"][3:])[0]][giveArrayCoord(moves[-1]["w"][3:])[1]] = "0"
            return True

def parseKing(startCoords, endCoords, turn, goToSpot):
    if abs(startCoords[0] - endCoords[0]) <= 1 and abs(startCoords[1] - endCoords[1]) <= 1 and board[endCoords[0]][endCoords[1]][0] != turn:
        print("king move succesfull")
        board[startCoords[0]][startCoords[1]] = "0"
        board[endCoords[0]][endCoords[1]] = turn + "K"
    else:
        return "invalid move"

def parseMove(move, turn):
    startCoords = giveArrayCoord(move[:2])
    endCoords = giveArrayCoord(move[3:])
    piece = board[startCoords[0]][startCoords[1]]
    goToSpot = board[endCoords[0]][endCoords[1]]
    if piece == turn + "p":
        if checkForMovePawn(startCoords, endCoords, turn, "move") == True:
            return makeMove("p", startCoords, endCoords, turn)
    elif piece == turn + "N":
        if checkForMoveKnight(startCoords, endCoords, turn) == True:
            return makeMove("N", startCoords, endCoords, turn)
    elif piece == turn + "B":
        if checkForMoveBishop(startCoords, endCoords, turn) == True:
            return makeMove("B", startCoords, endCoords, turn)
    elif piece == turn + "R":
        if checkForMoveRook(startCoords, endCoords, turn) == True:
            return makeMove("R", startCoords, endCoords, turn)
    elif piece == turn + "Q":
        if checkForMoveQueen(startCoords, endCoords, turn) == True:
            return makeMove("Q", startCoords, endCoords, turn)
    elif piece == turn + "K":
        if checkForMoveKing(startCoords, endCoords, turn) == True:
            return makeMove("K", startCoords, endCoords, turn)
    return False

def main():
    done = False
    turn = "w"

    while not done:
        drawBoard()
        print(turn)
        move = input("Your move: ")

        if turn == "w":
            moves.append({"w": move})
        else:
            moves[-1]["b"] = move

        if parseMove(move, turn) == False:
            print("invalid move")
            if turn == "w":
                try:
                    moves.remove(-1)
                except ValueError:
                    pass
            continue

        if turn == "w":
            #checkForCheck(getKingPos("b"), board)
            turn = "b"
        else:
            #checkForCheck(getKingPos("w"), board)
            turn = "w"
main()
