import sys, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

results = {}


print("[1] SuperWisdomCoordinator...", flush=True)
try:
    from src.intelligence.super_wisdom_coordinator import SuperWisdomCoordinator
    c = SuperWisdomCoordinator()
    results['SuperWisdomCoordinator'] = 'OK'
    print("  OK")
except Exception as e:
    results['SuperWisdomCoordinator'] = 'FAIL: ' + str(e)[:80]
    print(f"  FAIL: {e}")

print("[2] UnifiedIntelligenceCoordinator...", flush=True)
try:
    from src.intelligence.unified_intelligence_coordinator import UnifiedIntelligenceCoordinator
    c = UnifiedIntelligenceCoordinator()
    results['UnifiedIntelligenceCoordinator'] = 'OK'
    print("  OK")
except Exception as e:
    results['UnifiedIntelligenceCoordinator'] = 'FAIL: ' + str(e)[:80]
    print(f"  FAIL: {e}")

print("[3] GlobalWisdomScheduler...", flush=True)
try:
    from src.intelligence.global_wisdom_scheduler import get_scheduler
    s = get_scheduler()
    results['GlobalWisdomScheduler'] = 'OK'
    print("  OK")
except Exception as e:
    results['GlobalWisdomScheduler'] = 'FAIL: ' + str(e)[:80]
    print(f"  FAIL: {e}")

print("[4] ThinkingMethodFusionEngine...", flush=True)
try:
    from src.intelligence.thinking_method_engine import ThinkingMethodFusionEngine
    e = ThinkingMethodFusionEngine()
    results['ThinkingMethodFusionEngine'] = 'OK'
    print("  OK")
except Exception as e:
    results['ThinkingMethodFusionEngine'] = 'FAIL: ' + str(e)[:80]
    print(f"  FAIL: {e}")

print("[5] SomnCore wisdom layers...", flush=True)
try:
    from src.core.somn_core import SomnCore
    core = SomnCore()
    results['SomnCore.super_wisdom'] = 'OK' if core.super_wisdom else 'None(graceful)'
    results['SomnCore.unified_coordinator'] = 'OK' if core.unified_coordinator else 'None(graceful)'
    results['SomnCore.global_wisdom'] = 'OK' if core.global_wisdom else 'None(graceful)'
    results['SomnCore.thinking_engine'] = 'OK' if core.thinking_engine else 'None(graceful)'
    print(f"  super_wisdom: {results['SomnCore.super_wisdom']}")
    print(f"  unified_coordinator: {results['SomnCore.unified_coordinator']}")
    print(f"  global_wisdom: {results['SomnCore.global_wisdom']}")
    print(f"  thinking_engine: {results['SomnCore.thinking_engine']}")
except Exception as e:
    results['SomnCore'] = 'FAIL: ' + str(e)[:80]
    print(f"  FAIL: {e}")

print("[6] _run_wisdom_analysis end-to-end...", flush=True)
try:
    from src.core.somn_core import SomnCore
    core = SomnCore()
    r = core._run_wisdom_analysis(
        description="如何制定SaaS增长策略",
        structured_req={"objective": "提升留存", "task_type": "strategy"},
        context={},
    )
    schools = r.get('activated_schools', [])
    insights = r.get('insights', [])
    recommendations = r.get('recommendations', [])
    results['_run_wisdom_analysis'] = {
        'triggered': r.get('triggered'),
        'schools': schools[:5],
        'source': r.get('source'),
        'insights': insights[:5],
        'insight_count': len(insights),
        'recommendations': recommendations[:3],
    }
    print(f"  triggered={r.get('triggered')}, source={r.get('source')}")
    print(f"  schools: {schools[:5]}")
    print(f"  insights: {insights[:2]}")
    print(f"  recommendations: {recommendations[:2]}")
except Exception as e:
    import traceback
    results['_run_wisdom_analysis'] = 'FAIL: ' + str(e)[:120]
    print(f"  FAIL: {e}")
    traceback.print_exc()

# Write results
out = Path(__file__).parent.parent / 'data' / 'wisdom_diag.json'
out.parent.mkdir(exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nResults written to {out}")
ok_count = sum(1 for v in results.values() if v == 'OK' or (isinstance(v, dict) and v.get('triggered')))
print(f"Summary: {ok_count}/{len(results)} components operational")
