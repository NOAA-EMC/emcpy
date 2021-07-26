# coding: utf-8 -*-

'''
stats.py contains statistics utility functions
'''

__all__ = ['mstats', 'lregress', 'ttest', 'get_weights', 'get_weighted_mean',
           'get_linear_regression']

import numpy as _np
from scipy.stats import t as _t
from sklearn.linear_model import LinearRegression


def mstats(x):
    '''
    Function that computes and displays
    various statistics of a variable.

    A better alternative is `scipy.stats.describe()`

    Parameters
    ----------
        x : numpy variable whose statistics are to be computed and displayed
    '''

    OUT = type('', (), {})

    OUT.MatrixSize = _np.shape(x)
    OUT.NElements = _np.prod(OUT.MatrixSize)
    OUT.Nnans = _np.sum(_np.isnan(x))
    OUT.NAnalyzedElements = OUT.NElements - OUT.Nnans

    datatype = x.dtype

    xf = x.flatten()
    xf = xf[~_np.isnan(xf)]
    absxf = _np.abs(xf)

    OUT.Mean = _np.mean(xf)
    OUT.Max = _np.max(xf)
    OUT.Min = _np.min(xf)
    OUT.Median = _np.median(xf)
    OUT.StDev = _np.std(xf, ddof=1)
    OUT.MeanAbs = _np.mean(absxf)
    OUT.MinAbs = _np.min(absxf[absxf > 0.0])
    OUT.FracZero = len(xf[xf == 0.0]) / OUT.NAnalyzedElements
    OUT.FracNan = OUT.Nnans / OUT.NElements

    print('================= m s t a t s ==================')
    print('        MatrixSize: %s' % (str(OUT.MatrixSize)))
    print('         NElements: %d' % (OUT.NElements))
    print(' NAnalyzedElements: %d' % (OUT.NAnalyzedElements))
    if datatype in ['int', 'int8', 'int16', 'int32', 'int64',
                    'uint8', 'uint16', 'uint32', 'uint64',
                    'float', 'float16', 'float32', 'float64']:
        print('              Mean: %f' % (OUT.Mean))
        print('               Max: %f' % (OUT.Max))
        print('               Min: %f' % (OUT.Min))
        print('            Median: %f' % (OUT.Median))
        print('             StDev: %f' % (OUT.StDev))
        print('           MeanAbs: %f' % (OUT.MeanAbs))
        print('            MinAbs: %f' % (OUT.MinAbs))
    if datatype in ['complex', 'complex64', 'complex128']:
        print('              Mean: %f + %fi' % (OUT.Mean.real, OUT.Mean.imag))
        print('               Max: %f + %fi' % (OUT.Max.real, OUT.Max.imag))
        print('               Min: %f + %fi' % (OUT.Min.real, OUT.Min.imag))
        print('            Median: %f + %fi' %
              (OUT.Median.real, OUT.Median.imag))
        print('             StDev: %f + %fi' %
              (OUT.StDev.real, OUT.StDev.imag))
        print('           MeanAbs: %f + %fi' %
              (OUT.MeanAbs.real, OUT.MeanAbs.imag))
        print('            MinAbs: %f + %fi' %
              (OUT.MinAbs.real, OUT.MinAbs.imag))
    print('          FracZero: %f' % (OUT.FracZero))
    print('           FracNaN: %f' % (OUT.FracNan))
    print('================================================')

    return


def lregress(x, y, ci=95.0):
    '''
    Function that computes the linear regression between two variables and
    returns the regression coefficient and statistical significance
    for a t-value at a desired confidence interval.

    Parameters
    ----------
        x : independent variable
        y : dependent variable
        ci : confidence interval (default: 95%)

    Returns
    -------
        rc : linear regression coefficient
        sb : standard error on the linear regression coefficient
        ssig : statistical significance of the linear regression coefficient
    '''

    # make sure the two samples are of the same size
    if (len(x) != len(y)):
        raise ValueError('samples x and y are not of the same size')
    else:
        nsamp = len(x)

    pval = 1.0 - (1.0 - ci / 100.0) / 2.0
    tcrit = _t.ppf(pval, 2 * len(x) - 2)

    covmat = _np.cov(x, y=y, ddof=1)
    cov_xx = covmat[0, 0]
    cov_yy = covmat[1, 1]
    cov_xy = covmat[0, 1]

    # regression coefficient (rc)
    rc = cov_xy / cov_xx
    # total standard error squared (se)
    se = (cov_yy - (rc**2) * cov_xx) * (nsamp - 1) / (nsamp - 2)
    # standard error on rc (sb)
    sb = _np.sqrt(se / (cov_xx * (nsamp - 1)))
    # error bar on rc
    eb = tcrit * sb

    ssig = True if (_np.abs(rc) - _np.abs(eb)) > 0.0 else False

    return rc, sb, ssig


def ttest(x, y=None, ci=95.0, paired=True, scale=False):
    '''
    Given two samples, perform the Student's t-test and return the errorbar.  The test assumes the sample size be the same between x and y.
    Parameters
    ----------
        x: control
        y: experiment (default: x)
        ci: confidence interval (default: 95%)
        paired: paired t-test (default: True)
        scale: normalize with mean(x) and return as a percentage (default: False)
    Returns
    -------
        diffmean: (normalized) difference in the sample means
        errorbar: (normalized) errorbar with respect to control

    To mask out statistically significant values:\n
    `diffmask = numpy.ma.masked_where(numpy.abs(diffmean)<=errorbar,diffmean).mask`
    '''

    nsamp = x.shape[0]

    if y is None:
        y = x.copy()

    pval = 1.0 - (1.0 - ci / 100.0) / 2.0
    tcrit = _t.ppf(pval, 2*(nsamp-1))

    xmean = _np.nanmean(x, axis=0)
    ymean = _np.nanmean(y, axis=0)

    diffmean = ymean - xmean

    if paired:
        # paired t-test
        std_err = _np.sqrt(_np.nanvar(y-x, axis=0, ddof=1) / nsamp)
    else:
        # unpaired t-test
        std_err = _np.sqrt((_np.nanvar(x, axis=0, ddof=1) +
                            _np.nanvar(y, axis=0, ddof=1)) / (nsamp-1.))

    errorbar = tcrit * std_err

    # normalize (rescale) the diffmean and errorbar
    if scale:
        scale_fac = 100.0 / xmean
        diffmean = diffmean * scale_fac
        errorbar = errorbar * scale_fac

    return diffmean, errorbar


def get_weights(lats):
    '''
    Get weights for latitudes to do weighted mean
    Parameters
    ----------
        lats: Latitudes
    Return
    ------
        weights: weights for latitudes
    '''
    return _np.cos((_np.pi / 180.0) * lats)


def get_weighted_mean(data, weights, axis=None):
    '''
    Given the weights for latitudes, compute weighted mean
    of data in that direction
    Note, `data` and `weights` must be same dimension
    Uses `numpy.average`
    Parameters
    ----------
        data: input data array
        weights: input weights
        axis: direction to compute weighted average
    Returns
    -------
        weighted average: data weighted mean by weights
    '''
    assert data.shape == weights.shape, (
        'data and weights mis-match array size')

    return _np.average(data, weights=weights, axis=axis)


def get_linear_regression(x, y):
    """
    Calculate linear regression between two sets of data.
    Fits a linear model with coefficients to minumize the
    residual sum of squares between the observed targets
    in the dataset, and the targets predicted by the linear
    approximation.

    Parameters
    ----------
        y, x : array like, Data to calculate linear regression

    Returns
    -------
        y_pred : float, Predicted y values of from calculation
        r_sq : float, R squared value
        intercept : float, Intercept from slope intercept equation for y_pred
        slope : float, Slope from slope intercept equation for y_pred
    """
    x = x.reshape((-1, 1))
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    intercept = model.intercept_
    slope = model.coef_[0]
    # This is the same as if you calculated y_pred
    # by y_pred = slope * x + intercept
    y_pred = model.predict(x)
    return y_pred, r_sq, intercept, slope
