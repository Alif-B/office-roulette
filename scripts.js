// Default values for a bet
var theBet = "no-bet";
var theBettor = "unknown";
var apiGateway = "https://d5n3ltvz28.execute-api.us-east-1.amazonaws.com/Prod";

function betted(bettedOn){
    theBet = bettedOn

    let clear = document.getElementsByClassName('bet');
    for (let i=0; i<clear.length; i++)  {clear[i].style.opacity = 0};

    document.getElementById(bettedOn).style.opacity = 1;
}

function submitBet(){
    theBettor = document.getElementById("selection").value;
    console.log(theBettor + " bet on " + theBet);
    
    // forming the request path
    var fullApiPath = apiGateway+"/bet?action=bets&bettor="+theBettor+"&bet="+theBet;
    console.log(fullApiPath);

    // sending the request
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "PUT", fullApiPath);
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function selectVictim(){
    let password = prompt("Password");
    let victim = prompt("victim");

    var fullApiPath = apiGateway+"/score?action=scores&bettor="+victim+"&bet="+password;
    console.log(fullApiPath);

    // sending the request
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "PUT", fullApiPath);
    xmlHttp.send( null );
    return xmlHttp.responseText;
}