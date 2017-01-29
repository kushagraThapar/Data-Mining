import sys
from src import UtilsModule


def main():
    if len(sys.argv) < 2:
        print("USAGE : python3 initiator.py <obama.csv> <romney.csv>")
        UtilsModule.exit_program()

    obama_file = sys.argv[1]
    romney_file = sys.argv[2]
    obama_data = UtilsModule.read_file(obama_file)
    romney_data = UtilsModule.read_file(romney_file)
    UtilsModule.process_tweets(obama_data)
    print(obama_data)
    print(romney_data)


if __name__ == '__main__':
    main()
