import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):

        self.crossword = crossword
        self.domains = {
            var : self.crossword.words.copy()
            for var in self.crossword.variables
        }
    
    def letter_grid(self, assignment):

        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]

        for variable, word in assignment.items():

            direction = variable.direction
            for k in range(len(word)):

                i = variable.i + (k if direction == variable.DOWN else 0)
                j = variable.j + (k if direction == variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):

        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):

            for j in range(self.crossword.width):

                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end = " ")
                else:
                    print("█", end = "")
            print()
    
    def save(self, assignment, filename):

        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        #create a blank canvas
        img = Image.new(
            "RGBA",
            (self.corssword.width * cell_size,
             self.crossword.height * cell_size),
             "black"
        )

        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf",80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):

            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                     ((i + 1) * cell_size - cell_border,
                      (i + 1) * cell_size - cell_border)
                ]

                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill = "white")
                    if letters[i][j]:
                        _,_,w,h = draw.textbbox((0,0),letters[i][j], font = font)
                        draw.text (
                            (rect[0][0] + (interior_size - w) / 2,
                            rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill = "black", font = font
                        )
        img.save(filename)

    def solve(self):

        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        
        for var in self.crossword.variables:
            
            for word in self.domains[var]:
                if len(word) != var.length:
                    self.domains[var].remove(word)
                    

    def revise(self, x, y):

        revised = False
        
        for i in self.domains[x]:
            
            newDomain = self.domains[y].copy().remove(i)
            
            overlap = self.crossword.overlaps[x,y]
            if overlap:
                for j in self.domains[y]:

                    wordI = x.cells.index(overlap)
                    wordJ = y.cells.index(overlap)
                    if i[wordI] != j[wordJ]:
                        newDomain.remove(j)
                    
            if len(newDomain) == 0:
                self.domains[x].remove(x)
                revised = True
                
        return revised
    
    def ac3(self, arcs=None):
        
        q = []
        if arcs:
            
            q = arcs.copy()
            
            while q:
                x,y = q.pop(0)
                if self.revise(x,y):
                    if len(self.domains[x]) == 0:
                        return False
                    else:
                        for z in self.crossword.neighbors(x) - {y}:
                            q.append((z,x))
        else:
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    q.append((x,y))
                    
            while q:
                x,y = q.pop(0)
                if self.revise(x,y):
                    if len(self.domains[x]) == 0:
                        return False
                    else:
                        for z in self.crossword.neighbors(x) - {y}:
                            q.append((z,x))
        return True
            

    def assignment_complete(self, assignment):
        
        for var in self.crossword.variables:
            if var not in assignment:
                return False
            if assignment[var] not in self.domains[var]:
                return False
        
        return True


    def consistent(self, assignment):

        for var, words in assignment:
            if var.length != len(words):
                return False
            for neighbor in self.crossword.neighbors(var):
                
                overlap = tuple(self.crossword.overlaps[var, neighbor])
                
                if overlap:    
                    wordI = var.cells.index(overlap)
                    wordJ = neighbor.cells.index(overlap)   
                    
                    for word in words:
                        if word[wordI] != neighbor[wordJ]:
                            return False
        return True 
        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = crossword(structure, words)
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

