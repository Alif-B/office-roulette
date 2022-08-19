// Default values for a bet
var theBet = "no-bet";
var apiGateway = "https://d5n3ltvz28.execute-api.us-east-1.amazonaws.com/Prod/bet?";

function betted(bettedOn){
    theBet = bettedOn

    let clear = document.getElementsByClassName('bet');
    for (let i=0; i<clear.length; i++)  {clear[i].style.opacity = 0};

    document.getElementById(bettedOn).style.opacity = 1;
}

function submitBet(){
    theBettor = document.getElementById("selection").value;
    betAmount = parseInt(document.getElementById("betAmount").value);
    if(theBet != "no-bet"){
        window.alert(theBettor.charAt(0).toUpperCase() + theBettor.slice(1) + "! You are betting " + betAmount + " blamebucks on " + theBet.charAt(0).toUpperCase() + theBet.slice(1));
        fullBet = theBet+"amount"+betAmount;
        // forming the request path
        var fullApiPath = apiGateway+"action=bets&bettor="+theBettor+"&bet="+fullBet;
    
        // sending the request
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "PUT", fullApiPath);
        xmlHttp.send( null );
        return xmlHttp.responseText;
    }
    else{
        window.alert("Pick A Victim!");
    }
}

function scoreboard(){
    var fullApiPath = apiGateway+"action=scoreboard&bettor=na&bet=na";
    
    // sending the request
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", fullApiPath);
    xmlHttp.onload = function () {
        if(xmlHttp.status == 200) {
            // Checking the returned values
            rows = JSON.parse(xmlHttp.response);

            // Dynamically making the scoreboard table
            var table = "<table id='scoreboard-table'>";
            table += "<tr><th>Name</th><th>Current Bet</th><th>Bet Amount</th><th>Holdings</th><th>Past Bet</th></tr>"
            for(i = 0; i < 7; i++) {
                table += "<tr class='scoreboard-rows'>";
                table += "<td class='scoreboard-cells'>" + rows[i]["name"].charAt(0).toUpperCase() + rows[i]["name"].slice(1) + "</td>";
                table += "<td class='scoreboard-cells'>" + rows[i]["bet"].charAt(0).toUpperCase() + rows[i]["bet"].slice(1) + "</td>";
                table += "<td class='scoreboard-cells'>" + rows[i]["bet-amount"] + " BB</td>";
                table += "<td class='scoreboard-cells'>" + rows[i]["score"] + " BB</td>";
                table += "<td class='scoreboard-cells'>" + rows[i]["past-bet"].charAt(0).toUpperCase() + rows[i]["past-bet"].slice(1) + "</td>";
                table += "</tr>"
            }
            table += "</table><div id='footer'></div>";
            document.getElementById("scoreboard").innerHTML = table;
        }
    };
    xmlHttp.send( null );
}

function selectVictim(){
    let password = prompt("Password");
    let victim = document.getElementById("victim-selection").value;

    var fullApiPath = apiGateway+"action=scores&bettor="+victim+"&bet="+password;

    // sending the request
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "PUT", fullApiPath);
    xmlHttp.send( null );
    return xmlHttp.responseText;
}


function lockBets(){
    let password = prompt("Password");
    fullApiPath = apiGateway+"action=lockBets&bettor=na&bet="+password;

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "PUT", fullApiPath);
    xmlHttp.send( null );
    return xmlHttp.responseText;

}