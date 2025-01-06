# Lambda Invoke

import json
import boto3

if __name__ == '__main__':
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName='YamadaLambda',
        InvocationType='RequestResponse',
        Payload=json.dumps({'key1': 'value1', 'key2': 'value2'})
    )
    print(response['Payload'].read().decode('utf-8'))
