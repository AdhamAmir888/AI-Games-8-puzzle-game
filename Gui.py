import numpy as np
import tkinter as tk

from timeit import default_timer as timer
import game

class PuzzleGUI:
    def __init__(self, master, solver):
        self.master = master
        self.master.title("8 Puzzle Solver")
        self.solver = solver

        # Variables to store solution data
        self.solution_path = []
        self.current_step = 0

        # Set up GUI layout
        self.setup_gui()

    def setup_gui(self):
        # Create frame for puzzle grid
        self.puzzle_frame = tk.Frame(self.master)
        self.puzzle_frame.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # Create buttons for controlling the puzzle
        tk.Button(self.master, text="Solve with BFS", command=self.solve_bfs).grid(row=1, column=0)
        tk.Button(self.master, text="Solve with DFS", command=self.solve_dfs).grid(row=1, column=1)
        tk.Button(self.master, text="Solve with IDFS", command=self.solve_idfs).grid(row=1, column=2)
        tk.Button(self.master, text="Solve with A*", command=self.solve_astar).grid(row=1, column=3)
        tk.Button(self.master, text="Solve with A* Euclidean", command=self.solve_astar_euclidean).grid(row=1, column=4)

        # Step-through controls
        tk.Button(self.master, text="Next Step", command=self.next_step).grid(row=2, column=0, columnspan=4)

        # Puzzle tiles as labels
        self.tiles = [[tk.Label(self.puzzle_frame, text='', font=("Helvetica", 24), width=4, height=2, borderwidth=2, relief="groove")
                      for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.tiles[i][j].grid(row=i, column=j)

        # Solution info labels
        self.path_label = tk.Label(self.master, text="Path length: 0")
        self.path_label.grid(row=3, column=0, columnspan=2)
        self.nodes_label = tk.Label(self.master, text="Solution steps: 0")
        self.nodes_label.grid(row=3, column=2, columnspan=2)
        self.time_label = tk.Label(self.master, text="Execution Time: 0.0s")
        self.time_label.grid(row=4, column=0, columnspan=4)
        self.search_label = tk.Label(self.master, text="Search depth: 0")
        self.search_label.grid(row=3, column=3, columnspan=4)

        # Display initial state
        self.update_puzzle(self.solver.Puzzle.initial_state)

    def update_puzzle(self, board):
        for i in range(3):
            for j in range(3):
                value = board[i, j]
                if value != 0:
                
                    self.tiles[i][j].config(text=str(value))
                else:
                  self.tiles[i][j].config(text=str(''))
                  

    def display_solution(self, path, path_length, nodes_explored,search_depth ,exec_time):
        self.solution_path = path
        self.current_step = 0
        self.update_puzzle(self.solution_path[self.current_step])
        self.path_label.config(text=f"Path length: {path_length}")
        self.nodes_label.config(text=f"Solution steps: {nodes_explored}")
        self.time_label.config(text=f"Execution Time: {exec_time:.4f}s")
        self.search_label.config(text=f"Search depth: {search_depth}")

    def next_step(self):
        if self.solution_path and self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.update_puzzle(self.solution_path[self.current_step])

    def solve_bfs(self):
        start = timer()
        path, nodes_explored, path_length,bfs_max_depth= self.solver.solve_bfs()
        end = timer()
        self.display_solution(path, path_length, nodes_explored,bfs_max_depth,end - start)
        print("BFS Execution Time:", end - start)

    def solve_dfs(self):
        start = timer()
        path, nodes_explored, path_length,dfs_max_depth= self.solver.solve_dfs()
        end = timer()
        self.display_solution(path, path_length, nodes_explored,dfs_max_depth,end - start)
        print("DFS Execution Time:", end - start)

    def solve_idfs(self):
        start = timer()
        path, nodes_explored, path_length,idfs_max_depth= self.solver.solve_idfs()
        end = timer()
        self.display_solution(path, path_length, nodes_explored,idfs_max_depth,end - start)
        print("IDFS Execution Time:", end - start)

    def solve_astar(self):
        start = timer()
        path, nodes_explored, path_length,astar_max_depth= self.solver.astar()
        end = timer()
        self.display_solution(path, path_length, nodes_explored,astar_max_depth,end - start)
        print("A* Execution Time:", end - start)

    def solve_astar_euclidean(self):
        start = timer()
        path, nodes_explored, path_length,Astar_eucleadian= self.solver.astarecl()
        end = timer()
        self.display_solution(path, path_length, nodes_explored,Astar_eucleadian,end - start)
        print("A* Euclidean Execution Time:", end - start)

# Define initial and goal states
initial_state = [
    # [1, 2, 5],
    # [3, 4, 0],
    # [6, 7, 8]]
       # [1, 2, 3],
    # [0, 4, 5],
    # [6, 7, 8]]

    #     [1, 2, 3],
    #     [4, 0, 5],
    #     [7, 8, 6]
    # ]
        #   [1, 2, 3],
        #   [4, 0, 5],
        #   [7, 8, 6]
        #         ]
        # [1,2,3],
        # [5 ,6,0],
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

# Initialize Puzzle and solver
puzzle = game.Puzzle(initial_state, goal_state)
solver = game.gamesolving(puzzle)

# Create GUI
gui = tk.Tk()
Mygame = PuzzleGUI(gui, solver)
gui.mainloop()
