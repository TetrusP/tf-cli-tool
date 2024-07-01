## Main entry for CLI tool

##python library parser for cli arguments
import argparse

## import functions
from cli_functions.apply import apply
from cli_functions.destroy import destroy
from cli_functions.generate import generate
from cli_functions.plan import plan

##Main Function
def main():

    ## CLI description
    cli = argparse.ArgumentParser(description='CLI for generating AWS Terraform Files and Applying them')

    ## CLI Options
    cli.add_argument('options', choices=['apply', 'generate', 'destroy', 'plan', ], help='CLI Options')

    ## CLI Chosen Options
    cli_inputs = cli.parse_args()

    ## CLI Generate TF Config from Options
    if cli_inputs.options == 'generate':
        generate()

    ## CLI TF Apply Generated Config
    if cli_inputs.options == 'apply':
        apply()

    ## CLI TF Plan Generated Config
    if cli_inputs.options == 'plan':
        plan()

    ## CLI TF Destroy Generated Resources
    if cli_inputs.options == 'destroy':
        destroy()

    else:
        print("Choose valid option") 

main() 
