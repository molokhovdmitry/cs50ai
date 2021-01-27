import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.safes.add(cell)
        self.mark_safe(cell)
        
        # Get nearby cells
        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Check if it's the cell itself
                if (i, j) != cell:
                    # Check if cell out of bounds
                    if 0 <= i < self.height and 0 <= j < self.width:
                        if (i, j) in self.mines:
                            count -= 1
                        elif (i, j) not in self.safes:
                            cells.add((i, j))

        # Add sentence
        if len(cells):
            newSentence = Sentence(cells, count)
            if newSentence not in self.knowledge:
                self.knowledge.append(Sentence(cells, count))

        # Update knowledge until no changes made
        newKnowledge = True
        while newKnowledge == True:
            newKnowledge = False
            # Loop through every sentence in knowledge
            for sentence in self.knowledge:
                # Check sentence for mines
                mines = sentence.known_mines()
                # Keep track of mines
                self.mines = self.mines.union(mines)
                if len(mines):
                    newKnowledge = True
                    # Mark every mine in every sentence
                    for mine in mines.copy():
                        self.mark_mine(mine)

                # Check sentence for safe cells
                safes = sentence.known_safes()
                # Keep track of safe cells
                self.safes = self.safes.union(safes)
                if len(safes):
                    newKnowledge = True
                    # Mark every safe cell in every sentence
                    for safe in safes.copy():
                        self.mark_safe(safe)

                """
                Add new inference to knowledge.

                Compare every sentence with every sentence.
                Any time we have two sentences `set1 = count1`
                and `set2 = count2` where `set1` is a subset
                of `set2`, construct the new sentence
                `set2 - set1 = count2 - count1`.
                """
                for anotherSentence in self.knowledge:
                    if sentence != anotherSentence:
                        set1 = sentence.cells
                        count1 = sentence.count
                        set2 = anotherSentence.cells
                        count2 = anotherSentence.count
                        if set1.issubset(set2):
                            newSentence = Sentence(set2.difference(set1), count2 - count1)
                            if newSentence not in self.knowledge:
                                newKnowledge = True
                                self.knowledge.append(newSentence)
                
        # Remove empty sentences
        while Sentence(set(), 0) in self.knowledge:
            self.knowledge.remove(Sentence(set(), 0))


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Substract made moves from safe moves
        moves = self.safes.difference(self.moves_made)
        if len(moves):
            # Choose move with min values for more realistic behavior
            return min(moves)


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Get all cells
        moves = set()
        for i in range(self.height):
            for j in range(self.width):
                moves.add((i, j))

        # Substract made moves and mines
        moves.difference_update(self.moves_made)
        moves.difference_update(self.mines)

        # Choose random move
        if len(moves):
            return random.choice(tuple(moves))
        