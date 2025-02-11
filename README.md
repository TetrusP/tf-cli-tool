# tf-cli-tool

This CLI tool is designed to ask a user if they want to generate configs for terraform deployments and then apply those configs. Currently it only works with an AWS cloud provider however it can expanded upon to work with GCP and Azure.

For the time being it can only generate configs for EC2 and RDS/postgresql.

The CLI tool assumes the user is starting from a clean slate and configures new resources for the following

    VPC subnets, routing, etc.

The preconfigured EC2 and RDS templates can be edited in the tf_aws_gen.py script under the write_terraform_db_config and write_terraform_config functions.

Tool Requirements:

python
terraform

Update terraform directory in plan.py

    # Define the path to your Terraform configuration directory
    terraform_dir = '<Input Path here>'


Tool improvements:

The tool can be further improved to manage the state file in a more secure fashion (for the sake of a proof of concept I've kept the state file to be managed locally). The tool can fetch all resource options dynamically instead of providing preconfigured static options. The tool can also be improved to include Terraform output and variables files to simplify the config generation functions and reusability. 

Additionally, the tool can be further streamlined by adding a force feature which reduces the number of prompts the user will need to input. This will enable further automation if a user wants to incorporate this into their infrastructure workflows. The tool can also be configured to ask the user where they want their working terraform directory to be instead of having to manually add the absolute path in the plan.py function. A generic .env file would be beneficial


Tool instructions:

The CLI has 4 options:

    apply, generate, destroy, plan

To generate Terraform configs run: 

    %python3 main.py generate ##And follow the prompts

To Plan a Terraform config run:

    %python3 main.py plan ##And follow the prompts

To Apply a Terraform config run:

    %python3 main.py apply ##And follow the prompts

To Destroy the created resources run:

    %python3 main.py destroy ##And follow the prompts

