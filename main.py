import random

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

def knight_tour_random(threshold, board_size=8, trials=100000):
    """Run the knight's tour with a random approach."""
    results = []
    for _ in range(trials):
        board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
        current_pos = (random.randrange(board_size), random.randrange(board_size))
        board[current_pos[0]][current_pos[1]] = 0  # start position
        for move_number in range(1, board_size ** 2):
            legal_moves = generate_legal_moves(current_pos[0], current_pos[1], board_size)
            if not legal_moves: break  # no more legal moves, end the tour
            current_pos = random.choice(legal_moves)
            board[current_pos[0]][current_pos[1]] = move_number
        
        success = move_number >= (threshold * board_size ** 2) / 100
        results.append({
            'start': current_pos,
            'success': success,
            'tour_length': move_number,
            'board': board
        })
    return results

# Example of running the algorithm for a threshold of 70%
example_results = knight_tour_random(70, trials=10)  # Just 10 trials for a quick example

# Output the results of the example run
for result in example_results:
    print(f"Start Position: {result['start']} | Success: {result['success']} | Tour Length: {result['tour_length']}")
    for row in result['board']:
        print(row)
    print("\n---\n")
