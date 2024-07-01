import subprocess


def destroy():
    #Ask the user for confirmation and execute 'terraform destroy' to tear down infrastructure.
    confirmation = input("Are you sure you want to destroy all the infrastructure? (yes/no): ")
    if confirmation.lower() == 'yes':
        try:
            print("Destroying the infrastructure...")
            # Running Terraform destroy
            result = subprocess.run(['terraform', 'destroy', '-auto-approve'], capture_output=True, text=True, check=True)
            print("Infrastructure destroyed successfully.")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Failed to destroy infrastructure:")
            print(e.stderr)
    else:
        print("Destruction canceled.")