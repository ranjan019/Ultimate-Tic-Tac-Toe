import sys
import random
import signal
import copy
class Player9:
	
	def __init__(self):
		# self._ALPHA_BETA_DEPTH=2
		# self._acts_res=[]
		self.maxxx=100000000000
		# You may initialize your object here and use any variables for storing throughout the game
		pass

	MAXX = 9223372036854775807
	def move(self,state,temp_block,old_move,flag):
		#List of permitted blocks, based on old move.
		blocks_allowed = self.determine_blocks_allowed(old_move, temp_block)
		#Get list of empty valid cells
		cells = self.get_empty_out_of(state, blocks_allowed,temp_block)
		acts_res=[]
		ALPHA_BETA_DEPTH=3
	    	

		if(len(cells) == 1):
			return(cells[0][0],cells[0][1])

		for action in cells:
			successor_state=self.generate_successor(state,action,flag)
			acts_res.append((action, self.__min_val_ab(successor_state,ALPHA_BETA_DEPTH, temp_block, flag, action,cells)))


		best_val = max(acts_res, key=lambda x: x[1])
		best_cell=best_val[0]
		row=best_cell[0]
		col=best_cell[1]
		return best_cell

	def generate_successor(self, state, action, flag):
		board = copy.deepcopy(state)
		board[action[0]][action[1]] = flag
		return board

	def __min_val_ab(self,state, depth, temp_block, flag, old_move,alpha=-(MAXX), beta=(MAXX)):	
		if self.terminal_test(state, depth, temp_block):
			return self.eval_state(state, temp_block, flag)
		val = (self.maxxx)
		blocks_allowed = self.determine_blocks_allowed(old_move, temp_block)
		cells = self.get_empty_out_of(state, blocks_allowed,temp_block)

		for action in cells:	
			successor_state = self.generate_successor(state, action, flag)
			val = min(val, self.__max_val_ab(successor_state,  depth - 1, temp_block, flag, action, alpha, beta))
			if val <= alpha:
				return val
			beta = min(beta, val)
		return val

	
	def __max_val_ab(self,state, depth, temp_block,flag, old_move, alpha=-(MAXX), beta=(MAXX)):
		if self.terminal_test(state, depth, temp_block):
			return self.eval_state(state, temp_block, flag)
		val = -(self.maxxx)
		blocks_allowed = self.determine_blocks_allowed(old_move, temp_block)
		cells = self.get_empty_out_of(state, blocks_allowed,temp_block)

		for action in cells:
			successor_state = self.generate_successor(state, action, flag)
			val = max(val, self.__min_val_ab(successor_state, depth, temp_block, flag, action, alpha, beta))
			if val >= beta:
				return val
			alpha = max(alpha, val)
		return val


	def terminal_test(self,state, depth, temp_block):
		if depth==0:
			return True
		a,b =  self.terminal_state_reached(state, temp_block,100,100)
		return a

	def eval_state(self,state,temp_block,flag):
		uttt_board = copy.deepcopy(state)
		mini_board = copy.deepcopy(temp_block)
		score_calc=0
		score=0
		# """if moving in this block else subtract score"""
		# for i in range(3):
		# 	for j in range(3):
		# 		k=3*i
		# 		m=3*j
		# 		for a in range(3+k):
		# 			for b in range(3+m)
		# 			if uttt_board[a][b]==flag:
		# 				cc++;
		# 			elif uttt_board[a][b]==flagop:
		# 				cco--;
		# 		if(cc-cco>=2 ):
		# 			score_calc+=100
		# 		elif(cc-cco>=1 ):
		# 			score_calc+=50
		# 		elif(cco-cc>=2):
		# 			score_calc+=70
		# 		elif(cco-cc>0):
		# 			score_calc+=20
		# 		else:
		# 			score_calc=0

		# """heuristic big board"""
		for i in range(3):
			for j in range(3):
				k=3*i
				m=3*j
				score+=self.modify_score_row(k,m,flag,uttt_board,score_calc)
				score+=self.modify_score_col(k,m,flag,uttt_board,score_calc)
		        score+=self.modify_score_d1(k,m,flag,uttt_board,score_calc)
		        score+=self.modify_score_d2(k,m,flag,uttt_board,score_calc)
	def modify_score_row(self,k,m,flag,uttt_board,score_calc):
		if(flag == 'x'):
			flagop='o'
		else:
			flagop='x'

		if uttt_board[k][m]==flag:
			score_calc+=10
			if uttt_board[k][m+1]==flag:
				score_calc+=90
				if uttt_board[k][m+2]==flag:
					score_calc+=900
		elif uttt_board[k][m+1]==flag:
			score_calc+=10
			if uttt_board[k][m+2]==flag:
					score_calc+=90
		elif uttt_board[k][m+2]==flag:
			score_calc+=10

		if uttt_board[k][m]==flagop:
			score_calc-=10
			if uttt_board[k][m+1]==flagop:
				score_calc-=90
				if uttt_board[k][m+2]==flagop:
					score_calc-=900
		elif uttt_board[k][m+1]==flagop:
			score_calc-=10
			if uttt_board[k][m+2]==flagop:
					score_calc-=90
		elif uttt_board[k][m+2]==flagop:
			score_calc-=10
		return score_calc

	def modify_score_col(self,k,m,flag,uttt_board,score_calc):
		
		if(flag == 'x'):
			flagop='o'
		else:
			flagop='x'

		if uttt_board[k][m]==flag:
			score_calc+=10
			if uttt_board[k+1][m]==flag:
				score_calc+=90
				if uttt_board[k+2][m]==flag:
					score_calc+=900
		elif uttt_board[k+1][m]==flag:
			score_calc+=10
			if uttt_board[k+2][m]==flag:
					score_calc+=90
		elif uttt_board[k+2][m]==flag:
			score_calc+=10

		if uttt_board[k][m]==flagop:
			score_calc-=10
			if uttt_board[k+1][m]==flagop:
				score_calc-=90
				if uttt_board[k+2][m]==flagop:
					score_calc-=900
		elif uttt_board[k+1][m]==flagop:
			score_calc-=10
			if uttt_board[k+2][m]==flagop:
					score_calc-=90
		elif uttt_board[k+2][m]==flagop:
			score_calc-=10
		return score_calc

	def modify_score_d1(self,k,m,flag,uttt_board,score_calc):
		
		if(flag == 'x'):
			flagop='o'
		else:
			flagop='x'

		if uttt_board[k][m]==flag:
			score_calc+=10*2
			if uttt_board[k+1][m+1]==flag:
				score_calc+=90*2
				if uttt_board[k+2][m+2]==flag:
					score_calc+=900*2
		elif uttt_board[k+1][m+1]==flag:
			score_calc+=10*2
			if uttt_board[k+2][m+2]==flag:
					score_calc+=90*2
		elif uttt_board[k+2][m+2]==flag:
			score_calc+=10*2

		if uttt_board[k][m]==flagop:
			score_calc-=10*2
			if uttt_board[k+1][m+1]==flagop:
				score_calc-=90*2
				if uttt_board[k+2][m+2]==flagop:
					score_calc-=900*2
		elif uttt_board[k+1][m+1]==flagop:
			score_calc-=10*2
			if uttt_board[k+2][m+2]==flagop:
					score_calc-=90*2
		elif uttt_board[k+2][m+2]==flagop:
			score_calc-=10*2
		return score_calc
	def modify_score_d2(self,k,m,flag,uttt_board,score_calc):
		if(flag == 'x'):
			flagop='o'
		else:
			flagop='x'


		if uttt_board[k][m+2]==flag:
			score_calc+=10*2
			if uttt_board[k+1][m+1]==flag:
				score_calc+=90*2
				if uttt_board[k+2][m]==flag:
					score_calc+=900*2
		elif uttt_board[k+1][m+1]==flag:
			score_calc+=10*2
			if uttt_board[k+2][m]==flag:
					score_calc+=90*2
		elif uttt_board[k+2][m]==flag:
			score_calc+=10*2

		if uttt_board[k][m+2]==flagop:
			score_calc-=10*2
			if uttt_board[k+1][m+1]==flagop:
				score_calc-=90*2
				if uttt_board[k+2][m]==flagop:
					score_calc-=900*2
		elif uttt_board[k+1][m+1]==flagop:
			score_calc-=10*2
			if uttt_board[k+2][m]==flagop:
					score_calc-=90*2
		elif uttt_board[k+2][m]==flagop:
			score_calc-=10*2
		return score_calc
	def determine_blocks_allowed(self,old_move, block_stat):
		blocks_allowed = []
		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			blocks_allowed = [1,3]
		elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
			blocks_allowed = [1,5]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
			blocks_allowed = [3,7]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
			blocks_allowed = [5,7]
		elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
			blocks_allowed = [0,2]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
			blocks_allowed = [0,6]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
			blocks_allowed = [6,8]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
			blocks_allowed = [2,8]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
			blocks_allowed = [4]
		else:
			sys.exit(1)
		final_blocks_allowed = []
		for i in blocks_allowed:
			if block_stat[i] == '-':
				final_blocks_allowed.append(i)
		return final_blocks_allowed

	def get_empty_out_of(self,gameb, blal,block_stat):
		cells = []  # it will be list of tuples
		#Iterate over possible blocks and get empty cells
		for idb in blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))

		# If all the possible blocks are full, you can move anywhere
		if cells == []:
			new_blal = []
			all_blal = [0,1,2,3,4,5,6,7,8]
			for i in all_blal:
				if block_stat[i]=='-':
					new_blal.append(i)

			for idb in new_blal:
				id1 = idb/3
				id2 = idb%3
				for i in range(id1*3,id1*3+3):
					for j in range(id2*3,id2*3+3):
						if gameb[i][j] == '-':
							cells.append((i,j))
		return cells
	def terminal_state_reached(self,game_board, block_stat,point1,point2):
	### we are now concerned only with block_stat
		bs = block_stat
		## Row win
		if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='D') or (bs[3]!='-' and bs[3]!='D' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='D' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
			return True, 'W'
		## Col win
		elif (bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-' and bs[0]!='D') or (bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-' and bs[4]!='D') or (bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-' and bs[5]!='D'):
			return True, 'W'
		## Diag win
		elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='D') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='D'):
			return True, 'W'
		else:
			smfl = 0
			for i in range(9):
				if block_stat[i] == '-':
					smfl = 1
					break
			if smfl == 1:
				return False, 'Continue'
			
			else:
				if point1>point2:
					return True, 'P1'
				elif point2>point1:
					return True, 'P2'
				else:
					return True, 'D'	


"""=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (3, 6) with x
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (1, 5) with o
=========== Game Board ===========
- - -  - - -  - - -
- - -  - - o  - - -
- - -  - - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (0, 6) with x
=========== Game Board ===========
- - -  - - -  x - -
- - -  - - o  - - -
- - -  - - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (0, 4) with o
=========== Game Board ===========
- - -  - o -  x - -
- - -  - - o  - - -
- - -  - - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (0, 0) with x
=========== Game Board ===========
x - -  - o -  x - -
- - -  - - o  - - -
- - -  - - -  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (2, 5) with o
=========== Game Board ===========
x - -  - o -  x - -
- - -  - - o  - - -
- - -  - - o  - - -

- - -  - - -  x - -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (3, 7) with x
=========== Game Board ===========
x - -  - o -  x - -
- - -  - - o  - - -
- - -  - - o  - - -

- - -  - - -  x x -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (1, 0) with o
=========== Game Board ===========
x - -  - o -  x - -
o - -  - - o  - - -
- - -  - - o  - - -

- - -  - - -  x x -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (0, 1) with x
=========== Game Board ===========
x x -  - o -  x - -
o - -  - - o  - - -
- - -  - - o  - - -

- - -  - - -  x x -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (2, 1) with o
=========== Game Board ===========
x x -  - o -  x - -
o - -  - - o  - - -
- o -  - - o  - - -

- - -  - - -  x x -
- - -  - - -  - - -
- - -  - - -  - - -

- - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (6, 0) with x
=========== Game Board ===========
x x -  - o -  x - -
o - -  - - o  - - -
- o -  - - o  - - -

- - -  - - -  x x -
- - -  - - -  - - -
- - -  - - -  - - -

x - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 2 made the move: (4, 0) with o
=========== Game Board ===========
x x -  - o -  x - -
o - -  - - o  - - -
- o -  - - o  - - -

- - -  - - -  x x -
o - -  - - -  - - -
- - -  - - -  - - -

x - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

Player 1 made the move: (0, 2) with x
=========== Game Board ===========
x x x  - o -  x - -
o - -  - - o  - - -
- o -  - - o  - - -

- - -  - - -  x x -
o - -  - - -  - - -
- - -  - - -  - - -

x - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 2 made the move: (3, 8) with o
=========== Game Board ===========
x x x  - o -  x - -
o - -  - - o  - - -
- o -  - - o  - - -

- - -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  - - -

x - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 1 made the move: (0, 3) with x
=========== Game Board ===========
x x x  x o -  x - -
o - -  - - o  - - -
- o -  - - o  - - -

- - -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  - - -

x - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 2 made the move: (1, 3) with o
=========== Game Board ===========
x x x  x o -  x - -
o - -  o - o  - - -
- o -  - - o  - - -

- - -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  - - -

x - -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 1 made the move: (6, 1) with x
=========== Game Board ===========
x x x  x o -  x - -
o - -  o - o  - - -
- o -  - - o  - - -

- - -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  - - -

x x -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 2 made the move: (1, 8) with o
=========== Game Board ===========
x x x  x o -  x - -
o - -  o - o  - - o
- o -  - - o  - - -

- - -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  - - -

x x -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 1 made the move: (0, 7) with x
=========== Game Board ===========
x x x  x o -  x x -
o - -  o - o  - - o
- o -  - - o  - - -

- - -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  - - -

x x -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 2 made the move: (0, 8) with o
=========== Game Board ===========
x x x  x o -  x x o
o - -  o - o  - - o
- o -  - - o  - - -

- - -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  - - -

x x -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 1 made the move: (0, 5) with x
=========== Game Board ===========
x x x  x o x  x x o
o - -  o - o  - - o
- o -  - - o  - - -

- - -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  - - -

x x -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 2 made the move: (5, 7) with o
=========== Game Board ===========
x x x  x o x  x x o
o - -  o - o  - - o
- o -  - - o  - - -

- - -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  - o -

x x -  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
- - -
==================================

Player 1 made the move: (6, 2) with x
=========== Game Board ===========
x x x  x o x  x x o
o - -  o - o  - - o
- o -  - - o  - - -

- - -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  - o -

x x x  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
x - -
==================================

Player 2 made the move: (5, 6) with o
=========== Game Board ===========
x x x  x o x  x x o
o - -  o - o  - - o
- o -  - - o  - - -

- - -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  o o -

x x x  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
x - -
==================================

Player 1 made the move: (3, 0) with x
=========== Game Board ===========
x x x  x o x  x x o
o - -  o - o  - - o
- o -  - - o  - - -

x - -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  o o -

x x x  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
x - -
==================================

Player 2 made the move: (2, 3) with o
=========== Game Board ===========
x x x  x o x  x x o
o - -  o - o  - - o
- o -  o - o  - - -

x - -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  o o -

x x x  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
x - -
==================================

Player 1 made the move: (3, 1) with x
=========== Game Board ===========
x x x  x o x  x x o
o - -  o - o  - - o
- o -  o - o  - - -

x x -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  o o -

x x x  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
x - -
==================================

Player 2 made the move: (2, 6) with o
=========== Game Board ===========
x x x  x o x  x x o
o - -  o - o  - - o
- o -  o - o  o - -

x x -  - - -  x x o
o - -  - - -  - - -
- - -  - - -  o o -

x x x  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
- - -
x - -
==================================

Player 1 made the move: (3, 2) with x
=========== Game Board ===========
x x x  x o x  x x o
o - -  o - o  - - o
- o -  o - o  o - -

x x x  - - -  x x o
o - -  - - -  - - -
- - -  - - -  o o -

x x x  - - -  - - -
- - -  - - -  - - -
- - -  - - -  - - -
==================================
=========== Block Status =========
x - -
x - -
x - -
==================================

P1
COMPLETE

"""