function isTerminal(board: number[][]) {
  for (let i = 0; i < 3; i++) {
    if (board[i][0] && board[i][0] === board[i][1] && board[i][0] === board[i][2]) return true
    if (board[0][i] && board[0][i] === board[1][i] && board[0][i] === board[2][i]) return true
  }
  if (board[0][0] && board[0][0] === board[1][1] && board[0][0] === board[2][2]) return true
  if (board[0][2] && board[0][2] === board[1][1] && board[0][2] === board[2][0]) return true
  for (const item of board.flat()) if (item === 0) return false
  return true
}

function utility(board: number[][]) {
  for (let i = 0; i < 3; i++) {
    if (board[i][0] && board[i][0] == board[i][1] && board[i][0] == board[i][2]) return board[i][0]
    if (board[0][i] && board[0][i] == board[1][i] && board[0][i] == board[2][i]) return board[0][i]
  }
  if (board[0][0] && board[0][0] == board[1][1] && board[0][0] == board[2][2]) return board[0][0]
  if (board[0][2] && board[0][2] == board[1][1] && board[0][2] == board[2][0]) return board[0][2]
  return 0
}

function minValue(board: number[][], alpha: number, beta: number) {
  if (isTerminal(board)) return utility(board)
  let v = Infinity
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      if (!board[i][j]) {
        board[i][j] = -1
        v = Math.min(v, maxValue(board, alpha, beta))
        board[i][j] = 0
        if (v <= alpha) return v
        beta = Math.min(beta, v)
      }
    }
  }
  return v
}

function maxValue(board: number[][], alpha: number, beta: number) {
  if (isTerminal(board)) return utility(board)
  let v = -Infinity
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      if (!board[i][j]) {
        board[i][j] = 1
        v = Math.max(v, minValue(board, alpha, beta))
        board[i][j] = 0
        if (v >= beta) return v
        alpha = Math.max(alpha, v)
      }
    }
  }
  return v
}

function alphaBetaSearch(board: number[][]) {
  if (isTerminal(board)) return [-1, -1]
  let alpha = -Infinity
  // eslint-disable-next-line prefer-const
  let beta = Infinity
  let v = -Infinity
  let pos = [-1, -1]
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      if (!board[i][j]) {
        board[i][j] = 1
        const t = minValue(board, alpha, beta)
        if (t > v) {
          v = t
          alpha = Math.max(alpha, v)
          pos = [i, j]
        }
        board[i][j] = 0
      }
    }
  }
  return pos
}

export { isTerminal, alphaBetaSearch, utility }
