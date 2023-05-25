# Vault to AWS Secrets Manager Migration Tool

This tool is a Python script that automates the process of fetching secrets from HashiCorp's Vault and uploading them to AWS Secrets Manager. It was created to simplify the process of migrating secrets between these two systems. 

## Prerequisites

- Python 3.6 or later.
- The `hvac` Python library for interacting with Vault.
- The `boto3` Python library for interacting with AWS.
- Access to a Vault server and a valid Vault token.
- AWS credentials that have permission to create secrets in AWS Secrets Manager.

## How to Use

1. Clone this repository to your local machine.
2. Install the necessary Python libraries, if they're not already installed. You can do this with pip:

    ```
    pip install hvac boto3
    ```

3. Ensure that the `VAULT_ADDR` and `VAULT_TOKEN` environment variables are set in your shell. These should be the address of your Vault server and your Vault token, respectively.

4. Ensure that your AWS credentials are correctly configured in your environment. You can do this by setting the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` environment variables, or by configuring the AWS credentials file.

5. Run the script, passing the necessary arguments. The script takes the following arguments:

    - `service`: The name of the service for which to retrieve secrets from Vault.
    - `--env`: (Optional) The name of the environment for which to retrieve secrets. If not provided, secrets will be retrieved for the service only.
    - `sm_store_path`: The path in AWS Secrets Manager where the secrets will be stored.

    Here's an example of how to run the script:

    ```shell
    python fetch_and_upload_secrets.py my_service /my/sm/path
    ```

    In this example, replace `my_service` with the name of your service and `/my/sm/path` with your desired path in AWS Secrets Manager.

    If you want to specify an environment, you can do so with the `--env` option:

    ```shell
    python fetch_and_upload_secrets.py my_service --env my_environment /my/sm/path
    ```

    Again, replace `my_service`, `my_environment`, and `/my/sm/path` with your actual values.

Please note: This script will fail if a secret with the given name already exists in AWS Secrets Manager. If you need to overwrite existing secrets, you will need to modify the script to use the `update_secret` method or handle exceptions that arise from trying to create a duplicate secret.
