import heapq
import numpy as np 
import random

class Node:
    def __init__(self, state, p=None, g=0, h=0):
        self.state = state
        self.p = p
        self.g = g
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

def AstarLowlevel(start, goal, get_neighbors, heuristic):
    open_list = [Node(start, None, 0, heuristic(start, goal))]
    closed = set()
    best_g = {start: 0}

    while open_list:
        curr = heapq.heappop(open_list)

        if curr.state == goal:
            path = []
            while curr:
                path.append(curr.state)
                curr = curr.p
            return path[::-1]

        if curr.state in closed:
            continue
        closed.add(curr.state)

        for nxt, cost in get_neighbors(curr.state):
            g_score = curr.g + cost

            if nxt in best_g and g_score >= best_g[nxt]:
                continue

            best_g[nxt] = g_score
            heapq.heappush(open_list, Node(nxt, curr, g_score, heuristic(nxt, goal)))

    return None

def print_grid(arr):
    n = len(arr)
    for i in range(n):
        print("|", end="")
        for j in range(n):
            if arr[i][j] == 0:
                print("  |", end="")
            else:
                print(f"{arr[i][j]:2d}|", end="")
        print()

def get_unique_grid(n):
    numbers = random.sample(range(n * n), n * n)
    grid = tuple(tuple(numbers[i*n:(i+1)*n]) for i in range(n))
    return grid

def get_inversions(arr, k):
    flat_arr = [x for row in arr for x in row if x != 0]
    
    def merge_sort_and_count(arr_1d):
        if len(arr_1d) <= 1:
            return arr_1d, 0
        
        mid = len(arr_1d) // 2
        left, left_count = merge_sort_and_count(arr_1d[:mid])
        right, right_count = merge_sort_and_count(arr_1d[mid:])
        
        merged, merge_count = merge_and_count(left, right)
        
        return merged, left_count + right_count + merge_count

    def merge_and_count(left, right):
        merged = []
        i = j = count = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                count += (len(left) - i)
                j += 1
                
        merged.extend(left[i:])
        merged.extend(right[j:])
        
        return merged, count

    _, total_inversions = merge_sort_and_count(flat_arr)
    return total_inversions

def get_neighbors(state):
    n = len(state)
    neighbors = []
    zero_pos = [(i, j) for i in range(n) for j in range(n) if state[i][j] == 0][0]
    x, y = zero_pos

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < n and 0 <= new_y < n:
            temp = [list(row) for row in state]
            temp[x][y], temp[new_x][new_y] = temp[new_x][new_y], temp[x][y] 
            temp_state = tuple(tuple(row) for row in temp)
            neighbors.append((temp_state, 1))
    return neighbors

def find_the_star(arr, k):
    if not isSolvable(arr, k):
        return None
    
    start = arr 
    
    
    goal_list = []
    val = 1
    for i in range(k):
        row = []
        for j in range(k):
            if i == k - 1 and j == k - 1:
                row.append(0)
            else:
                row.append(val)
                val += 1
        goal_list.append(tuple(row))
    goal = tuple(goal_list)
    
    path = AstarLowlevel(start, goal, get_neighbors, heuristic)
    return path

def heuristic(state, goal):
    return manhattan_distance(state, goal)

def manhattan_distance(state, goal):
    n = len(state)
    distance = 0
    for i in range(n):
        for j in range(n):
            if state[i][j] != 0:
                goal_x, goal_y = divmod(state[i][j] - 1, n)
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

def isSolvable(arr, k):
    numof_inversions = get_inversions(arr, k)
    if k % 2 == 1:
        return numof_inversions % 2 == 0
    else:
        blank_row_idx = -1
        for i in range(k):
            if 0 in arr[i]:
                blank_row_idx = i
                break
        row_from_bottom = k - blank_row_idx
        if row_from_bottom % 2 == 1:
            return numof_inversions % 2 == 0
        else:
            return numof_inversions % 2 == 1

def process_file(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        lines = infile.read().splitlines()
        lines = [line.strip() for line in lines if line.strip()]
        
        if not lines:
            return
        
        num_tests = int(lines[0])
        idx = 1
        
        for t in range(num_tests):
            if idx >= len(lines):
                break
                
            k = int(lines[idx])
            idx += 1
            
            grid_rows = []
            for _ in range(k):
                row_str = lines[idx]
                idx += 1
                if ' ' in row_str:
                    row_data = [int(x) for x in row_str.split()]
                else:
                    row_data = [int(x) for x in row_str]
                grid_rows.append(tuple(row_data))
            
            start_grid = tuple(grid_rows)
            result = find_the_star(start_grid, k)
            
            if result is None:
                outfile.write("Unsolvable puzzle\n")
            else:
                moves = len(result) - 1
                outfile.write(f"Minimum number of moves = {moves}\n")
                for state in result:
                    for row in state:
                        
                        outfile.write(" ".join(f"{x} " for x in row) + "\n")
                        
                            
                    
                    outfile.write("\n") 

if __name__ == "__main__":
    process_file("input.txt", "output.txt")