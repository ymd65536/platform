import json
import boto3


def describe_parameters():
    ssm = boto3.client('ssm')
    name_parameters = []

    response = ssm.describe_parameters()
    if 'Parameters' in response:
        for parameter in response['Parameters']:
            name_parameters.append(parameter['Name'])

    while 'NextToken' in response:
        response = ssm.describe_parameters(NextToken=response['NextToken'])
        if 'Parameters' in response:
            for parameter in response['Parameters']:
                name_parameters.append(parameter['Name'])

    return name_parameters


def put_parameter(name, value, type='String', overwrite=True, description=''):
    ssm = boto3.client('ssm')
    ssm.put_parameter(
        Name=name,
        Value=value,
        Type=type,
        Overwrite=overwrite,
        Description=description
    )


def put_parameters(name_values=[], type='String', overwrite=False, description=''):
    ssm = boto3.client('ssm')
    for name, value in name_values:
        ssm.put_parameter(
            Name=name,
            Value=value,
            Type=type,
            Overwrite=True,
            Description=description
        )


def put_parameter_from_env_list_json(json_file='parameters.json', ssm_param_pass='/dev/'):
    with open(json_file) as f:
        data = json.load(f)
        for environment in data.get('environments'):
            name = environment.get('name')
            value = environment.get('value')
            put_parameter(ssm_param_pass + name, value)
