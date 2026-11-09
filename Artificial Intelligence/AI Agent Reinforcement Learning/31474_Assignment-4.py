"""
================================================================================
ASSIGNMENT No. 4 - Reinforcement Learning
================================================================================
Name:     SHREEYA S TAPASWI
Roll No:  31474
Batch:    N4
--------------------------------------------------------------------------------
Problem Statement: 
Develop an AI agent that learns to play a simple game (Maze Navigation) using 
Reinforcement Learning. The agent must learn to find the shortest path from the 
start (0,0) to the goal (5,5) in a 6x6 grid, navigating through obstacles (walls) 
and avoiding penalty zones (traps). The agent should utilize the Q-Learning 
algorithm to update its knowledge based on rewards and penalties received during 
interaction with the environment.
================================================================================
"""

import tkinter as tk
import random

# --- REINFORCEMENT LEARNING HYPERPARAMETERS ---
ALPHA = 0.1    # Learning Rate: How much the AI weighs new information over old.
GAMMA = 0.9    # Discount Factor: How much the AI values future rewards vs immediate ones.
EPSILON = 0.1  # Exploration Rate: 10% chance to take a random step to discover new paths.

GRID_SIZE = 6 
CELL_SIZE = 75

class QLearningBrain:
    """
    The 'Brain' of the AI. It stores the Q-Table, which is a mapping of
    (state, action) pairs to their expected utility (Q-Value).
    """
    def __init__(self, actions):
        self.actions = actions
        self.q_table = {} # Dictionary key: (row, col), value: [Q_up, Q_down, Q_left, Q_right]

    def get_q(self, state):
        """Initializes state in Q-Table with zeros if it hasn't been visited yet."""
        if state not in self.q_table:
            self.q_table[state] = [0.0] * len(self.actions)
        return self.q_table[state]

    def choose_action(self, state):
        """Action Selection using Epsilon-Greedy strategy."""
        if random.random() < EPSILON:
            # Exploration: Choose a random action
            return random.randint(0, len(self.actions) - 1)
        else:
            # Exploitation: Choose the action with the highest Q-value
            values = self.get_q(state)
            return values.index(max(values))

    def learn(self, state, action, reward, next_state):
        """
        Updates the Q-Table using the Bellman Equation:
        Q(s,a) = Q(s,a) + alpha * [Reward + gamma * max(Q(s',a')) - Q(s,a)]
        """
        current_q = self.get_q(state)[action]
        max_future_q = max(self.get_q(next_state))
        
        # Calculate new Q-value
        new_q = current_q + ALPHA * (reward + GAMMA * max_future_q - current_q)
        self.q_table[state][action] = new_q

class MazeApp:
    """Handles the UI and the simulation loop."""
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive AI Lab - Reinforcement Learning")
        
        # --- UI THEME COLORS ---
        self.bg_color = "#000B1A"      # Persian Bluish Black
        self.header_bg = "#001F3F"     # Slightly lighter blue for header
        self.highlight = "#00d2ff"     # Neon Cyan
        self.btn_color = "#003366"     # Deep blue for buttons
        
        self.root.configure(bg=self.bg_color)

        # UI Header section
        header_text = "Name: Shreeya S Tapaswi    Roll no. 31474    Batch: N4"
        tk.Label(root, text=header_text, font=("Consolas", 11, "bold"), 
                 bg=self.header_bg, fg="white", pady=12).pack(fill="x")

        # Define Game Environment coordinates
        self.agent_pos = [0, 0] # Starting point
        self.goal = [5, 5]      # Target point
        self.walls = [[1,1], [1,2], [3,3], [3,4]] # Impassable barriers
        self.traps = [[2,1], [4,3], [2,4], [4,1]] # High penalty zones
        
        self.is_running = False  # Simulation control state
        self.episode = 1
        self.score = 0
        self.ai = QLearningBrain(actions=['up', 'down', 'left', 'right'])
        
        self.setup_ui()
        self.draw_maze()

    def setup_ui(self):
        """Initializes buttons, sliders, and labels."""
        # Episode/Score Display
        self.info_label = tk.Label(self.root, text="Status: Ready | Episode: 1", 
                                  fg=self.highlight, bg=self.bg_color, font=("Verdana", 12))
        self.info_label.pack(pady=10)

        # Drawing Canvas
        self.canvas = tk.Canvas(self.root, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE, 
                                bg=self.bg_color, highlightthickness=1, highlightbackground=self.highlight)
        self.canvas.pack(padx=20)

        # Speed Slider
        self.speed_scale = tk.Scale(self.root, from_=1000, to=10, orient="horizontal", 
                                    label="Adjust Learning Speed (ms delay)", length=320,
                                    bg=self.bg_color, fg=self.highlight, 
                                    highlightthickness=0, troughcolor=self.header_bg)
        self.speed_scale.set(200) 
        self.speed_scale.pack(pady=5)

        # Legend/Guide
        legend_frame = tk.Frame(self.root, bg=self.bg_color)
        legend_frame.pack(pady=5)
        legend_text = "Blue: AI  |  Green: Goal  |  Black: Wall  |  Orange: Trap"
        tk.Label(legend_frame, text=legend_text, font=("Verdana", 9), 
                 fg="#8ECAE6", bg=self.bg_color).pack()

        # Interaction Buttons
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=15)

        self.start_btn = tk.Button(btn_frame, text="▶ Start AI", width=12, bg=self.btn_color, 
                                   fg="white", command=self.start_ai)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.pause_btn = tk.Button(btn_frame, text="⏸ Pause", width=12, bg=self.btn_color, 
                                   fg="white", command=self.pause_ai)
        self.pause_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = tk.Button(btn_frame, text="🔄 Reset Brain", width=12, bg="#5c0000", 
                                   fg="white", command=self.reset_brain)
        self.reset_btn.grid(row=0, column=2, padx=5)

    def start_ai(self):
        """Starts or resumes the simulation loop."""
        if not self.is_running:
            self.is_running = True
            self.run_loop()

    def pause_ai(self):
        """Stops the simulation loop."""
        self.is_running = False

    def reset_brain(self):
        """Wipes the AI's Q-Table to show learning from scratch."""
        self.is_running = False
        self.ai.q_table = {}  # Memory Wipe
        self.agent_pos = [0, 0]
        self.episode = 1
        self.score = 0
        self.draw_maze()
        self.info_label.config(text="Memory Wiped | Episode: 1")

    def draw_maze(self):
        """Renders the grid based on current environment state."""
        self.canvas.delete("all")
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = "#001529" # Empty path color
                
                # Assign colors based on tile type
                if [r, c] == self.goal: color = "#2ecc71" # Green Goal
                elif [r, c] in self.walls: color = "black" # Wall
                elif [r, c] in self.traps: color = "#e67e22" # Orange Trap
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, 
                                           outline="#003366", width=1)

        # Draw AI Agent (Blue Circle)
        ar, ac = self.agent_pos
        ax, ay = ac * CELL_SIZE, ar * CELL_SIZE
        self.canvas.create_oval(ax+15, ay+15, ax+CELL_SIZE-15, ay+CELL_SIZE-15, 
                               fill="#00BFFF", outline="white", width=2)

    def run_loop(self):
        """The core RL cycle: Observe -> Act -> Reward -> Learn."""
        if not self.is_running:
            return

        state = tuple(self.agent_pos)
        action_idx = self.ai.choose_action(state)
        
        # Determine target position based on action
        new_pos = list(self.agent_pos)
        if action_idx == 0: new_pos[0] -= 1 # Up
        elif action_idx == 1: new_pos[0] += 1 # Down
        elif action_idx == 2: new_pos[1] -= 1 # Left
        elif action_idx == 3: new_pos[1] += 1 # Right

        reward = -1 # Living penalty (to encourage finding the exit quickly)
        done = False

        # Collision with Walls or Grid Edges
        if (new_pos[0] < 0 or new_pos[0] >= GRID_SIZE or 
            new_pos[1] < 0 or new_pos[1] >= GRID_SIZE or 
            new_pos in self.walls):
            reward = -10
            new_pos = self.agent_pos # Don't move
        # Reached Goal
        elif new_pos == self.goal:
            reward = 100
            done = True
        # Stepped in Trap
        elif new_pos in self.traps:
            reward = -20 
        
        # Update the AI's Q-Table
        self.ai.learn(state, action_idx, reward, tuple(new_pos))
        
        # Update system state
        self.agent_pos = new_pos
        self.score += reward
        self.draw_maze()
        self.info_label.config(text=f"Status: Running... | Episode: {self.episode}")

        if done:
            # Small delay at goal for visibility then reset for next episode
            self.root.after(800, self.reset_episode)
        else:
            # Repeat loop after specified delay
            self.root.after(self.speed_scale.get(), self.run_loop)

    def reset_episode(self):
        """Resets agent to start but keeps the Q-Table learned knowledge."""
        self.agent_pos = [0, 0]
        self.episode += 1
        self.score = 0
        if self.is_running:
            self.run_loop()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x780") # Fixed UI size
    app = MazeApp(root)
    root.mainloop()