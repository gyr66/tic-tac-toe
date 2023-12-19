import numpy as np


class TicTacToeGame:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.winner = None
        self.current_player = PLAYER_X

    def play_move(self, row, col, player):
        if self.board[row, col] == EMPTY and self.winner is None:
            self.board[row, col] = player
            self.current_player *= -1
            self.winner = self.check_winner()

    def available_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == EMPTY]

    def check_winner(self):
        for i in range(3):
            row_sum = self.board[i, :].sum()
            col_sum = self.board[:, i].sum()
            if abs(row_sum) == 3:
                return np.sign(row_sum)
            if abs(col_sum) == 3:
                return np.sign(col_sum)
        diag_sum_primary = np.diagonal(self.board).sum()
        diag_sum_secondary = np.diagonal(np.fliplr(self.board)).sum()
        if abs(diag_sum_primary) == 3:
            return np.sign(diag_sum_primary)
        if abs(diag_sum_secondary) == 3:
            return np.sign(diag_sum_secondary)
        if not self.available_moves():
            return 0
        return None


class AIPlayer:
    def __init__(self, symbol, epsilon=0.2):
        self.symbol = symbol
        self.state_value_function = {}
        self.state_visit_counts = {}
        self.epsilon = epsilon

    def get_move(self, game):
        if np.random.rand() < self.epsilon:
            moves = game.available_moves()
            move = moves[np.random.choice(len(moves))]
        else:
            best_move = None
            best_value = -float("inf")
            for move in game.available_moves():
                next_board = game.board.copy()
                next_board[move] = self.symbol
                next_state_value = self.state_value_function.get(
                    state_to_key(next_board), 0
                )
                if next_state_value > best_value:
                    best_value = next_state_value
                    best_move = move
            move = best_move
        return move


def state_to_key(state):
    return tuple(state.flatten())


def update_state_values(player, state_keys, reward):
    for state_key in state_keys:
        if state_key not in player.state_visit_counts:
            player.state_visit_counts[state_key] = 0
            player.state_value_function[state_key] = 0.0
        visits = player.state_visit_counts[state_key] + 1
        player.state_visit_counts[state_key] = visits
        value = player.state_value_function[state_key]
        player.state_value_function[state_key] += (reward - value) / visits


def train(game, player_x, player_o, num_episodes=10000):
    for episode in range(num_episodes):
        game.__init__()
        state_history = {PLAYER_X: [], PLAYER_O: []}

        while game.winner is None:
            player = player_x if game.current_player == PLAYER_X else player_o
            move = player.get_move(game)
            game.play_move(*move, game.current_player)
            state_key = state_to_key(game.board)
            state_history[player.symbol].append(state_key)
            if game.winner is not None:
                reward_X = (
                    1 if game.winner == PLAYER_X else 0 if game.winner == 0 else -1
                )
                reward_O = -reward_X
                update_state_values(player_x, state_history[PLAYER_X], reward_X)
                update_state_values(player_o, state_history[PLAYER_O], reward_O)
                break
        print(f"Episode {episode + 1}: Winner = {game.winner}")


EMPTY = 0
PLAYER_X = 1
PLAYER_O = -1


player_x = AIPlayer(PLAYER_X)
player_o = AIPlayer(PLAYER_O)

game = TicTacToeGame()

train(game, player_x, player_o, num_episodes=100000)


with open("state_values_x.txt", "w") as file:
    for state_key, value in player_x.state_value_function.items():
        state_str = ",".join(map(str, state_key))
        file.write(f"{state_str}:{value}\n")

with open("state_values_o.txt", "w") as file:
    for state_key, value in player_o.state_value_function.items():
        state_str = ",".join(map(str, state_key))
        file.write(f"{state_str}:{value}\n")
