#REVERSI
import random
import sys

rnge=[]
for i in range(11,89):
        rnge.append(str(i))

def drawBoard(board):
    HLINE='  +---+---+---+---+---+---+---+---+'
    VLINE='  |   |   |   |   |   |   |   |   |'
    print('    1   2   3   4   5   6   7   8')
    print(HLINE)
    for i in range(8):
        print(VLINE)
        print(i+1,end=' ')
        for j in range(8):
            print('| %s' %(board[j][i]),end=' ')
        print('|')
        print(VLINE)
        print(HLINE)

def resetBoard(board):              #2
    for i in range(8):
        for j in range(8):
            board[i][j]=' '


    board[3][3]='X'
    board[4][3]='O'
    board[3][4]='O'
    board[4][4]='X'

def getNewBoard():                  #3
    board=[]
    for i in range(8):
        board.append([' ']*8)

    return board

def isOnBoard(x,y):                 #4
    return (x >= 0 and x <= 7 and y >= 0 and y <= 7)

def isOnCorner(x,y):                #5
    return [x,y] in [[0,0],[7,0],[7,7],[0,7]]


def isValidMove(xs,ys,tile,bo):     #6
    if not isOnBoard(xs,ys) or bo[xs][ys] != ' ':
        return False
    tilesToFlip=[]
    bo[xs][ys]=tile
    x=xs
    y=ys
    if tile=='X':
        otherTile='O'
    else:
        otherTile='X'
    for xd,yd in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
        x+=xd
        y+=yd
        if not isOnBoard(x,y) or bo[x][y]==' ' or bo[x][y]==tile:
                x,y=xs,ys
                continue
        while isOnBoard(x,y) and bo[x][y]==otherTile:
            x+=xd
            y+=yd
        if not isOnBoard(x,y):
            x,y=xs,ys
            continue
        elif bo[x][y]==tile:
            while True:
                x-=xd
                y-=yd
                if bo[x][y]==tile:
                    break
                tilesToFlip.append([x,y])
        
        x,y=xs,ys
    bo[xs][ys]=' '
    if len(tilesToFlip)==0:
        return False
    else:
        return tilesToFlip
    
def getBoardCopy(bo):           #7
    dupBo=getNewBoard()
    for i in range(8):
        for j in range(8):
            dupBo[i][j]=bo[i][j]
    return dupBo

def pA():                       #8
    print('Do you want to play again? (y or n)')
    return input().lower().startswith('y')

def makeMove(x,y,tile,bo):      #9
    ttf=isValidMove(x,y,tile,bo)
    if ttf==False:
        return False
    bo[x][y]=tile
    for i,j in ttf:
        bo[i][j]=tile
    return True

def getValidMoves(tile,bo):     #10
    validMoves=[]
    for i in range(8):
        for j in range(8):
            if not isValidMove(i,j,tile,bo):
                continue
            else:
                validMoves.append([i,j])
    return validMoves

def getBoardWithValidMoves(tile,bo):            #11
    boCopy=getBoardCopy(bo)
    vMoves=getValidMoves(tile,boCopy)
    for i,j in vMoves:
        boCopy[i][j]='.'
    return boCopy

def getScoreOfBoard(pTile,cTile,bo):            #12
    xScore,yScore=0,0
    for i in range(8):
        for j in range(8):
            if bo[i][j]=='X':
                xScore+=1
            elif bo[i][j]=='O':
                yScore+=1
            else:
                continue
    return {'X':xScore,'O':yScore}

def enterPlayerTile():                          #13
    pTile=''
    while not pTile in 'X O'.split():
        print('What do you want "x" or "o"')
        pTile=input().upper()
    if pTile=='X':
        return ['X','O']
    else:
        return ['O','X']

def getPMove(ptile,bo,rnge):                    #14
    vMoves=getValidMoves(pTile,bo)
    if len(vMoves)==0:
        print('You have no possible place to move. Game ends')
        return None
    print('Enter your next move as "xy" for (x,y) or "hints" for hints ')
    Move=input()
    while not Move in rnge or not isValidMove(int(Move[0])-1,int(Move[1])-1,pTile,bo):
        print('Plz enter in valid move range 11 - 88. Enter your next move as "xy" ')
        Move=input()
    return [int(Move[0])-1,int(Move[1])-1]

def getCMove(pTile,cTile,bo):                         #15
    vMoves=getValidMoves(cTile,bo)
    random.shuffle(vMoves)
    maxscore=0
    for x,y in vMoves:
        if isOnCorner(x,y):
            return [x,y]
        score=len(isValidMove(x,y,cTile,bo))
        if score==0:
            return None
        elif score>maxscore:
            maxscore=score
            mx,my=x,y
    if len(vMoves)==0:
        return None
    return [mx,my]

def showPoints(pTile,cTile,bo):                         #16
    score=getScoreOfBoard(pTile,cTile,bo)
    print('Your Sore : %s      CPU score : %s'%(score[pTile],score[cTile]))

def firstMove():                                        #17
    fm=random.randint(0,1)
    if fm==0:
        return 'player'
    else:
        return 'computer'

def isBoardFull(bo):                                    #18
    for i in range(8):
        for j in range(8):
            if bo[i][j]!=' ':
                return False
    return True

print('Welcome to REVERSI ')
while True:
    pTile,cTile=enterPlayerTile()
    bo=getNewBoard()
    resetBoard(bo)
    drawBoard(bo)
    print('Do you want hints for possible moves? "yes" or "no" ')
    ans=input()
    turn=firstMove()
    if turn=='computer':
        print('Computer will go first')
    else:
        print('You will go first')
    while True:
        if turn=='computer':
            
            print('Hit enter to see Computer\'s move .')
            input()
            cMove=getCMove(pTile,cTile,bo)
            if cMove!=None:
                makeMove(cMove[0],cMove[1],cTile,bo)
                drawBoard(bo)
                showPoints(pTile,cTile,bo)

        turn='player'
        if  turn=='player':
            if ans=='yes':
                drawBoard(getBoardWithValidMoves(pTile,bo))
            pMove=getPMove(pTile,bo,rnge)
            if pMove!=None:
                makeMove(pMove[0],pMove[1],pTile,bo)
                drawBoard(bo)
                showPoints(pTile,cTile,bo)

        turn='computer'
        if getValidMoves(cTile,bo)==[] and getValidMoves(pTile,bo)==[]:                     #sdfgh
            print('No next move possible for anyone. Hence this match ends')    #new extra line
            break
        if isBoardFull(bo):
            print('Board is filled completely. Hence this match ends')          #new extra line
            break
    print()                             #new extra line
    print('Final score:')               #new extra line
    showPoints(pTile,cTile,bo)
    scr=getScoreOfBoard(pTile,cTile,bo)
    if scr[pTile]>scr[cTile]:
        print('Hurrey! You defeated computer :o')
    else:
        print('Computer has defeated you')

    if not pA():
        break

print('THANK YOU FOR PLAYING. SEE YOU NEXT TIME :)')



