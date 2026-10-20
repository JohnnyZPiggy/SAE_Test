import torch


def _check(a, omega):
    if a.ndim not in (2, 3) or omega.ndim != a.ndim:
        raise ValueError("Expected matching 2-D matrices or 3-D batches")
    if a.shape[-1] != omega.shape[-2] or a.shape[:-2] != omega.shape[:-2]:
        raise ValueError("Matrix and batch dimensions must match; no broadcasting")
    if min(a.shape[-2:]) < 1 or not 1 <= omega.shape[-1] <= min(a.shape[-2:]):
        raise ValueError("Require positive dimensions and 1 <= sketch width <= min(m,n)")
    if a.dtype not in (torch.float32, torch.float64) or omega.dtype != a.dtype:
        raise ValueError("Expected matching float32 or float64 tensors")
    if a.device != omega.device:
        raise ValueError("Expected tensors on the same device")


def range_basis(a, omega):
    """Return reduced QR basis for A Omega, preserving batch dimensions.

    Inputs must be finite. Rank-deficient sketches have nonunique completions;
    this is an orthonormal sketch basis, not a numerical rank estimator.
    """
    _check(a, omega)
    return torch.linalg.qr(a @ omega, mode="reduced").Q


def loop_basis(a, omega):
    """Per-matrix reference, with the identical explicitly supplied sketch."""
    _check(a, omega)
    if a.ndim == 2:
        return torch.linalg.qr(a @ omega, mode="reduced").Q
    if a.shape[0] == 0:
        return a.new_empty((0, a.shape[-2], omega.shape[-1]))
    return torch.stack([torch.linalg.qr(x @ w, mode="reduced").Q
                        for x, w in zip(a, omega)])


def project(a, q):
    return q @ (q.transpose(-2, -1) @ a)
