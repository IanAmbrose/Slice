import os
import json
import hvac
import boto3
import argparse

def fetch_secrets(vault_addr, vault_token, service, env=None):
    client = hvac.Client(url=vault_addr, token=vault_token)

    if not client.is_authenticated():
        raise Exception('Vault authentication failed.')

    secret_path = f'{service}/{env}' if env else f'{service}'
    list_response = client.secrets.kv.v1.list_secrets(path=secret_path, mount_point='secret')

    secrets = {}
    for secret in list_response['data']['keys']:
        read_response = client.secrets.kv.v1.read_secret(path=f"{secret_path}/{secret}", mount_point='secret')
        secrets[secret] = read_response['data']['value']  # Assuming the secret is stored under 'value' key

    return secrets

def upload_to_sm(secrets, sm_store_path, aws_profile='default'):
    session = boto3.Session(profile_name=aws_profile)
    sm_client = session.client('secretsmanager')

    # Convert secrets to JSON
    secrets_json = json.dumps(secrets)

    # Create a single secret in Secrets Manager
    sm_client.create_secret(
        Name=f'{sm_store_path}',
        SecretString=secrets_json
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('service', type=str, help='The service for which to retrieve secrets.')
    parser.add_argument('--env', type=str, help='The environment for which to retrieve secrets.')
    parser.add_argument('--sm_store_path', type=str, help='The AWS Secrets Manager store path.')
    parser.add_argument('--aws_profile', type=str, default='default', help='The AWS profile to use.')
    args = parser.parse_args()

    vault_addr = os.environ['VAULT_ADDR']
    vault_token = os.environ['VAULT_TOKEN']

    secrets = fetch_secrets(vault_addr, vault_token, args.service, args.env)

    if args.sm_store_path:
        upload_to_sm(secrets, args.sm_store_path, args.aws_profile)
