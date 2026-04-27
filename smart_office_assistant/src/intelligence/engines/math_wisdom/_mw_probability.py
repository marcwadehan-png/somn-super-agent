"""数学智慧核心 - 离散概率引擎"""

import math
from typing import List

from ._mw_dataclasses import ProbabilityAnalysis

__all__ = [
    'bayesian_inference',
    'cross_entropy',
    'entropy',
    'kl_divergence',
    'mutual_information',
]

class DiscreteProbabilityEngine:
    """离散概率引擎 - 贝叶斯推断与信息论"""
    
    # 常用分布参数
    BERNOULLI = "bernoulli"
    BINOMIAL = "binomial"
    POISSON = "poisson"
    GEOMETRIC = "geometric"
    
    @classmethod
    def bayesian_inference(cls, prior: float, likelihood: float, evidence: float) -> ProbabilityAnalysis:
        """
        贝叶斯推断
        
        P(H|E) = P(E|H) × P(H) / P(E)
        
        Args:
            prior: 先验概率 P(H)
            likelihood: 似然 P(E|H)
            evidence: 证据 P(E)
            
        Returns:
            概率分析结果
        """
        if evidence == 0:
            posterior = 0
        else:
            posterior = likelihood * prior / evidence
        
        # 计算贝叶斯因子
        if prior > 0 and (1 - prior) > 0:
            # 简化的贝叶斯因子
            if posterior > 0 and (1 - posterior) > 0:
                bayes_factor = (posterior / (1 - posterior)) / (prior / (1 - prior))
            else:
                bayes_factor = float('inf') if posterior > prior else 0
        else:
            bayes_factor = 1.0
        
        return ProbabilityAnalysis(
            prior_probability=prior,
            likelihood=likelihood,
            posterior_probability=posterior,
            bayes_factor=bayes_factor,
            credible_interval=(max(0, posterior - 0.1), min(1, posterior + 0.1))
        )
    
    @classmethod
    def entropy(cls, probability_distribution: List[float]) -> float:
        """
        计算香农熵
        
        H(X) = -Σ p(x) × log(p(x))
        
        Args:
            probability_distribution: 概率分布
            
        Returns:
            熵值
        """
        h = 0.0
        for p in probability_distribution:
            if p > 0:
                h -= p * math.log2(p)
        return h
    
    @classmethod
    def mutual_information(cls, joint: List[List[float]], 
                          marginal_x: List[float], 
                          marginal_y: List[float]) -> float:
        """
        计算互信息
        
        I(X; Y) = Σ Σ p(x, y) × log(p(x, y) / (p(x) × p(y)))
        
        Args:
            joint: 联合概率分布
            marginal_x: X的边缘分布
            marginal_y: Y的边缘分布
            
        Returns:
            互信息
        """
        mi = 0.0
        for i, pxy in enumerate(joint):
            for j, pxy_i in enumerate(pxy):
                if pxy_i > 0 and marginal_x[i] > 0 and marginal_y[j] > 0:
                    mi += pxy_i * math.log2(pxy_i / (marginal_x[i] * marginal_y[j]))
        return mi
    
    @classmethod
    def kl_divergence(cls, p: List[float], q: List[float]) -> float:
        """
        计算KL散度
        
        D_KL(P || Q) = Σ P(x) × log(P(x) / Q(x))
        
        Args:
            p: 真实分布
            q: 近似分布
            
        Returns:
            KL散度
        """
        kl = 0.0
        for pi, qi in zip(p, q):
            if pi > 0:
                if qi <= 0:
                    return float('inf')
                kl += pi * math.log2(pi / qi)
        return kl
    
    @classmethod
    def cross_entropy(cls, p: List[float], q: List[float]) -> float:
        """
        计算交叉熵
        
        H(P, Q) = -Σ P(x) × log(Q(x))
        
        Args:
            p: 真实分布
            q: 预测分布
            
        Returns:
            交叉熵
        """
        h = 0.0
        for pi, qi in zip(p, q):
            if pi > 0:
                if qi <= 0:
                    return float('inf')
                h -= pi * math.log2(qi)
        return h
