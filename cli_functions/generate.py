
from .gen_script.tf_aws_gen import configure_ec2, configure_postgres, configure_provider
from .provider import create_aws_provider_config, setup_aws_credentials


def generate():
    print("Generate will create your Terraform File based on the options you choose")
    print("Choose Compute Platform:")
    print("aws | azure | gcp")
    compute_platform = input("Enter your desired platform: ")

    ##If user chooses aws, execute aws tf generator
    if compute_platform == 'aws':

        print("Here are the available regions you can generate in")

        setup_aws_credentials()
        picked_region = create_aws_provider_config()
        if picked_region:
            print(f"Configured for region: {picked_region}")
        else:
            print("No valid region picked")

        configure_provider(picked_region)

        ec2_wanted = input("Do you want to configure an EC2 instance? (yes/no): ").strip().lower() == 'yes'
        postgres_wanted = input("Do you want to configure a PostgreSQL database? (yes/no): ").strip().lower() == 'yes'

        if ec2_wanted:
            configure_ec2(picked_region)
            
        if postgres_wanted:
            configure_postgres(picked_region)

        if not ec2_wanted and not postgres_wanted:
            print("No configurations selected for AWS.")

    else:
        print ("Sorry, Azure and GCP functionality is coming soon")
