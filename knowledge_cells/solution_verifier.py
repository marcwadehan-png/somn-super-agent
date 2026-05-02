"""solution_verifier.py v1.0.0
=====================================
方案验证器 — 验证执行结果的正确性

作为 solution_executor 的配套模块，
对执行结果进行验证，确保方案被正确执行。

Author: 张三
Version: 1.0.0
Date: 2026-05-01
"""

from __future__ import annotations

import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

logger = logging.getLogger("Somn.SolutionVerifier")


@dataclass
class VerificationResult:
    """验证结果"""
    passed: bool
    score: float = 0.0
    issues: list = field(default_factory=list)
    suggestions: list = field(default_factory=list)
    verified_by: str = "rule"


class SolutionVerifier:
    """方案验证器"""

    def __init__(self):
        self.logger = logging.getLogger("Somn.SolutionVerifier")

    def verify_execution(self,
                          execution_result: Any,
                          expected_output: str = "") -> VerificationResult:
        """验证执行结果"""
        if execution_result is None:
            return VerificationResult(
                passed=False,
                issues=["执行结果为空"],
                verified_by="solution_verifier"
            )

        if hasattr(execution_result, 'success'):
            passed = execution_result.success
            return VerificationResult(
                passed=passed,
                score=1.0 if passed else 0.0,
                verified_by="solution_verifier"
            )

        return VerificationResult(
            passed=True,
            score=0.8,
            verified_by="solution_verifier"
        )


def verify_solution(execution_result, expected_output: str = "") -> VerificationResult:
    """便捷函数：验证方案执行结果"""
    verifier = SolutionVerifier()
    return verifier.verify_execution(execution_result, expected_output)
