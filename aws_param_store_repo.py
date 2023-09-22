import boto3
from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

ssm_client = boto3.client("ssm",
    aws_access_key_id=config["AWS_ACCESS_KEY"], 
    aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"], 
    region_name="us-east-1"
    )

TEST_PRODUCT_NAME = "/test-product"

def set_parameter(parameter_name, parameter_value):
    try:
        ssm_client.put_parameter(
            Name=f"/test-product/{parameter_name}",
            Value=parameter_value,
            Type="String",  # Type of the parameter value
            Overwrite=True
        )
        return True
    except Exception as e:
        print(f"Error creating parameter: {str(e)}")
        return False
    
def get_parameter(parameter_name):
    try:
        PARAM_SET = ssm_client.get_parameter(
            Name=f"/test-product/{parameter_name}",
            WithDecryption=True  # Decrypt the secret value if it's encrypted
        )
        return PARAM_SET['Parameter']['Value']
    except Exception as e:
        print(f"Error getting parameter: {str(e)}")
        return False
    
def get_all_parameters(parameter_path):
    try:
        paginator = ssm_client.get_paginator('get_parameters_by_path')
        response_iterator = paginator.paginate(Path=parameter_path)

        parameters=[]
        for page in response_iterator:
            for entry in page['Parameters']:
                parameters.append(entry)

        parameter_key_pairs = {entry['Name']:entry['Value'] for entry in parameters}
        return parameter_key_pairs
    except Exception as e:
        print(f"Error getting parameters from path: {str(e)}")
        return False

    
def delete_parameter(parameter_name):
    try:
        ssm_client.delete_parameter(
            Name=f"/test-product/{parameter_name}"
        )
        return True
    except Exception as e:
        print(f"Error deleting parameter: {str(e)}")
        return False


    
# Example usage:

set_parameter("test-parameter", "test-parameter-value")
set_parameter("test-parameter2", "test-parameter-value2")
param = get_parameter("test-parameter2")
params = get_all_parameters("/test-product")
print("PARAM")
print(param)
print("PARAMS")
print(params)
delete_parameter("test-parameter")
delete_parameter("test-parameter2")
