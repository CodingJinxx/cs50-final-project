var Grid; // [x][y]
var Solution; // [x][y]
var Lives;
var GameOver;
var CellsLeft;

function UpdateStats()
{
    document.getElementById("Lives").innerText = "Lives: " + Lives;
    document.getElementById("Cells").innerText = "Cells: " + CellsLeft;
}

function generateGrid(size)
{          
    Lives = 3;
    GameOver = false;
    CellsLeft = size * size;
    UpdateStats();
    
    Grid = createArray(size, size);
    Solution = generatePuzzle(size);
    for(let x = 0; x < size; x++)
    {
        let numbers = document.createElement("ul");
        for(let j = 0; j < Solution.xNumber[x].length; j++)
        {
            let number = document.createElement("li");
            number.appendChild(document.createTextNode(Solution.xNumber[x][j]));
            numbers.appendChild(number);
        }

        let a = document.createElement("div");
        a.appendChild(numbers);
        let b = document.createElement("div");
        b.appendChild(a);
        document.getElementById("xNumbers").appendChild(b);
    }

    for(let y = 0; y < size; y++)
    {
        let numbers = document.createElement("ul");
        for(let j = 0; j < Solution.yNumber[y].length; j++)
        {
            let number = document.createElement("li");
            number.appendChild(document.createTextNode(Solution.yNumber[y][j]));
            numbers.appendChild(number);
        }
        let a = document.createElement("div");
        a.appendChild(numbers);
        let b = document.createElement("div");
        b.appendChild(a);
        document.getElementById("yNumbers").appendChild(b);
    }

    for(let x = 0; x < size; x++)
    {
        let row = document.createElement("div");
        row.className = "Row";
        for(let y = 0; y < size; y++)
        {
            let cell = document.createElement("div");
            cell.className = "Cell";
            cell.id = x + "|" + y;
            cell.oncontextmenu = () => {return false};
            cell.onmousedown = cellClicked;
            cell.onmouseenter = cellMouseEnter;
            cell.onmouseleave = cellMouseLeave;
            row.appendChild(cell);
        }
        document.getElementById("gridCanvas").appendChild(row);
    }
}

function setCell(x, y, value)
{
    if(value != -2 && value != -1 && value != 0 && value != 1 && value != -3)
    {
        alert("ERROR");
        return false;
    }
    Grid[x][y] = value;
    let cell = document.getElementById(x + "|" + y);
    switch(value)
    {
        case 1:
            toggleClass(cell, "Cell-O", true)
            toggleClass(cell, "Cell-X", false)
            break;
        case -1:
            toggleClass(cell, "Cell-X", true)
            toggleClass(cell, "Cell-O", false)
            break;
        case 0:
            toggleClass(cell, "Cell-O", false)
            toggleClass(cell, "Cell-X", false)
        case -2:
            toggleClass(cell, "Cell-O", false)
            toggleClass(cell, "Cell-X", false)
            toggleClass(cell, "Cell-Red", true)
            Lives -= 1;
            UpdateStats();
            break;
        case -3:
            cell.onmousedown = null;   
            break;
    }
}

function checkGrid()
{
    for(let i = 0; i < Grid.length; i++)
    {
        for(let j = 0; j < Grid[0].length; j++)
        {        
            if(Grid[i][j] == -1 || Grid[i][j] == 1)
            {
                console.log(Grid[i][j] + " == " + Solution.grid[i][j]);
                if(Grid[i][j] != Solution.grid[i][j])
                {
                    setCell(i, j, -2)
                }
            }
        }
    }
}

function isCellCorrect(x,y, value)
{
    if(value == Solution.grid[x][y])
    {
        return true;
    }
    return false;
}

function cellClicked(event)
{
    toggleClass(this, "Cell-Hover", false);
    position = this.id.split("|").map(function(item)
    {
        return parseInt(item, 10);
    });
    toggleClass(this, "Cell-Red", false);
    switch(event.which)
    {
        case 1:
            if(!isCellCorrect(position[0], position[1], 1))
            {
                setCell(position[0], position[1], -2);
                setCell(position[0],position[1], -1);
            }
            else
            {
                setCell(position[0], position[1], 1);
            }
            break;

        case 3: 
            if(!isCellCorrect(position[0], position[1], -1))
            {
                setCell(position[0],position[1], -2);
                setCell(position[0],position[1], 1);
            }
            else
            {
                setCell(position[0],position[1], -1);
            }
            break;
        default:
    }
    CellsLeft -= 1;
    UpdateStats();
    if(CellsLeft == 0 || Lives == 0)
    {
        game_over(Lives, CellsLeft);
        disableCells();
    }
    this.onmousedown = null
}
function disableCells()
{
    for(let x = 0; x < Grid.length; x++)
    {
        for(let y = 0; y < Grid[0].length; y++)
        {
            setCell(x,y,-3);
            
        }
    }
}

function cellMouseEnter(event)
{   
    position = this.id.split("|").map(function(item)
    {
        return parseInt(item, 10);
    });
    if(Grid[position[0]][position[1]] == null)
    {
        toggleClass(this, "Cell-Hover", true);
    }
}

function cellMouseLeave()
{
    toggleClass(this, "Cell-Hover", false);
}

function generatePuzzle(size)
{
    xNumber = createArray(size, 0);
    yNumber = createArray(size, 0);
    grid = createArray(size, size);

    // --------- GRID ---------
    // Each Row/y
    for(let y = 0; y < size; y++)
    {
        // Each Column/x
        for(let x = 0; x < size; x++)
        {
            let chance = Math.random()
            if(chance < 0.4)
            {
                grid[x][y] = -1;
            }
            else
            {
                grid[x][y] = 1;
            }
        }
    }

    // ---------  XNUMBER ---------
    // Each Column - xNumber
    let totalCounter = 0;
    let blockCounter = 0;
    for(let x = 0; x < size; x++)
    {
        if(blockCounter > 0)
        {
            xNumber[x - 1].push(blockCounter);
        }
        totalCounter = 0;
        blockCounter = 0;
        while(totalCounter < size)
        {
            if(grid[x][totalCounter] == 1)
            {
                blockCounter++;
            }
            else if(grid[x][totalCounter] == -1 && blockCounter != 0)
            {
                xNumber[x].push(blockCounter);
                blockCounter = 0;
            }
            totalCounter++;
        }
    }
    if(blockCounter > 0)
    {
        xNumber[size - 1].push(blockCounter);
    }

    // --------- YNUMBER ---------
    // Each Row - yNumber
    totalCounter = 0;
    blockCounter = 0;
    for(let y = 0; y < size; y++)
    {
        if(blockCounter > 0)
        {
            yNumber[y - 1].push(blockCounter);
        }
        totalCounter = 0;
        blockCounter = 0;
        while(totalCounter < size)
        {
            if(grid[totalCounter][y] == 1)
            {
                blockCounter++;
            }
            else if(grid[totalCounter][y] == -1 && blockCounter != 0)
            {
                yNumber[y].push(blockCounter);
                blockCounter = 0;
            }
            totalCounter++;
        }
    }
    if(blockCounter > 0)
    {
        yNumber[size - 1].push(blockCounter);
    }
    return {xNumber, yNumber, grid};
}

function show()
{
    for(let x = 0; x < Solution.grid.length; x++)
    {
        for(let y = 0; y < Solution.grid[0].length; y++)
        {
            setCell(x, y, Solution.grid[x][y]);
        }
    }
}

function createArray(length) {
    var arr = new Array(length || 0),
        i = length;

    if (arguments.length > 1) {
        var args = Array.prototype.slice.call(arguments, 1);
        while(i--) arr[length-1 - i] = createArray.apply(this, args);
    }

    return arr;
}

function toggleClass(elem, theClass, newState) {
    var matchRegExp = new RegExp('(?:^|\\s)' + theClass + '(?!\\S)', 'g');
    var add=(arguments.length>2 ? newState : (elem.className.match(matchRegExp) == null));
    elem.className=elem.className.replace(matchRegExp, ''); // clear all
    if (add) 
    {
        elem.className += ' ' + theClass;
        return true;
    }
    return false;
}