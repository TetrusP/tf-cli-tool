import os

def create_aws_provider_config():

    from cli_functions.gen_script.tf_aws_gen import fetch_aws_regions

    print("Here are the available regions you can generate in")

    regions = fetch_aws_regions()

    picked_region = input("Please type the region you would like: ")

    if picked_region not in regions:
        print ("Invalid option")
        return None
    return picked_region

def setup_aws_credentials():
    # Guide user to set up AWS credentials securely using AWS CLI.
    print("Checking for AWS credentials...")
    credentials_path = os.path.expanduser('~/.aws/credentials')
    if not os.path.exists(credentials_path):
        print("AWS credentials not found. Please configure them using the AWS CLI.")
        print("Run 'aws configure' to set up your credentials securely.")
    else:
        print("AWS credentials are configured.")

