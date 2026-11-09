"""Explicit contraction of saved Aer MPS tensors, independently checked."""
import numpy as np


def amplitude(mps, basis_label):
    gammas, lambdas = mps
    vector = np.array([[1 + 0j]])
    for j, gamma in enumerate(gammas):
        vector = vector @ gamma[(basis_label >> j) & 1]
        if j < len(lambdas):
            vector = vector * np.asarray(lambdas[j])[None, :]
    return complex(vector.item())


def norm_squared(mps):
    gammas, lambdas = mps
    transfer = np.array([[1 + 0j]])
    for j, gamma in enumerate(gammas):
        transfer = sum(g.conj().T @ transfer @ g for g in gamma)
        if j < len(lambdas):
            scale = np.asarray(lambdas[j])
            transfer = scale[:, None] * transfer * scale[None, :]
    if abs(transfer.item().imag) > 1e-8:
        raise ValueError("MPS norm acquired a nonnegligible imaginary part")
    return float(transfer.item().real)
