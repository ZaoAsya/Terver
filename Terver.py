from fractions import Fraction


DistrLaw = {'k': {i: Fraction(1, 6) for i in range(1, 7)},
            'm': {1: Fraction(1, 12), 2: Fraction(1, 12), 3: Fraction(1, 3),
                  4: Fraction(1, 3), 5: Fraction(1, 12), 6: Fraction(1, 12)}}  # Distribution law


GetValue = {'t_kn302': lambda k, m: (max(k + m, 2 * m), DistrLaw['k'][k] * DistrLaw['m'][m]),
            't_kb301': lambda k, m: (min(pow(2, k), m), DistrLaw['k'][k] * DistrLaw['m'][m]),
            't3': lambda x, y: (x * y, DistrLaw['t_kn302'][x] * DistrLaw['t_kb301'][y])}


def get_distribution_law(res, drv1, drv2):
    d = {i: 0 for i in range(0, 145)}
    for k in DistrLaw[drv1].keys():
        for m in DistrLaw[drv2].keys():
            val, p = GetValue[res](k, m)
            d[val] += p
    DistrLaw[res] = {val:d[val] for val in d.keys() if d[val] > 0}
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


def get_mean_square_deviation(dispersion):
    """r = D^(1/2)"""
    return pow(dispersion, 1 / 2)


def get_median(distribution):
    """distribution = {value: possibility, ...}"""
    possibility = 0
    for value in distribution.keys():
        possibility += distribution[value]
        if possibility >= 1/2:
            return value


def get_covariance(math_exp_1, math_exp_2):
    """cov(c1, c2) = E(c1*c2)-E(c1)*E(c2)"""
    t3 = get_distribution_law('t3', 't_kn302', 't_kb301')
    return get_mathematical_expectation(t3) - math_exp_1 * math_exp_2


def get_correlation(cov, d1, d2):
    """p(t1, t2) = Cov(t1, t2) / (D(t1)*D(t2))^(1/2)"""
    return cov / pow(d1*d2, 1/2)


def get_data_for(name_drv, drv1, drv2):
    distrLaw = get_distribution_law(name_drv, drv1, drv2)
    E = get_mathematical_expectation(distrLaw)
    D = get_dispersion(distrLaw)
    r = get_mean_square_deviation(D)
    M = get_median(distrLaw)
    return distrLaw, E, D, r, M


def print_data(name_drv, distrLaw, E, D, r, M):
    print(name_drv)
    print(">>>Distribution law:")
    for value in distrLaw.keys():
        if distrLaw[value] != 0:
            print('   ', value, '->', distrLaw[value])
    print('>>>Mathematical expectation =', E)
    print('>>>Dispersion =', D)
    print('>>>Mean square deviation =', r)
    print('>>>Median =', M, '\n')


if __name__ == '__main__':
    t_kn302 = get_data_for('t_kn302', 'k', 'm')
    print_data('T1 = max(k + m, 2m)', *t_kn302)
    t_kb301 = get_data_for('t_kb301', 'k', 'm')
    # print_data('T2 = min(2^k, m)', *t_kb301)
    cov = get_covariance(t_kn302[1], t_kb301[1])
    print('>>>Covariance between t1 = max(k + m, 2m) and t2 = min(2^k, m) =', cov)
    print('>>>Correlation between t1 = max(k + m, 2m) and t2 = min(2^k, m) =',
          get_correlation(cov, t_kn302[2], t_kb301[2]))
