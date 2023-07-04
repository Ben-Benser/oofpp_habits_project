import typer
import sys

def get_input(prompt_text):
    """
        Function that enables the User to cancel almost every command in the App.
        :param prompt_text: Input from User, that gets checked whether it's a cancel-statement
        """
    user_input = str(typer.prompt(prompt_text))
    if user_input.isnumeric():
        return int(user_input)
    else:
        if user_input.upper() == "CANCEL":
            typer.echo("You successfully canceled the actual Process. Feel free to type in another Command.")
            sys.exit(0)
        else:
            return user_input
