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
                    print(letters[i][j] or " ", end = "")
                else:
                    print("█", end = "")
            print()
    
    def save(self, assignment, filename):

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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)


    def solve(self):

        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        
        for var in self.crossword.variables:
            for word in self.domains[var].copy():
                if len(word) != var.length:
                    self.domains[var].remove(word) 

    def revise(self, x, y):
    
        revised = False
        
        for i in self.domains[x].copy():
            
            overlap = self.crossword.overlaps[x,y]
            if overlap:
                a,b = overlap
                exists = False
                for j in self.domains[y].copy():
                    
                    if i[a] == j[b]:
                        exists = True
                if not exists:
                    self.domains[x].remove(i)
                    revised = True

        return revised
                        
    def ac3(self, arcs=None):
        
        q = []
        if arcs:

            q = arcs
            
            while q:
                
                x,y = q.pop(0)
                
                if self.revise(x,y):

                    if len(self.domains[x]) == 0:
                        return False
                    for z in self.crossword.neighbors(x) - {y}:
                        q.append((z,x))
        else:
            
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    q.append((x,y))
            return self.ac3(q)
            
    def assignment_complete(self, assignment):
        
        for var in self.crossword.variables:
            if var not in assignment:
                return False
        return True

    def consistent(self, assignment):
        
        if len(set(assignment.values())) < len(assignment):
            print("Duplicate words found in the assignment.")
            return False
        for var in assignment:
            if len(assignment[var]) != var.length:
                print("Length of word does not match the variable's length requirement.")
                return False

            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    continue

                overlap = self.crossword.overlaps[var, neighbor]
                if overlap:
                    i, j = overlap
                    if assignment[var][i] != assignment[neighbor][j]:
                        return False
        return True


    def order_domain_values(self, var, assignment):

        countOut = dict()
        
        for word in self.domains[var]:
            
            countOut[word] = 0
            
            for neighbor in self.crossword.neighbors(var):
                
                if neighbor in assignment: continue
                
                overlap = self.crossword.overlaps[var, neighbor] 
                    
                if overlap:
                    i,j = overlap
                    
                    for neighborWord in self.domains[neighbor]:

                        if word[i] != neighborWord[j]:
                            countOut[word] += 1
                        
        return sorted(countOut, key = lambda x:countOut[x])
                
    def select_unassigned_variable(self, assignment):

        minVariable = None
        
        for var in self.crossword.variables:
            
            if var in assignment: continue
            if minVariable == None:
                minVariable = var
            
            elif len(self.domains[var]) < len(self.domains[minVariable]):
                minVariable = var
            elif len(self.domains[var]) == len(self.domains[minVariable]):
                if len(self.crossword.neighbors(var)) > len(self.crossword.neighbors(minVariable)):
                    minVariable = var
                            
        return minVariable                    
            
    def backtrack(self, assignment):

        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        
        for value in self.order_domain_values(var, assignment):
            
            assignmentCopy = assignment.copy() 
            assignmentCopy[var] = value

            if self.consistent(assignmentCopy):
                
                assignment[var] = value                
                result = self.backtrack(assignment)
                if result:
                    return result
                assignment.pop(var)
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

