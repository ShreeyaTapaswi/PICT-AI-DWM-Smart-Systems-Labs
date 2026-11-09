"""
================================================================================
ASSIGNMENT No. 1 - N-PUZZLE SOLVER (A*)
================================================================================
Name:     SHREEYA S TAPASWI
Roll No:  31474
Batch:    N4
--------------------------------------------------------------------------------
Algorithm: A* Search (Optimal for N-Puzzle)
Heuristic: Manhattan Distance
================================================================================
"""
import heapq
import time
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ==============================================================================
# CORE A* SEARCH ALGORITHM LOGIC
# ==============================================================================

class PuzzleNode:
    """
    PuzzleNode represents a single state of the N*N board in the search space.
    It encapsulates the board configuration, path tracking, and cost calculations.
    """
    def __init__(self, board, parent=None, move="", depth=0, n=3):
        # The board is stored as a flat 1D list for memory efficiency
        self.board = board
        # Reference to the node from which this state was reached
        self.parent = parent
        # The direction ('UP', 'DOWN', etc.) taken to reach this state
        self.move = move
        # g(n): The path cost — the number of moves taken from the start
        self.depth = depth
        # Dimension of the puzzle (n x n)
        self.n = n
        
        # f(n) = g(n) + h(n)
        # Total estimated cost. A* explores the lowest f(n) first.
        self.cost = self.depth + self._calculate_manhattan()

    def _calculate_manhattan(self):
        """
        HEURISTIC h(n): Manhattan Distance.
        Sum of vertical/horizontal distances of each tile from its target position.
        This is an admissible heuristic, ensuring an optimal solution.
        """
        distance = 0
        for i, tile in enumerate(self.board):
            # Skip the blank space (0)
            if tile != 0:
                # Find current 2D row and column
                curr_r, curr_c = divmod(i, self.n)
                # Find target 2D row and column (Goal: 1, 2, 3... 0)
                dest_r, dest_c = divmod(tile - 1, self.n)
                # Add Absolute Distance
                distance += abs(curr_r - dest_r) + abs(curr_c - dest_c)
        return distance

    def __lt__(self, other):
        """Used by heapq to sort nodes by f(n) cost."""
        return self.cost < other.cost

def is_solvable(board, n):
    """
    Determines if the puzzle configuration is mathematically solvable 
    using the inversion count parity logic.
    """
    flat_no_zero = [t for t in board if t != 0]
    inversions = 0
    for i in range(len(flat_no_zero)):
        for j in range(i + 1, len(flat_no_zero)):
            if flat_no_zero[i] > flat_no_zero[j]:
                inversions += 1
    
    if n % 2 != 0:
        # Odd grid (3x3): Solvable if inversions are even
        return inversions % 2 == 0
    else:
        # Even grid (4x4): Parity depends on blank row position
        blank_row_from_bottom = n - (board.index(0) // n)
        return (inversions + blank_row_from_bottom) % 2 != 0

def get_neighbors(node):
    """
    Expansion: Finds the blank space and returns all valid adjacent states.
    """
    neighbors = []
    n = node.n
    blank_idx = node.board.index(0)
    r, c = divmod(blank_idx, n)

    # Coordinates for possible moves
    moves = {'UP': (r - 1, c), 'DOWN': (r + 1, c), 'LEFT': (r, c - 1), 'RIGHT': (r, c + 1)}

    for move_name, (nr, nc) in moves.items():
        # Boundary check
        if 0 <= nr < n and 0 <= nc < n:
            new_idx = nr * n + nc
            new_board = list(node.board)
            # Swap values
            new_board[blank_idx], new_board[new_idx] = new_board[new_idx], new_board[blank_idx]
            # Create neighbor node
            neighbors.append(PuzzleNode(new_board, node, move_name, node.depth + 1, n))
    return neighbors

def solve_a_star(start_board, n):
    """
    Executes A* search using a Priority Queue (Open List) and 
    a visited set (Closed List).
    """
    goal_board = list(range(1, n * n)) + [0]
    start_node = PuzzleNode(start_board, n=n)
    
    # Min-Heap Priority Queue
    open_list = [start_node]
    # Set for visited configurations (tuples are hashable)
    closed_set = set()

    while open_list:
        # Pop node with minimum f(n)
        current_node = heapq.heappop(open_list)

        # Success check
        if current_node.board == goal_board:
            return current_node

        closed_set.add(tuple(current_node.board))

        for neighbor in get_neighbors(current_node):
            if tuple(neighbor.board) not in closed_set:
                heapq.heappush(open_list, neighbor)
    return None

def serialize_path(node, n):
    """
    Backtracks from goal node to start node to return a list of board states.
    """
    path = []
    curr = node
    while curr:
        grid_2d = [list(curr.board[i : i + n]) for i in range(0, n * n, n)]
        path.append({"board": grid_2d, "move": curr.move if curr.move else "START"})
        curr = curr.parent
    path.reverse()
    return path

# ==============================================================================
# FLASK SERVER & Interactive UI
# ==============================================================================

@app.route("/")
def index():
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>N-Puzzle Solver | Rounded Tiles</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            :root { 
                --primary: #1e293b; --accent: #3b82f6; --bg: #f1f5f9; 
                --tile-bg: #f59e0b; --tile-border: #d97706; --board-border: #475569;
                --sq-radius: 12px; /* Radius for EACH square */
            }
            body { font-family: 'Inter', sans-serif; background: var(--bg); padding: 40px 20px; color: var(--primary); margin:0; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
            header { border-bottom: 2px solid #e2e8f0; padding-bottom: 20px; margin-bottom: 30px; }
            .metadata { display: flex; justify-content: space-between; background: #f8fafc; padding: 15px 25px; border-radius: 12px; font-size: 0.9em; }
            
            /* GRID INPUT STYLING */
            .grid-container { 
                display: grid; 
                gap: 6px; /* Small gap to show the rounded corners of each square */
                width: fit-content; margin-bottom: 30px; padding: 10px;
                background: #e2e8f0; border-radius: 16px;
            }
            .grid-item { 
                width: 60px; height: 60px; text-align: center; font-size: 1.2em; font-weight: 700; 
                border: none; border-radius: var(--sq-radius); /* ROUNDED SQUARE */
                background: white; outline: none; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }

            button { 
                padding: 12px 24px; background: var(--accent); color: white; border: none; 
                border-radius: 10px; cursor: pointer; font-weight: 600; 
            }
            
            .solve-area { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 40px; margin-top: 30px; }

            /* RESULT BOARD STYLING */
            .puzzle-board { 
                display: grid; 
                gap: 6px; /* Space between rounded squares */
                background: var(--board-border); 
                padding: 10px; border-radius: 20px;
                width: fit-content; margin: 0 auto;
            }
            .tile { 
                width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; 
                background: var(--tile-bg); color: white; font-size: 1.5em; font-weight: 700; 
                border-radius: var(--sq-radius); /* ROUNDED SQUARE */
                box-shadow: inset 0 -4px 0 rgba(0,0,0,0.1);
            }
            .tile.blank { background: #cbd5e1; box-shadow: none; }

            .log { max-height: 350px; overflow-y: auto; border: 1px solid #e2e8f0; border-radius: 12px; }
            .log-item { padding: 12px 20px; border-bottom: 1px solid #f1f5f9; cursor: pointer; }
            .log-item.active { background: #eff6ff; border-left: 5px solid var(--accent); color: var(--accent); font-weight: bold; }
            .controls { display: flex; gap: 10px; justify-content: center; margin-top: 25px; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>N-Puzzle Solver (A*)</h1>
                <div class="metadata">
                    <div>Name: <b>SHREEYA S TAPASWI</b></div>
                    <div>Roll No: <b>31474</b></div>
                    <div>Batch: <b>N4</b></div>
                </div>
            </header>

            <div style="display:flex; gap:20px; align-items:center; margin-bottom:20px;">
                <select id="gridSize" onchange="initGrid()" style="padding:10px; border-radius:8px;">
                    <option value="3">3 x 3</option>
                    <option value="4">4 x 4</option>
                </select>
                <button onclick="solve()">SOLVE NOW</button>
            </div>

            <div id="gridInput" class="grid-container"></div>

            <div id="solveArea" class="solve-area" style="display:none;">
                <div style="text-align: center;">
                    <h2 id="stepHeader" style="color:var(--accent)">Step 0</h2>
                    <div id="renderBoard" class="puzzle-board"></div>
                    <div class="controls">
                        <button onclick="prev()" style="background:#64748b">BACK</button>
                        <button onclick="next()">NEXT</button>
                    </div>
                </div>
                <div>
                    <h3 style="color:#64748b">STEP LOG</h3>
                    <div id="moveLog" class="log"></div>
                </div>
            </div>
        </div>

        <script>
            let path = [];
            let currentIdx = 0;

            function initGrid() {
                const n = parseInt(document.getElementById('gridSize').value);
                const container = document.getElementById('gridInput');
                container.style.gridTemplateColumns = `repeat(${n}, 1fr)`;
                container.innerHTML = '';
                const default3x3 = [1, 2, 3, 4, 0, 5, 6, 7, 8];
                for(let i=0; i<n*n; i++) {
                    const input = document.createElement('input');
                    input.type = 'number';
                    input.className = 'grid-item';
                    input.value = n === 3 ? default3x3[i] : (i === n*n-1 ? 0 : i+1);
                    container.appendChild(input);
                }
                document.getElementById('solveArea').style.display = 'none';
            }

            async function solve() {
                const n = parseInt(document.getElementById('gridSize').value);
                const board = Array.from(document.querySelectorAll('.grid-item')).map(i => parseInt(i.value) || 0);
                const response = await fetch('/solve', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ board, n })
                });
                const data = await response.json();
                if (data.status === 'success') {
                    path = data.path;
                    currentIdx = 0;
                    document.getElementById('solveArea').style.display = 'grid';
                    render();
                    buildLog();
                } else { alert(data.message); }
            }

            function render() {
                const step = path[currentIdx];
                const boardDiv = document.getElementById('renderBoard');
                const n = step.board.length;
                boardDiv.style.gridTemplateColumns = `repeat(${n}, 1fr)`;
                boardDiv.innerHTML = '';
                step.board.flat().forEach(val => {
                    const tile = document.createElement('div');
                    tile.className = 'tile' + (val === 0 ? ' blank' : '');
                    tile.innerText = val === 0 ? '' : val;
                    boardDiv.appendChild(tile);
                });
                document.getElementById('stepHeader').innerText = `Step ${currentIdx}: ${step.move}`;
                document.querySelectorAll('.log-item').forEach((item, i) => {
                    item.classList.toggle('active', i === currentIdx);
                });
            }

            function buildLog() {
                const logDiv = document.getElementById('moveLog');
                logDiv.innerHTML = path.map((s, i) => 
                    `<div class="log-item" onclick="goTo(${i})"><b>Step ${i}</b>: ${s.move}</div>`
                ).join('');
            }

            function goTo(i) { currentIdx = i; render(); }
            function next() { if(currentIdx < path.length - 1) goTo(currentIdx + 1); }
            function prev() { if(currentIdx > 0) goTo(currentIdx - 1); }

            initGrid();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()
    board, n = data.get("board"), int(data.get("n", 3))

    if not is_solvable(board, n):
        return jsonify({"status": "error", "message": "Unsolvable configuration."})

    result_node = solve_a_star(board, n)
    if result_node:
        return jsonify({"status": "success", "path": serialize_path(result_node, n)})
    
    return jsonify({"status": "error", "message": "No solution found."})

if __name__ == "__main__":
    app.run(debug=True)