// Default values for a bet
var theBet = "no-bet";
var theBettor = "unknown";
var lambdaUrl = "https://a4j2yx62yf.execute-api.us-east-1.amazonaws.com/default/office-roulette";

function betted(bettedOn){
    theBet = bettedOn

    let clear = document.getElementsByClassName('bet');
    for (let i=0; i<clear.length; i++)  {clear[i].style.opacity = 0};

    document.getElementById(bettedOn).style.opacity = 1;
}

function submitBet(){
    theBettor = document.getElementById("selection").value;
    console.log(theBettor + " bet on " + theBet);

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function selectVictim(){
    let password = prompt("Password")
    let victim = prompt("victim")
}