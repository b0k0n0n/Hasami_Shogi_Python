A_CONSTANT = 97                                 # constant for ASCII value of 'a'
NUMBER_OF_PIECES = 9                            # constant for number of pieces each side has to start


class HasamiShogiGame:
    """
    Class that creates instance of playable Hasami Shogi Game
    """

    def __init__(self):
        """
        Parameter: none
        Return: none
        Data members:
        _gameboard - blank to start but filled in init_game
        _turn - will be used to set initial turn and each subsequent turn
        _black_count - number of black pieces captured
        _red_count - number of red pieces captured
        """
        self._gameboard = []
        self._turn = ""
        self._black_count = 0
        self._red_count = 0

        self.init_game()                        # initializes gameboard

    def square_to_coordinates(self, square):
        """
        Takes parameter square and turns it into coordinates on the gameboard
        :param square: square on board
        :return: coordinates in numerical form
        """
        # ord is used for ASCII value of first char in square; column is cast to INT to use as coordinates
        row, column = ord(square[0]) - A_CONSTANT, int(square[1]) - 1
        return row, column

    def coordinates_to_square(self, row, column):
        """
        Converts coordinates back to a specific square
        :param row: int value of row to be converted
        :param column: int value of column to be converted
        :return: numeric coordinates into a specific square
        """
        # revert back to grid square; since a = index[0], any row + A_CONSTANT = appropriate row
        return chr(row + A_CONSTANT) + str(column + 1)

    def init_game(self):
        """
        Starts the game by setting number of pieces on each team to appropriate number (9),
        sets start turn to "BLACK", and fills gameboard
        """
        self._red_count = NUMBER_OF_PIECES
        self._black_count = NUMBER_OF_PIECES
        self._turn = "BLACK"
        for row in range(NUMBER_OF_PIECES):
            self._gameboard.append([])
            for col in range(NUMBER_OF_PIECES):
                piece = "R" if row == 0 else "B" if row == NUMBER_OF_PIECES - 1 else "*"
                self._gameboard[row].append(piece)

    def get_active_player(self):
        """
        Returns player whose turn it is
        :return: active player
        """
        return self._turn

    def get_enemy_player(self):
        """
        Returns non-active player; used to check for captures
        :return: non-active player
        """
        return "BLACK" if self._turn == "RED" else "RED"

    def toggle_players(self):
        """
        Switches turn after current player's turn ends
        """
        self._turn = "BLACK" if self._turn == "RED" else "RED"

    def get_square_occupant(self, square):
        """
        Gets occupant of square on board, if one exists
        :param square: square on gameboard
        :return: "RED", "BLACK", or "NONE"
        """
        row, column = self.square_to_coordinates(square)
        piece = self._gameboard[row][column]                # piece, if there is one, on square being checked
        return "RED" if piece == "R" else "BLACK" if piece == "B" else "NONE"

    def set_square_occupant(self, square, value):
        """
        Sets occupant of square; used after moves and captures
        :param square: square being changed
        :param value: what square should be set to
        """
        row, column = self.square_to_coordinates(square)
        self._gameboard[row][column] = value

    def get_game_state(self):
        """
        Returns whether either side won the game or the game is unfinished
        :return: "RED_WON", "BLACK_WON", or "UNFINISHED"
        """
        return "RED_WON" if self._black_count < 2 else "BLACK_WON" if self._red_count < 2 else "UNFINISHED"

    def get_num_captured_pieces(self, color):
        """
        Gets number of captured pieces of one color
        :param color: color to check number of captured pieces
        :return: number of pieces captured
        """
        if color == "BLACK":
            return NUMBER_OF_PIECES - self._black_count
        elif color == "RED":
            return NUMBER_OF_PIECES - self._red_count

    def check_captures(self, square):
        """
        Check for corner capture after move
        :param square: square moved to
        """
        corner_dict = {"a1": ["b1", "a2"], "a9": ["a8", "b9"], "i1": ["h1", "i2"], "i9": ["i8", "h9"]}
        capture_pieces = []             # hold pieces corner captured
        capture_counter = 0
        active, enemy = self.get_active_player(), self.get_enemy_player()
        # keys are corners, values are spaces to which if active player moves, corner capture should be checked
        for key, value in corner_dict.items():
            # if the space is in the value, that space is removed to know which space to check
            if square in value:
                corner_dict[key].remove(square)
                # if corner occupant is enemy and piece in remaining value is active player, corner is captured
                if self.get_square_occupant(key) == enemy and self.get_square_occupant(corner_dict[key][0]) == active:
                    capture_pieces.append(key)

        # sets square to coordinates to iterate through list of lists
        row, column = self.square_to_coordinates(square)

        # rows have been converted to ints; checks rows for captures, decrementing to and including 0
        if row > 1:
            # holds potentially captured pieces
            pieces = []
            next_row = row - 1
            next_piece = self.get_square_occupant(self.coordinates_to_square(next_row, column))

            # while adjacent piece is enemy, since those are only pieces that can be captured
            while next_piece == enemy:
                pieces.append(self.coordinates_to_square(next_row, column))
                next_row -= 1
                # stop after last row is checked
                if next_row < 0:
                    break
                # get next piece to check
                next_piece = self.get_square_occupant(self.coordinates_to_square(next_row, column))

            # if you reach the same color piece, pieces have been captured
            if next_piece == active:
                for item in pieces:
                    capture_pieces.append(item)

        # rows have been converted to ints; checks rows for captures, incrementing to and including 8
        if row < 7:
            # holds potentially captured pieces
            pieces = []
            next_row = row + 1
            next_piece = self.get_square_occupant(self.coordinates_to_square(next_row, column))

            # while adjacent piece is enemy, since those are only pieces that can be captured
            while next_piece == enemy:
                # add piece to captured pieces
                pieces.append(self.coordinates_to_square(next_row, column))
                next_row += 1
                # stop after last row is checked
                if next_row > 8:
                    break
                # get next piece to check
                next_piece = self.get_square_occupant(self.coordinates_to_square(next_row, column))

            # if you reach the same color piece, pieces have been captured
            if next_piece == active:
                for item in pieces:
                    capture_pieces.append(item)

        # checks columns for captures, decrementing to and including 0
        if column > 1:
            # holds potentially captured pieces
            pieces = []
            next_column = column - 1
            next_piece = self.get_square_occupant(self.coordinates_to_square(row, next_column))

            # while adjacent piece is enemy, since those are only pieces that can be captured
            while next_piece == enemy:
                # add piece to captured pieces
                pieces.append(self.coordinates_to_square(row, next_column))
                next_column -= 1
                # stop after last column is checked
                if next_column < 0:
                    break
                # get next piece to check
                next_piece = self.get_square_occupant(self.coordinates_to_square(row, next_column))

            # if you reach the same color piece, pieces have been captured
            if next_piece == active:
                for item in pieces:
                    capture_pieces.append(item)

        # checks columns for captures, incrementing to and including 8
        if column < 7:
            # holds potentially captured pieces
            pieces = []
            next_column = column + 1
            next_piece = self.get_square_occupant(self.coordinates_to_square(row, next_column))
            while next_piece == enemy:
                # add piece to captured pieces
                pieces.append(self.coordinates_to_square(row, next_column))
                next_column += 1
                # stop after last column is checked
                if next_column > 8:
                    break
                # get next piece to check
                next_piece = self.get_square_occupant(self.coordinates_to_square(row, next_column))

            # if you reach the same color piece, pieces have been captured
            if next_piece == active:
                for item in pieces:
                    capture_pieces.append(item)

        # sets value at squares captured to "*" to indicate square is empty
        for piece in capture_pieces:
            self.set_square_occupant(piece, "*")
            capture_counter += 1

        # decrements appropriate number of pieces for enemy player based on # of pieces captured
        if enemy == "BLACK":
            self._black_count -= capture_counter
        else:
            self._red_count -= capture_counter

    def make_move(self, move_from, move_to):
        """
        Allows active player to make move if valid
        :param move_from: square from which active player wants to move
        :param move_to: square to which active player wants to move
        :return: True or False depending on whether move is valid or not valid
        """
        if self.get_game_state() != "UNFINISHED":
            return False

        # you can't move to the spot you are already in
        if move_from == move_to:
            return False

        # gets color of player trying to move
        active = self.get_active_player()

        # gets occupant of origin square and destination square and ensures value are active player and NONE
        piece_from, piece_to = self.get_square_occupant(move_from), self.get_square_occupant(move_to)
        if piece_from != active or piece_to != "NONE":
            return False

        # sets each square to grid coordinates to check list of lists (gameboard)
        from_row, from_column = self.square_to_coordinates(move_from)
        to_row, to_column = self.square_to_coordinates(move_to)

        # ensures move is linear; must move either along same row or same column for move to be valid
        same_row = from_row == to_row
        same_col = from_column == to_column

        if not (same_row or same_col):
            return False

        # sets step for range check based on which way needs to be checked: left or right
        if same_row:
            step = 1 if from_column < to_column else -1
            for col in range(from_column + step, to_column, step):
                # if space is vacant, no capture
                if self._gameboard[from_row][col] != "*":
                    return False

        # sets step for range check based on which way needs to be checked: up or down
        if same_col:
            step = 1 if from_row < to_row else -1
            for row in range(from_row + step, to_row, step):
                # if space is vacant, no capture
                if self._gameboard[row][from_column] != "*":
                    return False

        # if move is valid, set move from square to "*", indicating square is vacant
        self.set_square_occupant(move_from, "*")
        # if move is valid, set move to square to color of active player
        self.set_square_occupant(move_to, active[0])

        # call check_captures to see if the square moved to results in any captures
        self.check_captures(move_to)

        # turn has ended, so change active player to other player
        self.toggle_players()

        return True