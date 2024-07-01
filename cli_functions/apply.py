import subprocess
from .plan import plan

def apply():

    print("This is what your configuration will apply")
    print("==========================================")
    plan()

    # Run 'terraform apply' to make changes to infrastructure.
    user_input = input("Do you want to apply the changes? Type 'yes' to confirm: ")
    if user_input.lower() == 'yes':
        try:
            # Running Terraform apply
            print("Applying Terraform changes...")
            result = subprocess.run(['terraform', 'apply', '-auto-approve'], capture_output=True, text=True, check=True)
            print("Terraform apply completed successfully.")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Failed to apply Terraform changes:")
            print(e.stderr)
    else:
        print("Terraform apply was not confirmed and has been aborted.")