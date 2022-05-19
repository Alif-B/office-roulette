// Default values for a bet
var theBet = "no-bet";
var apiGateway = "https://d5n3ltvz28.execute-api.us-east-1.amazonaws.com/Prod";

function betted(bettedOn){
    theBet = bettedOn

    let clear = document.getElementsByClassName('bet');
    for (let i=0; i<clear.length; i++)  {clear[i].style.opacity = 0};

    document.getElementById(bettedOn).style.opacity = 1;
}

function submitBet(){
    theBettor = document.getElementById("selection").value;
    betAmount = parseInt(document.getElementById("betAmount").value);
    window.alert(theBettor + " bet " + betAmount + " blamebucks on " + theBet);
    fullBet = theBet+"amount"+betAmount;
    
    // forming the request path
    var fullApiPath = apiGateway+"/bet?action=bets&bettor="+theBettor+"&bet="+fullBet;
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


function scoreboard(){
    var fullApiPath = apiGateway+"/scoreboard?action=scoreboard&bettor=na&bet=na";
    console.log(fullApiPath);


    // sending the request
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", fullApiPath);
    xmlHttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xmlHttp.setRequestHeader('Access-Control-Allow-Origin', '*');
    xmlHttp.send( null );
    xmlHttp.onload = ()=>{
        console.log(xmlHttp);
        if(xmlHttp.status == 200) {
            console.log(JSON.parse(xmlHttp.response))
        }
    }
}

//scoreboard();