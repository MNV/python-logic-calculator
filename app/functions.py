import itertools


def nand(a, b):
    return not (a and b)


def nor(a, b):
    return not (a or b)


def implies(a, b):
    return (not a) or b


def xor(a, b):
    return a ^ b


def get_pdnf(data_frame, function_name, variables):
    """Calculates the prime disjunctive normal form (PDNF)"""
    result_batch = []
    for index, row in data_frame.iterrows():
        row_batch = []
        if row[function_name]:
            for variable in variables:
                row_batch.append('¬' + variable.upper() if not row[variable] else variable.upper())
            result_batch.append(''.join(row_batch))

    return ' ∨ '.join(result_batch)


def get_pcnf(data_frame, function_name, variables):
    """Calculates the prime conjunctive normal form (PCNF)"""
    result_batch = []
    for index, row in data_frame.iterrows():
        row_batch = []
        if not row[function_name]:
            for variable in variables:
                row_batch.append(variable.upper() if not row[variable] else '¬' + variable.upper())
            result_batch.append('(' + ' ∨ '.join(row_batch) + ')')

    return ' ∧ '.join(result_batch) if result_batch else 'Does not exist.'


def get_mdnf(data_frame, function_name, variables):
    """Calculates the minimal disjunctive normal form"""
    vars_dict = {}
    for index, row in data_frame.iterrows():
        if row[function_name]:
            var_row = {}
            for variable in variables:
                var_row.update({variable: row[variable]})
            vars_dict.update({index: var_row})

    #print(vars_dict)

    if len(vars_dict) == len(data_frame):
        return '1'

    implicants = find_implicants(vars_dict, variables, len(variables) - 1)

    #print('implicants: ')
    #print(implicants)

    resulted_terms = find_optimal_coverage(implicants)
    #print('resulted_terms: ')
    #print(resulted_terms)

    result_batch = []
    for term_dict in resulted_terms:
        row_batch = []
        for variable, value in term_dict.items():
            row_batch.append(variable.upper() if value else '¬' + variable.upper())
        result_batch.append(''.join(row_batch))

    return ' ∨ '.join(result_batch)


def find_implicants(var_dict, variables, count):

    if count < 1:
        return var_dict

    glued_indices = []
    implicants_dict = {}
    #print('find_implicants: ')
    #print(var_dict.items())
    for index, vars_dict in var_dict.items():
        for indx, vd in var_dict.items():
            if vars_dict != vd:
                matches = 0
                matched_vars = []
                for variable in variables:
                    if all(key in vd.keys() for key in vars_dict) and\
                            variable in vars_dict and vars_dict[variable] == vd[variable]:
                        matches += 1
                        matched_vars.append(variable)
                if matches == count:
                    glued_indices.append(index)
                    glued_indices.append(indx)
                    implicants_dict.update({(index, indx): {var: vd[var] for var in matched_vars}})

    indices = set()
    implicants_dict_pure = {}
    for key, value in implicants_dict.items():
        indices.update(key)
        if value not in implicants_dict_pure.values():
            implicants_dict_pure[tuple(sorted(key))] = value

    #print('implicants_dict_pure: ')
    #print(implicants_dict_pure)

    #print('glued_indices: ')
    glued_indices = list(set(glued_indices))
    #print(glued_indices)

    unglued_indices = set(var_dict.keys()) - set(glued_indices)
    #print('unglued_indices: ')
    #print(list(unglued_indices))
    unglued_indices = tuple(unglued_indices)
    unglued_dict = {}
    for indx in unglued_indices:
        unglued_dict.update({indx: var_dict[indx]})

    #print('unglued_dict: ')
    #print(unglued_dict)

    implicants_dict_pure.update(unglued_dict)

    if not glued_indices and unglued_indices:
        return var_dict

    return var_dict.update(unglued_dict) \
        if not find_implicants(implicants_dict_pure, variables, count - 1) \
        else find_implicants(implicants_dict_pure, variables, count - 1)


def find_optimal_coverage(implicants_dict):
    indices = list(set(flatten(list(implicants_dict.keys()))))
    #print('indices: ')
    #print(indices)

    combs = list(itertools.permutations(implicants_dict.keys(), len(implicants_dict)))

    gr = []
    vars = []
    indices_set = set()
    for index_combs in combs:
        for index_comb in index_combs:
            if isinstance(index_comb, int):
                indices_set.update((index_comb,))
            else:
                indices_set.update(set(flatten(index_comb)))
            vars.append(implicants_dict[index_comb])
            if indices_set == set(indices):
                gr.append(vars)
                break
        indices_set = set()
        vars = []

    #print('RESULT: ')
    #print(min(gr, key=len))

    #print(gr)

    return min(gr, key=len)


def flatten(list_to_flatten):
    if not isinstance(list_to_flatten, (list, tuple)):
        return list_to_flatten

    for elem in list_to_flatten:
        if isinstance(elem, (list, tuple)):
            for x in flatten(elem):
                yield x
        else:
            yield elem
