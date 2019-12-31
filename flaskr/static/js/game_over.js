function game_over(Lives, CellsLeft)
{
    stats = {
        won : false
    }
    document.getElementById("play").innerText = "Play Again";
    if(Lives == 0)
    {
        document.getElementById("Result").innerText = "You lost all your Lives";
        document.getElementById("Additional_Info").innerText = "Cells left: " + CellsLeft;
    }
    else
    {
        document.getElementById("Result").innerText = "You won!";
        document.getElementById("Additional_Info").innerText = "Lives left: " + Lives;
        stats.won = true;
    }
    document.getElementById("gameOverlay").style.display = "flex";
    
    $.ajax(
        {
            "url": "/stats/",
            "method": "POST",
            "headers": {
              "Content-Type": "application/json"
            },
            "data": JSON.stringify(stats),
        }
    );
}

function remove_overlay()
{
    document.getElementById("gameOverlay").style.display = "none";
}
