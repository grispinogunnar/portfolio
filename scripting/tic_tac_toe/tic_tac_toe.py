class Game():
    def __init__(self):
        self.board = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        self.indices = {'1': (0, 0), '2': (0, 1), '3': (0, 2), '4': (1, 0), '5': (1, 1), '6': (1, 2), '7': (2, 0), '8': (2, 1), '9': (2, 2)}
        self.moves = 0  
        self.max_moves = 9
        return


    def get_index(self, num):
        return self.indices.get(str(num))


    def print_board(self):
        print()
        for row in self.board:
            print("-------------")
            print(f"| {row[0]} | {row[1]} | {row[2]} |")
        print("-------------")


    def get_val(self, position):
        if position is not None:
            row, col = self.get_index(position)
            return self.board[row][col]
        else:
            return None


    def change_element(self, position, new_element):
        row, col = self.get_index(position)
        self.board[row][col] = new_element
        return

    
    def check_win(self, char):
        for val in range(3):
            #Row
            if(self.board[val][0] == char):
                if(self.board[val][1] == char):
                    if(self.board[val][2] == char):
                        return True
            #Col
            if(self.board[0][val] == char):
                if(self.board[1][val] == char):
                    if(self.board[2][val] == char):
                        return True
        #Diagonals
        if(self.board[0][0] == char):
            if(self.board[1][1] == char):
                if(self.board[2][2] == char):
                    return True
        if(self.board[0][2] == char):
            if(self.board[1][1] == char):
                if(self.board[2][0] == char):
                    return True
        return False


if __name__ == "__main__":
    ttt_board = Game()
    while(True):
        ttt_board.print_board()
        if(ttt_board.moves == ttt_board.max_moves):
            print("Draw!")
            exit()
        while(True):
            user_input = input("User 'X', enter a position: ")
            pos_index = ttt_board.get_index(user_input)
            if(pos_index is not None):
                if(ttt_board.get_val(user_input) != user_input):
                    print("Invalid position. Try again!")
                else:
                    ttt_board.change_element(user_input, 'X')
                    ttt_board.moves += 1
                    if(ttt_board.check_win('X') == True):
                        ttt_board.print_board()
                        print("User 'X' Wins!")
                        exit()
                break
            else:
                print("Invalid position. Try again!")
        ttt_board.print_board()
        if(ttt_board.moves == ttt_board.max_moves):
            print("Draw!")
            exit()
        while(True):
            user_input = input("User 'O', enter a position: ")
            pos_index = ttt_board.get_index(user_input)
            if(pos_index is not None):
                if(ttt_board.get_val(user_input) != user_input):
                    print("Invalid position. Try again!")
                else:
                    ttt_board.change_element(user_input, 'O')
                    ttt_board.moves += 1
                    if(ttt_board.check_win('O') == True):
                        ttt_board.print_board()
                        print("User 'O' Wins!")
                        exit()
                break
            else:
                print("Invalid position. Try again!")



