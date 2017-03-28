import heapq

class Cell(object):
    def __init__(self, x, y, reachable):
        '''Initializes a new cell object.
        This allows connections with neighbors'''
        # self.closed = closed
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        # The g variable is the distance from the current cell to the next cell
        self.g = 0
        # the h variable is the distance from the current cell to the ending cell
        self.h = 0
        # f is the sum of h and g
        self.f = 0


class AStar(object):
    def __init__(self, height, width):
        # Remember to pass the height --> len(maze) and width --> len(maze[0])
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = height
        self.grid_width = width

    def init_grid(self, start, end, maze):
        walls = []
        for i in maze:
            for j in i:
                if j == 'x':
                    walls.append((i, j))
        # for k in walls:
        #     for l in k:
        #         print l
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(*start)
        self.end = self.get_cell(*end)

    def get_heuristic(self, cell):
        '''
        Compute the heuristic value H for a cell: distance between
        this cell and the ending cell multiply by 10.

        :param self:
        :param cell:
        :return: heuristic value H
        '''
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        '''
        Returns a cell from the cells list

        @param x cell x coordinate
        @param y cell coordinate
        @returns cell
        '''
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cell(self, cell):
        '''
        Returns the adjacent cells to a cell. Clockwise starting
        from the one on the right.
        :param self:
        :param cell: get adjacent cells from this cell.
        :return: adjacent cells list.
        '''

        cells = []
        if cell.x < self.grid_width - 1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height - 1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def display_path(self):
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            print('path: cell: %d, %d' % (cell.x, cell.y))

    def update_cell(self, adj, cell):
        '''
        Update Adjacent cell

        :param self:
        :param adj: adjacent cell to current cell
        :param cell: current cell being processed
        '''
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process_algorithm(self):
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        # while the opened heap is not empty
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice.
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                self.display_path()
                break
            adj_cells = self.get_adjacent_cell(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found for this adj
                        # cell.
                        if adj_cell.g > adj_cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))

def read_data(path):
    maze = []
    with open(path, 'r') as f:
        for row in f:
            element = [ele for ele in row.split()]
            maze.append(ele)
    return maze

def write_data(path):

def main():
    maze = read_data("Arena.txt")
    # for i in maze:
    #     for j in i:
    #         print(j)
    print('grid height: %d \n grid length: %d' % (len(maze), len(maze[0])))
    a_star = AStar(len(maze), len(maze[0]))
    a_star.init_grid((0, 0), (5, 5), maze)
    a_star.process_algorithm()

main()