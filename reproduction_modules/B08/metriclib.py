"""Frozen pure-Python B08 metric implementation.

This file consolidates the Phase4 RUN02 corrected metric path and the Phase5
robustness/post-hoc metric path without changing their numerical definitions.
"""
from bisect import bisect_right, bisect_left
import hashlib
import math
import struct


def clean_samples(seq, minimum=100):
    out = []
    for x in seq:
        try:
            y = float(x)
        except Exception:
            continue
        if math.isfinite(y):
            out.append(y)
    if len(out) < minimum:
        raise ValueError(f"INSUFFICIENT_FINITE_SAMPLES:{len(out)}")
    return out


def quantile_linear_sorted(s, q):
    if not s:
        raise ValueError("empty")
    h = (len(s) - 1) * q
    lo = int(math.floor(h))
    hi = int(math.ceil(h))
    if lo == hi:
        return float(s[lo])
    f = h - lo
    return float(s[lo] * (1 - f) + s[hi] * f)


def summarize(a):
    s = sorted(clean_samples(a))
    q05 = quantile_linear_sorted(s, 0.05)
    q16 = quantile_linear_sorted(s, 0.16)
    q25 = quantile_linear_sorted(s, 0.25)
    med = quantile_linear_sorted(s, 0.50)
    q75 = quantile_linear_sorted(s, 0.75)
    q84 = quantile_linear_sorted(s, 0.84)
    q95 = quantile_linear_sorted(s, 0.95)
    return {
        "n": len(s),
        "median": med,
        "q16": q16,
        "q84": q84,
        "q05": q05,
        "q95": q95,
        "q25": q25,
        "q75": q75,
        "width68": q84 - q16,
        "width90": q95 - q05,
        "iqr": q75 - q25,
    }


def sample_variance(a):
    n = len(a)
    m = sum(a) / n
    return sum((x - m) ** 2 for x in a) / (n - 1)


def wasserstein_uniform_1d(a, b):
    # Integral |F-G| dx over the union support; equal to scipy.stats.wasserstein_distance
    # for equally weighted one-dimensional empirical samples.
    u = sorted(a)
    v = sorted(b)
    vals = sorted(set(u + v))
    if len(vals) < 2:
        return 0.0
    total = 0.0
    for x0, x1 in zip(vals[:-1], vals[1:]):
        fu = bisect_right(u, x0) / len(u)
        fv = bisect_right(v, x0) / len(v)
        total += abs(fu - fv) * (x1 - x0)
    return total


def paired(a, b):
    a = clean_samples(a)
    b = clean_samples(b)
    sa = summarize(a)
    sb = summarize(b)
    scale = (sa["iqr"] + sb["iqr"]) / 2.0
    if (not math.isfinite(scale)) or scale <= 0:
        scale = math.sqrt((sample_variance(a) + sample_variance(b)) / 2.0)
    scale = max(float(scale), 1e-12)
    den = min(sa["width68"], sb["width68"])
    overlap = None if den <= 0 else max(
        0.0,
        min(sa["q84"], sb["q84"]) - max(sa["q16"], sb["q16"]),
    ) / den
    ratio = None if sa["width68"] <= 0 else sb["width68"] / sa["width68"]
    return {
        "delta_median": sb["median"] - sa["median"],
        "width68_ratio": ratio,
        "normalized_w1": wasserstein_uniform_1d(a, b) / scale,
        "central68_overlap": overlap,
    }


class MT19937:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.index = 624
        self.mt[0] = seed & 0xFFFFFFFF
        for i in range(1, 624):
            self.mt[i] = (
                1812433253 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i
            ) & 0xFFFFFFFF

    def twist(self):
        for i in range(624):
            y = (self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7FFFFFFF)
            self.mt[i] = self.mt[(i + 397) % 624] ^ (y >> 1)
            if y & 1:
                self.mt[i] ^= 0x9908B0DF
        self.index = 0

    def uint32(self):
        if self.index >= 624:
            self.twist()
        y = self.mt[self.index]
        self.index += 1
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        return y & 0xFFFFFFFF

    def random_sample(self):
        a = self.uint32() >> 5
        b = self.uint32() >> 6
        return (a * 67108864.0 + b) / 9007199254740992.0


def official_grid_density_samples(x, y, N=50000, seed=42):
    x = [float(v) for v in x]
    y = [float(v) for v in y]
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("grid shape")
    if any(x[i + 1] <= x[i] for i in range(len(x) - 1)):
        raise ValueError("grid monotonic")
    if any(v < 0 or not math.isfinite(v) for v in y):
        raise ValueError("density")

    trap = 0.0
    for i in range(len(x) - 1):
        trap += (x[i + 1] - x[i]) * (y[i + 1] + y[i]) * 0.5
    if trap <= 0:
        raise ValueError("density norm")
    pdf = [v / trap for v in y]
    cdf = []
    acc = 0.0
    for v in pdf:
        acc += v
        cdf.append(acc)
    last = cdf[-1]
    cdf = [v / last for v in cdf]

    rng = MT19937(seed)
    out = []
    for _ in range(N):
        u = rng.random_sample()
        j = bisect_left(cdf, u)
        if j <= 0:
            i0, i1 = 0, 1
        elif j >= len(cdf):
            i0, i1 = len(cdf) - 2, len(cdf) - 1
        else:
            i0, i1 = j - 1, j
        c0, c1 = cdf[i0], cdf[i1]
        x0, x1 = x[i0], x[i1]
        if c1 == c0:
            val = x0
        else:
            val = x0 + (u - c0) * (x1 - x0) / (c1 - c0)
        out.append(val)
    return out


def sample_digest(a):
    h = hashlib.sha256()
    for x in a:
        h.update(struct.pack("<d", float(x)))
    return h.hexdigest()
