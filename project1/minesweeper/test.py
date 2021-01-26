from minesweeper import Sentence

height, width, mines = 8, 8, 8

board = []
for i in range(height):
            row = []
            for j in range(width):
                row.append(False)
            board.append(row)

knowledge = []
knowledge.append(Sentence({(0, 1), (0, 0)}, 1))
knowledge.append(Sentence({(0, 1), (0, 2), (0, 0)}, 2))

for sentence in knowledge:
    print(sentence.__str__())
print()

for sentence in knowledge:
    for anotherSentence in knowledge:
        if sentence != anotherSentence:
            if sentence.cells.issubset(anotherSentence.cells):
                newSentence = Sentence(anotherSentence.cells.difference(sentence.cells), anotherSentence.count - sentence.count)
                if newSentence not in knowledge:
                    newKnowledge = True
                    knowledge.append(newSentence)

for sentence in knowledge:
    print(sentence.__str__())