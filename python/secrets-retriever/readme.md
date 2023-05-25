# Vault to AWS Secrets Manager Migration Tool

This tool is a Python script that automates the process of fetching secrets from HashiCorp's Vault and uploading them to AWS Secrets Manager. It was created to simplify the process of migrating secrets between these two systems. 

## Prerequisites

- Python 3.6 or later.
- The `hvac` Python library for interacting with Vault.
- The `boto3` Python library for interacting with AWS.
- Access to a Vault server and a valid Vault token.
- AWS credentials that have permission to create secrets in AWS Secrets Manager.

## Input parameters
- `service`: The service for which to retrieve secrets. This is a required parameter.
- `--env`: The environment for which to retrieve secrets. This is optional. If not provided, the script will retrieve secrets for the service irrespective of the environment.
- `--sm_store_path`: AWS Secret Manager store path to upload secrets. This is optional. If provided, the script will upload the fetched secrets from Vault to the specified path in AWS Secrets Manager.
- `--aws_profile`: AWS profile to use for uploading to Secrets Manager. This is optional. If not provided, the script will use the 'default' profile.

## AWS Configuration
If you plan to upload secrets to AWS Secrets Manager, you need to configure your AWS credentials by using the AWS CLI. The script uses boto3 to interact with AWS.

Setup can be found at: {WIKI LINK}

You can then use the profiles by passing the profile name to the `--aws_profile` parameter when running the script.
    
## How to Use

1. Clone this repository to your local machine.
2. Install the necessary Python libraries, if they're not already installed. You can do this with pip:

    ```
    pip install hvac boto3
    ```

3. Ensure that the `VAULT_ADDR` and `VAULT_TOKEN` environment variables are set in your shell. These should be the address of your Vault server and your Vault token, respectively.

4. Ensure that your AWS credentials are correctly configured in your environment. You can do this by setting the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` environment variables, or by configuring the AWS credentials file.

5. Run the script, passing the necessary arguments:

    Here's an example of how to run the script:
    
    ```console
    python fetch_and_upload_secrets.py user-service --sm_store_path user-service/dev/secret --aws_profile development
    ```

    In this example, replace `user-service` with the name of your service and `user-service/dev/secret` with your desired path in AWS Secrets Manager.

    If you want to specify an environment, you can do so with the `--env` option:

    ```console
      python fetch_and_upload_secrets.py user-service --env dev --sm_store_path /user-service/dev/secret --aws_profile development
     ```

    Again, replace `user-service`, `dev`, `user-service/dev/secret`, and `development` with your actual values.

Please note: This script will fail if a secret with the given name already exists in AWS Secrets Manager. If you need to overwrite existing secrets, you will need to modify the script to use the `update_secret` method or handle exceptions that arise from trying to create a duplicate secret.
