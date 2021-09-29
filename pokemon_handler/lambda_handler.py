import json
from services.sqs_queue import SQSQueue


def lambda_handler(event, context):
    sqs = SQSQueue()
    pokemon_list = []

    for item in event['Records']:
        if (item['eventName'] == 'MODIFY'):
            pokemon_list.append(sqs.send_to_pokeball(item))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"{len(pokemon_list)} pokemon caught",
            "items": pokemon_list
        }),
    }
