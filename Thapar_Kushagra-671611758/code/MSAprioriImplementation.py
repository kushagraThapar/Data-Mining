from collections import OrderedDict
from itertools import combinations

from kthapa2 import CustomConstants

item_support_count_map = {}
item_support_map = {}
item_frequency_map = {}
item_tailcount_map = {}
minimum_item_support_map = OrderedDict()
cannot_be_together = set()
must_have = set()


def ms_apriori_algorithm(transactions, minimum_item_support_list, sdc_value):
    minimum_item_support_list.sort(key=lambda tup: (float(tup[1]), int(tup[0])))
    for element in minimum_item_support_list:
        minimum_item_support_map[element[0]] = element[1]
    f_1 = []
    f_final = []
    l_list = init_pass(minimum_item_support_map, transactions)
    for element in l_list:
        if item_support_map[element] >= minimum_item_support_map[element]:
            if element in must_have:
                f_1.append(element)
                fill_item_map(frozenset([element]), transactions, item_tailcount_map)

    if len(f_1) == 0:
        return f_final

    f_k = f_1
    f_final.append(f_k)
    k = 2
    f_k_without_must_have = []
    while True:

        if k == 2:
            c_k = level2_candidate_gen_function(l_list, sdc_value)
        else:
            c_k = ms_candidate_generation(f_k_without_must_have, sdc_value, k - 1)

        for single_transaction in transactions:
            single_transaction_set = frozenset(single_transaction)
            for single_candidate in c_k:
                single_candidate = list(single_candidate)
                single_candidate_set = frozenset(single_candidate)
                if single_candidate_set.issubset(single_transaction):
                    fill_item_map(single_candidate_set, transactions, item_frequency_map)

                single_candidate_without_first_element = frozenset(single_candidate[1:])
                if len(single_candidate_without_first_element) > 0 and single_candidate_without_first_element.issubset(
                        single_transaction_set):
                    fill_item_map(single_candidate_without_first_element, transactions, item_tailcount_map)

        f_k = []
        f_k_without_must_have = []
        for candidate in c_k:
            candidate = list(candidate)
            candidate_set = frozenset(candidate)
            if candidate_set in item_frequency_map and item_frequency_map[candidate_set] / len(
                    transactions) >= \
                    minimum_item_support_map[candidate[0]]:
                f_k_without_must_have.append(candidate)
                element_present = False
                for element in must_have:
                    if element in candidate:
                        element_present = True
                        break

                if element_present:
                    are_together = False
                    for single_set in set(combinations(candidate_set, 2)):
                        if set(single_set).issubset(cannot_be_together):
                            are_together = True
                            break

                    if not are_together:
                        f_k.append(candidate)

        if len(f_k_without_must_have) == 0:
            return f_final

        f_final.append(f_k)
        k += 1

    return f_final


def init_pass(minimum_item_support_map_copy, transactions):
    list_to_be_returned = []
    initiating_element_mis = None
    for element in minimum_item_support_map_copy:
        count = 0
        for single_transaction in transactions:
            if element in single_transaction:
                count += 1
        item_support_count_map[element] = count
        support = round(count / len(transactions), CustomConstants.ROUND_FLOAT_DIGITS)
        item_support_map[element] = support
        if initiating_element_mis is not None and support >= initiating_element_mis:
            list_to_be_returned.append(element)
        elif support >= minimum_item_support_map_copy[element]:
            initiating_element_mis = minimum_item_support_map_copy[element]
            list_to_be_returned.append(element)

    return list_to_be_returned


def level2_candidate_gen_function(l_list, sdc_value):
    c_2 = []
    for element in l_list:
        if item_support_map[element] >= minimum_item_support_map[element]:
            for new_element in l_list[l_list.index(element) + 1:]:
                if minimum_item_support_map[new_element] >= minimum_item_support_map[element] and abs(
                                item_support_map[new_element] - item_support_map[element]) <= sdc_value:
                    # Check for the cannot be together condition
                    if not {element, new_element}.issubset(cannot_be_together):
                        c_2.append([element, new_element])
    return c_2


def ms_candidate_generation(f_k_1, sdc_value, k):
    c_k_final = []
    f_k_1_set = set()
    for element in f_k_1:
        f_k_1_set.add(frozenset(element))

    f_k_1_set = frozenset(f_k_1_set)
    current_index = -1
    for single_f_1 in f_k_1:
        for single_f_2 in f_k_1[f_k_1.index(single_f_1) + 1:]:
            if frozenset(single_f_1[:-1]) == frozenset(single_f_2[:-1]) and single_f_1[-1] != single_f_2[-1] and \
                            minimum_item_support_map[single_f_1[-1]] <= minimum_item_support_map[single_f_2[-1]] \
                    and abs(item_support_map[single_f_1[-1]] - item_support_map[single_f_2[-1]]) <= sdc_value:

                c_k_local = single_f_1[:]
                c_k_local.append(single_f_2[-1])
                current_index += 1
                c_k_final.append(c_k_local)

                first = c_k_local[0]
                second = c_k_local[1]
                # Do the pruning step
                for each_subset in set(combinations(c_k_local, k)):
                    if first in each_subset or minimum_item_support_map[first] == \
                            minimum_item_support_map[second]:
                        if frozenset(each_subset) not in f_k_1_set:
                            del c_k_final[current_index]
                            current_index -= 1
                            break

    return c_k_final


def fill_item_map(item, transactions, input_map):
    if item in input_map:
        return

    for single_transaction in transactions:
        if item.issubset(set(single_transaction)):
            if item not in input_map:
                input_map[item] = 0

            input_map[item] += 1
