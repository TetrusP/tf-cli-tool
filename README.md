# tf-cli-tool

This CLI tool is designed to ask a user if they want to generate configs for terraform deployments and then apply those configs. Currently it only works with an AWS cloud provider however it can expanded upon to work with GCP and Azure.

For the time being it can only generate configs for EC2 and RDS/postgresql.

The CLI tool assumes the user is starting from a clean slate and configures new resources for the following

    VPC subnets, routing, etc.

Tool Requirements:

python
terraform


Tool improvements:

The tool can be further improved to manage the state file in a more secure fashion (for the sake of a proof of concept I've kept the state file to be managed locally). The tool can fetch all resource options dynamically instead of providing preconfigured static options. The tool can also be improved to include Terraform output and variables files to simplify the config generation functions and reusability.

Tool instructions:

run: 

%python3 main.py