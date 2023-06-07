let player = "X";
let cells = document.querySelectorAll(".cell");
let gameOver = false;
let startTime = new Date();
let outcome;
let numMoves = 0;
let isUserTurn = true;
let board = [];

function updateBoard() {
  for (let i = 0; i < cells.length; i++) {
    board[i] = cells[i].innerHTML;
  }
}

function handleClick() {
  if (gameOver || !isUserTurn) return;
  if (this.innerHTML !== "") {
    toastr.error("That cell is already taken!");
    return;
  }

  this.style.color = "#3C3F4A";
  this.innerHTML = player;
  updateBoard();
  numMoves++;

  if (checkForWin() === "X") {
    toastr.success("You Win!");
    gameOver = true;
    outcome = "Win";
    updateGameStatus();
    return;
  }

  if (checkForDraw()) {
    toastr.info("It's a draw!");
    gameOver = true;
    outcome = "Draw";
    updateGameStatus();
    return;
  }

  player = "O";
  isUserTurn = false;
  computerMove();
}

function computerMove() {
  let bestScore = -Infinity;
  let bestMove = -1;
  for (let i = 0; i < board.length; i++) {
    if (board[i] === "") {
      board[i] = "O";
      let score = minimax(false);
      board[i] = "";
      if (score > bestScore) {
        bestScore = score;
        bestMove = i;
      }
    }
  }

  cells[bestMove].style.color = "#f5f5f5";
  cells[bestMove].innerHTML = player;
  updateBoard();
  numMoves++;

  if (checkForWin() === "O") {
    toastr.error("You Lose!");
    gameOver = true;
    outcome = "Loss";
    updateGameStatus();
    return;
  }

  if (checkForDraw()) {
    toastr.info("It's a draw!");
    gameOver = true;
    outcome = "Draw";
    updateGameStatus();
    return;
  }

  player = "X";
  isUserTurn = true;
}

function minimax(isMaximizingPlayer) {
  if (checkForWin() === "O") {
    return 10;
  } else if (checkForWin() === "X") {
    return -10;
  } else if (checkForDraw()) {
    return 0;
  }

  if (isMaximizingPlayer) {
    let bestScore = -Infinity;
    for (let i = 0; i < board.length; i++) {
      if (board[i] === "") {
        board[i] = "O";
        let score = minimax(false);
        board[i] = "";
        bestScore = Math.max(bestScore, score);
      }
    }
    return bestScore;
  } else {
    let bestScore = Infinity;
    for (let i = 0; i < board.length; i++) {
      if (board[i] === "") {
        board[i] = "X";
        let score = minimax(true);
        board[i] = "";
        bestScore = Math.min(bestScore, score);
      }
    }
    return bestScore;
  }
}

function checkForWin() {
  let winningCombinations = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];

  for (let i = 0; i < winningCombinations.length; i++) {
    let combo = winningCombinations[i];

    if (
      board[combo[0]] === board[combo[1]] &&
      board[combo[1]] === board[combo[2]]
    ) {
      return board[combo[0]];
    }
  }

  return null;
}

function checkForDraw() {
  for (let i = 0; i < board.length; i++) {
    if (board[i] === "") {
      return false;
    }
  }

  return true;
}

function updateGameStatus() {
  console.log(startTime);
  $.ajax({
    type: "POST",
    url: "/update_match",
    data: {
      status: outcome,
      moves: numMoves,
      start_time: startTime,
      duration: (new Date() - startTime) / 1000,
    },
    success: function (data, textStatus, xhr) {
      let location = xhr.getResponseHeader("Location");
      window.location.replace(location);
    },
    error: function (error) {
      console.log(error);
    },
  });
}

for (let i = 0; i < cells.length; i++) {
  cells[i].addEventListener("click", handleClick);
  board.push("");
}
