import itertools

from sympy.logic import SOPform, POSform
from sympy import symbols, Symbol
from sympy.logic.boolalg import Not, And, Or, to_cnf

def cnf_terms_sympy(terms, minterms):

    symbol_str = ' '.join([str(term[0]) for term in terms])
    dontcares = []
    posForm = POSform(symbols(symbol_str), minterms, dontcares)

    clauses = []

    def minisat_var(arg):
        if type(arg) == Not:
            return -arg.args[0]
        else:
            return arg

    def minisat_or(or_):
        eq = []
        for arg in or_:
            eq.append(minisat_var(arg))
        return eq

    if type(posForm) == And:
        for arg in posForm.args:
            if type(arg) == Or:
                clauses.append(minisat_or(arg.args))
            else:
                clauses.append(minisat_var(arg))
    else:
        clauses.append(minisat_or(posForm.args))

    return clauses
