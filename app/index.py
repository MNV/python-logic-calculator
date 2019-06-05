import gnureadline
from typing import List, Callable
import os
import re
import string
import pandas
from itertools import product

from docs import Docs
from functions import nand, nor, implies, xor, get_pcnf, get_pdnf, get_mdnf


ALLOWED_LEXIS = ('(', ')', '0', '1', 'implies', 'nand', 'nor', 'and', 'not', 'xor', 'or', '==')
user_expression = ''
variables = []

os.system('clear')
docs = Docs()
print(docs.get_welcome_message())


def truth_table(func: Callable) -> pandas.DataFrame:
    """Prints out the truth table using the given function to calculate"""
    values = [list(args) + [int(func(*args))] for args in product([0, 1], repeat=func.__code__.co_argcount)]
    return pandas.DataFrame(
        values,
        columns=(list(func.__code__.co_varnames) + [user_expression]))


def check(expression: str) -> bool:
    """Checks if the given expression has unknown lexis"""
    lexis = set(string.ascii_lowercase)
    lexis.update(ALLOWED_LEXIS)
    return set(re.findall(r'\w+', expression)) <= lexis


def get_expression() -> str:
    """Prompts the user to input expression to process"""
    user_input = input('Please, enter the expression: ')
    if not check(user_input):
        raise Exception('Invalid expression format: unknown lexis.')
    return user_input


def extract_variables(expression: str) -> List[str]:
    """Extracts the variables from given expression"""
    expr_variables = expression
    lexis = tuple(ALLOWED_LEXIS)
    for sign in lexis:
        expr_variables = expr_variables.replace(sign, '')

    expr_variables = re.split(r'\s*,?', expr_variables)
    expr_variables = list(filter(None, expr_variables))
    expr_variables = sorted(tuple(set(expr_variables)))

    return expr_variables


def init() -> None:
    """Application initialization"""
    globals()['user_expression'] = get_expression()
    expr_variables = extract_variables(user_expression)
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
