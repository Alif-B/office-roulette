import boto3
import json

client = boto3.client('secretsmanager')
office_roulette = 'arn:aws:secretsmanager:us-east-1:692775622467:secret:office-roulette-mTGzMC'
office_roulette_bets = "arn:aws:secretsmanager:us-east-1:692775622467:secret:office-roulette-bets-PsG6od"


def match_password(entered):
    password = client.get_secret_value(SecretId=office_roulette)

    if entered == password:
        return True
    else:
        return False


def store_bet(bettor, bet):
    secret = client.get_secret_value(SecretId=office_roulette_bets)
    secret_dict = json.loads(secret['SecretString'])
    secret_dict[bettor] = bet

    response = client.update_secret(
        SecretId=office_roulette_bets,
        SecretString=json.dumps(secret_dict)
    )


def pick_victim(victim):
    bets = client.get_secret_value(SecretId=office_roulette_bets)
    bets_dict = json.loads(bets['SecretString'])

    winners_list = []

    for bettor in bets_dict:
        if bets_dict[bettor] == victim:
            winners_list.append(bettor)

    return winners_list


def update_scores(winners):
    scores = client.get_secret_value(SecretId=office_roulette)
    scores_dict = json.loads(scores['SecretString'])

    for winner in winners:
        scores_dict[winner] += 1

    response = client.update_secret(
        SecretId=office_roulette,
        SecretString=json.dumps(scores_dict)
    )

    clear_votes()


def clear_votes():
    response = client.update_secret(
        SecretId=office_roulette_bets,
        SecretString='{"jaden":"no-bet","will":"no-bet","benson":"no-bet","alif":"no-bet","jordan":"no-bet",'
                     '"clem":"no-bet","jesse":"no-bet"}'
    )


def lambda_handler(action, bettor, bet):
    if action == "bets":
        store_bet(bettor, bet)
    elif action == "scores":
        winners = pick_victim(bettor)
        update_scores(winners)

    