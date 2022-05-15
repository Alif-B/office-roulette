import boto3
import json

# Globally used variables
office_roulette = 'arn:aws:secretsmanager:us-east-1:692775622467:secret:office-roulette-mTGzMC'
table = boto3.resource('dynamodb').Table("roulette-scores")


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
    response = table.update_item(
        Key={'name': bettor},
        AttributeUpdates={"bet": {"Value": bet}}
    )


def pick_victim(victim):
    """
    After the admin enters the victim, this function compares the victim with the bets and increments
    the scores by one and updates them in the database. Then it calls the clear_votes function
    """
    response = table.scan()
    data = response['Items']

    for entry in data:
        if entry['bet'] == victim:
            response = table.update_item(
                Key={'name': entry['name']},
                AttributeUpdates={"score": {"Value": entry['score'] + 1}}
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
               "bet": {"Value": "no-bet"}
            }
        )


def lambda_handler(action, bettor, bet):
    """
    This function handles which functions AWS Lambda will run based on the parameters of the request
    """
    if action == "bets":
        store_bet(bettor, bet)
    elif action == "scores":
        if match_password(bet):
            pick_victim(bettor)

    