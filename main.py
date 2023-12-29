import random
import os

def generate_legal_moves(x, y, board_size):
    """Generate all possible moves for a knight on an 8x8 chessboard."""
    new_moves = []
    move_offsets = [(-2, -1), (-1, -2), (-2, 1), (-1, 2),
                    (1, -2), (2, -1), (1, 2), (2, 1)]
    
    for move in move_offsets:
        new_x = x + move[0]
        new_y = y + move[1]
        if legal_coord(new_x, board_size) and \
           legal_coord(new_y, board_size):
            new_moves.append((new_x, new_y))
    return new_moves

def legal_coord(x, board_size):
    """Check if the coordinates are within the board."""
    return 0 <= x < board_size

def knight_tour_random(threshold, board_size=8, trials=100):
    """Run the knight's tour with a random approach."""
    results = []
    threshold_squares = (threshold * board_size ** 2) / 100  # Calculate the threshold in terms of squares
    
    for trial in range(trials):
        board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
        move_sequence = []
        current_pos = (random.randrange(board_size), random.randrange(board_size))
        move_sequence.append(current_pos)  # record the start position
        board[current_pos[0]][current_pos[1]] = 0  # mark the start position as visited

        for move_number in range(1, board_size ** 2):
            legal_moves = generate_legal_moves(current_pos[0], current_pos[1], board_size)
            if not legal_moves:
                break  # no more legal moves, end the tour
            current_pos = random.choice(legal_moves)
            move_sequence.append(current_pos)  # record each move
            board[current_pos[0]][current_pos[1]] = move_number  # mark the square as visited
        
        success = len(move_sequence) > threshold_squares  # Check if the tour was successful
        results.append({
            'start': move_sequence[0],
            'move_sequence': move_sequence,
            'success': success,
            'tour_length': len(move_sequence),  # the actual tour length is the length of move_sequence
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
            
            
def run_knight_tour_simulation(p, board_size=8, trials=100000):
    """Run the knight's tour simulation and print the summary of results."""
    successful_tours = 0
    results = knight_tour_random(p, board_size, trials)
    
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
    print(f"Probability of a successful tour: {probability_of_success:.5f} \n")

# Run the simulation for different values of p and print the results
for p_value in [0.7, 0.8, 0.85]:
    run_knight_tour_simulation(p_value, trials=100)  # Use 100000 for the actual project run
