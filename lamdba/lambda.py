import boto3
import json

# Globally used variables
office_roulette = 'arn:aws:secretsmanager:us-east-1:692775622467:secret:office-roulette-mTGzMC'
table = boto3.resource('dynamodb').Table("roulette-scores")


def get_all_scores():
    """
    This function scans the whole AWS DynamoDB table and returns everything.
    """
    table_bettors = table.scan()['Items']

    for bettor in table_bettors:
        bettor["score"] = int(bettor["score"])

    return table_bettors


def validate_bet(bettor, bet):
    """
    This function validates if an allowed user is making the bets
    """
    table_bettors = table.scan()['Items']
    bettor_name = [bettor['name'] for bettor in table_bettors]
    bet_amounts = [1, 5, 10, 25]

    print(bettor, bet)
    if bettor in bettor_name and bet[0] in bettor_name and int(bet[1]) in bet_amounts:
        return True
    else:
        return False


def match_password(entered):
    """ This function authenticates the admin before the victim can be picked """

    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=office_roulette)
    password = json.loads(response['SecretString'])['password']

    if entered == password:
        print("Access Granted")
        return True
    else:
        print("Access Denied")
        return False


def store_bet(bettor, bet):
    """ This function stores the players' updated bets in AWS DynamoDB """
    print(bet)
    response = table.update_item(
        Key={'name': bettor},
        AttributeUpdates={
            "bet": {"Value": bet[0]},
            "bet-amount": {"Value": int(bet[1])}}
    )


def pick_victim(victim):
    """
    After the admin enters the victim, this function compares the victim with the bets and increments
    the scores by one and updates them in the database. Then it calls the clear_votes function
    """
    data = get_all_scores()

    for entry in data:
        if entry['bet'] == victim:
            response = table.update_item(
                Key={'name': entry['name']},
                AttributeUpdates={"score": {"Value": entry['score'] + entry['bet-amount']}}
            )
        else:
            response = table.update_item(
                Key={'name': entry['name']},
                AttributeUpdates={"score": {"Value": entry['score'] - entry['bet-amount']}}
            )

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


def lambda_handler(event, context):
    """
    This function handles which functions AWS Lambda will run based on the parameters of the request
    """
    action = event["queryStringParameters"]["action"]
    bettor = event["queryStringParameters"]["bettor"]
    bet = event["queryStringParameters"]["bet"]

    responseSent = {}
    responseSent['statusCode'] = 200
    responseSent['headers'] = {}
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
            pick_victim(bettor)
            responseSent['body'] = "Scores Updated!"
        else:
            responseSent['body'] = "Wrong Password!"

        return responseSent

#     elif action == "scoreboard":
#         scoreboard = get_all_scores()
#         responseSent['body'] = json.dumps(scoreboard)
#         return responseSent

# if __name__ == "__main__":
#     action = "bets"
#     bettor = "alif"
#     bet = "jaden+1"

#     store_bet(bettor, bet.split("+"))