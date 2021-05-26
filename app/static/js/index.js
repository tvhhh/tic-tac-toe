
var board = [];
var size = 3;
var turn = "O";

var over = false;
var waiting = true;
var winner = undefined;

var host = window.location.host;


$(".btn").on("click", function() {
    if ($(this).html() == "X" || $(this).html() == "O") {
        $("#turn-container").find(".active").removeClass("active");
        $(this).addClass("active");
        turn = $(this).html();
    } else {
        $("#size-container").find(".active").removeClass("active");
        $(this).addClass("active");
        size = parseInt($(this).html());
    }
});

$("#start-btn").on("click", function() {
    $("#overlay").css("display", "none");
    resetGameState();
    makeBoard();
});

$("#close-btn").on("click", function() {
    $("#overlay").css("display", "none");
});

$("#restart-btn").on("click", function() {
    $(".active").removeClass("active");
    $("#overlay").css("display", "flex");
});

function makeBoard() {
    $("#board-container").empty();
    for (let i = 0; i < size; i++) {
        $("#board-container").append("<div class='row-container'></div>");
        for (let j = 0; j < size; j++) {
            cell = `<div class='cell' id='cell-${i}-${j}' onClick='makeMove(${i},${j})'></div>`;
            $(".row-container").last().append(cell);
        }
    }
    $(".cell").css({ "width": `${60/size}vmin`, "height": `${60/size}vmin`, "font-size": `${2400/size}%` });

    $("#status-container").html("WAITING...");
    $("#status-container").css("color", "skyblue");
    $.post(`http://${host}/make-board`, 
        JSON.stringify({ size: size, turn: turn }),
        (data, status, xhr) => {
            if (status !== "success") return;
            if (data.x !== undefined && data.y !== undefined) {
                let { x, y } = data;
                botTurn = turn == "X" ? "O" : "X";
                $(`#cell-${x}-${y}`).html(botTurn);
                $(`#cell-${x}-${y}`).css("color", botTurn == "X" ? "red" : "skyblue");
            }
            waiting = false;
            $("#status-container").html("YOUR TURN!");
            $("#status-container").css("color", "red");
        }
    );
}

function makeMove(x, y) {
    if (over || waiting) return;
    if ($(`#cell-${x}-${y}`).html()) return;
    
    $(`#cell-${x}-${y}`).html(turn);
    $(`#cell-${x}-${y}`).css("color", turn == "X" ? "red" : "skyblue");
    
    $("#status-container").html("WAITING...");
    $("#status-container").css("color", "skyblue");
    $.post(`http://${host}/make-move`, 
        JSON.stringify({ x: x, y: y }),
        (data, status, xhr) => {
            if (status !== "success") return;
            if (data.x !== undefined && data.y !== undefined) {
                let { x, y } = data;
                botTurn = turn == "X" ? "O" : "X";
                $(`#cell-${x}-${y}`).html(botTurn);
                $(`#cell-${x}-${y}`).css("color", botTurn == "X" ? "red" : "skyblue");
            }
            if (data.over) {
                over = true;
                winner = data.winner;
                if (winner) {
                    if (winner == turn) {
                        $("#status-container").html("YOUR WIN!");
                        $("#status-container").css("color", "red");
                    } else {
                        $("#status-container").html("YOUR LOSE!");
                        $("#status-container").css("color", "red");
                    }
                } else {
                    $("#status-container").html("DRAW!");
                    $("#status-container").css("color", "red");
                }
                return;
            }
            waiting = false;
            $("#status-container").html("YOUR TURN!");
            $("#status-container").css("color", "red");
        }
    );
}

function resetGameState() {
    over = false;
    waiting = true;
    winner = undefined;
}