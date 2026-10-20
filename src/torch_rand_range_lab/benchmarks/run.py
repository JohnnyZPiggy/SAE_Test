"""Numerical oracle and synchronized same-device loop/batch benchmark."""
import argparse
import hashlib
import json
import math
import platform
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

import torch
from torch_rand_range_lab import range_basis, loop_basis, project


def fixture(b, m, n, rank, width, seed=42, kind="exact", dtype=torch.float32):
    g = torch.Generator(device="cpu").manual_seed(seed)
    u = torch.linalg.qr(torch.randn(b, m, rank, generator=g, dtype=dtype)).Q
    v = torch.linalg.qr(torch.randn(b, n, rank, generator=g, dtype=dtype)).Q
    s = (torch.linspace(1, .5, rank, dtype=dtype) if kind == "exact"
         else 1 / torch.arange(1, rank + 1, dtype=dtype).sqrt())
    a = (u * s) @ v.transpose(-2, -1)
    w = torch.randn(b, n, width, generator=g, dtype=dtype)
    return a, w


def sync(device):
    if device.type == "cuda":
        torch.cuda.synchronize(device)


def metrics(a, w):
    q, r = range_basis(a, w), loop_basis(a, w)
    pa, pr = project(a, q), project(a, r)
    denom = torch.linalg.vector_norm(a, dim=(-2, -1)).clamp_min(torch.finfo(a.dtype).tiny)
    residual = torch.linalg.vector_norm(a - pa, dim=(-2, -1)) / denom
    agreement = torch.linalg.vector_norm(pa - pr, dim=(-2, -1)) / denom
    gram = q.transpose(-2, -1) @ q
    orth = (gram - torch.eye(q.shape[-1], device=a.device, dtype=a.dtype)).abs().max()
    assert q.shape == (*a.shape[:-2], a.shape[-2], w.shape[-1])
    assert torch.isfinite(q).all() and torch.isfinite(residual).all()
    assert float(orth) < 3e-5, f"orthogonality {orth}"
    assert float(agreement.max()) < 1e-4, f"projection disagreement {agreement}"
    return {"max_relative_residual": float(residual.max()),
            "max_projection_disagreement": float(agreement.max()),
            "max_orthogonality_error": float(orth)}


def numerical_tests(device):
    torch.manual_seed(42)
    cases = {}
    for seed in (42, 123, 2026):
        a, w = fixture(16, 128, 96, 16, 24, seed)
        result = metrics(a.to(device), w.to(device))
        assert result["max_relative_residual"] <= 1e-3
        cases[f"exact_rank16_seed{seed}"] = result
    a, w = fixture(4, 48, 32, 32, 12, kind="slow")
    cases["slow_full_rank_diagnostic"] = metrics(a.to(device), w.to(device))
    for name, a, w in [
        ("zero", torch.zeros(2, 8, 6), torch.randn(2, 6, 4)),
        ("zero_sketch", torch.randn(2, 8, 6), torch.zeros(2, 6, 4)),
        ("singleton", torch.ones(1, 1, 1), torch.ones(1, 1, 1)),
        ("wide", *fixture(2, 8, 12, 8, 8)),
        ("float64", *fixture(2, 20, 16, 4, 6, dtype=torch.float64)),
    ]:
        cases[name] = metrics(a.to(device), w.to(device))
    a, w = fixture(1, 12, 10, 4, 6)
    cases["single_matrix"] = metrics(a[0].to(device), w[0].to(device))
    for fn in (range_basis, loop_basis):
        assert fn(a[:0].to(device), w[:0].to(device)).shape == (0, 12, 6)
        for bad_a, bad_w in [(a, w[..., :0]), (a, w[..., :9, :]),
                              (a, w.double()), (a, w.expand(2, -1, -1)),
                              (torch.ones(2), torch.ones(2)),
                              (torch.ones(1, 2, 2), torch.ones(1, 2, 3))]:
            try:
                fn(bad_a.to(device), bad_w.to(device))
            except ValueError:
                continue
            raise AssertionError("Invalid input accepted")
    return {"status": "PASS", "cases": cases,
            "edge_contract": "Zero/rank-deficient sketches: finite orthonormal completion; no rank estimate or universal accuracy bound. Nonfinite inputs outside contract."}


def benchmark(device, repeats=7, warmup=2):
    records = []
    for shape in [(16, 128, 96, 16, 24), (16, 512, 256, 32, 40)]:
        a, w = fixture(*shape)
        input_sha = hashlib.sha256(a.numpy().tobytes() + w.numpy().tobytes()).hexdigest()
        a, w = a.to(device), w.to(device)
        check = metrics(a, w)
        assert check["max_relative_residual"] < 1e-3
        samples = {"loop": [], "batched": []}
        first = {}
        for name, fn in [("loop", loop_basis), ("batched", range_basis)]:
            sync(device)
            start = time.perf_counter()
            fn(a, w)
            sync(device)
            first[name] = time.perf_counter() - start
            for _ in range(warmup):
                fn(a, w)
            sync(device)
        # Alternate order so thermal/clock drift does not always favor one form.
        for i in range(repeats):
            order = [("loop", loop_basis), ("batched", range_basis)]
            for name, fn in (order if i % 2 == 0 else order[::-1]):
                sync(device)
                start = time.perf_counter()
                fn(a, w)
                sync(device)
                samples[name].append(time.perf_counter() - start)
        stats = {name: {"median_seconds": statistics.median(v),
                        "min_seconds": min(v), "max_seconds": max(v),
                        "sample_stdev_seconds": statistics.stdev(v),
                        "p95_seconds": sorted(v)[math.ceil(.95 * len(v)) - 1],
                        "samples_seconds": v} for name, v in samples.items()}
        records.append({"shape_B_m_n_rank_width": shape, "seed": 42,
                        "cpu_input_sha256": input_sha, "correctness": check,
                        "first_call_seconds": first, "warmup_runs": warmup,
                        "timed_runs": repeats, "timings": stats,
                        "observed_loop_over_batched_speedup": stats["loop"]["median_seconds"] / stats["batched"]["median_seconds"]})
    return records


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    p.add_argument("--source-sha", required=True)
    p.add_argument("--output", default="result.json")
    p.add_argument("--probe-only", action="store_true")
    args = p.parse_args()
    start = time.perf_counter()
    device = torch.device(args.device)
    torch.set_num_threads(2)
    if device.type == "cuda":
        assert torch.cuda.is_available(), "CUDA unavailable"
        torch.backends.cuda.matmul.allow_tf32 = False
    data = {"status": "FAIL", "source_sha": args.source_sha,
            "classification": ("PROBE_ONLY" if args.probe_only else
                               "EXACT_SHA_EVIDENCE_PENDING_ARCHITECT_REVIEW" if len(args.source_sha) == 40 else "EXPLORE_DIRTY_LOCAL"),
            "utc_start": datetime.now(timezone.utc).isoformat(),
            "environment": {"python": platform.python_version(), "torch": torch.__version__,
                            "device": str(device), "hardware": torch.cuda.get_device_name() if device.type == "cuda" else platform.processor(),
                            "platform": platform.platform(), "cuda": torch.version.cuda,
                            "threads": torch.get_num_threads(), "dtype": "float32", "tf32": False,
                            "compile": "NOT_RUN; eager-only benchmark"},
            "methodology": "CPU-generated inputs, identical Omega; eager QR only timed, projection outside timing; transfer excluded; CUDA synchronized; warmups and first-call separate; same device loop/batch; no fusion claim"}
    try:
        with torch.inference_mode():
            if args.probe_only:
                a, w = fixture(2, 32, 24, 4, 8)
                data["probe"] = metrics(a.to(device), w.to(device))
                assert data["probe"]["max_relative_residual"] < 1e-3
            else:
                data["correctness"] = numerical_tests(device)
                data["benchmark"] = benchmark(device)
            data["status"] = "PASS"
    except Exception as exc:
        data["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        data["elapsed_seconds"] = time.perf_counter() - start
        data["utc_end"] = datetime.now(timezone.utc).isoformat()
        Path(args.output).write_text(json.dumps(data, indent=2) + "\n")
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
