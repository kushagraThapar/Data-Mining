import sys

from kthapa2 import CustomConstants


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


def parse_minimum_item_support(single_line):
    # If single line is empty then return None and handle None at the caller side
    if single_line is None or single_line.strip() is "":
        return None

    # If 'MIS(' is not found, then return None and handle None at the caller side
    if CustomConstants.MIS_CONSTANT not in single_line:
        return None

    single_line = single_line.strip()
    # Return some sort of Map.entry kind of thing which will have item value and minimum item support for that item
    index_of_item_start = single_line.find(CustomConstants.MIS_START_CONSTANT) + 1
    index_of_item_stop = single_line.find(CustomConstants.MIS_STOP_CONSTANT)
    item = int(single_line[index_of_item_start:index_of_item_stop].strip())
    index_of_mis_start = single_line.find(CustomConstants.EQUALS_OPERATOR) + 1
    mis_value = round(float(single_line[index_of_mis_start:].strip()), CustomConstants.ROUND_FLOAT_DIGITS)
    return item, mis_value


def parse_transactions(single_line):
    # If single line is empty then return None and handle None at the caller side
    if single_line is None or single_line.strip() is "":
        return None

    # Check if it has opening and closing curly braces
    if CustomConstants.CURLY_BRACE_OPENING not in single_line \
            or CustomConstants.CURLY_BRACE_CLOSING not in single_line:
        return None

    single_line = single_line.strip()
    elements_array = single_line[(single_line.find(CustomConstants.CURLY_BRACE_OPENING) + 1):single_line.find(
        CustomConstants.CURLY_BRACE_CLOSING)].split(CustomConstants.COMMA_OPERATOR)
    temp_array = []
    for element in elements_array:
        if element is not None and element.strip() is not "":
            temp_array.append(int(element.strip()))

    return temp_array


def parse_sdc_value(single_line):
    # If single line is empty then return None and handle None at the caller side
    if single_line is None or single_line.strip() is "":
        return None

    if CustomConstants.SDC_CONSTANT in single_line:
        single_line = single_line.strip()
        return float(single_line[single_line.find(CustomConstants.EQUALS_OPERATOR) + 1:].strip())

    return None


def parse_cannot_be_together_values(single_line):
    # If single line is empty then return None and handle None at the caller side
    if single_line is None or single_line.strip() is "":
        return None

    if CustomConstants.CANNOT_BE_TOGETHER in single_line:
        single_line = single_line.strip()
        elements_array = single_line[(single_line.find(CustomConstants.CURLY_BRACE_OPENING) + 1):single_line.find(
            CustomConstants.CURLY_BRACE_CLOSING)].split(CustomConstants.COMMA_OPERATOR)
        temp_array = []
        for element in elements_array:
            if element is not None and element.strip() is not "":
                temp_array.append(int(element.strip()))

        return temp_array

    return None


def parse_must_have_values(single_line):
    # If single line is empty then return None and handle None at the caller side
    if single_line is None or single_line.strip() is "":
        return None
    temp_array = []
    if CustomConstants.MUST_HAVE in single_line:
        single_line = single_line.strip()
        elements_array = single_line.split(CustomConstants.SPACE)
        for element in elements_array:
            if element is not None and element.strip() is not "" and element.isdigit():
                temp_array.append(int(element))

        return temp_array

    return None


def print_output(f_final, item_frequency_map, item_tailcount_map):
    k = 1
    for f_k in f_final:
        print("Frequent", str(k) + "-Item Sets\n")
        if k == 1:
            for element in f_k:
                print("\t\t", item_tailcount_map[frozenset([element])], ": {", element, "}")
        else:
            for element in f_k:
                print("\t\t", item_frequency_map[frozenset(element)], ": {", element, "}")
                print("Tailcount =", item_tailcount_map[frozenset(element[1:])])
        print("\n\t\tTotal number of frequent", str(k) + "-Item Sets =", len(f_k), "\n\n")
        k += 1


def exit_program():
    print("Program will exit now... ")
    sys.exit(1)
