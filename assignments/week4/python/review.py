import os
import subprocess
import click


def show_with_os():
    print("\nRunning ls with os.system():")
    os.system("ls")


def show_with_subprocess():
    print("\nRunning ls -la with subprocess.run():")
    subprocess.run(["ls", "-la"], check=True)


@click.command()
@click.argument("name")
@click.option(
    "--method",
    type=click.Choice(["os", "subprocess", "both"]),
    default="both",
    help="Choose how to run the shell command.",
)
def main(name, method):
    print(f"Hello, {name}!")

    if method in ("os", "both"):
        show_with_os()

    if method in ("subprocess", "both"):
        show_with_subprocess()


if __name__ == "__main__":
    main()
