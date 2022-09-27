import boto3
import os
import json


def lambda_handler(event, context):

    # writes event data from alarm action to Dynamo db

    # read sns notification in json format from event paramter
    # parse fields and select for insertion in DB
    # write in DB
    
    #get table name from env variable

    '''
    Gets the data from the alert and writes it in the database.
    '''
    table_name = str(os.environ['table_name'])

    # Creating a boto3 client for dynamoDB
    client = boto3.client('dynamodb')

    # Parsing string into JSON so values can be extracted easily.
    msg = json.loads(event['Records'][0]['Sns']['Message'])
    
    id_msg = event['Records'][0]['Sns']['MessageId']
    timestamp = event['Records'][0]['Sns']['Timestamp']
    url = msg['Trigger']['Dimensions'][0]['value']
    breached = msg['Trigger']['MetricName']
    response = client.put_item(
        TableName = table_name,
        Item={

            # Putting Items in table
            'id': { 'S' : id_msg},
            'url': { 'S' :  url},
            'breached': { 'S' : breached},
            'Timestamp': { 'S' : timestamp }
        }
    )
