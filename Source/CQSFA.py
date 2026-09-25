"""Shared CQSFA/OrbitFinder RESI saddle-point action & amplitude helpers.

Extracted from `Frankenstein_vs_SFA_RESI.ipynb` (originally copied from
`Uniform_Approximation_Test.ipynb` / `Frankenstein_CQSFA_Times.ipynb`) so multiple notebooks can
reuse the same validated implementation of OrbitFinder's uniform approximation
(`ActionAnalytics::getA`/`getMij_C`/`getMij_Q` in `OrbitFinder/ActionAnalytics.cpp`) instead of
duplicating it.
"""
from dataclasses import dataclass

import numpy as np
from scipy.special import jv, kv


@dataclass
class RESIParams:
    """Physical constants shared by all saddle-point action/amplitude functions."""

    omega: float
    Up0: float
    Ip1: float
    Ip2: float
    Ip12: float
    BUMP: float = 1e-4


def f12(p: RESIParams, e1_long, e1_trans, t1, t2):
    """Electron 1's (ionize + rescatter) action, as a function of its own saddle times."""
    p10 = e1_long * np.sqrt(p.Up0)
    p1tr0 = e1_trans * np.sqrt(p.Up0)
    ip10, ip120, ip20 = p.Ip1 / p.omega, p.Ip12 / p.omega, p.Ip2 / p.omega
    sin_t1, sin_2t1, sin_t2 = np.sin(t1), np.sin(2 * t1), np.sin(t2)
    X = (sin_t2 - sin_t1) ** 2 / (t2 - t1)
    return (
        t1 * (p.Up0 + ip10)
        + t2 * (ip20 - ip120 + 0.5 * (p10 ** 2 + p1tr0 ** 2))
        + sin_2t1 * 0.5 * p.Up0 + sin_t2 * 2 * p10 * np.sqrt(p.Up0) + X * 2 * p.Up0
    )


def f3(p: RESIParams, e2_long, e2_trans, t3):
    """Electron 2's (ionize-only, field-driven) action, as a function of its own saddle time."""
    p20 = e2_long * np.sqrt(p.Up0)
    p2tr0 = e2_trans * np.sqrt(p.Up0)
    ip120 = p.Ip12 / p.omega
    return (
        t3 * (0.5 * (p20 ** 2 + p2tr0 ** 2) + p.Up0 + ip120)
        + np.sin(t3) * p20 * np.sqrt(4 * p.Up0) + np.sin(2 * t3) * 0.5 * p.Up0
    )


def hessian_f12(p: RESIParams, e1_long, e1_trans, t1, t2):
    """Finite-difference Hessian of `f12` w.r.t. (t1, t2), matching Action::ddf's numerical mode."""
    S = lambda a, b: f12(p, e1_long, e1_trans, a, b)
    d11 = (S(t1 + p.BUMP, t2) - 2 * S(t1, t2) + S(t1 - p.BUMP, t2)) / p.BUMP ** 2
    d22 = (S(t1, t2 + p.BUMP) - 2 * S(t1, t2) + S(t1, t2 - p.BUMP)) / p.BUMP ** 2
    d12 = (S(t1 + p.BUMP, t2 + p.BUMP) - S(t1 + p.BUMP, t2 - p.BUMP) - S(t1 - p.BUMP, t2 + p.BUMP) + S(t1 - p.BUMP, t2 - p.BUMP)) / (4 * p.BUMP ** 2)
    return d11, d22, d12


def d33_f3(p: RESIParams, e2_long, e2_trans, t3):
    """Finite-difference second derivative of `f3` w.r.t. t3."""
    S = lambda a: f3(p, e2_long, e2_trans, a)
    return (S(t3 + p.BUMP) - 2 * S(t3) + S(t3 - p.BUMP)) / p.BUMP ** 2


def getA_from_e2factor(diff, e2_factor, t1, t2):
    """Same as `getA`, but takes electron 2's own stability contribution (`1/sqrt(-1j*d33)` in the
    Coulomb-free SFA model) directly as a precomputed complex factor, instead of deriving it from
    `d33`. This is what makes it possible to substitute CQSFA_fwd's own native `qPref`/`prefactor`
    (from `Prefactor_Grid`, already Coulomb-corrected) in place of electron 2's stability term:
    `getA(diff, d33, t1, t2) == getA_from_e2factor(diff, 1/np.sqrt(-1j*d33), t1, t2)` exactly,
    since `getA` is separable into an electron-1-only piece and an electron-2-only piece."""
    factor = (2 * np.pi) ** 3
    ts3 = (np.sqrt(1j * (t1 - t2))) ** 3
    e1_factor = factor / (np.sqrt(-diff) * ts3)
    return e1_factor * e2_factor


def getA(diff, d33, t1, t2):
    """Stationary-phase / Hessian-determinant prefactor (ActionAnalytics::getA)."""
    return getA_from_e2factor(diff, 1 / np.sqrt(-1j * d33), t1, t2)


def getdS(X, Y): return 0.5 * (X - Y)
def getdA(X, Y): return 0.5 * (X - 1j * Y)
def getSbar(X, Y): return 0.5 * (X + Y)
def getAbar(X, Y): return 0.5 * (1j * X - Y)


def getMij_C(a1, a2, A1, A2):
    """Uniform approximation, classically-allowed/Stokes side (Bessel J thirds)."""
    dS, dA, Sbar, Abar = getdS(a1, a2), getdA(A1, A2), getSbar(a1, a2), getAbar(A1, A2)
    Rcomp = np.sqrt(2 * np.pi / 3 * dS)
    expS = np.exp(1j * (Sbar + np.pi / 4))
    Bsum = (jv(1 / 3, dS) + jv(-1 / 3, dS)) * dA + (jv(2 / 3, dS) - jv(-2 / 3, dS)) * Abar
    return expS * Bsum * Rcomp


def getMij_Q(a1, a2, A1, A2):
    """Uniform approximation, classically-forbidden/anti-Stokes side (Bessel K thirds)."""
    dS, dA, Sbar, Abar = getdS(a1, a2), getdA(A1, A2), getSbar(a1, a2), getAbar(A1, A2)
    Darg = 1j * dS
    Rcomp = np.sqrt(2 / np.pi * Darg)
    expS = np.exp(1j * Sbar)
    Darg2 = -Darg
    Lpart = Abar * kv(1 / 3, Darg2)
    Rpart = 1j * dA * kv(2 / 3, Darg2)
    return expS * (Lpart + Rpart) * Rcomp


def load_orbit(fname):
    """Load an OrbitFinder `.shortorbit`/`.longorbit` file onto its native (p_long, p_trans) grid."""
    rows = np.loadtxt(fname)
    pl, pt = rows[:, 0], rows[:, 1]
    t1 = rows[:, 2] + 1j * rows[:, 3]
    t2 = rows[:, 4] + 1j * rows[:, 5]
    t3 = rows[:, 6] + 1j * rows[:, 7]
    long_axis = np.unique(np.round(pl, 3))
    trans_axis = np.unique(np.round(pt, 3))
    n = len(long_axis)

    def to_grid(vals):
        g = np.full((n, n), np.nan, dtype=vals.dtype)
        i_idx = np.searchsorted(long_axis, np.round(pl, 3))
        j_idx = np.searchsorted(trans_axis, np.round(pt, 3))
        g[i_idx, j_idx] = vals
        return g

    return long_axis, trans_axis, to_grid(t1), to_grid(t2), to_grid(t3)


@dataclass
class Electron1Times:
    """Electron 1's own precomputed short/long saddle-point quantities (independent of electron 2)."""

    pax: np.ndarray
    tax_half: np.ndarray
    t1_short: np.ndarray
    t2_short: np.ndarray
    t1_long: np.ndarray
    t2_long: np.ndarray
    action_short: np.ndarray
    action_long: np.ndarray
    diff_short: np.ndarray
    diff_long: np.ndarray
    stoke: np.ndarray

    @property
    def n(self) -> int:
        return len(self.pax)

    @property
    def hsize(self) -> int:
        return len(self.tax_half)


def compute_electron1_times(params: RESIParams, pax, tax_half, T1S, T2S, T1L, T2L) -> Electron1Times:
    """Precompute electron 1's short/long action, Hessian-determinant, and Stokes-selection arrays."""
    n, hsize = len(pax), len(tax_half)
    action_short = np.zeros((n, hsize), dtype=complex)
    action_long = np.zeros((n, hsize), dtype=complex)
    diff_short = np.zeros((n, hsize), dtype=complex)
    diff_long = np.zeros((n, hsize), dtype=complex)
    stoke = np.zeros((n, hsize), dtype=bool)

    for i in range(n):
        action_short[i] = f12(params, pax[i], tax_half, T1S[i, :hsize], T2S[i, :hsize])
        action_long[i] = f12(params, pax[i], tax_half, T1L[i, :hsize], T2L[i, :hsize])
        d11s, d22s, d12s = hessian_f12(params, pax[i], tax_half, T1S[i, :hsize], T2S[i, :hsize])
        d11l, d22l, d12l = hessian_f12(params, pax[i], tax_half, T1L[i, :hsize], T2L[i, :hsize])
        diff_short[i] = d11s * d22s - d12s ** 2
        diff_long[i] = d11l * d22l - d12l ** 2
        stoke[i] = (action_short[i] - action_long[i]).real > 0

    return Electron1Times(
        pax=pax, tax_half=tax_half,
        t1_short=T1S[:, :hsize], t2_short=T2S[:, :hsize],
        t1_long=T1L[:, :hsize], t2_long=T2L[:, :hsize],
        action_short=action_short, action_long=action_long,
        diff_short=diff_short, diff_long=diff_long, stoke=stoke,
    )


def compute_M(params: RESIParams, e1: Electron1Times, T0_grid, valid_grid):
    """Complex amplitude combining electron 1's short+long uniform approximation with a SINGLE
    electron-2 time branch (T0_grid), shape (n, n, hsize, hsize). Invalid (uncovered) electron-2
    points contribute exactly 0."""
    n, hsize = e1.n, e1.hsize
    M = np.zeros((n, n, hsize, hsize), dtype=complex)
    for j in range(n):
        t0_col = T0_grid[j, :]
        s3_col = f3(params, e1.pax[j], e1.tax_half, t0_col)
        d33_col = d33_f3(params, e1.pax[j], e1.tax_half, t0_col)
        valid_col = valid_grid[j, :]
        for i in range(n):
            for ii in range(hsize):
                Along_vec = getA(e1.diff_long[i, ii], d33_col, e1.t1_long[i, ii], e1.t2_long[i, ii])
                Ashort_vec = getA(e1.diff_short[i, ii], d33_col, e1.t1_short[i, ii], e1.t2_short[i, ii])
                action_short = e1.action_short[i, ii] + s3_col
                action_long = e1.action_long[i, ii] + s3_col
                if e1.stoke[i, ii]:
                    Mij_row = getMij_C(action_short, action_long, Ashort_vec, Along_vec)
                else:
                    Mij_row = getMij_Q(action_long, action_short, Along_vec, Ashort_vec)
                M[i, j, ii, :] = np.where(valid_col, Mij_row, 0.0)
    return M


def compute_M_native(params: RESIParams, e1: Electron1Times, s2_grid, e2_factor_grid, valid_grid):
    """Same as `compute_M`, but electron 2's ACTION is taken directly from `s2_grid` - CQSFA_fwd's
    own native total action `Stotal` (`Action_Grid`'s St+Sp0+Sv0+Sp+Sv), interpolated onto this
    grid the same way `qPref`/`prefactor` already are - instead of being recomputed via the
    Coulomb-free SFA formula `f3`. This matches the Frankenstein approximation's own definition
    (Eory & Holtmann MSci report, Eq. 5.7: S_FR = S_A + S_CQSFA - electron 2's action term must be
    the FULL CQSFA action, not the plain-SFA propagation term `f3` computes). Electron 2's
    stability/prefactor WEIGHT (`e2_factor_grid`, e.g. native `qPref`/`prefactor`) is unchanged."""
    n, hsize = e1.n, e1.hsize
    M = np.zeros((n, n, hsize, hsize), dtype=complex)
    for j in range(n):
        s3_col = s2_grid[j, :]
        e2_factor_col = e2_factor_grid[j, :]
        valid_col = valid_grid[j, :]
        for i in range(n):
            for ii in range(hsize):
                Along_vec = getA_from_e2factor(e1.diff_long[i, ii], e2_factor_col, e1.t1_long[i, ii], e1.t2_long[i, ii])
                Ashort_vec = getA_from_e2factor(e1.diff_short[i, ii], e2_factor_col, e1.t1_short[i, ii], e1.t2_short[i, ii])
                action_short = e1.action_short[i, ii] + s3_col
                action_long = e1.action_long[i, ii] + s3_col
                if e1.stoke[i, ii]:
                    Mij_row = getMij_C(action_short, action_long, Ashort_vec, Along_vec)
                else:
                    Mij_row = getMij_Q(action_long, action_short, Along_vec, Ashort_vec)
                M[i, j, ii, :] = np.where(valid_col, Mij_row, 0.0)
    return M

