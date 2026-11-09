'''
AIL Mock Assignment
Name: Shreeya Sandeep Tapaswi
Roll No. 31474

Problem Statement: Problem Statement: Implement the Map Colouring Problem for Indian States/any country/region mapping using CSP.
'''

# Input the states
n = int(input("Enter the number of states: "))
states = []
for i in range(n):
    state = input(f"Enter state {i + 1}: ").strip()
    states.append(state)

# Input the neighbouring states
graph = {}
for state in states:
    neighbours = input(f"Enter neighbours of {state} (comma-separated): ")
    graph[state] = [neighbour.strip() for neighbour in neighbours.split(",") if neighbour.strip()]

# Input available colours
colours = input("Enter available colours (comma-separated): ").split(",")
colours = [colour.strip() for colour in colours if colour.strip()]

assigned = {}

# Check whether a colour can be assigned safely
def is_safe(state, colour):
    for neighbour in graph[state]:
        if assigned.get(neighbour) == colour:
            return False
    return True

# Backtracking algorithm
def backtrack():
    if len(assigned) == len(states):
        return True

    state = next(s for s in states if s not in assigned)

    for colour in colours:
        if is_safe(state, colour):
            assigned[state] = colour
            if backtrack():
                return True
            del assigned[state]
    return False

# Display the result
if backtrack():
    print()
    print("Map Colouring Solution:")
   
    for state in states:
        print(f"    {state}: {assigned[state]}")
    print()
else:
    print()
    print("No solution exists with the given colours.")
    print()