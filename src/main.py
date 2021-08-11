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
ways to draw:
threefold repetition
stalemate
insufficient material
'''

def checkForFiftyMoveRule():
    if len(moves) - 49 <= 0:
        return False
    i = len(moves) - 1
    while i > len(moves) - 49:
        print(i)
        try:
            if moves[i]["w"]["piece"][-1] == "p" or moves[i]["w"]["goto"][0] != "0" or moves[i]["b"]["piece"][-1] == "p" or moves[i]["b"]["goto"][0] != "0":
                return False
        except IndexError:
            return False
        except KeyError:
            pass
        i -= 1
    return True

def tryToBlockCheck(kingCoordinates, checkingPieceCoordinates, turn):
    print(kingCoordinates, checkingPieceCoordinates)
    if kingCoordinates[0] == checkingPieceCoordinates[0] or kingCoordinates[1] == checkingPieceCoordinates[1]:
        #rook
        squares = checkForMoveRook(checkingPieceCoordinates, kingCoordinates, turn, True)
        print(squares)
        for i in range(len(squares)):
            if checkForCheck(squares[i], board, turn) == False:
                return False
    else:
        #bishop
        return
    return True

def pieceHasMoved(turn, square):
    for i in range(len(moves) - 1):
        if giveArrayCoord(moves[i][turn]["move"][:2])[0] == square[0] and giveArrayCoord(moves[i][turn]["move"][:2])[1] == square[1]:
            return True
    return False

def giveArrayCoord(coord):
    alphabet = "abcdefgh"
    return (8 - int(coord[1]), alphabet.find(coord[0]))

def drawBoard():
    for i in range(len(board)):
        strToPrint = ""
        for j in range(len(board[i])):
            if board[i][j] != "0":
                strToPrint += board[i][j][1] + " "
            else:
                strToPrint += board[i][j] + " "
        print(strToPrint)

def makeMove(piece, startCoords, endCoords, turn):
    originalSquare = board[endCoords[0]][endCoords[1]]
    board[startCoords[0]][startCoords[1]] = "0"
    board[endCoords[0]][endCoords[1]] = turn + piece
    #has to check for check 2 times, if they are in check and if opponent is in check
    if checkForCheck(getKingPos(turn), board, otherTurn[turn]) == False:
        print(checkForFiftyMoveRule())
        if checkForCheck(getKingPos(otherTurn[turn]), board, turn) != False:
            print("check!!")
            #now check if checkmate
            if isCheckmate(getKingPos(otherTurn[turn]), turn) == True:
                print("checkmate!!")
        return True
    board[startCoords[0]][startCoords[1]] = turn + piece
    board[endCoords[0]][endCoords[1]] = originalSquare
    return False

def checkForCheck(kingCoords, tempBoard, turn):
    whosChecking = turn
    for i in range(len(tempBoard)):
        for j in range(len(tempBoard[i])):
            if tempBoard[i][j] != "0":
                if tempBoard[i][j] == whosChecking + "p":
                    if checkForMovePawn((i, j), kingCoords, whosChecking, "isCheck") == True:
                        return (i, j)
                elif tempBoard[i][j] == whosChecking + "N":
                    if checkForMoveKnight((i, j), kingCoords, whosChecking) == True:
                        return (i, j)
                elif tempBoard[i][j] == whosChecking + "B":
                    if checkForMoveBishop((i, j), kingCoords, whosChecking) == True:
                        return (i, j)
                elif tempBoard[i][j] == whosChecking + "R":
                    if checkForMoveRook((i, j), kingCoords, whosChecking, False) != False:
                        #print("ROOK CHECK!!!")
                        return (i, j)
                elif tempBoard[i][j] == whosChecking + "Q":
                    if checkForMoveQueen((i, j), kingCoords, whosChecking) == True:
                        return (i, j)
    return False

def getKingPos(turn):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == turn + "K":
                return (i, j)

def isCheckmate(kingCoordinates, turn):
    opts = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, 1], [1, 0], [1, -1]]
    #check if king can move out of check
    for i in range(len(opts)):
        if board[kingCoordinates[0] + opts[i][0]][kingCoordinates[1] + opts[i][1]] == "0":
            if kingCoordinates[0] + opts[i][0] in range(0, 7) and kingCoordinates[1] + opts[i][1] in range(0, 7) and checkForCheck((kingCoordinates[0] + opts[i][0], kingCoordinates[1] + opts[i][1]), board, turn) == False and board[kingCoordinates[0] + opts[i][0]][kingCoordinates[1] + opts[i][1]][0] != turn:
                print(board[kingCoordinates[0] + opts[i][0]][kingCoordinates[1] + opts[i][1]][0], turn)
                print(kingCoordinates[0] + opts[i][0], kingCoordinates[1] + opts[i][1], False)
                return False
    print("cant move")
    checkingPiece = checkForCheck(kingCoordinates, board, turn)
    print(checkingPiece)
    #check if checking piece can be taken
    if checkForCheck(checkingPiece, board, otherTurn[turn]) != False: #replace kingCoords with square where checking piece is
        return False
    print("cant capture")
    #now check through every square that can block checking piece
    if tryToBlockCheck(kingCoordinates, checkingPiece, turn) == True:
        return False
    return True

def checkForCastling(kingCoordinates, destinationCoordinates, turn):
    if turn == "w":
        row = 7
    else:
        row = 0
    if kingCoordinates[0] == row and kingCoordinates[1] == 4 and destinationCoordinates[0] == row and destinationCoordinates[1] == 6:
        #if kingside castling
        if (board[row][4] == turn + "K" and
            board[row][5] == "0" and checkForCheck((row, 5), board, otherTurn[turn]) == False and
            board[row][6] == "0" and checkForCheck((row, 6), board, otherTurn[turn]) == False and
            board[row][7] == turn + "R"):
            
            if pieceHasMoved(turn, kingCoordinates) == False and pieceHasMoved(turn, (row, 7)) == False:
                board[row][5] = turn + "R"
                board[row][7] = "0"
                return True
    elif kingCoordinates[0] == row and kingCoordinates[1] == 4 and destinationCoordinates[0] == row and destinationCoordinates[1] == 2:
        #if queenside castling
        if (board[row][4] == turn + "K" and
            board[row][3] == "0" and checkForCheck((row, 3), board, turn) == False and
            board[row][2] == "0" and checkForCheck((row, 2), board, turn) == False and
            board[row][1] == "0" and checkForCheck((row, 1), board, turn) == False and
            board[row][0] == turn + "R"):
            
            if pieceHasMoved(turn, kingCoordinates) == False and pieceHasMoved(turn, (row, 0)) == False:
                board[row][3] = turn + "R"
                board[row][0] = "0"
                return True
    return False

def checkForMoveKing(kingCoordinates, destinationCoordinates, turn):
    if abs(kingCoordinates[0] - destinationCoordinates[0]) <= 1 and abs(kingCoordinates[1] - destinationCoordinates[1]) <= 1 and board[destinationCoordinates[0]][destinationCoordinates[1]][0] != turn:
        return True
    return checkForCastling(kingCoordinates, destinationCoordinates, turn)

def checkForMoveQueen(queenCoordinates, destinationCoordinates, turn):
    #just rook and bishop combined
    if checkForMoveRook(queenCoordinates, destinationCoordinates, turn, False) == False:
        return checkForMoveBishop(queenCoordinates, destinationCoordinates, turn)
    return True

def checkForMoveRook(rookCoordinates, destinationCoordinates, turn, squareChecking):
    squares = []
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
            return squares
        if sameI == 0:
            squares.append([rookCoordinates[sameI], i])
            if board[rookCoordinates[sameI]][i] != "0":
                return False
        else:
            squares.append([i, rookCoordinates[sameI]])
            if board[i][rookCoordinates[sameI]] != "0":
                return False

def checkForMoveBishop(bishopCoordinates, destinationCoordinates, turn):
    #first check if squares lineup diagonally
    if abs(bishopCoordinates[0] - destinationCoordinates[0]) != abs(bishopCoordinates[1] - destinationCoordinates[1]):
        return False
    x = bishopCoordinates[0]
    y = bishopCoordinates[1]
    while True:
        #print(x, y)
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
        elif pawnCoordinates[0] == 3 and giveArrayCoord(moves[-2]["b"]["move"][3:])[0] == 3 and abs(giveArrayCoord(moves[-2]["b"]["move"][3:])[1] - pawnCoordinates[1]) == 1 and giveArrayCoord(moves[-2]["b"]["move"][:2])[0] == 1:
            board[giveArrayCoord(moves[-2]["b"]["move"][3:])[0]][giveArrayCoord(moves[-2]["b"]["move"][3:])[1]] = "0"
            return True
    else:
        if pawnCoordinates[0] + 1 == destinationCoordinates[0] and pawnCoordinates[1] == destinationCoordinates[1] and purpose == "move":
            return True
        elif pawnCoordinates[0] == 1 and pawnCoordinates[0] + 2 == destinationCoordinates[0] and pawnCoordinates[1] == destinationCoordinates[1] and purpose == "move":
            return True
        elif pawnCoordinates[0] + 1 == destinationCoordinates[0] and (pawnCoordinates[1] + 1 == destinationCoordinates[1] or pawnCoordinates[1] - 1 == destinationCoordinates[1]) and board[destinationCoordinates[0]][destinationCoordinates[1]][0] == "w":
            return True
        elif pawnCoordinates[0] == 4 and giveArrayCoord(moves[-1]["w"]["move"][3:])[0] == 4 and abs(giveArrayCoord(moves[-1]["w"]["move"][3:])[1] - pawnCoordinates[1]) == 1 and giveArrayCoord(moves[-1]["w"]["move"][:2])[0] == 6:
            board[giveArrayCoord(moves[-1]["w"]["move"][3:])[0]][giveArrayCoord(moves[-1]["w"]["move"][3:])[1]] = "0"
            return True

def parseMove(move, turn):
    startCoords = giveArrayCoord(move[:2])
    endCoords = giveArrayCoord(move[3:])
    piece = board[startCoords[0]][startCoords[1]]
    goToSpot = board[endCoords[0]][endCoords[1]]
    moves[-1][turn]["piece"] = piece
    moves[-1][turn]["goto"] = goToSpot
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
        if checkForMoveRook(startCoords, endCoords, turn, False) != False:
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
            moves.append({"w": {"move": move}})
        else:
            moves[-1]["b"] = {"move": move}

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
