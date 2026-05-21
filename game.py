import numpy as np
import heapq
from collections import deque
from timeit import default_timer as timer
import matplotlib.pyplot as plt

class Node:
    def __init__(self, board, parent= None,move= None,g=0,h=0,depth=0):
        self.board = board #elshakl el7aly
        self.parent = parent #shakl elboard ely ablo
        self.move = move
        self.g = g  
        self.h = h  
        self.f = g + h  
        self.depth=depth
    def __eq__(self,other):
        return np.array_equal(self.board, other.board)
    def __lt__(self, other):
        return self.f < other.f
    def __hash__(self):
        return hash(self.board.tobytes())

class Puzzle:
    def __init__(self, initial_state, goal_state):
        self.initial_state = np.array(initial_state)
        self.goal_state = np.array(goal_state)
        self.size = self.initial_state.shape[0]
        self.goal_positions = self.get_goal_positions()

    def get_goal_positions(self):
        positions = {}
        rows=self.goal_state.shape[0]      
        cloumns=self.goal_state.shape[1]   
        for r in range(rows):  
            for c in range(cloumns):  
                value = self.goal_state[r][c]  
                positions[value]=(r,c)  
        return positions
    

    def find_neighbors(self, node):
        neighbors = []
        zero_pos = None  #Initialize zero_pos
    # Searching for the position of the blank tile
        for r in range(self.goal_state.shape[0]):
            for c in range(self.goal_state.shape[1]):
                if node.board[r][c] == 0:
                    zero_pos = (r, c)
                    break
            if zero_pos is not None:  # Exit outer loop if blank is found
                break
        if zero_pos is None:#If zero_pos is not found, return an empty array neighbors
            return neighbors

        possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  #The moves that can be madee
        for row, column in possible_moves:
            new_pos = (zero_pos[0] + row, zero_pos[1] + column)
            #trying to check if this move is valid in the bounds of the board
            if 0 <= new_pos[0] < self.goal_state.shape[0] and 0 <= new_pos[1] < self.goal_state.shape[1]:
                modified_board = node.board.copy()
                modified_board[zero_pos[0], zero_pos[1]] = modified_board[new_pos[0], new_pos[1]]
                modified_board[new_pos[0], new_pos[1]] = 0  # Move the blank tile
                neighbor_node = Node(modified_board, node, depth=node.depth + 1)
                neighbors.append(neighbor_node)

        return neighbors



    def puzzle_solved(self, board):
        return np.array_equal(board, self.goal_state)
    

    def heuristic(self, board):
        dis_to_goal = 0
        for row in range(board.shape[0]):
            for column in range(board.shape[1]):
                if board[row, column] != 0:  
                    goalrow, goalcolumn = self.goal_positions[board[row, column]]
                    dis_to_goal += abs(row - goalrow) + abs(column - goalcolumn)
        return dis_to_goal
    
    def heuristic_ecl(self, board):
        dis_to_goal = 0
        for row in range(board.shape[0]):
            for column in range(board.shape[1]):
                if board[row, column] != 0:
                    goal_row, goal_column = self.goal_positions[board[row, column]]
                    dis_to_goal += np.sqrt((row - goal_row) ** 2 + (column - goal_column) ** 2)
        return dis_to_goal

class gamesolving:
    def __init__(self,puzzle) :
        self.Puzzle=puzzle
        self.max_depth = 0

    def find_path(self, node):
        path = []
        while node:
            # print("depth is: ",node.depth)
            path.append(node.board)
            node = node.parent
        reversed_path = path.copy()  
        reversed_path.reverse()  
        return reversed_path 

    def get_search_depth(self, node):
        depth = 0
        while node:
            depth += 1
            node = node.parent
        return depth-1

    def solve_bfs(self):
        print("BFS loading...:")
        initial_node = Node(self.Puzzle.initial_state)

        if self.Puzzle.puzzle_solved(initial_node.board):
            path = self.find_path(initial_node)
            return path, len(path) - 1, 0,0
    
        frontier = deque([initial_node])#Initializing the queue
        explored = set()
        frontier_set = {initial_node}  

        while frontier:#while the Queue is not empty
            current_node = frontier.popleft()  
            frontier_set.remove(current_node)  
            self.max_depth = max(self.max_depth, current_node.depth)
            if self.Puzzle.puzzle_solved(current_node.board):
                path = self.find_path(current_node)
                return path, len(path) - 1, len(explored),self.max_depth  

            for neighbor in self.Puzzle.find_neighbors(current_node):
             if neighbor not in explored and neighbor not in frontier_set:
                    frontier.append(neighbor)  
                    frontier_set.add(neighbor)  
                    explored.add(neighbor)  

        return None, 0,0,self.max_depth #Cant find an answer to the given state


        
    def solve_dfs(self):
        print("DFS loading...:")
        initial_node = Node(self.Puzzle.initial_state)
        if self.Puzzle.puzzle_solved(initial_node.board):
             path = self.find_path(initial_node)
             return self.find_path(initial_node),len(path) - 1,0,0
        
        frontier = [initial_node] #Initializing the stack
        explored = set()
        explored.add(initial_node) 

        while frontier:#while the stack is not empty
            current_node = frontier.pop()
            explored.add(current_node)
            self.max_depth = max(self.max_depth, current_node.depth)
            if self.Puzzle.puzzle_solved(current_node.board):
                path = self.find_path(current_node)
                return self.find_path(current_node),len(path) - 1,len(explored),self.max_depth
            
            for neighbor in self.Puzzle.find_neighbors(current_node):
                if neighbor not in explored:
                    frontier.append(neighbor)                 
        return None,0,0,self.max_depth  #Cant find an answer to the given state
    


 
    def solve_idfs(self): 
        print("IDFS loading...")
        initial_node = Node(self.Puzzle.initial_state)
        if self.Puzzle.puzzle_solved(initial_node.board):
            path = self.find_path(initial_node)
            return path, len(path) - 1, 0, 0
    
        depth = 0
        total_visited = 0

        while True:
            frontier = [initial_node]
            explored = set() 
            self.max_depth = depth  

            while frontier:
                current_node = frontier.pop()
                if current_node in explored:
                    continue
                explored.add(current_node) 
                total_visited += 1

                if self.Puzzle.puzzle_solved(current_node.board):
                    path = self.find_path(current_node)
                    return path, len(path) - 1, total_visited, self.max_depth
                if current_node.depth < depth:
                    for neighbor in self.Puzzle.find_neighbors(current_node):
                        if neighbor not in explored and neighbor not in frontier:
                            frontier.append(neighbor)
            depth += 1

    def astar(self):
        print("Astar loading...")
        initial_node = Node(self.Puzzle.initial_state, h=self.Puzzle.heuristic(self.Puzzle.initial_state))
        priority_queue = []
        heapq.heappush(priority_queue, initial_node)
        visited_set = set()
        max=0
        while priority_queue:
            current_node = heapq.heappop(priority_queue)
            # self.max_depth = max(self.max_depth, current_node.depth)
            depth=self.get_search_depth(current_node)
            if depth>max:
                max=depth
            if self.Puzzle.puzzle_solved(current_node.board):
                path = self.find_path(current_node)
                return self.find_path(current_node),len(path) - 1,len(priority_queue),max
            visited_set.add(current_node)

            for neighbor in self.Puzzle.find_neighbors(current_node):
                if neighbor in visited_set:
                    continue
                neighbor.g=current_node.g+1
                neighbor.h = self.Puzzle.heuristic(neighbor.board)
                neighbor.f = neighbor.g + neighbor.h
                if neighbor not in priority_queue:
                    heapq.heappush(priority_queue, neighbor)
                else:
                    for node in priority_queue:
                        if neighbor == node and neighbor.g < node.g:
                            node.g = neighbor.g
                            node.f = neighbor.f
                            node.parent = current_node
                            break
        return None, 0,0,self.max_depth
    def astarecl(self):
            print("Astar eucleadian loading...")
            initial_node = Node(self.Puzzle.initial_state, h=self.Puzzle.heuristic(self.Puzzle.initial_state))
            priority_queue = []
            heapq.heappush(priority_queue, initial_node)
            visited_set = set()
            max=0
            while priority_queue:
                current_node = heapq.heappop(priority_queue)
                # self.max_depth = max(self.max_depth, current_node.depth)
                depth=self.get_search_depth(current_node)
                if depth>max:
                    max=depth
                if self.Puzzle.puzzle_solved(current_node.board):
                    path = self.find_path(current_node)
                    return self.find_path(current_node),len(path) - 1,len(priority_queue),max
                visited_set.add(current_node)

                for neighbor in self.Puzzle.find_neighbors(current_node):
                    if neighbor in visited_set:
                        continue
                    neighbor.g=current_node.g+1
                    neighbor.h = self.Puzzle.heuristic_ecl(neighbor.board)
                    neighbor.f = neighbor.g + neighbor.h
                    if neighbor not in priority_queue:
                        heapq.heappush(priority_queue, neighbor)
                    else:
                        for node in priority_queue:
                            if neighbor == node and neighbor.g < node.g:
                                node.g = neighbor.g
                                node.f = neighbor.f
                                node.parent = current_node
                                break
            return None, 0,0,self.max_depth #Cant find an answer to the given state

initial_state = [
    # [1, 2, 3],
    # [0, 4, 5],
    # [6, 7, 8]]
    #     [1, 2, 3],
    #     [4, 0, 5],
    #     [7, 8, 6]
    #  ]
        #   [1, 2, 5],
        #   [3, 4, 0],
        #   [6, 7, 8]
        #         ]
        # [1,2,3],
        # [4 ,8,0],
        # [7 ,8 ,4]]
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
goal_state = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]



timing=[]
cost_of_path=[]
explored_nodes=[]
depth=[]
puzzle = Puzzle(initial_state, goal_state)
solver = gamesolving(puzzle)
start=timer()
bfs_path,bfs_count_path,bfs_explored_count,bfs_max_depth = solver.solve_bfs()
end=timer()
executing_time=end-start
timing.append(executing_time)
cost_of_path.append(bfs_count_path)
explored_nodes.append(bfs_explored_count)
depth.append(bfs_max_depth)



# # for step in bfs_path:
# #     print(step)
print("Number of explored nodes in BFS:", bfs_explored_count)
print("Total cost(no of moves) BFS",bfs_count_path)
print("Max depth reached by bfs is",bfs_max_depth)
print("The executing time of BFS is",executing_time)
print("\n")



start=timer()
dfs_path,dfs_count_path,dfs_explored_count,dfs_max_depth = solver.solve_dfs()
end=timer()
executing_time=end-start
timing.append(executing_time)
cost_of_path.append(dfs_count_path)
explored_nodes.append(dfs_explored_count)
depth.append(dfs_max_depth)

# # if dfs_path:
# #     for step in dfs_path:
# #         print(step)
# # else:
# #     print("No solution found.")
print("Number of explored nodes in DFS:", dfs_explored_count)
print("Total cost(no of moves) for DFS",dfs_count_path)
print("Max depth reached by dfs is",dfs_max_depth)
print("The executing time of DFS is",executing_time)
print("\n")

start=timer()
idfs_path, idfs_count_path, idfs_explored_count,idfs_max_depth= solver.solve_idfs()
end=timer()
executing_time=end-start
timing.append(executing_time)
cost_of_path.append(idfs_count_path)
explored_nodes.append(idfs_explored_count)
depth.append(idfs_max_depth)
# # if idfs_path:
# #     for step in idfs_path: 
# #         print(step)
# #     else:
# #         print("No solution found.")
    
print("Number of explored nodes in IDFS:", idfs_explored_count) #139526# number of moves
print("Total cost(no of moves):", idfs_count_path)
print("Max depth reached by idfs is",idfs_max_depth)
print("The executing time of IDFS is",executing_time)
print("\n")


start=timer()
astar_path,astar_count_path,astar_explored_count,astar_max_depth= solver.astar()
end=timer()
executing_time=end-start
timing.append(executing_time)
cost_of_path.append(astar_count_path)
explored_nodes.append(astar_explored_count)
depth.append(astar_max_depth)
# # if astar_path:
# #     for step in astar_path:
# #         print(step)
# # else:
# #     print("No solution found.")

print("Number of explored nodes of A*:", astar_explored_count)
print("Total cost(no of moves) for A*:", astar_count_path)
print("Max depth reached by A* is",astar_max_depth)
print("The executing time of A* is",executing_time)
print("\n")


start=timer()
astar_ecl_path, astar_ecl_count_path, astar_ecl_explored_count,astar_ecl_max_depth= solver.astarecl()
end=timer()
executing_time=end-start
timing.append(executing_time)
cost_of_path.append(astar_ecl_count_path)
explored_nodes.append(astar_ecl_explored_count)
depth.append(astar_ecl_max_depth)
# # if astar_ecl_path:
# #         print("Steps to solve the puzzle using A* Recursive with Custom Heuristic:")
# #         for step in astar_ecl_path:
# #             print(step)
# # else:    
# #     print("No solution found for A* Recursive with Custom Heuristic.")
    
print("Number of explored nodes of Astar eucleadian:", astar_ecl_explored_count)
print("Total cost(no of moves) for Astar eucleadian:", astar_ecl_count_path)
print("Max depth reached by Astar eucleadian is",astar_ecl_max_depth)
print("The executing time of Astar eucleadian is",executing_time)
print("\n")

#Runtime graph
plt.figure(figsize=(8, 6))
Algorith_names=["BFS","DFS","IDFS","A*","Astar eucleadian*"]
plt.bar(Algorith_names, timing, color='cyan')
plt.title("Timing Barchart")
plt.xlabel("Algorith Names")
plt.ylabel("time in sec")
plt.ylim(0.000, 0.005)
plt.show()

#Total cost graph
plt.figure(figsize=(8, 6))
plt.bar(Algorith_names, cost_of_path, color='Red')
plt.title("Total cost(tot no of moves)")
plt.xlabel("Algorith Names")
plt.ylabel("Cost")
plt.ylim(0,100)
plt.show()

#Explored nodes graph
plt.figure(figsize=(8, 6))
plt.bar(Algorith_names, explored_nodes, color='blue')
plt.title("Exploring nodes")
plt.xlabel("Algorith Names")
plt.ylabel("No of explored nodes")
plt.ylim(0,500)
plt.show()


#Depth graph
plt.figure(figsize=(8, 6))
plt.bar(Algorith_names, depth, color='orange')
plt.title("Depth of Algorithm")
plt.xlabel("Algorith Names")
plt.ylabel("Depth")
plt.ylim(0,10)
plt.show()