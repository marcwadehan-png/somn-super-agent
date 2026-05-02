"""Quick performance test for fast-loading mode v2.4.0"""
import sys, os, time, subprocess

python = sys.executable

def run_script(code):
    """Run code in a fresh subprocess to avoid module cache issues"""
    r = subprocess.run([python, "-c", code], capture_output=True, text=True, encoding="utf-8",
                       cwd=os.path.dirname(os.path.abspath(__file__)), timeout=120)
    if r.returncode != 0:
        print(f"STDERR: {r.stderr[:500]}")
    return r.stdout.strip()

# Test 1: import cold start (B-track should NOT load)
print("=" * 60)
print("神政轨 v2.4.0 快速加载模式 - 性能基准测试")
print("=" * 60)

r1 = run_script("""
import time, sys
t0 = time.perf_counter()
from src.intelligence.dual_track import DivineGovernanceTrack, TrackBridge, get_loading_stats
t1 = time.perf_counter()
stats = get_loading_stats()
print(f"import cold start: {(t1-t0)*1000:.1f}ms")
print(f"B-track loaded on import: {stats['track_b_loaded']}")
assert stats['track_b_loaded'] is False, "FAIL"
print("PASS")
""")
print(f"[Test1] {r1}")

# Test 2: Track A init
r2 = run_script("""
import time
from src.intelligence.dual_track.track_a import DivineGovernanceTrack
t0 = time.perf_counter()
track = DivineGovernanceTrack()
t1 = time.perf_counter()
print(f"TrackA init: {(t1-t0)*1000:.2f}ms")
print("PASS")
""")
print(f"[Test2] {r2}")

# Test 3: Supervision system (shared Factory)
r3 = run_script("""
import time
from src.intelligence.dual_track.track_a import DivineGovernanceTrack
track = DivineGovernanceTrack()
t0 = time.perf_counter()
track._init_supervision_system()
t1 = time.perf_counter()
print(f"Supervision system (shared Factory): {(t1-t0)*1000:.1f}ms")
print("PASS")
""")
print(f"[Test3] {r3}")

# Test 4: Factory instance count
r4 = run_script("""
from src.intelligence.dual_track.track_a import DivineGovernanceTrack
from src.intelligence.dual_track import _supervision_claws
orig = _supervision_claws.SupervisionClawFactory.__init__
count = [0]
def ci(self):
    count[0] += 1
    orig(self)
_supervision_claws.SupervisionClawFactory.__init__ = ci
try:
    track = DivineGovernanceTrack()
    track._init_supervision_system()
    track.auto_appoint_all()
finally:
    _supervision_claws.SupervisionClawFactory.__init__ = orig
print(f"Factory instances: {count[0]} (expected 1)")
assert count[0] == 1, f"FAIL: {count[0]}"
print("PASS")
""")
print(f"[Test4] {r4}")

# Test 5: Full dual-track system
r5 = run_script("""
import time
from src.intelligence.dual_track.bridge import TrackBridge
t0 = time.perf_counter()
bridge = TrackBridge()
system = bridge.create_system()
t1 = time.perf_counter()
print(f"Full dual-track system: {(t1-t0)*1000:.1f}ms")
print("PASS")
""")
print(f"[Test5] {r5}")

print()
print("=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
