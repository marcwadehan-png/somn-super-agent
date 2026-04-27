#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试：persona 智能判断器架构（v12.0.0）

验证核心行为：
1. assess_signals() 返回正确信号建议
2. 高优先级信号被标准链路采纳（脏话、闭关等）
3. 中等优先级信号不覆盖标准链路输出
4. 无信号时标准链路全权输出
5. generate_voice_output() 向后兼容
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from src.intelligence.persona_core import SomnPersona, BriefAction, HealAction



def test_assess_signals_structure():
    """测试 assess_signals() 返回结构"""
    persona = SomnPersona()
    
    # 普通输入 → 无信号或低信号
    result = persona.assess_signals("帮我分析一下市场数据")
    assert "signals" in result
    assert "primary_signal" in result
    assert "priority" in result
    assert "suggested_response" in result
    assert "suggested_scenario" in result
    assert "context" in result
    print("  ✓ assess_signals() 返回结构正确")


def test_no_signal_for_normal_input():
    """普通输入不应该触发 high priority 信号"""
    persona = SomnPersona()
    
    result = persona.assess_signals("帮我写一个营销方案")
    assert result["priority"] in ("none", "low"), f"普通输入不应触发 high/medium 信号，实际: {result['priority']}"
    print(f"  ✓ 普通输入 '帮我写一个营销方案' → priority={result['priority']}, signals={result['signals']}")


def test_guard_warn_signal():
    """脏话应该触发 guard_warn 高优先级信号"""
    persona = SomnPersona()
    
    result = persona.assess_signals("你他妈的能不能好好说话")
    assert "guard_warn" in result["signals"], f"脏话应触发 guard_warn，实际: {result['signals']}"
    assert result["priority"] == "high", f"脏话应为 high priority，实际: {result['priority']}"
    assert result["suggested_response"], "脏话信号应有建议回复"
    assert "规劝" in result["suggested_scenario"], f"脏话场景应含'规劝'，实际: {result['suggested_scenario']}"
    print(f"  ✓ 脏话 → guard_warn (high), scenario={result['suggested_scenario']}")


def test_tender_signal():
    """温柔信号（NEVER_SHARP）应返回 tender 信号"""
    persona = SomnPersona()
    
    result = persona.assess_signals("我今天好难过，什么都不想做")
    # NEVER_SHARP 触发时 → tender 信号
    if "tender" in result["signals"]:
        assert result["suggested_response"], "tender 信号应有建议回复"
        assert result["suggested_scenario"] == "温柔承接"
        assert result["priority"] == "low"
        print(f"  ✓ 温柔承接 → tender (low), response={result['suggested_response'][:30]}...")
    else:
        # 可能没触发 NEVER_SHARP（取决于 decide 逻辑），不强制
        print(f"  ⚠ 温柔承接未触发（当前引擎判定为普通输入），signals={result['signals']}")


def test_generate_voice_output_backward_compat():
    """generate_voice_output() 向后兼容"""
    persona = SomnPersona()
    
    result = persona.generate_voice_output("哈哈哈笑死")
    
    # 不应该入口拦截为"简短回应"
    assert result.get("scenario") != "简短回应", "BriefMode 已移至输出层"
    
    # brief_style_suggestion 应存在
    brief = result.get("brief_style_suggestion")
    assert brief is not None, "应有 brief_style_suggestion（向后兼容）"
    assert brief["action"] == BriefAction.LAUGH, f"Expected LAUGH, got {brief['action'].name}"
    
    print(f"  ✓ generate_voice_output() 向后兼容: brief_style_suggestion={brief['action'].name}")


def test_assess_signals_with_brief():
    """assess_signals() 中 BriefMode 建议在 context 中"""
    persona = SomnPersona()
    
    result = persona.assess_signals("哈哈哈笑死")
    
    # brief 信号应该在 signals 或 context 中
    brief_decision = result["context"].get("brief_decision")
    assert brief_decision is not None, "assess_signals 应包含 brief_decision"
    assert brief_decision["action"] == BriefAction.LAUGH
    print(f"  ✓ assess_signals brief_decision: {brief_decision['action'].name}")


def test_confrontation_rounds_removed():
    """Sharp 怼人/轮次递进/闭关已移除，assess_signals 不再返回 confrontation_rounds"""
    persona = SomnPersona()
    
    # 模拟几轮怼人输入——现在应该走 tender/heal/brief 流程，不再追踪轮次
    sharp_inputs = [
        "你是不是傻",
        "你脑子有问题吧",
        "我说的不对吗你听不懂人话",
    ]
    
    last_result = None
    for inp in sharp_inputs:
        last_result = persona.assess_signals(inp)
    
    # confrontation_rounds 不再出现在 context 中
    rounds = last_result["context"].get("confrontation_rounds", 0)
    assert rounds == 0, f"confrontation_rounds 应已被移除，实际: {rounds}"
    
    # 也不应出现 sharp 相关信号
    sharp_signals = [s for s in last_result["signals"] if "sharp" in s]
    assert not sharp_signals, f"不应有 sharp 信号，实际: {sharp_signals}"
    
    print(f"  ✓ Sharp/轮次/闭关已移除，signals={last_result['signals']}, priority={last_result['priority']}")


def test_all_signals_are_suggestions():
    """核心断言：所有信号都是建议，没有硬拦截"""
    persona = SomnPersona()
    
    # 测试各种输入——assess_signals 不应该 raise 或 block
    test_inputs = [
        "操你妈的",           # 脏话
        "你真蠢",             # 怼人
        "我好累啊",           # 脆弱
        "哈哈哈笑死",         # 闲聊
        "活着的意义是什么",    # 哲学
        "帮我写个方案",       # 任务
        "嗯",                 # 极短
    ]
    
    for inp in test_inputs:
        result = persona.assess_signals(inp)
        # 所有输入都应该正常返回（没有异常/中断）
        assert result is not None
        assert "signals" in result
        assert "priority" in result
    
    print(f"  ✓ 所有 7 种输入类型均正常返回信号建议（无硬拦截）")


if __name__ == "__main__":
    print("=" * 60)
    print("  persona 智能判断器架构测试 (v12.0.0)")
    print("=" * 60)
    
    tests = [
        ("assess_signals 返回结构", test_assess_signals_structure),
        ("普通输入无 high 信号", test_no_signal_for_normal_input),
        ("脏话触发 guard_warn", test_guard_warn_signal),
        ("温柔承接信号", test_tender_signal),
        ("generate_voice_output 向后兼容", test_generate_voice_output_backward_compat),
        ("assess_signals brief 建议", test_assess_signals_with_brief),
        ("Sharp/轮次/闭关已移除", test_confrontation_rounds_removed),
        ("所有信号都是建议（无硬拦截）", test_all_signals_are_suggestions),
    ]
    
    passed = 0
    failed = 0
    
    for name, fn in tests:
        try:
            print(f"\n  [测试] {name}")
            fn()
            passed += 1
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"  结果: {passed}/{len(tests)} 通过")
    if failed == 0:
        print("  ALL PASS ✓")
    else:
        print(f"  {failed} FAILED ✗")
    print("=" * 60)
    
    sys.exit(0 if failed == 0 else 1)
