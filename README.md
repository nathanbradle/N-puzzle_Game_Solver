# N-Puzzle Solver

This Python program solves the N-Puzzle (also known as the sliding puzzle) using various search algorithms including Breadth-First Search (BFS), Depth-First Search (DFS), and A* Search.

## Features

- **Breadth-First Search (BFS)**: Implements BFS to find the shortest path to the goal state.
- **Depth-First Search (DFS)**: Implements DFS to explore the depth of the puzzle tree.
- **A* Search**: Utilizes the A* search algorithm with the Manhattan distance heuristic to efficiently find a solution.
- **Manhattan Distance**: Calculates the Manhattan distance to use as a heuristic for the A* search.
- **Performance Metrics**: Outputs the path to the goal, cost of the path, number of nodes expanded, search depth, maximum search depth, running time, and maximum RAM usage.

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. This program is compatible with Python 3.x. You can check your Python version by running:

```bash
python --version
```

## Usage
```bash
python3 puzzle_solver.py [search_mode] [board]
```
Replace [search_mode] with bfs, dfs, or ast depending on the search strategy you want to use. Replace [board] with a comma-separated list of integers representing the initial state of the board (e.g., 0,1,2,3,4,5,6,7,8 for the goal state of a 3x3 puzzle).

For example:
```bash
python3 puzzle_solver.py bfs 1,2,5,3,4,0,6,7,8
```

## Output
The program writes the results to an output.txt file.