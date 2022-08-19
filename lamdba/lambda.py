import boto3
import json

# Globally used variables
office_roulette = 'arn:aws:secretsmanager:us-east-1:692775622467:secret:office-roulette-mTGzMC'
table = boto3.resource('dynamodb').Table("roulette-scores")
extra_table = boto3.resource('dynamodb').Table("roulette-extras")


def get_all_scores(method):
    """
    This function scans the whole AWS DynamoDB table and returns everything.
    """
    table_bettors = table.scan()['Items']

    if method == "victim":
        for bettor in table_bettors:
            bettor["score"] = int(bettor["score"])
    elif method == "scoreboard":
        for bettor in table_bettors:
            bettor["score"] = str(bettor["score"])
            bettor["bet-amount"] = str(bettor["bet-amount"])

    return table_bettors


def validate_bet(bettor, bet):
    """
    This function validates if an allowed user is making the bets
    """
    table_bettors = table.scan()['Items']
    bettor_name = [bettor['name'] for bettor in table_bettors]
    bet_amounts = [0, 1, 5, 10, 25]

    print(bettor, bet)
    if bettor in bettor_name and bet[0] in bettor_name and int(bet[1]) in bet_amounts:
        return True
    else:
        return False


def match_password(entered):
    """ This function authenticates the admin before the victim can be picked """
    password = extra_table.get_item(
        Key={"variable": "password"},
        AttributesToGet=['answer']
    )["Item"]["answer"]

    if entered == password:
        print("Access Granted")
        return True
    else:
        print("Access Denied")
        return False


def store_bet(bettor, bet):
    """ This function stores the players' updated bets in AWS DynamoDB """
    print(bet)
    print("here")

    locked = extra_table.get_item(
        Key={"variable": "locked"},
        AttributesToGet=['answer']
    )["Item"]["answer"]

    # for extra in extra_table.scan()['Items']:
    #     if extra['variable'] == "locked":
    #         locked = extra["answer"]

    print(locked)
    if locked == "False":
        response = table.update_item(
            Key={'name': bettor},
            AttributeUpdates={
                "bet": {"Value": bet[0]},
                "bet-amount": {"Value": int(bet[1])}}
        )


def lock_bets(locked):
    """
    This function changes the status of locked mode on dynamodb to true.
    Making the webapp not accept anymore bets until a victim has been picked
    """
    response = extra_table.update_item(
        Key={"variable": "locked"},
        AttributeUpdates={ 
            "answer": { "Value": locked } }
    )


def pick_victim(victim):
    """
    After the admin enters the victim, this function compares the victim with the bets and increments
    the scores by one and updates them in the database. Then it calls the clear_votes function
    """
    data = get_all_scores("victim")

    for entry in data:
        if entry['bet'] == victim:
            response = table.update_item(
                Key={'name': entry['name']},
                AttributeUpdates={"score": {"Value": entry['score'] + (7*entry['bet-amount'])}}
            )
        else:
            response = table.update_item(
                Key={'name': entry['name']},
                AttributeUpdates={"score": {"Value": entry['score'] - entry['bet-amount']}}
            )

    lock_bets("False")
    clear_votes(data)


def clear_votes(data):
    """
    This function moves all the current bets to `past-bets` column so users can see what they bet on.
    And then it updates all the bets with `no-bets` placeholders until users bet again
    """
    for entry in data:
        response = table.update_item(
            Key={'name': entry['name']},
            AttributeUpdates={
               "past-bet": {"Value": entry['bet']},
               "bet": {"Value": "no-bet"},
               "bet-amount": {"Value": 0}
            }
        )


# def main(event):
def lambda_handler(event, context):
    """
    This function handles which functions AWS Lambda will run based on the parameters of the request
    """
    action = event["queryStringParameters"]["action"]
    bettor = event["queryStringParameters"]["bettor"]
    bet = event["queryStringParameters"]["bet"]

    responseSent = {}
    responseSent['statusCode'] = 200
    responseSent['headers'] = {"Access-Control-Allow-Origin" : "*"}
    responseSent['headers']['Content-Type'] = "application/json"

    if action == "bets":
        bet = bet.split("amount")
        if validate_bet(bettor, bet):
            store_bet(bettor, bet)
            responseSent['body'] = f"{bettor} bet {bet[1]} blamebucks on {bet[0]}"
        else:
            responseSent['body'] = "Request did not pass validation!"
        return responseSent

    elif action == "scores":
        if match_password(bet):
            pick_victim(bettor.lower())
            responseSent['body'] = "Scores Updated!"
        else:
            responseSent['body'] = "Wrong Password!"

        return responseSent

    elif action == "scoreboard":
        scoreboard = get_all_scores("scoreboard")
        responseSent['body'] = json.dumps(scoreboard)
        return responseSent

    elif action == "lockBets":
        if match_password(bet):
            scoreboard = lock_bets("True")
            responseSent['body'] = "All bets have been locked, No more betting till next round"
        else:
            responseSent['body'] = "Wrong Password!"
        
        return responseSent

# if __name__ == "__main__":

    # event = {
    #     "queryStringParameters" : {
    #         "action": "bets",
    #         "bettor": "alif",
    #         "bet" : "rossamount10"
    #     }
    # }

    # event = {
    #     "queryStringParameters" : {
    #         "action": "lockBets",
    #         "bettor": "alif",
    #         "bet" : "peeOnFriends"
    #     }
    # }

    # event = {
    #     "queryStringParameters" : {
    #         "action": "scores",
    #         "bettor": "alif",
    #         "bet" : "peeOnFriends"
    #     }
    # }

    # main(event)