"""
Bude ukládat informace o současném stavu hry, bude také zhodnocovat možné tahy a udržovat log pohybů hráčů
"""
import random

class GameState():
    def __init__(self):
        #herní plochu reprezentujeme seznamem o rozměrech 11x11
        #první písmeno reprezentuje barvu
        #číslo reprezentuje pořadí
        #"--" reprezentuje postranní pole
        #"--" reprezentuje prázdné herní pole
        self.board = [
            ["r1","r2","--","--","19","20","21","--","--","g1","g2"],
            ["r3","r4","--","--","18","--","22","--","--","g3","g4"],
            ["--","--","--","--","17","--","23","--","--","--","--"],
            ["--","--","--","--","16","--","24","--","--","--","--"],
            ["11","12","13","14","15","--","25","26","27","28","29"],
            ["10","--","--","--","--","dice6","--","--","--","--","30"],
            ["9","8","7","6","5","--","35","34","33","32","31"],
            ["--","--","--","--","4","--","36","--","--","--","--"],
            ["--","--","--","--","3","--","37","--","--","--","--"],
            ["o1","o2","--","--","2","--","38","--","--","b1","b2"],
            ["o3","o4","--","--","1","40","39","--","--","b3","b4"]]
        self.initial = [
            ["RS1","RS2","--","--","19","20","21","--","--","GS1","GS2"],
            ["RS3","RS4","--","--","18","49","22","--","--","GS3","GS4"],
            ["--","--","--","--","17","50","23","--","--","--","--"],
            ["--","--","--","--","16","51","24","--","--","--","--"],
            ["11","12","13","14","15","52","25","26","27","28","29"],
            ["10","45","46","47","48","dice6","56","55","54","53","30"],
            ["9","8","7","6","5","44","35","34","33","32","31"],
            ["--","--","--","--","4","43","36","--","--","--","--"],
            ["--","--","--","--","3","42","37","--","--","--","--"],
            ["OS1","OS2","--","--","2","41","38","--","--","BS1","BS2"],
            ["OS3","OS4","--","--","1","40","39","--","--","BS3","BS4"]]

        self.moveLog = []
        self.outcomeLog = []
        self.captureLog = []

    def makeMove(self, move, playing, outcome):
        def backToBase(pawn,spawns):
            x = spawns[pawn][0]
            y = spawns[pawn][1]
            self.board[x[0]][y[0]] = move.pieceCaptured


                
        players = ["r1","r2","r3","r4","b1","b2","b3","b4","g1","g2","g3","g4","o1","o2","o3","o4"]
        spawns_red = { "r1":[[0],[0]],"r2":[[0],[1]],"r3":[[1],[0]], "r4" : [[1],[1]]}
        spawns_green = { "g1": [[0],[9]], "g2":[[0],[10]], "g3":[[1],[9]], "g4":[[1],[10]]}
        spawns_blue ={"b1": [[9],[9]], "b2":[[9],[10]], "b3":[[10],[9]], "b4":[[10],[10]]}
        spawns_orange = {"o1":[[9],[0]], "o2":[[9],[1]], "o3":[[10],[0]], "o4":[[10],[1]]}

        self.board[move.startRow][move.startCol] = self.initial[move.startRow][move.startCol]
        if [[move.endRow],[move.endCol]] == [[playing.deployment[0]],[playing.deployment[1]]]:
            if self.board[move.endRow][move.endCol] in players:
                self.captureLog.append(self.board[move.endRow][move.endCol])
                pawn = self.board[move.endRow][move.endCol]
                ######
                if pawn in playing.following.pawns or pawn in playing.following.following.pawns or pawn in playing.following.following.following.pawns:
                    #pokud hráč zabere figurku někomu jinému..

                    if pawn in spawns_red.keys():
                        backToBase(pawn,spawns_red)

                    elif pawn in spawns_green.keys():
                        backToBase(pawn,spawns_green)

                    elif pawn in spawns_blue.keys():
                        backToBase(pawn,spawns_blue)

                    elif pawn in spawns_orange.keys():
                        backToBase(pawn,spawns_orange)

                    self.board[move.endRow][move.endCol] = move.pieceMoved
                
            else:
                self.board[move.endRow][move.endCol] = move.pieceMoved
                self.captureLog.append("--")
                
                #######
            self.board[move.endRow][move.endCol] = move.pieceMoved
        elif self.board[move.endRow][move.endCol] in players:
            self.captureLog.append(self.board[move.endRow][move.endCol])
            pawn = self.board[move.endRow][move.endCol]
            if pawn in playing.following.pawns or pawn in playing.following.following.pawns or pawn in playing.following.following.following.pawns:

                if pawn in spawns_red.keys():
                    backToBase(pawn,spawns_red)

                elif pawn in spawns_green.keys():
                    backToBase(pawn,spawns_green)

                elif pawn in spawns_blue.keys():
                    backToBase(pawn,spawns_blue)

                elif pawn in spawns_orange.keys():
                    backToBase(pawn,spawns_orange)

                self.board[move.endRow][move.endCol] = move.pieceMoved
            
        elif self.initial[move.endRow][move.endCol] in playing.finish:
            self.captureLog.append("--")
            self.board[move.endRow][move.endCol] = move.pieceMoved
            playing.victorypoints += 1
        else:
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.captureLog.append("--")
        self.moveLog.append(move)
        self.outcomeLog.append(outcome)

        
    def undoMove(self):
        players = ["r1","r2","r3","r4","g1","g2","g3","g4","b1","b2","b3","b4","o1","o2","o3","o4"]
        
        move = self.moveLog.pop()
        outcome = self.outcomeLog.pop()
        piece = self.captureLog.pop()

        if piece in players:
            for r in range(len(self.board)):
                for c in range(len(self.board[r])):#hledáme souřadnice figurky
                    if self.board[r][c] == piece:
                        self.board[r][c] = "--"
                        break

        
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured        
        return outcome


    def validMove(self, move, outcome, playing, annotation):
        forbidden1 = ["39","40"]
        forbidden2 = ["45","46"]
        
        if self.initial[move.startRow][move.startCol].isdigit():
            if self.initial[move.startRow][move.startCol] in playing.finish:
                #zákaz pohybu vně finishe
                if annotation == 1:
                    print("Moving inside finish not allowed")
                return False
            #elif self.board[move.startRow][move.startCol][0] is not playing.colour:
                #zákaz pohybu figurkami ostatních
                #if annotation == 1:
                    #print("Cannot move other players pawns")
                #return False
            elif int(self.initial[move.startRow][move.startCol])<= int(playing.finishline) and int(self.initial[move.startRow][move.startCol]) + outcome > int(playing.finishline) and self.initial[move.endRow][move.endCol] not in playing.finish:
                #zákaz minutí finishe
                if annotation == 1:
                    print("Missing finish not allowed")
                return False
            elif playing.name == "Red" and self.initial[move.startRow][move.startCol] in forbidden1 and self.initial[move.endRow][move.endCol] in forbidden2:
                #zákaz skoku červené figurky z políčka "39" nebo z políčka "40" do základny
                return False
            elif [[move.endRow],[move.endCol]] in playing.following.base or [[move.endRow],[move.endCol]] in playing.following.following.base or [[move.endRow],[move.endCol]] in playing.following.following.following.base:
                #zákaz vstupu do základny jiného týmu
                if annotation == 1:
                    print("Moving inside other players base is not allowed")
                return False

            elif str((outcome+int(self.initial[move.startRow][move.startCol]))%40) == self.initial[move.endRow][move.endCol]:
                #pokud hráčův (výsledek hodu kostky) + (číslo políčka začátku) == (číslo políčka konce)
                if self.checkTeamkill(move) == False:
                    return True

            elif str((outcome+int(self.initial[move.startRow][move.startCol]))) == self.initial[move.endRow][move.endCol]:
                #speciální podmínka navíc, doplňující předchozí podmínku pro pole č.40 (modulo)
                if self.checkTeamkill(move) == False:
                    return True
            elif int(self.initial[move.startRow][move.startCol])<=int(playing.finishline) and outcome + int(self.initial[move.startRow][move.startCol]) > int(playing.finishline):
            #pokud (počáteční políčko < finishline) a zároveň (outcome + počáteční políčko > finishline), pak...
                movesleft = outcome + int(self.initial[move.startRow][move.startCol]) - int(playing.finishline)
                
                if str(movesleft + int(playing.finishlinev)) == self.initial[move.endRow][move.endCol]:
                    #pokud outcome + počáteční políčko - finishline + finishline(value) == koncové políčko, hráč může figurku posunout do finishe
                    if self.checkTeamkill(move) == False:
                        return True
                    else:
                        return False
                else:
                    if annotation == 1:
                        print("Can cross finishline, wrong end square")
                    return False
            
        elif [[move.startRow],[move.startCol]] in playing.base:
            
            if outcome == 6 and [[move.endRow],[move.endCol]] == [[playing.deployment[0]],[playing.deployment[1]]]:
                #pokud outcome == 6 a zároveň počáteční políčko je v playing.base a zároveň hráč klik na svůj deployment => spawn
                if self.checkTeamkill(move) == False:
                    return True
                else:
                    return False
        else:
            return False
            
        


    def checkTeamkill(self, move):
        
        
        if self.board[move.startRow][move.startCol][0] == self.board[move.endRow][move.endCol][0]:
            return True
            print("Teamkilling not allowed")
        
        else:
            return False

     
    def getAllPossibleMoves(self, playing, outcome):
        moves = []
        for r1 in range(len(self.board)):
            for c1 in range(len(self.board[r1])):#(r1,c1) je počáteční souřadnice figurky
                if self.board[r1][c1] in playing.pawns and self.initial[r1][c1] not in playing.finish:
                    piece = self.board[r1][c1]
                    for r2 in range(len(self.initial)):
                        for c2 in range(len(self.initial[r2])):
                            if self.initial[r2][c2] != "--":
                                if self.initial[r2][c2] not in playing.following.finish and self.initial[r2][c2] not in playing.following.following.finish and self.initial[r2][c2] not in playing.following.following.following.finish:
                                    if [[r2],[c2]] not in playing.following.base and [[r2],[c2]] not in playing.following.following.base and [[r2],[c2]] not in playing.following.following.following.base and [[r2],[c2]]==[[4],[1]]:
                                        move = Move((r1,c1),(r2,c2), self.board)
                                        if self.validMove(move,outcome, playing, 0) == True:
                                            moves.append([(r1,c1),(r2,c2)])
                                    elif [[r2],[c2]] not in playing.following.base and [[r2],[c2]] not in playing.following.following.base and [[r2],[c2]] not in playing.following.following.following.base:
                                        move = Move((r1,c1),(r2,c2), self.board)
                                        if self.validMove(move,outcome, playing, 0) == True:
                                            moves.append([(r1,c1),(r2,c2)])
                            
        return moves
    def getBestMove(self, moves, playing):
        killingmoves_human = []
        killingmoves_ai = []
        finishmoves = []
        for i in range(len(moves)):
            if self.board[moves[i][1][0]][moves[i][1][1]] in playing.finish:
                finishmoves.append(moves[i])
            elif self.board[moves[i][1][0]][moves[i][1][1]] in playing.following.pawns:
                if playing.following.ai == True:
                    killingmoves_ai.append(moves[i])
                else:
                    killingmoves_human.append(moves[i])
            elif self.board[moves[i][1][0]][moves[i][1][1]] in playing.following.following.pawns:
                if playing.following.following.ai == True:
                    killingmoves_ai.append(moves[i])
                else:
                    killingmoves_human.append(moves[i])
            elif self.board[moves[i][1][0]][moves[i][1][1]] in playing.following.following.following.pawns:
                if playing.following.following.following.ai == True:
                    killingmoves_ai.append(moves[i])
                else:
                    killingmoves_human.append(moves[i])
        if len(finishmoves)!= 0:
            return finishmoves
        elif len(killingmoves_human) !=0:
            return killingmoves_human
        elif len(killingmoves_ai) != 0:
            return killingmoves_ai
        else:
            return moves
                            
            
        
                    
    def rollDice(self):
        outcome = random.randint(1,6)
        print("Player rolls: ", outcome)
        return outcome

                
        
            
class Teams():
    def __init__(self, name, display_loc, colour, deployment ,base, pawns, finishline, finishlinev, finish, victorypoints, following, ai):
        self.name = name
        self.display_loc = display_loc
        self.colour = colour
        self.deployment = deployment
        self.base = base
        self.pawns = pawns
        self.finishline = finishline
        self.finishlinev = finishlinev
        self.finish = finish
        self.victorypoints = 0
        self.following = None
        self.ai = ai

    def next(x):
        print(x.name, "'s turn has ended. Current turn: ", x.following.name, sep="")
        return x.following




class Move():
    initial = [
            ["RS1","RS2","--","--","19","20","21","--","--","GS1","GS2"],
            ["RS3","RS4","--","--","18","49","22","--","--","GS3","GS4"],
            ["--","--","--","--","17","50","23","--","--","--","--"],
            ["--","--","--","--","16","51","24","--","--","--","--"],
            ["11","12","13","14","15","52","25","26","27","28","29"],
            ["10","45","46","47","48","dice6","56","55","54","53","30"],
            ["09","08","07","06","05","44","35","34","33","32","31"],
            ["--","--","--","--","04","43","36","--","--","--","--"],
            ["--","--","--","--","03","42","37","--","--","--","--"],
            ["OS1","OS2","--","--","02","41","38","--","--","BS1","BS2"],
            ["OS3","OS4","--","--","01","40","39","--","--","BS4","BS4"]]

    row = [0,1,2,3,4,5,6,7,8,9,10]
    col = [0,1,2,3,4,5,6,7,8,9,10]


    def __init__(self, startSq, endSq, board):
        #uživatel se chce posunout od startSq do endSq (pouze tato informace)
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getCloveceNotation(self):
        #umožňuje nám zaznamenávat kroky
        return self.getRankFile(self.startRow, self.startCol) + " to " + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.initial[r][c]














    
