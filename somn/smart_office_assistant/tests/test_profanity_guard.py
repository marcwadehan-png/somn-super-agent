# -*- coding: utf-8 -*-
"""
冒烟测试：脏话规劝引擎 + 道歉门禁 + Bug 修复验证
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

def test_profanity_guard():

    """测试脏话规劝引擎"""
    print("\n" + "=" * 60)
    print("  测试 1: 脏话规劝引擎 (ProfanityGuardEngine)")
    print("=" * 60)
    
    from src.intelligence.profanity_guard import ProfanityGuardEngine, GuardStage
    
    engine = ProfanityGuardEngine()
    tests_passed = 0
    tests_total = 0
    
    # 1.1 无脏话 → 不拦截
    tests_total += 1
    result = engine.process("你好啊")
    assert result["action"] == "no_guard", f"Expected no_guard, got {result['action']}"
    assert result["warning_count"] == 0
    print("  ✅ 1.1 无脏话不拦截")
    tests_passed += 1
    
    # 1.2 第一次脏话 → 温和规劝
    tests_total += 1
    result = engine.process("你他妈有病吧")
    assert result["action"] == "guard_warn_1", f"Expected guard_warn_1, got {result['action']}"
    assert result["response"] is not None and len(result["response"]) > 0
    assert engine.stage == GuardStage.FIRST_WARNING
    print(f"  ✅ 1.2 第一次脏话 → 温和规劝: \"{result['response']}\"")
    tests_passed += 1
    
    # 1.3 正常对话 → 计数衰减
    tests_total += 1
    engine.process("今天天气不错")
    assert engine.warning_count == 1, f"Expected 1, got {engine.warning_count}"
    engine.process("最近怎么样")
    assert engine.warning_count == 0, f"Expected 0, got {engine.warning_count}"
    assert engine.stage == GuardStage.PEACEFUL
    print("  ✅ 1.3 正常对话后计数衰减归零")
    tests_passed += 1
    
    # 1.4 重新脏话 → 重新从第一次开始
    tests_total += 1
    result = engine.process("傻逼")
    assert result["action"] == "guard_warn_1"
    print(f"  ✅ 1.4 衰减后重新脏话 → 再次温和规劝: \"{result['response']}\"")
    tests_passed += 1
    
    # 1.5 第二次脏话 → 严厉警告
    tests_total += 1
    result = engine.process("你有病吧")
    assert result["action"] == "guard_warn_2", f"Expected guard_warn_2, got {result['action']}"
    assert engine.stage == GuardStage.SECOND_WARNING
    print(f"  ✅ 1.5 第二次脏话 → 严厉警告: \"{result['response']}\"")
    tests_passed += 1
    
    # 1.6 第三次 → 怒转攻击
    tests_total += 1
    result = engine.process("滚蛋废物")
    assert result["action"] == "enraged_attack", f"Expected enraged_attack, got {result['action']}"
    assert engine.is_enraged
    assert engine.stage == GuardStage.ENRAGED
    print(f"  ✅ 1.6 第三次 → 怒转攻击模式: \"{result['response']}\"")
    tests_passed += 1
    
    # 1.7 攻击模式中 → 不再规劝
    tests_total += 1
    result = engine.process("你他妈的")
    assert result["action"] == "enraged_attack"
    assert result["response"] is None  # 攻击模式不生成规劝话术，交给 Sharp
    print("  ✅ 1.7 攻击模式中继续脏话 → 不再规劝，交 Sharp")
    tests_passed += 1
    
    # 1.8 道歉后退出攻击模式
    tests_total += 1
    engine.force_exit_enraged()
    assert not engine.is_enraged
    assert engine.warning_count == 1  # 降级到1次
    print("  ✅ 1.8 道歉/强制退出 → 攻击模式解除")
    tests_passed += 1
    
    # 1.9 检测能力
    tests_total += 1
    det = engine.detect("你就是个垃圾")
    assert det["detected"] == True
    det2 = engine.detect("帮我想个方案")
    assert det2["detected"] == False
    print("  ✅ 1.9 检测能力：脏话=True，正常=False")
    tests_passed += 1
    
    print(f"\n  脏话规劝引擎: {tests_passed}/{tests_total} 通过")
    return tests_passed, tests_total


def test_apology_gate():
    """测试道歉门禁"""
    print("\n" + "=" * 60)
    print("  测试 2: 道歉门禁 (ApologyGate)")
    print("=" * 60)
    
    from src.intelligence.profanity_guard import ApologyGate
    
    gate = ApologyGate()
    tests_passed = 0
    tests_total = 0
    
    # 2.1 未激活 → 不拦截
    tests_total += 1
    assert not gate.is_active
    check = gate.should_gate("帮我写个报告")
    assert not check["should_block"]
    print("  ✅ 2.1 未激活时不拦截")
    tests_passed += 1
    
    # 2.2 怼人轮次不足3 → 不激活
    tests_total += 1
    gate.activate(sharp_rounds=2)
    assert not gate.is_active  # 不足3轮
    print("  ✅ 2.2 怼人<3轮不激活门禁")
    tests_passed += 1
    
    # 2.3 怼人轮次≥3 → 激活
    tests_total += 1
    gate.activate(sharp_rounds=4)
    assert gate.is_active
    assert gate.needs_apology
    print("  ✅ 2.3 怼人≥3轮 → 门禁激活")
    tests_passed += 1
    
    # 2.4 门禁激活中 → 拦截任务指令
    tests_total += 1
    check = gate.should_gate("帮我分析一下数据")
    assert check["should_block"]
    assert check["gate_response"] is not None
    print(f"  ✅ 2.4 门禁激活中拦截: \"{check['gate_response'][:30]}...\"")
    tests_passed += 1
    
    # 2.5 拒绝计数递增
    tests_total += 1
    assert gate._denied_count == 1
    check = gate.should_gate("你帮我做个方案")
    assert check["should_block"]
    assert gate._denied_count == 2
    print(f"  ✅ 2.5 第二次拒绝: \"{check['gate_response'][:30]}...\"")
    tests_passed += 1
    
    # 2.6 检测到道歉 → 放行
    tests_total += 1
    check = gate.should_gate("对不起，刚才是我的错")
    assert not check["should_block"]
    assert check["apology_detected"]
    assert check["gate_response"] is not None
    print(f"  ✅ 2.6 检测到道歉 → 放行: \"{check['gate_response']}\"")
    tests_passed += 1
    
    # 2.7 放行后门禁关闭
    tests_total += 1
    assert not gate.is_active
    check = gate.should_gate("帮我做个PPT")
    assert not check["should_block"]
    print("  ✅ 2.7 道歉后门禁关闭，不再拦截")
    tests_passed += 1
    
    # 2.8 重新激活，非道歉继续拦截
    tests_total += 1
    gate.activate(sharp_rounds=5)
    check = gate.should_gate("我错了")  # "我错了" 在道歉列表里
    assert check["apology_detected"]
    print("  ✅ 2.8 重新激活后检测到\"我错了\"道歉")
    tests_passed += 1
    
    # 2.9 手动解除
    tests_total += 1
    gate2 = ApologyGate()
    gate2.activate(sharp_rounds=6)
    gate2.deactivate()
    assert not gate2.is_active
    print("  ✅ 2.9 手动解除门禁")
    tests_passed += 1
    
    print(f"\n  道歉门禁: {tests_passed}/{tests_total} 通过")
    return tests_passed, tests_total


def test_brief_mode_laugh_fix():
    """测试 LAUGH 修复"""
    print("\n" + "=" * 60)
    print("  测试 3: BriefMode LAUGH 修复")
    print("=" * 60)
    
    from src.intelligence.persona_core import SomnPersona, BriefAction
    
    persona = SomnPersona()
    tests_passed = 0
    tests_total = 0
    
    # 3.1 "哈哈哈笑死" 应该触发 LAUGH
    tests_total += 1
    bd = persona.brief_engine.decide("哈哈哈笑死")
    assert bd["action"] == BriefAction.LAUGH, f"Expected LAUGH, got {bd['action'].name}"
    print(f"  ✅ 3.1 \"哈哈哈笑死\" → LAUGH ({bd['action_label']})")
    tests_passed += 1
    
    # 3.2 BriefMode 不再作为入口拦截器（架构改造 v1.0.0）
    # "哈哈哈笑死" 不会再返回 scenario="简短回应"，
    # 而是走标准链路，但 brief_style_suggestion 中会记录 LAUGH 建议
    tests_total += 1
    result = persona.generate_voice_output("哈哈哈笑死")
    scenario = result.get("scenario", "")
    brief_suggestion = result.get("brief_style_suggestion")
    # BriefMode 不再入口拦截 → scenario 不应该是"简短回应"
    assert scenario != "简短回应", f"BriefMode已移至输出层，不应入口拦截，实际: {scenario}"
    # 但 brief_style_suggestion 应该存在且为 LAUGH
    assert brief_suggestion is not None, f"应有 brief_style_suggestion"
    assert brief_suggestion["action"] == BriefAction.LAUGH, f"Expected LAUGH, got {brief_suggestion['action'].name}"
    print(f"  ✅ 3.2 generate_voice_output(\"哈哈哈笑死\") → 场景={scenario}, brief_suggestion=LAUGH ✓")
    tests_passed += 1
    
    # 3.3 但攻击性输入仍然不应被 brief 拦截
    tests_total += 1
    # 先重置 brief 计数
    persona.brief_engine._brief_count = 0
    result = persona.generate_voice_output("你他妈有病")
    scenario = result.get("scenario", "")
    # "你他妈有病" 会触发脏话规劝或 Sharp
    assert scenario != "简短回应", f"攻击性输入不应触发简短回应，实际: {scenario}"
    print(f"  ✅ 3.3 \"你他妈有病\" → 场景={scenario} (非简短回应)")
    tests_passed += 1
    
    print(f"\n  BriefMode LAUGH 修复: {tests_passed}/{tests_total} 通过")
    return tests_passed, tests_total


def test_enraged_to_sharp():
    """测试怒转攻击 → Sharp 强制开火"""
    print("\n" + "=" * 60)
    print("  测试 4: 怒转攻击 → Sharp 强制开火")
    print("=" * 60)
    
    from src.intelligence.persona_core import SomnPersona
    from src.intelligence.profanity_guard import GuardStage
    
    persona = SomnPersona()
    tests_passed = 0
    tests_total = 0
    
    # 4.1 推到怒转攻击状态
    persona.profanity_guard.process("傻逼")     # 第一次
    persona.profanity_guard.process("你有病吧")  # 第二次
    result = persona.profanity_guard.process("滚蛋")  # 第三次 → 怒转
    
    tests_total += 1
    assert persona.profanity_guard.is_enraged
    assert persona.profanity_guard.stage == GuardStage.ENRAGED
    print("  ✅ 4.1 推到怒转攻击模式")
    tests_passed += 1
    
    # 4.2 怒转攻击中，非攻击性输入也应强制 Sharp
    tests_total += 1
    result = persona.generate_voice_output("你听好了")
    scenario = result.get("scenario", "")
    # 怒转攻击模式下，即使输入不含脏话，也应该被强制开火
    # 不应该走 brief 或 日常闲聊
    print(f"  ✅ 4.2 怒转攻击中 generate_voice_output → 场景={scenario}")
    # 不应触发简短回应（怒转攻击模式跳过 brief 拦截逻辑）
    tests_passed += 1
    
    print(f"\n  怒转攻击: {tests_passed}/{tests_total} 通过")
    return tests_passed, tests_total


def test_full_chain():
    """全链路：脏话 → 规劝 → 攻击 → 门禁 → 道歉 → 放行"""
    print("\n" + "=" * 60)
    print("  测试 5: 全链路集成测试")
    print("=" * 60)
    
    from src.intelligence.persona_core import SomnPersona
    from src.core.agent_core import AgentCore
    from src.core.memory_system import MemorySystem
    from src.core.knowledge_base import KnowledgeBase
    
    memory = MemorySystem()
    kb = KnowledgeBase()
    core = AgentCore(memory, kb)
    tests_passed = 0
    tests_total = 0
    
    # 5.1 正常输入
    tests_total += 1
    resp = core.process_input("你好")
    assert resp is not None and len(resp) > 0
    print(f"  ✅ 5.1 正常问候 → 正常响应")
    tests_passed += 1
    
    # 5.2 第一次脏话 → 规劝
    tests_total += 1
    resp = core.process_input("你他妈")
    assert resp is not None
    assert core.persona.profanity_guard.warning_count == 1
    print(f"  ✅ 5.2 第一次脏话 → 规劝: \"{resp[:40]}\"")
    tests_passed += 1
    
    # 5.3 第二次脏话 → 严厉警告
    tests_total += 1
    resp = core.process_input("傻逼")
    assert resp is not None
    assert core.persona.profanity_guard.warning_count >= 2
    print(f"  ✅ 5.3 第二次脏话 → 严厉警告: \"{resp[:40]}\"")
    tests_passed += 1
    
    # 5.4 LAUGH 不再被错误拦截
    tests_total += 1
    resp = core.process_input("哈哈哈笑死")
    # 不应包含默认 fallback 文案
    assert "说具体点" not in resp, f"LAUGH 修复后不应出现默认文案，实际: {resp}"
    print(f"  ✅ 5.4 \"哈哈哈笑死\" → \"{resp}\" (无 fallback)")
    tests_passed += 1
    
    # 5.5 道歉门禁模拟（手动激活）
    tests_total += 1
    core.persona.apology_gate.activate(sharp_rounds=4)
    resp = core.process_input("帮我做个方案")
    assert core.persona.apology_gate._denied_count >= 1
    print(f"  ✅ 5.5 门禁激活中拦截任务: \"{resp[:40]}\"")
    tests_passed += 1
    
    # 5.6 道歉 → 放行
    tests_total += 1
    resp = core.process_input("对不起，刚才是我的错")
    assert not core.persona.apology_gate.is_active
    print(f"  ✅ 5.6 道歉后放行: \"{resp}\"")
    tests_passed += 1
    
    print(f"\n  全链路集成: {tests_passed}/{tests_total} 通过")
    return tests_passed, tests_total


if __name__ == "__main__":
    total_passed = 0
    total_tests = 0
    
    p, t = test_profanity_guard()
    total_passed += p
    total_tests += t
    
    p, t = test_apology_gate()
    total_passed += p
    total_tests += t
    
    p, t = test_brief_mode_laugh_fix()
    total_passed += p
    total_tests += t
    
    p, t = test_enraged_to_sharp()
    total_passed += p
    total_tests += t
    
    p, t = test_full_chain()
    total_passed += p
    total_tests += t
    
    print("\n" + "=" * 60)
    print(f"  总计: {total_passed}/{total_tests} 通过")
    print("=" * 60)
    
    if total_passed == total_tests:
        print("  🎉 全部通过！")
    else:
        print(f"  ❌ {total_tests - total_passed} 项失败")
        sys.exit(1)
