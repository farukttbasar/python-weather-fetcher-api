import argparse 

# ARGPARSE
def parse_cli():
    parser = argparse.ArgumentParser(
        description="A CLI tool that fetches current weather info via Open-Meteo"
    )

    parser.add_argument(
        "-c",
        "--city",
        type=str,
        help="Enter the name of city / district"
    )

    return parser.parse_args()

# INTERACTIVE INPUT

def get_input():
    print("=" * 40)
    print("--- Weather Fetcher Interactive Menu ---")
    print("=" * 40)

    while True:
        city = input("Enter the name of city / district > ").strip()

        if city:
            break
        else:
            print("City name cannot be empty!")

    return argparse.Namespace(city=city)
        