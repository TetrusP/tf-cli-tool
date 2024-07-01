import re
import subprocess
import json

def fetch_aws_regions():
    #Fetch and display available AWS regions using the AWS CLI.
    try:
        # Run AWS CLI command to list regions
        result = subprocess.run(['aws', 'ec2', 'describe-regions', '--output', 'json'], capture_output=True, text=True, check=True)
        
        # Parse JSON output to extract regions
        regions = json.loads(result.stdout)['Regions']
        available_regions = [region['RegionName'] for region in regions]

        print("Available AWS Regions:")
        for region in available_regions:
            print(region)

        return available_regions

    except subprocess.CalledProcessError as e:
        print("Failed to fetch AWS regions:")
        print(e.stderr)
        return []

def fetch_amis(region):
    #Fetch a list of available AMIs for a specific instance type in a region and return a structured dictionary.
    try:
        result = subprocess.run([
            'aws', 'ec2', 'describe-images',
            '--region', region,
            '--filters', 'Name=description,Values=*Amazon Linux 2 AMI*',
            '--query', 'Images[*].[ImageId,Description]',
            '--output', 'json'
        ], capture_output=True, text=True, check=True)

        amis_list = json.loads(result.stdout)
        amis = {str(index + 1): {'id': ami[0], 'description': ami[1]} for index, ami in enumerate(amis_list)}
        return amis

    except subprocess.CalledProcessError as e:
        print("Failed to fetch AMIs:")
        print(e.stderr)
        return None

def is_valid_name(name):
    #Check if the provided name is valid for Terraform resources.
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_-]*$'
    return re.match(pattern, name) is not None

def write_terraform_configuration(ec2_config):
    #Write the EC2 Terraform configuration to a file, dynamically including VPC and subnet setup.
    with open('ec2_vpc_setup.tf', 'w') as f:
        f.write(f"""

# Adjust as necessary
resource "aws_vpc" "my_vpc" {{
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {{
    Name = "MyVPC"
  }}
}}

# Adjust as necessary
resource "aws_subnet" "my_subnet" {{
  vpc_id     = aws_vpc.my_vpc.id
  cidr_block = "{ec2_config['subnet_cidr']}"
  map_public_ip_on_launch = true
  availability_zone = "{ec2_config['picked_region']}a"

  tags = {{
    Name = "MySubnet"  # Adjust as necessary
  }}
}}

# Adjust as necessary
resource "aws_internet_gateway" "my_igw" {{
  vpc_id = aws_vpc.my_vpc.id
}}

# Adjust as necessary
resource "aws_route_table" "my_route_table" {{
  vpc_id = aws_vpc.my_vpc.id
  route {{
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.my_igw.id
  }}
}}

# Adjust as necessary
resource "aws_route_table_association" "a" {{
  subnet_id      = aws_subnet.my_subnet.id
  route_table_id = aws_route_table.my_route_table.id
}}

# Adjust as necessary
resource "aws_instance" "my_instance" {{
  ami           = "{ec2_config['ami']}"
  instance_type = "{ec2_config['instance_type']}"
  subnet_id     = aws_subnet.my_subnet.id
  

  root_block_device {{
    volume_type = "{ec2_config['disk_type']}"
    volume_size = {ec2_config['disk_size']}
  }}

  tags = {{
    Name = "{ec2_config['tags']['Name']}"
  }}
}}
""")
    print("Terraform configuration for EC2 and networking has been generated.")

def write_terraform_db_config(db_config):
    #Generate Terraform configuration for PostgreSQL within a shared or new VPC.
    with open('postgres_setup.tf', 'w') as f:
        f.write(f"""

# Adjust as necessary
resource "aws_vpc" "my_vpc_db" {{
  cidr_block = "10.1.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {{
    Name = "MyVPCdb"
  }}
}}
        
# Adjust as necessary
# Creating two subnets in different AZs
resource "aws_subnet" "postgres_subnet_1" {{
  vpc_id            = aws_vpc.my_vpc_db.id
  cidr_block        = "{db_config['subnet_cidr_1']}"
  availability_zone = "{db_config['picked_region']}a"

  tags = {{
    Name = "PostgreSQL Subnet 1"
  }}
}}

# Adjust as necessary
resource "aws_subnet" "postgres_subnet_2" {{
  vpc_id            = aws_vpc.my_vpc_db.id
  cidr_block        = "{db_config['subnet_cidr_2']}"
  availability_zone = "{db_config['picked_region']}b"

  tags = {{
    Name = "PostgreSQL Subnet 2"
  }}
}}

# Adjust as necessary
# DB Subnet Group using the above two subnets
resource "aws_db_subnet_group" "my_db_subnet_group" {{
  name       = "{db_config['name']}-subnet-group"
  subnet_ids = [aws_subnet.postgres_subnet_1.id, aws_subnet.postgres_subnet_2.id]

  tags = {{
    Name = "My DB Subnet Group"
  }}
}}

# Adjust as necessary
# RDS instance
resource "aws_db_instance" "my_postgres" {{
  identifier = "{db_config['name']}"
  instance_class = "{db_config['instance_class']}"
  engine = "postgres"
  username = "{db_config['username']}"
  password = "{db_config['password']}"
  db_subnet_group_name = aws_db_subnet_group.my_db_subnet_group.name
  allocated_storage = {db_config['allocated_storage']}
  skip_final_snapshot = true

  tags = {{
    Name = "{db_config['tags']['Name']}"
  }}
}}
""")
    print("Terraform configuration for PostgreSQL has been generated.")

def configure_provider(picked_region):
    #Generate the provider configuration for Terraform.

    with open('provider.tf', 'w') as f:
        f.write(f"""
provider "aws" {{
  region = "{picked_region}"
  # Optionally, specify profile if necessary
  # profile = "default"
}}

variable "region" {{
  description = "The AWS region to create resources in."
  default = "{picked_region}"
}}
""")
    print("Provider configuration has been written to provider.tf")

def configure_ec2(picked_region):
    # VM size options

    vm_sizes = {
        '1': {'display': 't2.micro', 'description': '1 vCPU, 1 GiB RAM'},
        '2': {'display': 't2.small', 'description': '1 vCPU, 2 GiB RAM'},
        '3': {'display': 't3.medium', 'description': '2 vCPU, 4 GiB RAM'}
    }

    # Subnet options with CIDR blocks
    print("Enter the CIDR block for your subnet (e.g., '10.0.1.0/24'):")
    subnet_cidr = input()

    # Select the VM size options
    print("Select the VM size:")
    for key, value in vm_sizes.items():
        print(f"{key}: {value['display']} ({value['description']})")
    size_choice = input("Choose a size (1, 2, 3): ")
    if size_choice not in vm_sizes:
        print("Invalid choice, please run the command again.")
        return
    instance_type = vm_sizes[size_choice]['display']

    # Select the AMI options for that region
    print("Available AMIs for region:" + picked_region)
    amis = fetch_amis(picked_region)
    if not amis:
        print("No valid AMIs found, cannot proceed with EC2 configuration.")
        return

    print("Choose the AMI ID:")
    for key, value in amis.items():
        print(f"{key}: {value['id']} - {value['description']}")
    ami_choice = input("Choose an AMI (1, 2, 3, etc): ")
    if ami_choice not in amis:
        print("Invalid choice, please run the command again.")
        return
    ami_id = amis[ami_choice]['id']

    # Select Disk type for VM
    print("Choose the type of storage disk:")
    print("1: HDD (Hard Disk Drive)")
    print("2: SSD (Solid State Drive)")
    disk_type_choice = input("Choose a disk type (1, 2): ")
    disk_type = "standard" if disk_type_choice == '1' else "gp2"
    disk_size = input("Enter the disk size in GB: ")

    # EC2 instance naming and tag
    ec2_name = input("Enter a name for your EC2 instance: ")
    ec2_tag_name = input("Enter a tag name for your EC2 instance: ")

    # Prepare EC2 configuration dictionary
    ec2_config = {
        "picked_region": picked_region,
        "name": ec2_name,
        "ami": ami_id,
        "instance_type": instance_type,
        "subnet_cidr": subnet_cidr,
        "disk_type": disk_type,
        "disk_size": disk_size,
        "tags": {"Name": ec2_tag_name}
    }

    write_terraform_configuration(ec2_config)

def configure_postgres(picked_region):
    print("Configuring PostgreSQL database...")

    # Type out the CIDR block for your postgres DB
    print("Enter your first CIDR block for your DB subnet (e.g., '10.1.0.0/24'):")
    subnet_cidr_1 = input()

    # Type out Second CIDR block for postgres DB
    print("Enter you're second CIDR block (eg 10.1.1.0/24): ")
    subnet_cidr_2 = input()

    # Instance class options, similar to EC2 but specific to RDS
    db_instance_classes = {
        '1': 'db.t3.micro',
        '2': 'db.t3.small',
        '3': 'db.t3.medium'
    }
    
    # Select the postgresql instance class option
    print("Select the PostgreSQL instance class:")
    for key, value in db_instance_classes.items():
        print(f"{key}: {value}")
    db_class_choice = input("Choose a DB instance class (1-3): ")
    if db_class_choice not in db_instance_classes:
        print("Invalid choice, please run the command again.")
        return
    instance_class = db_instance_classes[db_class_choice]

    # Database credentials and storage
    db_name = input("Enter a name for your PostgreSQL instance: ")
    allocated_storage = input("Enter the allocated storage in GB: ")
    db_username = input("Enter the DB username: ")
    db_password = input("Enter the DB password (minimum of 8 chars): ")
    db_tag_name = input("Enter a tag name for your PostgreSQL instance: ")

    postgres_config = {
        "picked_region": picked_region,
        "name": db_name,
        "instance_class": instance_class,
        "allocated_storage": allocated_storage,
        "username": db_username,
        "password": db_password,
        "subnet_cidr_1": subnet_cidr_1,
        "subnet_cidr_2": subnet_cidr_2,
        "tags": {"Name": db_tag_name}
    }

    write_terraform_db_config(postgres_config)