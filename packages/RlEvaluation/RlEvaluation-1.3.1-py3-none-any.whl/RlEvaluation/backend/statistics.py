import numpy as np
import numba as nb
import RlEvaluation._utils.numba as nbu

from scipy.stats import binom
from typing import Any, Callable, List, NamedTuple, Tuple

# ----------------------
# -- Basic Statistics --
# ----------------------

@nbu.njit(inline='always')
def mean(a: np.ndarray, axis: int = 0):
    return np.sum(a, axis=axis) / a.shape[axis]

@nbu.njit(inline='always')
def agg(a: np.ndarray, axis: int = 0):
    return np.sum(a, axis=axis)


# -----------------------------
# -- Statistical Simulations --
# -----------------------------

@nbu.njit
def percentile_bootstrap_ci(
    rng: np.random.Generator,
    a: np.ndarray,
    statistic: Callable[[np.ndarray], Any] = mean,
    alpha: float = 0.05,
    iterations: int = 10000,
):
    bs = np.empty(iterations, dtype=np.float64)

    for i in range(iterations):
        idxs = rng.integers(0, len(a), size=len(a))
        bs[i] = statistic(a[idxs])

    sample_stat = statistic(a)

    lo_b = (alpha / 2)
    hi_b = 1 - (alpha / 2)
    lo, hi = np.percentile(bs, (100 * lo_b, 100 * hi_b))

    return PercentileBootstrapResult(
        sample_stat=sample_stat,
        ci=(lo, hi),
    )


@nbu.njit
def stratified_percentile_bootstrap_ci(
    rng: np.random.Generator,
    a: np.ndarray | List[np.ndarray],
    class_probs: np.ndarray,
    statistic: Callable[[np.ndarray], Any] = mean,
    alpha: float = 0.05,
    iterations: int = 10000,
):
    bs = np.empty(iterations, dtype=np.float64)

    samples = sum([len(sub) for sub in a])
    c_samples = [int(max(1, p * samples)) for p in class_probs]

    # this may not be exactly equal to `samples` due to the max(1, ...)
    sub_samples = sum(c_samples)

    for i in range(iterations):
        sub_data = np.empty(sub_samples, dtype=np.float64)
        acc = 0
        for c in range(len(class_probs)):
            idxs = rng.integers(0, len(a[c]), size=c_samples[c])

            sub_data[acc:acc + c_samples[c]] = a[c][idxs]
            acc += c_samples[c]

        bs[i] = statistic(sub_data)

    sample_stat = bs.mean()
    lo_b = 100 * (alpha / 2)
    hi_b = 100 - 100 * (alpha / 2)
    lo, hi = np.percentile(bs, (lo_b, hi_b))

    return PercentileBootstrapResult(
        sample_stat=sample_stat,
        ci=(lo, hi),
    )


class PercentileBootstrapResult(NamedTuple):
    sample_stat: float
    ci: Tuple[float, float]

# -------------------------
# -- Tolerance Intervals --
# -------------------------

@nbu.njit
def tolerance_interval_curve(
    data: np.ndarray,
    alpha: float = 0.05,
    beta: float = 0.9,
):
    n = data.shape[0]
    l, u = get_tolerance_indices(n, alpha, beta)

    out = np.empty((2, data.shape[1]))

    for i in range(data.shape[1]):
        s = np.sort(data[:, i])

        out[0, i] = s[l]
        out[1, i] = s[u]

    return ToleranceIntervalCurveResult(
        ti=out
    )


class ToleranceIntervalCurveResult(NamedTuple):
    ti: np.ndarray


@nbu.njit
def get_tolerance_indices(n: int, alpha: float, beta: float):
    # we cannot jit compile most things from scipy.stats
    # so perform a callback to the python interpreter to obtain this value
    y = 0.
    with nb.objmode(y='float64'):
        y = ppf(n, alpha, beta)

    nu = int(n - y)

    # figure out indices
    if nu % 2 == 0:
        l = int(nu / 2)
        u = int(n - (nu / 2)) - 1
    else:
        nu1 = (nu / 2) - (1 / 2)
        l = int(nu1)
        u = int(n - (nu1 + 1))

    return l, u

def ppf(n: int, alpha: float, beta: float):
    return binom.ppf(1 - alpha, n, beta)
