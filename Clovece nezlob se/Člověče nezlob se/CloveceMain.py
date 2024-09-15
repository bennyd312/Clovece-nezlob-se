"""
Tento soubor bude přijímat input a zobrazovat GameState
"""

import pygame as p
import CloveceEngine
import random

p.init()
p.display.set_caption("Člověče, nezlob se!")
info = p.display.Info()

user_monitor = [info.current_w, info.current_h]

user_size = min(user_monitor)
user_optimal_size = 0
for i in range(100):
    if i*11*11<user_size-50:
        user_optimal_size = i*11*11
    else:
        break

WIDTH = HEIGHT = user_optimal_size  #rozměr
DIMENSION = 11 #dimenze člověče

SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # pro pripadne animace
IMAGES = {}
DIE = {}
outcome = 6
"""
Načítání obrázku do slovníku images
"""

def loadImages():
    #obrázky načteme do slovníku a můžeme k nim tedy v budoucnu přistupovat bez toho, abychom je načítali ze souboru znova
    pieces = ["r1","r2","r3","r4","g1","g2","g3","g4","o1","o2","o3","o4","b1","b2","b3","b4"]
    dices = ["dice1","dice2","dice3","dice4","dice5","dice6"]
    i=1

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE,SQ_SIZE))
    for dice in dices:
        DIE[i] = p.transform.scale(p.image.load("images/" + dice + ".png"), (SQ_SIZE,SQ_SIZE))
        i+=1
    

"""
Zde budeme procesovat input a aktualizovat herní plochu
"""

def main():
    outcome = 1
    p.init()
    screen = p.display.set_mode((WIDTH ,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = CloveceEngine.GameState()
    ts = CloveceEngine.Teams
    loadImages()
    running = True
    gameOver = False
    colours = ["r","o","g","b"]
    ai_delay_move = 1000
    r = ts("Red", [3,3] , str(colours[0]), (4,0),[ [[0],[0]], [[0],[1]], [[1],[0]], [[1],[1]]], ["r1","r2","r3","r4"], "10", "44", ["45","46","47","48"], 0, None, False)
    o = ts("Orange",[3,7] , str(colours[1]), (10,4), [ [[9],[0]], [[9],[1]], [[10],[0]], [[10],[1]]], ["o1","o2","o3","o4"], "40", "40", ["41","42","43","44"], 0, None, False)
    g = ts("Green", [7,3] , str(colours[2]), (0,6), [ [[0],[9]], [[0],[10]], [[1],[9]], [[1],[10]]], ["g1","g2","g3","g4"], "20", "48", ["49","50","51","52"] , 0, None, False)
    b = ts("Blue", [7,7], str(colours[3]), (6,10), [ [[9],[9]], [[9],[10]], [[10],[9]], [[10],[10]]], ["b1","b2","b3","b4"], "30", "52",["56","55","54","53"] , 0, None, False)
    r.following = g
    g.following = b
    b.following = o
    o.following = r
    playing = r
    
    f = open("settings.txt")#zde načítáme data od uživatele
    settings = [r,b,o,g,playing,ai_delay_move]
    results = []#zde dostaneme nastavení od uživatele
    for line in f:
        i=0
        text = line.rstrip()
        result = []
        for char in text:
            if char == "=":
                i = 1
            elif i==0 or char==" ":
                continue
            elif i==1:
                result.append(char)
        results.append("".join(result))

    f.close()
    for i in range(6):
        if i<4:
            if results[i] == "False":
                settings[i].ai = False
            else:
                settings[i].ai = True
        if i==4:
            if results[i] == "Red":
                playing = r
            elif results[i] == "Blue":
                playing = b
            elif results[i] == "Orange":
                playing = o
            elif results[i] == "Green":
                playing = g
        elif i==5:
            ai_delay_move = int(results[i])

    sqSelected = () #ze začátku nemáme žádný čtverec vybraný, zachovává poslední klik uživatele
    playerClicks = [] #záznam kliknutí (dvě tuples) např.: klik od (1,1) do (2,2) je [(1,1),(2,2)]
    diceRolled = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if gameOver == False and playing.ai == False:

                    location = p.mouse.get_pos()#(x,y) souřadnice myši
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if diceRolled == False:
                        if (col,row) == (5,5):
                            outcome = gs.rollDice()
                            sqSelected = ()
                            playerClicks = []
                            diceRolled = True
                            moves = gs.getAllPossibleMoves(playing,outcome)
                            print(moves)
                            if len(moves) == 0:
                                print(playing.name, "has no further valid moves.")
                                diceRolled = False
                                sqSelected = ()
                                playerClicks = []
                                playing = ts.next(playing)
                            else:
                                moves = gs.getAllPossibleMoves(playing,outcome)
                                drawHighlighting(screen, gs.board, moves)
                        else:
                            print("zzz")
                            sqSelected = ()
                            playerClicks = []
##########################################################################################################
                    else:
                        
                        if len(playerClicks)==0: #první kliknutí - uživatel vybírá čim bude hýbat
                            if gs.initial[row][col] in playing.finish:
                                sqSelected = (row,col)
                                playerClicks.append(sqSelected)

                            elif gs.board[row][col] == "--" or gs.board[row][col]=="dice6":#invalid square
                                print("Outside of the playing field")
                                sqSelected = ()
                                playerClicks = []

                            elif gs.board[row][col].isdigit() and len(playerClicks)==0:#clicked playing field first (invalid square)
                                print("Clicked playing field before clicking pawn to move with")
                                sqSelected= ()
                                playerClicks = []

                            else:
                                sqSelected = (row,col)
                                playerClicks.append(sqSelected)

                                
                        elif len(playerClicks)==1:#druhé kliknutí - uživatel vybírá, kam bude hýbat
                            if gs.initial[row][col] in playing.finish:
                                sqSelected = (row,col)
                                playerClicks.append(sqSelected)

                            elif gs.board[row][col] == "--" or gs.board[row][col] == "dice6":
                                print("Invalid square")
                                sqSelected = ()
                                playerClicks = []

                                
                            elif sqSelected == (row,col):#unselect
                                print("Unselected")
                                sqSelected = ()
                                playerClicks = []

                                
                            else:
                                sqSelected = (row,col)
                                playerClicks.append(sqSelected)
                                sqSelected = ()

                        if len(playerClicks)==2:

                            startSq = [[playerClicks[0][0]],[playerClicks[0][1]]]
                            endSq = [[playerClicks[1][0]],[playerClicks[1][1]]]
                            move = CloveceEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            if gs.validMove(move, outcome, playing, 1) == True:
                                print(move.getCloveceNotation())
                                gs.makeMove(move,playing,outcome)
                                if playing.victorypoints == 4:
                                    print(playing.name, "wins the game.")
                                    gameOver = True
                                    drawGameState(screen, gs,outcome)
                                    clock.tick(MAX_FPS)
                                    p.display.flip()
                                    break
                                sqSelected = ()
                                playerClicks = []
                                if outcome == 6:
                                    diceRolled = False
                                    print(playing.name, "rolled 6, rolls again.")
                                else:
                                    diceRolled = False
                                    playing = ts.next(playing)
                            else:
                                print("Invalid move")
                                sqSelected = ()
                                playerClicks = []

##################################################################################################
            elif e.type == p.KEYDOWN:#o krok zpět
                if e.key == p.K_z:
                    if len(gs.moveLog) != 0:
                        outcome = gs.undoMove()
                        if outcome == 6:
                            print("Undone move, currently playing: ", playing.name, "with dice roll outcome: ",outcome)
                            diceRolled = True
                            playerClicks = []
                            sqSelected = ()
                        else:
                            playing = playing.following.following.following
                            print("Undone move, currently playing: ", playing.name, "with dice roll outcome: ",outcome)
                            diceRolled = True
                            playerClicks = []
                            sqSelected = ()
                    else:
                        print("No moves to undo.")
        #ai move finder
        if gameOver == False and playing.ai == True:
            if diceRolled == False:
                outcome = gs.rollDice()
                p.time.delay(ai_delay_move)
                diceRolled = True
                moves = gs.getAllPossibleMoves(playing,outcome)
                if len(moves)==0:
                    print(playing.name, "has no further valid moves.")
                    diceRolled = False
                    playing = ts.next(playing)
                else:
                    moves = gs.getBestMove(gs.getAllPossibleMoves(playing,outcome),playing)
                    if len(moves) == 0:
                        print(playing.name , "has no possible moves for this outcome")
                        if outcome == 6:
                            diceRolled = False
                        else:
                            diceRolled = False
                            playing = ts.next(playing)
                    else:
                        move = moves[random.randint(0, len(moves)-1)]
                        AIMove = CloveceEngine.Move(move[0],move[1], gs.board)
                        p.time.delay(ai_delay_move)
                        print(AIMove.getCloveceNotation())
                        gs.makeMove(AIMove,playing, outcome)
                        if playing.victorypoints == 4:
                            print(playing.name, "wins the game.")
                            gameOver = True
                            drawGameState(screen, gs,outcome,playing)
                            clock.tick(MAX_FPS)
                            p.display.flip()
                            break
                        if outcome == 6:
                            diceRolled = False
                        else:
                            playing = ts.next(playing)
                            diceRolled = False
        
                    
        drawGameState(screen, gs,outcome, playing)
        if len(playerClicks) < 2 and playing.ai == False and diceRolled == True:
            moves = gs.getAllPossibleMoves(playing,outcome)
            drawHighlighting(screen, gs.board, moves)
            
        clock.tick(MAX_FPS)
        p.display.flip()
"""
Načítá grafiku v současném herním vstavu
"""

def drawGameState(screen, gs,outcome, playing):
    drawBoard(screen) #nakreslit pole
    drawPieces(screen , gs.board) #nakreslit figurky
    drawDice(screen, gs.board,outcome) #nakreslit kostku
    drawCurrentTurn(screen, gs.board, playing)

"""
Nakreslí čtverce na herní plochu
"""
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray"), p.Color("green"), p.Color("red"), p.Color("blue"), p.Color("orange")]
    gamefield = {0:[4,5,6] ,1:[4,6], 2:[4,6], 3:[4,6] , 4:[0,1,2,3,4,6,7,8,9,10], 5:[0,10]}#hrací pole, po kterém se budou hýbat figurky
    finish = {0:[100],1:[5],2:[5],3:[5],4:[5],5:[1,2,3,4,6,7,8,9]}# domečky figurek (ve hře kruhy s příslušnými barvami)
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if r<6:
                if c in gamefield[r]:
                    color = colors[1]
                    outline = "black"
                else:
                    color = colors[0]
            else:
                if c in gamefield[10-r]:
                    color = colors[1]
                    outline = "black"
                else:
                    color = colors[0] #zbytek je bílý
            if color == colors[1]:
                p.draw.rect(screen, outline, p.Rect(c*SQ_SIZE+SQ_SIZE/44, r*SQ_SIZE+SQ_SIZE/44, SQ_SIZE-SQ_SIZE/22, SQ_SIZE-SQ_SIZE/22))
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE+SQ_SIZE/22, r*SQ_SIZE+SQ_SIZE/22, SQ_SIZE-SQ_SIZE/11, SQ_SIZE-SQ_SIZE/11))
    i=0
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if r<6:
                if i<4:
                    if c in finish[r]:
                        color = colors[2]
                        p.draw.circle(screen, color, (c*SQ_SIZE+SQ_SIZE/2, r*SQ_SIZE+SQ_SIZE/2),SQ_SIZE/8)
                        i+=1
                elif i<8:
                    if c in finish[r]:
                        color = colors[3]
                        p.draw.circle(screen, color, (c*SQ_SIZE+SQ_SIZE/2, r*SQ_SIZE+SQ_SIZE/2),SQ_SIZE/8)
                        i+=1
                elif i<12:
                    if c in finish[r]:
                        color = colors[4]
                        p.draw.circle(screen, color, (c*SQ_SIZE+SQ_SIZE/2, r*SQ_SIZE+SQ_SIZE/2),SQ_SIZE/8)
                        i+=1
            else:
                if c in finish[10-r]:
                    color = colors[5]
                    p.draw.circle(screen, color, (c*SQ_SIZE+SQ_SIZE/2, r*SQ_SIZE+SQ_SIZE/2),SQ_SIZE/8)
    p.draw.circle(screen, "red", (SQ_SIZE/2, 4*SQ_SIZE+SQ_SIZE/2), SQ_SIZE/4)
    p.draw.circle(screen, "green", (6*SQ_SIZE+SQ_SIZE/2, SQ_SIZE/2), SQ_SIZE/4)
    p.draw.circle(screen, "orange", (4*SQ_SIZE+SQ_SIZE/2, 10*SQ_SIZE + SQ_SIZE/2), SQ_SIZE/4)
    p.draw.circle(screen, "blue", (10*SQ_SIZE+SQ_SIZE/2, 6*SQ_SIZE + SQ_SIZE/2), SQ_SIZE/4)
            
            
"""
Nakreslí figurky podle současného GameState.board
"""
def drawPieces(screen,board):
    spawns = ["RS1","RS2","RS3","RS4","GS1","GS2","GS3","GS4","OS1","OS2","OS3","OS4","BS1","BS2","BS3","BS4"]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--" and not piece.isdigit() and piece != "dice6" and piece not in spawns:
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    stred = board[5][5]
    screen.blit(DIE[6], p.Rect(5*SQ_SIZE, 5*SQ_SIZE, SQ_SIZE,SQ_SIZE))
def drawCurrentTurn(screen, board, playing):
    p.draw.rect(screen, playing.name, p.Rect(playing.display_loc[0]*SQ_SIZE + SQ_SIZE/44, playing.display_loc[1]*SQ_SIZE + SQ_SIZE/44, SQ_SIZE - SQ_SIZE/22, SQ_SIZE-SQ_SIZE/22))

def drawDice(screen,board,outcome):
    piece = board[5][5]
    screen.blit(DIE[outcome], p.Rect(5*SQ_SIZE, 5*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawHighlighting(screen, board, pieces):
    for i in range(len(pieces)):
        p.draw.rect(screen, "lightslateblue", p.Rect((pieces[i][1][1])*SQ_SIZE + SQ_SIZE/44, (pieces[i][1][0])*SQ_SIZE + SQ_SIZE/44, SQ_SIZE - SQ_SIZE/22, SQ_SIZE - SQ_SIZE/22))
    


main()










