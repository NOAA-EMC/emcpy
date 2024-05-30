from emcpy.stats.stats import mstats, lregress, ttest, get_weights, \
    get_linear_regression, bootstrap, calc_bins
import numpy as np


def test_mstats():
    sample_data = np.array([30, 37, 36, 43, 42, 43, 43, 46, 41, 42], dtype=np.float32())
    mstats(sample_data, verbose=True)


def test_lregress():
    x = np.array([1, 2, 2, 4, 5, 6, 6, 8, 9, 10], dtype=np.float32())
    y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=np.float32())
    rc, sb, ssig = lregress(x, y, ci=95.0)
    print(f' rc, sb, ssig = {rc, sb, ssig}')


def test_ttest():
    x = np.array([70, 65, 80, 90, 92, 88, 67, 72, 10, 95], dtype=np.float32())
    y = np.array([35, 75, 67, 81, 94, 71, 67, 74, 35, 85], dtype=np.float32())
    diffmean, errorbar = ttest(x, y, ci=95.0, paired=True, scale=False)
    print(f' diffmean, errorbar = {diffmean, errorbar}')


def test_get_weights():
    lats = np.array([90, -90, 0, 18, -25, -10.3, 45.5], dtype=np.float32())
    result = get_weights(lats)
    print(f' weighted means: {result}')


def test_get_linear_regression():
    x = np.array([70, 65, 80, 90, 92, 88, 67, 72, 10, 95], dtype=np.float32())
    y = np.array([35, 75, 67, 81, 94, 71, 67, 74, 35, 85], dtype=np.float32())
    y_pred, r_sq, intercept, slope = get_linear_regression(x, y)

    print(f'y_pred, r_sq, intercept, slope = {y_pred, r_sq, intercept, slope}')


def test_bootstrap():
    sample_data = np.array([30, 37, 36, 43, 42, 43, 43, 46, 41, 42], dtype=np.float32())
    ci_lower, ci_upper = bootstrap(sample_data, nrepl=10000)
    xbar = np.mean(sample_data)

    print(f'ci_lower,ci_upper = {xbar+ci_lower, xbar+ci_upper}')


def test_calc_bins():
    sample_data = np.array([0.5, -0.4, -0.7, 0.9, -0.01, 0.02, -0.6, 0.3, -0.9, 0.82, -0.03, 0.41],
                           dtype=np.float32())
    eval_type = 'omf'
    bins, binsize = calc_bins(sample_data, eval_type)

    print(f'bins, binsize = {bins, binsize}')
