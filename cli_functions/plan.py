
import subprocess
import os

def plan():
    # Define the path to your Terraform configuration directory
    terraform_dir = '<Input Path here>'

    from .generate import generate

    # Check if Terraform configuration files exist in the directory
    if not os.listdir(terraform_dir):
        print("No Terraform configuration files found in the directory.")
        user_decision = input("Would you like to generate configuration now? (yes/no): ")
        if user_decision.strip().lower() == 'yes':
            generate()  # Call generate function to create Terraform configuration files
        else:
            print("Cannot proceed without Terraform configuration files.")
            return
    
    print("Running 'terraform plan' to show changes...")
    try:
        # Ensure Terraform is initialized
        subprocess.run(['terraform', 'init'], check=True, cwd=terraform_dir)

        # Execute the Terraform plan command
        result = subprocess.run(['terraform', 'plan'], check=True, cwd=terraform_dir, capture_output=True, text=True)

        # Print the output from the Terraform plan
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess
        print("An error occurred while running Terraform plan:")
        print(e.output)
