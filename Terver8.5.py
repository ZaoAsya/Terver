from fractions import Fraction


DistrLaw = {'k': {i: Fraction(1, 10) for i in range(0, 10)},
            'n': {i: Fraction(1, 10) for i in range(0, 10)}}


GetValue = {'c1': lambda x, y: ((x * y) // 10, Fraction(1, 100)),
            'c2': lambda x, y: ((x * y) % 10, Fraction(1, 100)),
            'c3': lambda x, y: (x * y, DistrLaw['c1'][x] * DistrLaw['c2'][y])}


def get_distribution_law(v):
    d = {i: 0 for i in range(0, 82)}
    for k in range(0, 10):
        for n in range(0, 10):
            val, p = GetValue[v](k, n)
            d[val] += p
    DistrLaw[v] = d
    return d


def get_mathematical_expectation(drv):
    """E(T) = Sum[Ti*Pi]"""
    E = 0
    for v in drv.keys():
        E += v * drv[v]
    return E


def get_covariance(c1, c2):
    """cov(c1, c2) = E(c1*c2)-E(c1)*E(c2)"""
    c3 = get_distribution_law('c3')
    return get_mathematical_expectation(c3) \
           - get_mathematical_expectation(DistrLaw[c1])*get_mathematical_expectation(DistrLaw[c2])


if __name__ == '__main__':
    c1 = get_distribution_law('c1')
    print(">>>Distribution law for c1:")
    for value in c1.keys():
        if c1[value] != 0:
            print('   ', value, '->', c1[value])
    c2 = get_distribution_law('c2')
    print(">>>Distribution law for c2:")
    for value in c2.keys():
        if c2[value] != 0:
            print('   ', value, '->', c2[value])
    cov = get_covariance('c1', 'c2')
    mean = "independent" if cov == 0 else "dependent"
    print(">>>Covariance =", cov)
    print("   It means c1 and c2 are {}".format(mean))
