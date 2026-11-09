"""
================================================================================
ASSIGNMENT No. 3 - Map Colouring
================================================================================
Name:     SHREEYA S TAPASWI
Roll No:  31474
Batch:    N4
--------------------------------------------------------------------------------
Problem Statement: Implement Map colouring problem for Indian states/region 
mapping using Constraint Satisfaction Problem (CSP).
================================================================================
"""

from flask import Flask, render_template_string, request, jsonify

# ============================================================
# 1. CSP BACKTRACKING ALGORITHM LOGIC
# ============================================================

class MapColoringCSP:
    """
    Class to solve the Map Coloring Problem using CSP principles.
    Variables = States
    Domain = Colors
    Constraints = No two adjacent states share the same color.
    """
    def __init__(self, variables, neighbors, colors):
        # The list of states (nodes in the graph)
        self.variables = variables  
        # Adjacency list representing borders (constraints)
        self.neighbors = neighbors  
        # The available color palette (domain)
        self.colors = colors        
        # Dictionary to store final result {State: Color}
        self.assignment = {}        

    def is_safe(self, state, color):
        """
        Check if assigning 'color' to 'state' is valid.
        Iterates through neighbors to ensure none already have this color.
        """
        for neighbor in self.neighbors.get(state, []):
            if neighbor in self.assignment and self.assignment[neighbor] == color:
                return False
        return True

    def backtrack(self):
        """
        Recursive backtracking function to find a valid assignment.
        Returns True if a solution is found, else False.
        """
        # Base Case: If all variables have an assigned color, solution is complete
        if len(self.assignment) == len(self.variables):
            return True

        # Selection: Pick the first state that hasn't been colored yet
        unassigned = [v for v in self.variables if v not in self.assignment]
        state = unassigned[0]

        # Domain Selection: Try every color in the available palette
        for color in self.colors:
            if self.is_safe(state, color):
                # Apply the assignment
                self.assignment[state] = color
                
                # Recursively call backtrack for the next state
                if self.backtrack():
                    return True
                
                # If result is False, remove assignment (Backtrack) and try next color
                del self.assignment[state]
        
        return False

# ============================================================
# 2. FLASK WEB SERVER SETUP & UI TEMPLATE
# ============================================================

app = Flask(__name__)

# Modern Interactive UI using Vis.js for Graphing and Tailwind CSS for Styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Map Colouring CSP</title>
    <!-- Tailwind CSS for modern responsive layout -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Vis.js for interactive draggable map nodes -->
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        /* Height of the graph visualization area */
        #network-container { height: 450px; background: white; border-radius: 1rem; }
    </style>
</head>
<body class="bg-gray-100 min-h-screen font-sans">

    <div class="container mx-auto px-4 py-4 max-w-6xl">
        <!-- HEADER SECTION -->
        <header class="text-center mb-6">
            <h1 class="text-4xl font-black text-indigo-900 mb-2">Map Colouring</h1>
            
            <!-- COMPACT SINGLE LINE STUDENT DETAILS BAR -->
            <div class="bg-white shadow-sm rounded-full px-6 py-2 border border-indigo-200 inline-flex items-center gap-4 text-sm md:text-base">
                <span class="font-bold text-gray-700">Name: <span class="text-indigo-600">Shreeya S Tapaswi</span></span>
                <span class="text-gray-300">|</span>
                <span class="font-bold text-gray-700">Roll No: <span class="text-indigo-600">31474</span></span>
                <span class="text-gray-300">|</span>
                <span class="font-bold text-gray-700">Batch: <span class="text-indigo-600">N4</span></span>
            </div>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <!-- LEFT PANEL: MAP CONTROLS -->
            <div class="lg:col-span-1 bg-white p-5 rounded-2xl shadow-md border border-gray-200">
                <h2 class="font-bold text-lg mb-4 text-gray-800 border-b pb-2">Editor</h2>
                
                <div class="space-y-4">
                    <!-- Section to add new regions/states -->
                    <div>
                        <label class="text-[10px] font-bold text-gray-400 uppercase">1. Add State</label>
                        <input id="node-name" type="text" placeholder="State name" class="w-full mt-1 border p-2 rounded-lg text-sm focus:ring-1 focus:ring-indigo-500 outline-none">
                        <button onclick="addNode()" class="w-full mt-1 bg-indigo-600 text-white text-sm font-bold py-2 rounded-lg hover:bg-indigo-700 transition">Add State</button>
                    </div>

                    <!-- Section to define borders between states -->
                    <div>
                        <label class="text-[10px] font-bold text-gray-400 uppercase">2. Add Border</label>
                        <div class="flex gap-1 mt-1">
                            <input id="edge-u" type="text" placeholder="From" class="w-1/2 border p-2 rounded-lg text-sm">
                            <input id="edge-v" type="text" placeholder="To" class="w-1/2 border p-2 rounded-lg text-sm">
                        </div>
                        <button onclick="addEdge()" class="w-full mt-1 bg-emerald-500 text-white text-sm font-bold py-2 rounded-lg hover:bg-emerald-600 transition">Connect Border</button>
                    </div>

                    <!-- Solve Trigger -->
                    <div class="pt-4">
                        <button onclick="solveCSP()" class="w-full bg-orange-500 text-white py-3 rounded-xl font-black text-lg shadow-md hover:bg-orange-600 transition">
                            SOLVE CSP
                        </button>
                        <button onclick="location.reload()" class="w-full mt-2 text-gray-400 text-xs hover:text-red-500">Reset Map</button>
                    </div>
                </div>
            </div>

            <!-- RIGHT PANEL: GRAPH VISUALIZATION -->
            <div class="lg:col-span-3">
                <div id="network-container" class="shadow-inner border border-gray-200"></div>
                <p class="text-xs text-center text-gray-400 mt-2 italic">Drag nodes to reorganize the map view.</p>
            </div>
        </div>
    </div>

    <script>
        // Vis.js Graph Data Initialization
        let nodes = new vis.DataSet([]);
        let edges = new vis.DataSet([]);
        let container = document.getElementById('network-container');
        
        // Configuration for the Graph Physics and Visuals
        let network = new vis.Network(container, { nodes, edges }, {
            nodes: { shape: 'dot', size: 25, font: { size: 14, face: 'Arial', weight: 'bold' }, borderWidth: 3 },
            edges: { width: 2, color: '#CBD5E1', smooth: true },
            physics: { enabled: true, barnesHut: { gravitationalConstant: -1500 } }
        });

        // Function to add a state node to the canvas
        function addNode() {
            const name = document.getElementById('node-name').value.trim();
            if(name && !nodes.get(name)) {
                nodes.add({id: name, label: name, color: {background: '#F8FAFC', border: '#E2E8F0'}});
                document.getElementById('node-name').value = '';
            }
        }

        // Function to add a border (edge) between two existing states
        function addEdge() {
            const u = document.getElementById('edge-u').value.trim();
            const v = document.getElementById('edge-v').value.trim();
            if(u && v && nodes.get(u) && nodes.get(v)) {
                edges.add({from: u, to: v});
                document.getElementById('edge-u').value = '';
                document.getElementById('edge-v').value = '';
            } else {
                alert("Ensure both states exist!");
            }
        }

        // AJAX function to call Python backend to solve the CSP
        async function solveCSP() {
            const nodeList = nodes.getIds();
            const edgeList = edges.get().map(e => [e.from, e.to]);
            if (nodeList.length === 0) return;

            const response = await fetch('/solve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nodes: nodeList, edges: edgeList })
            });

            const result = await response.json();
            if(result.success) {
                // Update graph colors based on the CSP assignment returned from Python
                for (let state in result.assignment) {
                    nodes.update({id: state, color: {background: result.assignment[state], border: '#FFF'}});
                }
            } else {
                alert(result.message);
            }
        }
    </script>
</body>
</html>
"""

# ============================================================
# 3. BACKEND API ROUTES
# ============================================================

@app.route('/')
def index():
    """Route to serve the UI."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/solve', methods=['POST'])
def solve():
    """
    API endpoint that receives graph data, converts it 
    to a neighbor list, and runs the backtracking CSP.
    """
    data = request.json
    nodes = data.get('nodes', [])
    edges_list = data.get('edges', [])
    
    # Constructing adjacency list (neighbors dictionary)
    neighbors = {node: [] for node in nodes}
    for u, v in edges_list:
        if u in neighbors: neighbors[u].append(v)
        if v in neighbors: neighbors[v].append(u)

    # The available color domain (hex codes)
    colors = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#1A535C", "#A29BFE"] 
    
    # Initialize and solve the CSP
    csp = MapColoringCSP(nodes, neighbors, colors)
    if csp.backtrack():
        return jsonify({"success": True, "assignment": csp.assignment})
    else:
        return jsonify({"success": False, "message": "No valid solution found with these colors!"})

# Main execution block
if __name__ == '__main__':
    print("Map Colouring server starting at http://127.0.0.1:5000")
    app.run(debug=True)