import os
import json
import hvac
import argparse

def fetch_secrets(vault_addr, vault_token, service, env):
    client = hvac.Client(url=vault_addr, token=vault_token)

    if not client.is_authenticated():
        raise Exception('Vault authentication failed.')

    secret_path = f'{service}/{env}'
    list_response = client.secrets.kv.v1.list_secrets(path=secret_path, mount_point='secret')

    secrets = {}
    for secret in list_response['data']['keys']:
        read_response = client.secrets.kv.v1.read_secret(path=f"{secret_path}/{secret}", mount_point='secret')
        secrets[secret] = read_response['data']

    return secrets

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('service', type=str, help='The service for which to retrieve secrets.')
    parser.add_argument('env', type=str, help='The environment for which to retrieve secrets.')
    args = parser.parse_args()

    vault_addr = os.environ['VAULT_ADDR']
    vault_token = os.environ['VAULT_TOKEN']

    secrets = fetch_secrets(vault_addr, vault_token, args.service, args.env)

    print(json.dumps(secrets, indent=4))
