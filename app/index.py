import gnureadline
import os
import re
import pandas
from itertools import product

from docs import Docs
from functions import nand, nor, implies, xor, get_pcnf, get_pdnf, get_mdnf


ALLOWED_LEXIS = set(('and', 'or', 'not', 'implies', '==', 'xor', 'nor', 'nand', 'x', 'y', 'z', '0', '1'))
user_expression = ''
variables = []

os.system('clear')
docs = Docs()
print(docs.get_welcome_message())


def truth_table(func):
    values = [list(args) + [int(func(*args))] for args in product([0, 1], repeat=func.__code__.co_argcount)]
    return pandas.DataFrame(
        values,
        columns=(list(func.__code__.co_varnames) + [user_expression]))


def check(expression):
    return set(re.findall(r'\w+', expression)) <= ALLOWED_LEXIS


def get_expression():
    user_input = input('Please, enter the expression: ')
    if not check(user_input):
        raise Exception('Invalid expression format: unknown lexis.')
    return user_input


def init():
    globals()['user_expression'] = get_expression()

    expr_variables = re.findall(r'\W?[xyz]{1}\W?', user_expression)
    expr_variables = set(list(map(lambda char: char.strip('() ,'), expr_variables)))
    expr_variables = sorted(tuple(expr_variables))
    exec(f"""def expression_function({','.join(expr_variables)}): return eval(user_expression)""", globals())
    globals()['variables'] = expr_variables


while True:
    try:
        init()
        data = truth_table(expression_function)
        print(data)
        print('\r\nPDNF: ' + get_pdnf(data, user_expression, variables))
        print('\r\nPCNF: ' + get_pcnf(data, user_expression, variables))
        print('\r\nMDNF: ' + get_mdnf(data, user_expression, variables))
        break
    except Exception as exception:
        message = getattr(exception, 'message', repr(exception))
        print('Invalid input: ' + message)
        raise exception
