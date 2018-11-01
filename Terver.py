from fractions import Fraction


DistrLaw = {'k': {i: Fraction(1, 6) for i in range(1, 7)},
            'm': {1: Fraction(1, 12), 2: Fraction(1, 12), 3: Fraction(1, 3),
                  4: Fraction(1, 3), 5: Fraction(1, 12), 6: Fraction(1, 12)}}  # Distribution law


GetValue = {'t_kn302': lambda k, m: (max(k + m, 2 * m), DistrLaw['k'][k] * DistrLaw['m'][m]),
            't_kb301': lambda k, m: (min(pow(2, k), m), DistrLaw['k'][k] * DistrLaw['m'][m]),
            't3': lambda x, y: (x * y, DistrLaw['t_kn302'][x] * DistrLaw['t_kb301'][y])}


def get_distribution_law(v):
    d = {i: 0 for i in range(0, 145)}
    for k in range(1, 13):
        for m in range(1, 7):
            # if v == 't3':
            #     print(k, m, k*m)
            if v != 't3' and (k > 6 or m > 6): continue
            val, p = GetValue[v](k, m)
            d[val] += p
    DistrLaw[v] = d
    return d


def get_mathematical_expectation(drv, n=1):
    """E(T) = Sum[Ti*Pi]"""
    # print('exp',drv)
    E = 0
    for v in drv.keys():
        E += pow(v, n) * drv[v]
    return E


def get_dispersion(distribution):
    """D = E(t^2) - E(t)^2"""
    return get_mathematical_expectation(distribution, 2) - pow(get_mathematical_expectation(distribution), 2)


def get_mean_square_deviation(distribution):
    """r = D^(1/2)"""
    return pow(get_dispersion(distribution), 1/2)


def get_median(distribution):
    """distribution = {value: possibility, ...}"""
    possibility = 0
    for value in t1.keys():
        possibility += distribution[value]
        if possibility >= 1/2:
            return value


def get_covariance(math_exp_1, math_exp_2):
    """cov(c1, c2) = E(c1*c2)-E(c1)*E(c2)"""
    t3 = get_distribution_law('t3')
    return get_mathematical_expectation(t3) - math_exp_1 * math_exp_2


def get_correlation(cov, d1, d2):
    """p(t1, t2) = Cov(t1, t2) / (D(t1)*D(t2))^(1/2)"""
    # return get_covariance(t1, t2) / pow(get_dispersion(DistrLaw[t1]) * get_dispersion(DistrLaw[t2]), 1/2)
    return cov / pow(d1*d2, 1/2)


if __name__ == '__main__':
    print("T1 = max(k + m, 2m)")
    t1 = get_distribution_law('t_kn302')
    print(">>>Distribution law:")
    for value in t1.keys():
        if t1[value] != 0:
            print('   ', value, '->', t1[value])
    e1 = get_mathematical_expectation(t1)
    print('>>>Mathematical expectation =', e1)
    d1 = get_dispersion(t1)
    print('>>>Dispersion =', d1)
    print('>>>Mean square deviation =', get_mean_square_deviation(t1))
    print('>>>Median =', get_median(t1), '\n')
    t2 = get_distribution_law('t_kb301')
    print("T2 = min(2^k, m)")
    print(">>>Distribution law:")
    for value in t1.keys():
        if t2[value] != 0:
            print('   ', value, '->', t2[value])
    e2 = get_mathematical_expectation(t2)
    d2 = get_dispersion(t2)
    cov = get_covariance(e1, e2)
    print('\n>>>Covariance between t1 = max(k + m, 2m) and t2 = min(2^k, m) =', cov)
    p = get_correlation(cov, d1, d2)
    print('>>>Correlation between t1 = max(k + m, 2m) and t2 = min(2^k, m) =', p)
