from fractions import Fraction


DistrLaw = {'k': {i: Fraction(1, 6) for i in range(1, 7)},
            'm': {1: Fraction(1, 12), 2: Fraction(1, 12), 3: Fraction(1, 3),
                  4: Fraction(1, 3), 5: Fraction(1, 12), 6: Fraction(1, 12)}}  # Distribution law


def get_probability(k, m):
    return max(k + m, 2 * m), DistrLaw['k'][k] * DistrLaw['m'][m]


def get_distribution_law():
    t = {i: 0 for i in range(2, 13)}
    for i in range(1, 7):
        for j in range(1, 7):
            v, p = get_probability(i, j)
            t[v] += p
    DistrLaw['t'] = t
    return t


def get_mathematical_expectation(n=1):
    """E(T) = Sum[Ti*Pi]"""
    E = 0
    for v in DistrLaw['t'].keys():
        E += pow(v, n) * DistrLaw['t'][v]
    return E


def get_dispersion():
    """D = E(t)^2 - E(t^2)"""
    return pow(get_mathematical_expectation(), 2) - get_mathematical_expectation(2)


if __name__ == '__main__':
    """T = max(k + m, 2m)"""
    distributionLaw = get_distribution_law()
    print("T = max(k + m, 2m)")
    print(">>>Distribution law:")
    for value in distributionLaw.keys():
        print('   ', value, '->', distributionLaw[value])
    print('>>>Mathematical expectation =', get_mathematical_expectation())
    print('>>>Dispersion =', get_dispersion())
