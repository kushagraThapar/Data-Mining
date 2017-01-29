import sys


def write_file(filename, text):
    try:
        f = open(filename, "w")
        f.write(text)
        f.close()
    except IOError:
        print("IOError occurred in file [" + filename + "]")
        exit_program()
    return


def read_file(filename):
    try:
        f = open(filename, "rU")
        text = f.read()
        f.close()
        return text
    except FileNotFoundError:
        print("File not found with name [" + filename + "]")
    except IOError:
        print("IOError occurred in file [" + filename + "]")

    exit_program()


def process_tweets(tweet_data):
    if tweet_data is None or tweet_data.strip() is "":
        print("Tweet Data is Empty")
        exit_program()

    for single_row in tweet_data.split("\n"):
        single_row = single_row.strip()
        single_row_array = single_row.split(",", 3)
        if len(single_row_array) >= 3:
            last_index = single_row_array[3].rfind("\"")
            tweet = single_row_array[3][0:last_index + 1]
            tweet_class = single_row_array[3][last_index + 2:last_index + 3]


def exit_program():
    print("Program will exit now... ")
    sys.exit(1)
