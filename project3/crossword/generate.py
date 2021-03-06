import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Iterate over variables
        for variable in self.domains:
            # Iterate over words in variable's domain
            for word in self.domains[variable].copy():
                # Remove word if wrong length
                if len(word) != variable.length:
                    self.domains[variable].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        # Get positions of overlapping letters for `x` and `y`
        l = self.crossword.overlaps[(x, y)]
        if l:
            # Iterate over every word in `x`
            for wordX in self.domains[x].copy():
                """
                Remove word from `x` if no words from `y` contain letter
                `wordX[l[0]]` in position `l[1]` of `wordY`.
                """
                match = False
                for wordY in self.domains[y]:
                    if wordX[l[0]] == wordY[l[1]]:
                        match = True
                        break
                if match != True:
                    self.domains[x].remove(wordX)
                    revised = True
        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Make queue if `arcs` specified
        if arcs:
            queue = arcs
        # Make queue if `arcs=None`
        else:
            queue = set()
            for x in self.domains:
                for y in self.crossword.neighbors(x):
                    if x != y:
                        queue.add((x, y))

        # Go through queue
        while queue:
            # Dequeue
            (x, y) = queue.pop()
            # Revise and check if revision was made
            if self.revise(x, y):
                # Return `False` if empty domain
                if len(self.domains[x]) == 0:
                    return False
                # Enqueue neighbors to queue
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.add((z, x))
        return True
            

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return (
            True if len(assignment) == len(self.domains) else
            False
        )

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Ensure all values are distinct
        values = list(assignment.values())
        for value in values:
            if values.count(value) > 1:
                return False

        # Go through assigned variables
        for variable in assignment:
            # Go through neighbors
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    # Get positions of overlapping letters
                    l = self.crossword.overlaps[(variable, neighbor)]
                    # Return `False` if letters are different
                    if assignment[variable][l[0]] != assignment[neighbor][l[1]]:
                        return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        """
        Initialize a dict that will contain amount of constrainted
        values for every var's value
        """
        countConstraints = {}

        # Loop through values
        for value in self.domains[var]:
            countConstraints[value] = 0
            # Loop through var's neighbors
            for neighbor in self.crossword.neighbors(var):
                # Get overlap positions
                l = self.crossword.overlaps[(var, neighbor)]
                # Dont count already assigned variables
                if neighbor not in assignment:
                    # Loop through neighbor's values
                    for neighborValue in self.domains[neighbor]:
                        # Count constraint
                        if value[l[0]] != neighborValue[l[1]]:
                            countConstraints[value] += 1
        # Return sorted list
        return sorted(countConstraints, key=countConstraints.get)


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Count amount of values for every variable
        countValues = {}
        for variable in self.domains:
            if variable not in assignment:
                countValues[variable] = len(self.domains[variable])

        # Get variable(s) with min amount of values
        minValue = countValues[min(countValues, key=countValues.get)]
        variables = set()
        for variable in countValues:
            if countValues[variable] == minValue:
                variables.add(variable)

        # If more than 1 variables with min value
        if len(variables) > 1:
            # Get degrees of variables
            countOverlaps = {}
            for variable in variables:
                countOverlaps[variable] = len(self.crossword.neighbors(variable))
            # Return variable with max degrees
            return max(countOverlaps, key=countOverlaps.get)

        # If only 1 variable with min value
        return variables.pop()


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment
        
        # Try a new variable
        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            assignment[variable] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
