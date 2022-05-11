// Default values for a bet
var theBet = "no-bet";
var theBettor = "unknown";

function betted(bettedOn){
    theBet = bettedOn

    let clear = document.getElementsByClassName('bet');
    for (let i=0; i<clear.length; i++)  {clear[i].style.opacity = 0};

    document.getElementById(bettedOn).style.opacity = 1;
}

function submitBet(){
    theBettor = document.getElementById("selection").value;
    console.log(theBettor + " bet on " + theBet);
}