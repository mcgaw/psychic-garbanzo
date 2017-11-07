
def add_cnf_terms_(eqs, terms, violations):
    """
    Process the list of violations, converting
    them into CNF terms that must be satisfied
    to avoid the violation.
    """
    for violation in violations:                
        get_terms = lambda one_zero :list(map(lambda x: x[1], filter(lambda x: violation[x[0]] == one_zero, enumerate(terms))))
        one_terms = get_terms(1)
        zero_terms = get_terms(0) 

        assert len(one_terms) + len(zero_terms) == len(list(filter(lambda bin_val: not bin_val is None, violation)))

        num_vars = len(one_terms) + len(zero_terms)
        ones = len(one_terms)
        if num_vars == ones:
            # 111 or 11     
            eqs.append([-term[0] for i, term in enumerate(terms) if violation[i] is not None])
        elif ones == 0:
            # 000 or 00
            eqs.append([term[0] for i, term in enumerate(terms) if violation[i] is not None])
        elif ones == 1 and num_vars == 2:
            # 01 or 10
            eqs.append([-one_terms[0][0], zero_terms[0][0]])
        elif num_vars == 3:
            # Mix of 1's and 0's.
            vars_ = [item[0] for item in one_terms] + [-item[0] for item in zero_terms]
            eqs += not_all_true(*vars_)
        else:
            assert False, 'violation: {0} terms: {1}'.format(violation, terms)

"""
not: (h or g)(^h or ^g)
and: (h1 or ^g)(h2 or ^g)(^h1 or ^h2 or g)
or: (^h1 or g)(^h2 or g)(h1 or h2 or ^g)
"""

def not_all_true(x1, x2, x3):
    """
    Ensure x1 and x2 and x3 is False if
    and only if all the inputs are True.
    ^(x1 & x2 & x3) == (^x1 || ^x2 || ^x3)
    """
    g1, g2 = next(var_seq), next(var_seq)
    or_x1_x2 = [[x1, g1], [x2, g1], [-x1, -x2, g1]]
    or_g1_x3 = [[-g1, g2], [x3, g1], [g1, -x3, g2]]
    eqs = or_x1_x2 + or_g1_x3 + [[g2]]
    return eqs


def simplify_violations(violations):
    """
    Try to reduce the number of CNF terms by first
    looking for 'don't care' terms.
    Mark these terms by None in the violation array.
    """

    num_terms = len(violations[0])
    if num_terms == 1:
        # No simplification possible.
        return  

    def simplify(test, patterns):
        def match(positions, violation, pattern):
            """
            Test whether the pattern specified at this
            position matches.
            """
            return len(list(filter(lambda x: violation[x[1]] == pattern[x[0]], enumerate(positions)))) == len(positions)

        for pattern in patterns:
            matches = list(filter(lambda v: match(test, v, pattern), violations))
            if len(matches) == 2:
                # Found a 'don't care' term. Two violations
                # can be reduced to one smaller violation.
                simplified = [None] * num_terms
                for i, pos in enumerate(test):
                    simplified[pos] = pattern[i] 
                for m in matches:
                    violations.remove(m)
                violations.append(simplified)

    # Look for 'don't care' terms. First generate
    # all combinations of array indexes. Length of combination is
    # one less than the number of terms, leaving a possible 'don't
    # care' term which can be pattern matched.
    positions = itertools.combinations(list(range(0, num_terms)), num_terms - 1)
    values = list(itertools.product(*[list(range(2))] * (num_terms - 1)))
    for position in positions:
        simplify(position, values)
