import sys
import random
import copy 



def printBoard():
	
	board_print = copy.deepcopy(board)
	for i1 in range(board_size):
		for i2 in range(board_size):
			if(board[i1][i2]==0): # white
				board_print[i1][i2]='0'
			if(board[i1][i2]==2): # black
				board_print[i1][i2]='*'
			if(board[i1][i2]==-1): # empty
				board_print[i1][i2]=' '

	for ii in range(len(board)):
		print(board_print[ii])
		print()

def optimized_emptySlots():
	row_total = 0
	col_total = 0
	chess_count = 0
	for i in range(len(board)):
		for j in range(len(board[0])):
			if(board[i][j]==2 or board[i][j]==0):
				row_total += i
				col_total += j
				chess_count += 1

	row_center = int(row_total/chess_count)
	col_center = int(col_total/chess_count)

	# focus in an area of 8*8
	left_limit = max(0,col_center-5)
	right_limit = left_limit+10
	if(right_limit>board_size-1):
		left_limit -= right_limit - (board_size-1)
		right_limit = board_size-1

	up_limit = max(0,row_center-5)
	down_limit = up_limit+10
	if(down_limit>board_size-1):
		up_limit -= down_limit - (board_size-1)
		down_limit = board_size-1

	# print("row center:",row_center)
	# print("col center:",col_center)
	# print("box range up to down:",up_limit,"-",down_limit)
	# print("left to right:",left_limit,"-",right_limit)

	empty = []
	for i in range(up_limit,down_limit):
		for j in range(left_limit,right_limit):
			if(board[i][j]==-1):
				empty.append([i,j])
	return empty


def emptySlots():
	empty = []

	for i in range(len(board)):
		for j in range(len(board[0])):
			if(board[i][j]==-1):
				empty.append([i,j])
	return empty


def numToLet(row,col):
	row_display = row + 1
	col_display = chr(col+97)
	return col_display+str(row_display)

def letToNum(let,num):
	col = int (ord(let)-96) -1
	row = int (num) -1
	return str(row)+" "+str(col)


def Scoring(my_turn, connected_stone, openings): 

    # my turn
    if(my_turn and connected_stone==4 and openings==2): #(4 2)
        return 20000000
    if(my_turn and connected_stone==4 and openings==1): #(4 1)
        return 20000000
    if(my_turn and connected_stone==3 and openings==2): #(3 2)
        return 2500
    if(my_turn and connected_stone==3 and openings==1): #(3 1)
        return 15
    if(my_turn and connected_stone==2 and openings==2): #(2 2)
        return 12
    if(my_turn and connected_stone==2 and openings==1): #(2 1)
        return 6
    if(my_turn and connected_stone==1 and openings==2): #(1 2)
        return 2
    if(my_turn and connected_stone==1 and openings==1): #(1 1)
        return 1


    # not my turn
    if(not(my_turn) and connected_stone==4 and openings==2): #(4 2)
        return 100000
    if(not(my_turn) and connected_stone==4 and openings==1): #(4 1)
        return 100
    if(not(my_turn) and connected_stone==3 and openings==2): #(3 2)
        return 100
    if(not(my_turn) and connected_stone==3 and openings==1): #(3 1)
        return 10
    if(not(my_turn) and connected_stone==2 and openings==2): #(2 2)
        return 10
    if(not(my_turn) and connected_stone==2 and openings==1): #(2 1)
        return 5
    if(not(my_turn) and connected_stone==1 and openings==2): #(1 2)
        return 2
    if(not(my_turn) and connected_stone==1 and openings==1): #(1 1)
        return 1

    # no opening, 0 score
    if(openings==0 and connected_stone<5):
        return 0
    # win already
    else:
        return 50000000


def back_diag(grid):
    grid_size = len(grid)
    new_board = [[-2 for n in range(grid_size+grid_size-1)] for m in range(grid_size)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            k = grid_size -1 -i
            new_board[i][j+k] = grid[i][j]
    
    d_list_back = []
    
    for jj in range(len(new_board[0])):
        this_col = []
        for  ii in range(len(new_board)):
            if(new_board[ii][jj]!=-2):
                this_col.append(new_board[ii][jj])
        d_list_back.append(this_col)
    return d_list_back
    

def forward_diag(grid):
    grid_size = len(grid)
    new_board = [[-2 for n in range(grid_size+grid_size-1)] for m in range(grid_size)]
    k = -1
    for i in range(len(grid)):
        k += 1
        for j in range(len(grid[i])):
            new_board[i][j+k] = grid[i][j]
    
    d_list_forw = []
    
    for jj in range(len(new_board[0])):
        this_col = []
        for  ii in range(len(new_board)):
            if(new_board[ii][jj]!=-2):
                this_col.append(new_board[ii][jj])
        d_list_forw.append(this_col)
    return d_list_forw




def evaluate_row(my_turn,color):
    score = 0
    for i in range(len(board)):
        # reset open and connected to 0 every start of the row
        open_row = 0
        connected_stone = 0
        for j in range(len(board[i])):

            if(board[i][j]==color): # black
                connected_stone = connected_stone+ 1
            else: 
                if(board[i][j] == -1 and connected_stone>0): # empty, and have connected
                    open_row = open_row + 1
                    # get score for this connected
                    score = score + Scoring(my_turn, connected_stone, open_row)
                    # stop checking after this connected is done
                    connected_stone = 0
                    open_row = 1 # set to 1, just one open

                else: 
                    if(board[i][j] == -1): # if only empty
                        open_row = 1
                    else:
                        if(connected_stone > 0): # if only connected, evaluate
                            # get score
                            score = score + Scoring(my_turn, connected_stone, open_row)
                            connected_stone = 0
                            open_row = 0
                        else: # encoutner white then no open
                            open_row = 0

        if(connected_stone > 0): # evaluate every row finishes
            score = score + Scoring(my_turn, connected_stone, open_row)

    return score


def evaluate_diag(my_turn,color,diagonal_list):
    score = 0
    for i in range(len(diagonal_list)):
        open_diag = 0
        connected_stone = 0
        for j in range(len(diagonal_list[i])):
            if(diagonal_list[i][j]==color): 
                connected_stone = connected_stone + 1
            else:
                if(diagonal_list[i][j] == -1 and connected_stone>0): 
                    open_diag += 1
                    score = score + Scoring(my_turn, connected_stone, open_diag)
                    connected_stone = 0
                    open_diag = 1
                else:
                    if(diagonal_list[i][j] == -1):
                        open_diag = 1

                    else:
                        if(connected_stone > 0):
                            score = score + Scoring(my_turn, connected_stone, open_diag)
                            connected_stone = 0
                            open_diag = 0

                        else: 
                            open_diag = 0

        
        if(connected_stone > 0):
            score = score + Scoring(my_turn, connected_stone, open_diag)

    return score


def evaluate_col(my_turn,color):
    score = 0

    # check column iterate vertically, j then i
    for j in range(len(board[0])):
        open_col = 0
        connected_stone = 0
        for i in range(len(board)):
            if(board[i][j]==color): 
                connected_stone =connected_stone+ 1
            else:
                if(board[i][j] == -1 and connected_stone>0):

                    open_col = open_col+1
                    score = score + Scoring(my_turn, connected_stone, open_col)
                    connected_stone = 0
                    open_col = 1
                else:
                    if(board[i][j] == -1):
                        open_col = 1

                    else:
                        if(connected_stone > 0):
                            score = score + Scoring(my_turn, connected_stone, open_col)
                            connected_stone = 0
                            open_col = 0

                        else:
                            open_col = 0

        
        if(connected_stone > 0):
            score = score + Scoring(my_turn, connected_stone, open_col)


    return score








board_size = 11 # (default 11) 5*5 - 26*26
color = 0 # 0: human play black (default)  1: human play white


for itr in range(len(sys.argv)):
	if(sys.argv[itr]=="-l"):
		color = 1
	if(sys.argv[itr]=="-n"):
		board_size = int(sys.argv[itr+1])

# initialize board
board = [[-1 for n in range(board_size)] for m in range(board_size)]

# get conditions
if(color==0): 
	whoMove = 0 # human play black and first move = 0
	human_color = 2
	program_color = 0
	# count = 0 # human play 0 2, program play 1 3
else:
	whoMove = 1 # program play black and first move = 1
	human_color = 0
	program_color = 2

# if empty, -1
# empty slot = -1, black = 2, white = 0
empty = -1

# used only in the first iteration
count = 1

# firstly row and col are undefined
row = -1
col = -1



##########################################
# begin game
for i in range(board_size**2):

	if(whoMove==0): # human move
		move = str(input()) # letter = col, num = row, e.g b3
		col = int (ord(move[0])-96) -1
		row = int (move[1:len(move)]) -1
		board[row][col] = human_color
		print("Move played:",move)

	if(whoMove==1): # my program move
		
		if(count==1): # just for the first move of the program
			if(row==-1 and col==-1): # program make 1st move, human next turn
				S_row = int(board_size/2)
				S_col = int(board_size/2)

				board[S_row][S_col] = program_color
				row_a = S_row + 1
				col_a = chr(S_col+97)
				print("Move played:",col_a+str(row_a))
				count+=1

			else: # if program make 2nd move, following the human 1st move
				if(row+1<board_size): # move down 1
					board[row+1][col] = program_color
					move_row = row+1
					move_col = col
					row_d = move_row + 1
					col_d = chr(move_col+97)
					print("Move played:",col_d+str(row_d))
					count+=1
				else: # move up 1
					board[row-1][col] = program_color
					move_row = row-1
					move_col = col
					row_d = move_row + 1
					col_d = chr(move_col+97)
					print("Move played:",col_d+str(row_d))
					count+=1

		else: # if not first move of the program
			possible_moves1 = emptySlots()

			if(len(possible_moves1)>100): # if many empty slots, optimize
			 	possible_moves1 = optimized_emptySlots()

			Max = -9999999999
			
			best_move = [] # store the best move
			
			for (row1,col1) in possible_moves1: # root to first level
				# alpha = ALPHA
				# beta = BETA
				Min = 9999999999 # min is local I think
				
				# first make the move
				board[row1][col1] = program_color # remember to free this space if not chosen

				score1 = -1 # firstly it is undefined

				possible_moves2 = emptySlots()
				if(len(possible_moves2)>100):
					possible_moves2 = optimized_emptySlots()

				# print("move1 is: ",row1,col1,"[",numToLet(row1,col1),"]")

				for (row2,col2) in possible_moves2: # first to second level

					board[row2][col2] = human_color # remember to free this space if not chosen

					# diagonal list d_list
					d_list = back_diag(board) + forward_diag(board)

					# (currently program's turn!!!!!)
					# score = program_score - human_score

					# check_horizontal(if_current_turn,its color)
					score2 = (evaluate_row(1,program_color)+evaluate_col(1,program_color)+evaluate_diag(1,program_color,d_list)) - (evaluate_row(0,human_color)+evaluate_col(0,human_color)+evaluate_diag(0,human_color,d_list))
					

					# prunning: 
					if(score2<Max):
						# print("PRUNED: score2:",score2,"at(",row2,col2,") < MAX:",Max)
						score1 = score2
						board[row2][col2] = empty # free this space
						break
						

					if(score2<Min):
						# print("2MOVE: (",row2,col2,") [",numToLet(row2,col2),"] score2:",score2,"< Min",Min,": UPDATING MIN = ",score2)
						Min = score2

					# else:
						# print("2MOVE: (",row2,col2,") [",numToLet(row2,col2),"] score2:",score2,">= Min",Min,": so not updating")
						
					score1 = Min
					board[row2][col2] = empty # free this space

				if(score1>Max): # max of mins
					
					# print("1MOVE:(",row1,col1,") [",numToLet(row1,col1),"] score1:",score1,"> MAX",Max,": UPDATE MAX = ",score1)
					Max = score1
					best_move.append(row1)
					best_move.append(col1)

				# else:
					# print("1MOVE:(",row1,col1,") [",numToLet(row1,col1),"]score1:",score1,"<= MAX",Max,": not update MAX")

				# print("--------- move 2 Over")
				board[row1][col1] = -1 # free this space

			# Actually do the move
			move_row = best_move[len(best_move)-2]
			move_col = best_move[len(best_move)-1]
			board[move_row][move_col] = program_color 

			row_display = move_row + 1
			col_display = chr(move_col+97)
			print("Move played:",col_display+str(row_display))

	# alternate round
	whoMove = not whoMove

	printBoard()
	print("------------------------------------------------")





