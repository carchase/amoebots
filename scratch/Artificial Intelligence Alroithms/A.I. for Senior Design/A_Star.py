'''Author: Ben Smith
03/11/17
This is a test algorithm for A* search.
Hoping to turn this into an algorithm for multiple agents.'''
import heapq

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(maze, start, end):
    # The set of nods that have already been explored.
    unexplored = PriorityQueue()
    # The set of currently discovered nodes that are not explored yet.
    # Initially, the only node is the start node.
    unexplored.put(start, 0)

    explored = {}
    cost_so_far = {}
    explored[start] = None
    cost_so_far[start] = 0

    while not unexplored.empty():
        current = unexplored.get()

        if current == end:
            break

        for next in maze.neighbors(current):
            new_cost = cost_so_far[current] + maze.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                unexplored.put(next, priority)
                explored[next] = current

    return explored, cost_so_far


def read_file():
    with open("Arena.txt") as textFile:
        maze = [line.split() for line in textFile]
    return maze


class maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x, y) % 2 == 0: results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

class maze_with_weights(maze):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def reconstruct_path(came_from, start, end):
    current = end
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.append(start)
    path.reverse()
    return path


class SimpleGraph:
    def __init__(self):
        self.edges = {}

    def neighbors(self, id):
        return self.edges[id]


def main():
    example_graph = SimpleGraph()
    example_graph.edges = {
        'A': ['B'],
        'B': ['A', 'C', 'D'],
        'C': ['A'],
        'D': ['E', 'A'],
        'E': ['B']
    }
    # ma = read_file()
    # m = maze(len(ma), len(ma[0]))
    # came_from, cost_so_far = a_star_search(example_graph, (1, 3), (5, 6))
    came_from, cost_so_far = a_star_search(example_graph, (1, 4), (7, 8))
    draw_grid(diagram4, width=3, point_to=came_from, start=(1, 4), goal=(7, 8))
    print()
    draw_grid(diagram4, width=3, number=cost_so_far, start=(1, 4), goal=(7, 8))

main()
