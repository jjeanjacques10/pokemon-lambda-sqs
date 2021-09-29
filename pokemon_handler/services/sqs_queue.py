import boto3
import json
import os

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
QUEUE_URL = os.environ.get('POKEMON_QUEUE')
QUEUE_URL_DLQ = os.environ.get('POKEMON_QUEUE_DLQ')


class SQSQueue:

    def __init__(self):
        self.client = boto3.client(
            'sqs',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='us-east-1')
        self.queue_url = QUEUE_URL
        self._config_sqs_client()

    def _config_sqs_client(self):
        redrive_policy = {
            'deadLetterTargetArn': QUEUE_URL_DLQ,
            'maxReceiveCount': '10'
        }
        self.client.set_queue_attributes(
            QueueUrl=self.queue_url,
            Attributes={
                'RedrivePolicy': json.dumps(redrive_policy)
            }
        )

    def send_to_pokeball(self, item: object) -> object:
        pokemon = {
            'id': item['dynamodb']['NewImage']['id']['N'],
            'name': item['dynamodb']['NewImage']['name']['S']
        }

        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageAttributes={
                'Title': {
                    'DataType': 'String',
                    'StringValue': 'Pokemon Received'
                }
            },
            MessageBody=(
                str(pokemon)
            )
        )

        print(f"MessageId: {pokemon['name']}-{response['MessageId']}")
        return pokemon
