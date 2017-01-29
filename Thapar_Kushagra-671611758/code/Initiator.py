import sys
import time

from kthapa2 import MSAprioriImplementation

from kthapa2 import Utils as UtilsModule

minimum_item_support_list = []
frequent_1_item_sets = {}
transactions = []
sdc_value = -1
cannot_be_together = []
must_have = []


def main():
    if len(sys.argv) < 2:
        print("USAGE : python3 MSAprioriImplementation.py <input-data.txt> <parameter-file.txt>")
        UtilsModule.exit_program()

    input_file = sys.argv[1]
    parameter_file = sys.argv[2]

    #   Split the file data by new line
    parameter_array = UtilsModule.read_file(parameter_file).split("\n")
    input_data_array = UtilsModule.read_file(input_file).split("\n")

    # Parse those data arrays
    for parameter in parameter_array:
        temp_tuple = UtilsModule.parse_minimum_item_support(parameter)
        if temp_tuple is not None:
            minimum_item_support_list.append((temp_tuple[0], temp_tuple[1]))
            continue
        else:
            temp_value = UtilsModule.parse_sdc_value(parameter)
            if temp_value is not None:
                global sdc_value
                sdc_value = temp_value
                continue

            temp_value = UtilsModule.parse_cannot_be_together_values(parameter)
            if temp_value is not None:
                global cannot_be_together
                cannot_be_together = temp_value
                MSAprioriImplementation.cannot_be_together = set(cannot_be_together)
                continue

            temp_value = UtilsModule.parse_must_have_values(parameter)
            if temp_value is not None:
                global must_have
                must_have = temp_value
                MSAprioriImplementation.must_have = set(must_have)
                continue

    for parameter in input_data_array:
        temp_value = UtilsModule.parse_transactions(parameter)
        if temp_value is not None:
            transactions.append(temp_value)

    if len(transactions) == 0:
        print("No Transactions found")
        UtilsModule.exit_program()

    f_final = MSAprioriImplementation.ms_apriori_algorithm(transactions, minimum_item_support_list, sdc_value)

    UtilsModule.print_output(f_final, MSAprioriImplementation.item_frequency_map,
                             MSAprioriImplementation.item_tailcount_map)


if __name__ == '__main__':
    main()
