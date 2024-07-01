## Main entry for CLI tool

##python library parser for cli arguments

## import functions
from cli_functions.apply import apply
from cli_functions.destroy import destroy
from cli_functions.generate import generate
from cli_functions.plan import plan

##Main Function
def main():
    while True:
        # Display the menu options
        print("\nCLI for generating AWS Terraform Files and Applying them")
        print("1: Generate Terraform Config")
        print("2: Apply Terraform Config")
        print("3: Plan Terraform Deployment")
        print("4: Destroy Terraform Resources")
        print("5: Exit")

        # Get user choice
        choice = input("Please choose an option (1-5): ")

        # Execute based on choice
        if choice == '1':
            generate()
        elif choice == '2':
            apply()
        elif choice == '3':
            plan()
        elif choice == '4':
            destroy()
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid option, please try again.")

main() 
        
