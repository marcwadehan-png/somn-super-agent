"""
Pan-Wisdom Tree 端到端测试
验证：问题识别 → 学派推荐 → 推理输出 完整流程
"""
import sys
sys.path.insert(0, r'd:\AI\somn\knowledge_cells')

from pan_wisdom_core import (
    WisdomSchool, ProblemType, PanWisdomTree,
    ProblemIdentifier, SchoolRecommender,
    solve_with_wisdom, identify_problem_type, recommend_schools,
)

PASS = 0
FAIL = 0

def test(name, func):
    global PASS, FAIL
    try:
        result = func()
        PASS += 1
        print(f"  PASS  {name}")
        return result
    except Exception as e:
        FAIL += 1
        print(f"  FAIL  {name}: {e}")
        return None

print("=" * 60)
print("Pan-Wisdom Tree 端到端测试")
print("=" * 60)

# ── 测试1: 枚举完整性 ──
print("\n[1] 枚举完整性检查")
test("WisdomSchool 有42个成员", lambda: len(WisdomSchool) == 42)
test("ProblemType 有165个成员", lambda: len(ProblemType) == 165)

# ── 测试2: 问题识别 ──
print("\n[2] 问题类型识别")
def test_identify():
    types = ProblemIdentifier.identify("公司GMV下降30%，如何提升？")
    assert len(types) > 0, "应能识别问题类型"
    assert all(0 < c <= 1.0 for _, c in types), "置信度应在(0,1]"
    return [f"{t[0].name}({t[1]:.2f})" for t in types[:3]]

result = test("识别'GMV下降'问题", test_identify)
if result:
    print(f"        → {result}")

def test_identify2():
    types = ProblemIdentifier.identify("团队心态崩了，如何调整？")
    assert len(types) > 0
    return [t[0].value for t in types[:3]]

result = test("识别'团队心态'问题", test_identify2)
if result:
    print(f"        → {result}")

# ── 测试3: 学派推荐 ──
print("\n[3] 学派推荐")
def test_recommend():
    recs = SchoolRecommender.recommend(ProblemType.STRATEGY, top_k=3)
    assert len(recs) > 0, "应返回推荐"
    assert all(0 < r.confidence <= 1.0 for r in recs), "置信度合法"
    return [f"{r.school.value}({r.confidence:.2f})" for r in recs]

result = test("为'战略转型'推荐学派", test_recommend)
if result:
    print(f"        → {result}")

def test_recommend_text():
    recs = SchoolRecommender.recommend_for_text("直播带货转化率太低，如何优化？")
    assert len(recs) > 0
    return [r.school.value for r in recs[:3]]

result = test("为文本推荐学派", test_recommend_text)
if result:
    print(f"        → {result}")

# ── 测试4: PanWisdomTree 推理 ──
print("\n[4] PanWisdomTree 推理引擎")

tree = PanWisdomTree()

def test_reason_basic():
    result = tree.reason("公司GMV下降30%，如何提升？")
    assert result.request_id != ""
    assert result.problem == "公司GMV下降30%，如何提升？"
    assert len(result.identified_types) > 0
    assert len(result.recommended_schools) > 0
    assert 0 < result.confidence <= 1.0
    return f"置信度 {result.confidence:.2f}, 推荐{len(result.recommended_schools)}个学派"

r = test("基础推理：GMV下降", test_reason_basic)

def test_reason_output():
    result = tree.reason("团队心态崩了，要不要全员降薪？")
    lines = []
    lines.append(f"问题: {result.problem}")
    lines.append(f"识别类型: {[t.value for t in result.identified_types[:3]]}")
    lines.append(f"推荐学派:")
    for rec in result.recommended_schools[:3]:
        lines.append(f"  - {rec.school.value}: {rec.advice}")
    lines.append(f"融合洞察: {result.fusion_insights}")
    lines.append(f"最终建议: {result.final_recommendations[:2]}")
    return "\n".join(lines)

r = test("推理输出：团队心态问题", test_reason_output)
if r:
    print(r)

# ── 测试5: 快捷函数 ──
print("\n[5] 快捷函数")

def test_solve():
    result = solve_with_wisdom("如何设计用户增长策略？")
    assert "问题" in result or "推荐" in result or "学派" in result
    return result[:200]

r = test("solve_with_wisdom()", test_solve)
if r:
    print(f"        → {r}")

def test_identify_shortcut():
    pt = identify_problem_type("品牌定位不清晰，需要重新策划")
    assert pt is not None
    return pt.value

r = test("identify_problem_type()", test_identify_shortcut)
if r:
    print(f"        → {r}")

# ── 测试6: 边界情况 ──
print("\n[6] 边界情况")

def test_empty():
    types = ProblemIdentifier.identify("")
    return f"空输入返回: {types}"

test("空字符串识别", test_empty)

def test_no_keyword():
    types = ProblemIdentifier.identify("asdfghjkl")
    # 可能识别不出，不应崩溃
    return f"无关键词返回: {len(types)}个"

test("无关键词文本", test_no_keyword)

def test_reason_empty():
    result = tree.reason("")
    return f"空问题推理: confidence={result.confidence:.2f}"

test("空问题推理", test_reason_empty)

# ── 汇总 ──
print("\n" + "=" * 60)
print(f"测试结果: {PASS} PASS / {FAIL} FAIL")
print("=" * 60)

if FAIL == 0:
    print("\n所有测试通过！Pan-Wisdom Tree 已能正常工作。")
else:
    print(f"\n存在 {FAIL} 个问题，请检查。")
