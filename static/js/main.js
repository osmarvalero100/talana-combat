const keysEvent = ["P","K"];
const combinations = {
    players: [
        {
            id: 1,
            firtsAttack: null,
            movements: "",
            hit: ""
        },
        {
            id: 2,
            firtsAttack: null,
            movements: "",
            hit: ""
        }
    ]       
}
const fightEndpoint = "/api/fight";
let matchstarted = false;
let fight = {};
let currentPlayer = 1;
let fightId = null;


if (localStorage.getItem("fightId") > 0)
    fightId = localStorage.getItem("fightId");

function resertFight() {
    localStorage.removeItem("fightId");
    location.reload();
}

function activeButtons() {
    if (fight.combat.player1.movimientos.length > 0 || fight.combat.player2.movimientos.length > 0) {
        document.querySelectorAll('.controls__player__buttons button').forEach(button => {
            button.disabled = true;
        });
        if (fight.winner < 1) {
            document.querySelectorAll(`#playerControl${currentPlayer} button`).forEach(button => {
                button.disabled = false;
            });
        }
    }
}

function updateEnergyPlayers(players) {
    for (let i = 0; i < players.length; i++) {
        const player = players[i];
        playerEnergy = player.energy;
        const divQty = document.getElementById(`qty${i+1}`);
        divQty.innerText = playerEnergy;
        divQty.style.width = `${playerEnergy*20}px`;
    }
}
function updateFightLocal(data) {
    fight = data
    fight.combat = JSON.parse(fight.combat);
    changeCurrentPlayer();
    updateEnergyPlayers([fight.combat.player1, fight.combat.player2]);
    combinations.players.forEach(cp => {cp.movements="";cp.hit=""});

    if (data.winner > 0) {
        const winner = [data.combat.player1, data.combat.player2].find(p => p.player_id == data.winner);
        if (winner) {
            document.getElementById('winnerPlayerName').textContent = 'Vencedor: '+winner.name;
            document.getElementById('winner').style.display = "block";
        }
    }
}

function setPlayersNames() {
    document.getElementById('namePlayer1').innerText = fight.combat.player1.name;
    document.getElementById('namePlayer2').innerText = fight.combat.player2.name;
}

function startFight() {
    if (fightId < 1) {
        // Create a combat and save it locally
        fetch(fightEndpoint, {
            method: "POST",
            body: JSON.stringify({match: ""}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        })
        .then(response => response.json()) 
        .then(data => {
            updateFightLocal(data);
            setPlayersNames();
            fightId = data.id;
            localStorage.setItem("fightId", data.id)
        })
        .catch(err => console.log(err));
    } else {
        // Recover a started combat
        fetch(`${fightEndpoint}/${fightId}`)
        .then(response => response.json()) 
        .then(data => {
            updateFightLocal(data);
            fightId = data.id;
            setPlayersNames();
        })
        .catch(err => console.log(err));
    }
}

function addMove(move, playerId) {
    const player = combinations.players.find(p => p.id == playerId);
    let combination = player.movements;

    if (combination.length >= 3)
        combination = combination.slice(1);
    
    for (var i = 0; i < combinations.players.length; i++) {
        if (combinations.players[i].id == playerId) {
            combinations.players[i].movements = combination + move;
            break;
        }
    }
    currentPlayer = playerId
}

 
function getBestPlayerAttack(player1, player2) {
    const p1Attack = player1.movements + player1.hit;
    const p2Attack = player2.movements + player2.hit;
    // Parte atacando el jugador que envió una combinación menor de botones (movimiento + golpes)
    if (p1Attack.length != p2Attack.length) {
        if (p1Attack.length < p2Attack.length)
            return player1;
        return player2;
    }
    // En caso de empate, parte el con menos movimientos
    const p1Moves = player1.movements;
    const p2Moves = player2.movements;
    if (p1Moves.length != p2Moves.length) {
        if (p1Moves < p2Moves)
            return player1;
        return player2;
    }
    // si empatan de nuevo, inicia el con menos golpes
    if (player1.hit != player2.hit) {
        if (player1.hit == "K")
            return player1;
        return player2
    }
    // si hay empate de nuevo, inicia el player 1 (total el player 2 siempre es del hermano chico)
    return player1;
}

function getFirstPlayerAttack() {
    const player1 = combinations.players.find(p => p.id == 1);
    const player2 = combinations.players.find(p => p.id == 2);

    if ((player1.hit === null || player1.movements.length < 1) 
        || (player2.hit === null || player2.movements.length < 1))
        return null;
    
    return getBestPlayerAttack(player1, player2);
}

function changeCurrentPlayer() {
    if (currentPlayer == 1)
        currentPlayer = 2;
    else
        currentPlayer = 1;
    
    activeButtons();
}

async function updateCombat(playerAttack) {
    if (fight.combat.hasOwnProperty('player'+playerAttack.id)) {
        if (fight.combat['player'+playerAttack.id].hasOwnProperty('movimientos'))
            fight.combat['player'+playerAttack.id].movimientos.push(playerAttack.movements);
        else
            fight.combat['player'+playerAttack.id].movimientos = [playerAttack.movements];
        
        if (fight.combat['player'+playerAttack.id].hasOwnProperty('golpes'))
            fight.combat['player'+playerAttack.id].golpes.push(playerAttack.hit);
        else
            fight.combat['player'+playerAttack.id].golpes = [playerAttack.hit];
    } else {
        fight.combat['player'+playerAttack.id] = {};
        fight.combat['player'+playerAttack.id].movimientos = [playerAttack.movements];
        fight.combat['player'+playerAttack.id].golpes = [playerAttack.hit];
    }

    fight.combat['player'+playerAttack.id].attackMode = false;

    const data = {
        combat: JSON.stringify(fight.combat)
    }
    fetch(`${fightEndpoint}/${fightId}`, {
        method: "PATCH",
        body: JSON.stringify(data),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
    .then(response => response.json()) 
    .then(data => {
        if (data.hasOwnProperty('detail')) {
            console.warn(data.detail);
        } else {
            updateFightLocal(data);
        }
    })
    .catch(err => console.log(err));
}

function isCombatStarted() {
    if (fight.combat.player1.movimientos.length > 0 || fight.combat.player2.movimientos.length > 0)
        return true;
    return false;
}

function setHit(hit) {
    const player = combinations.players.find(p => p.id == currentPlayer);

    if (player.movements.length > 0 || fight.combat.player1.movimientos.length > 0 || fight.combat.player2.movimientos.length > 0) {
        const movements = player.movements;
        combinations.players[currentPlayer - 1].firtsAttack = `${movements}+${hit}`;

        for (var i = 0; i < combinations.players.length; i++) {
            if (combinations.players[i].id == currentPlayer) {
                combinations.players[i].hit = hit;
                break;
            }
        }
    }
}

document.addEventListener("keydown", async function(event) {
    const keyValue = event.key.toUpperCase();
    if (keysEvent.includes(keyValue)) {
        if (!isCombatStarted()) {
            setHit(keyValue);
            const playerAttcak = getFirstPlayerAttack();
            if (playerAttcak !== null)
                await updateCombat(playerAttcak);
        } else {
            setHit(keyValue);
            await updateCombat(combinations.players[currentPlayer-1]);
        }
    }
}, false);


startFight();