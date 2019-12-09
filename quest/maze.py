from collections import defaultdict
import random

def is_even(x):
    return x % 2 == 0

class Maze:
    """
    Implements a [flood-fill/depth-first search](http://algostructure.com/specials/maze.php)
    maze generation algorithm
    """
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows

    def generate(self, seed=None):
        if seed:
            random.seed(seed)
        self.links = defaultdict(list)
        visited = set()
        stack = [(1, 1)]
        current_point = (1, 1)
        while len(stack) > 0:
            visited.add(current_point)
            unvisited_neighbors = [n for n in self.neighbors(current_point) if n not in visited]
            if len(unvisited_neighbors) > 0:
                next_point = random.choice(unvisited_neighbors)
                self.connect(current_point, next_point)
                stack.append(current_point)
                current_point = next_point
            else:
                current_point = stack.pop()

    def connect(self, p0, p1):
        self.links[p0].append(p1)
        self.links[p1].append(p0)
                
    def connected(self, p0, p1):
        return p1 in self.links[p0]

    def neighbors(self, point):
        x, y = point
        possible_neighbors = [(x+2, y), (x-2, y), (x, y+2), (x, y-2)]
        return [n for n in possible_neighbors if self.is_in_bounds(n)]

    def is_in_bounds(self, point):
        x, y = point
        return x >= 0 and x < self.columns - 1 and y >= 0 and y < self.rows - 1

    def get_walls(self):
        walls = []
        for i in range(self.columns):
            for j in range(self.rows):
                if i == 0 or i == self.columns - 1 or j == 0 or j == self.rows - 1:
                    walls.append((i, j))
                elif is_even(i) and is_even(j):
                    walls.append((i, j))
                elif is_even(i) and (i+1, j) not in self.links[(i-1, j)]:
                    walls.append((i, j))
                elif is_even(j) and (i, j+1) not in self.links[(i, j-1)]:
                    walls.append((i, j))
        return walls

    def __str__(self):
        walls = set(self.get_walls())
        rows = []
        for j in reversed(range(self.rows)):
            row = ["X" if (i,j) in walls else " " for i in range(self.columns)]
            rows.append("".join(row))
        return "\n".join(rows)

if __name__ == '__main__':
    m = Maze(99, 99)
    m.generate()
    print(m)
