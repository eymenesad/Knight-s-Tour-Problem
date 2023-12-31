import random
import os

def generate_legal_moves(x, y, board):
    """Generate all possible moves for a knight on an 8x8 chessboard."""
    new_moves = []
    move_offsets = [(-2, -1), (-1, -2), (-2, 1), (-1, 2),
                    (1, -2), (2, -1), (1, 2), (2, 1)]
    
    for move in move_offsets:
        new_x, new_y = x + move[0], y + move[1]
        if legal_coord(new_x, len(board)) and legal_coord(new_y, len(board)) and board[new_x][new_y] == -1:
            new_moves.append((new_x, new_y))
    return new_moves

def legal_coord(x, board_size):
    """Check if the coordinates are within the board."""
    return 0 <= x < board_size

def knight_tour_random(threshold, trials, board_size=8):
    """Run the knight's tour with a random approach."""
    results = []
    threshold_squares = int(threshold * board_size ** 2)  # Calculate the threshold in terms of squares
    
    for trial in range(trials):
        board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
        move_sequence = []
        current_pos = (random.randrange(board_size), random.randrange(board_size))
        board[current_pos[0]][current_pos[1]] = 0  # mark the start position as visited
        move_sequence.append(current_pos)  # record the start position
        
        while True:
            legal_moves = generate_legal_moves(current_pos[0], current_pos[1], board)
            if not legal_moves:
                # No more legal moves, end the tour
                break
            current_pos = random.choice(legal_moves)
            board[current_pos[0]][current_pos[1]] = len(move_sequence)  # mark the square as visited
            move_sequence.append(current_pos)  # record each move
        
        success = len(move_sequence) - 1 >= threshold_squares  # Check if the tour was successful
        results.append({
            'start': move_sequence[0],
            'move_sequence': move_sequence,
            'success': success,
            'tour_length': len(move_sequence),
            'board': board
        })
    return results

def write_results_to_file(results, p, board_size=8):
    """Write the results of the knight's tour to a file."""
    filename = f"results_{p}.txt"
    with open(filename, 'w') as f:
        for count, result in enumerate(results, 1):
            f.write(f"Run {count}: starting from {result['start']}\n")
            for move in result['move_sequence']:
                f.write(f"Stepping to {move}\n")
            f.write(f"{'' if result['success'] else 'Un'}successful - Tour length: {result['tour_length']}\n")
            
            for row in result['board']:
                f.write(' '.join(str(cell) for cell in row) + '\n')
            
            f.write("\n---\n")

def run_knight_tour_simulation(p, trials, board_size=8):
    """Run the knight's tour simulation and print the summary of results."""
    successful_tours = 0
    results = knight_tour_random(p, trials, board_size)
    
    # Count the number of successful tours
    for result in results:
        if result['success']:
            successful_tours += 1
    
    # Calculate the probability of a successful tour
    probability_of_success = successful_tours / trials
    
    # Print the summary in the required format
    print(f"LasVegas Algorithm With p = {p}")
    print(f"Number of successful tours: {successful_tours}")
    print(f"Number of trials: {trials}")
    print(f"Probability of a successful tour: {probability_of_success:.5f}\n")

    # Call the function to write the results to a file
    write_results_to_file(results, p, board_size)


def knight_tour_deterministic(p, k, trials, board_size=8):
    """Run the knight's tour with a random approach for k steps, then use backtracking."""
    results = []
    threshold_squares = int(p * board_size ** 2)  # Calculate the threshold in terms of squares
    
    for trial in range(trials):
        board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
        move_sequence = []
        current_pos = (random.randrange(board_size), random.randrange(board_size))
        board[current_pos[0]][current_pos[1]] = 0  # mark the start position as visited
        move_sequence.append(current_pos)  # record the start position
        
        # Randomly move k steps
        for _ in range(k):
            legal_moves = generate_legal_moves(current_pos[0], current_pos[1], board)
            if not legal_moves:
                break  # No more legal moves
            current_pos = random.choice(legal_moves)
            board[current_pos[0]][current_pos[1]] = len(move_sequence)
            move_sequence.append(current_pos)

        # Use backtracking to complete the tour
        success = backtracking_tour(board, move_sequence, threshold_squares)
        
        results.append({
            'start': move_sequence[0],
            'move_sequence': move_sequence,
            'success': success,
            'tour_length': len(move_sequence),
            'board': board
        })
    
    return results

def backtracking_tour(board, move_sequence, threshold_squares):
    """Use backtracking to complete the knight's tour."""
    if len(move_sequence) - 1 >= threshold_squares:
        return True  # The tour is already successful

    current_pos = move_sequence[-1]
    legal_moves = generate_legal_moves(current_pos[0], current_pos[1], board)

    for move in legal_moves:
        move_sequence.append(move)
        board[move[0]][move[1]] = len(move_sequence) - 1  # mark the square as visited
        if backtracking_tour(board, move_sequence, threshold_squares):
            return True  # Continue the tour
        # If the tour is unsuccessful, backtrack
        move_sequence.pop()
        board[move[0]][move[1]] = -1
    
    return False  # No successful tour found

def run_knight_tour_simulation_det(p, k_values, trials, board_size=8):
    """Run the knight's tour simulation for different values of k and print the summary of results."""
    for k in k_values:
        successful_tours = 0
        results = knight_tour_deterministic(p, k, trials, board_size)
        
        # Count the number of successful tours
        for result in results:
            if result['success']:
                successful_tours += 1
        
        # Calculate the probability of a successful tour
        probability_of_success = successful_tours / trials
        
        # Print the summary in the required format
        print(f"LasVegas Algorithm With p = {p}, k = {k}")
        print(f"Number of successful tours: {successful_tours}")
        print(f"Number of trials: {trials}")
        print(f"Probability of a successful tour: {probability_of_success:.5f}\n")

    write_results_to_file(results, p, board_size)

# Run the simulation for different values of p and print the results
input_type = input("Enter part1 for Las Vegas Algorithm or part2 for Las Vegas Algorithm with Deterministic Algorithm: ")

if input_type == "part1":
    for p_value in [0.7, 0.8, 0.85]:
        trial_count = 10  # Use 100000 for the actual project run
        run_knight_tour_simulation(p_value, trial_count)
        break

elif input_type == "part2":
        # Run the simulation for different values of p, k, and print the results
    p_values = [0.7, 0.8, 0.85]
    k_values = [0, 1, 2, 3]
    trial_count = 10000

    #for p_value in p_values:
    #run_knight_tour_simulation_det(0.85, k_values, trial_count)
