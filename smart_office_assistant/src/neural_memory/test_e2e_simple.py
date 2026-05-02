import sys, os, traceback

result_file = os.path.join("d:\\AI\\somn", "e2e_simple.txt")
with open(result_file, "w", encoding="utf-8") as f:
    f.write("START\n")
    f.write(f"Python: {sys.version}\n")
    f.write(f"CWD: {os.getcwd()}\n")
    
    try:
        # Add paths
        src = "d:\\AI\\somn\\smart_office_assistant\\src"
        root = "d:\\AI\\somn"
        sys.path.insert(0, src)
        sys.path.insert(0, root)
        f.write(f"sys.path added: src={src}\n")
        
        # Test 1: import memory_types
        f.write("Test 1: import memory_types...\n")
        from neural_memory.memory_types import MemoryTier, MemoryGrade
        f.write(f"  OK: MemoryTier={len(MemoryTier)}, MemoryGrade={len(MemoryGrade)}\n")
        
        # Test 2: import neural_memory_v2
        f.write("Test 2: import neural_memory_v2...\n")
        from neural_memory.neural_memory_v2 import NeuralMemory
        f.write("  OK: NeuralMemory class imported\n")
        
        # Test 3: instantiate
        f.write("Test 3: instantiate...\n")
        nm = NeuralMemory(use_fast_load=True)
        f.write(f"  OK: {nm}\n")
        
        # Test 4: store
        f.write("Test 4: store...\n")
        rec = nm.store(
            title="Test memory",
            content="This is a test memory for NeuralMemory verification.",
            tags=["test"],
        )
        if rec:
            f.write(f"  OK: id={rec.id}, score={rec.score}, grade={rec.grade}\n")
        else:
            f.write("  FAIL: store returned None\n")
        
        # Test 5: get
        if rec:
            f.write("Test 5: get...\n")
            got = nm.get(rec.id)
            if got:
                f.write(f"  OK: title={got.title}\n")
            else:
                f.write("  FAIL: get returned None\n")
        
        # Test 6: search
        f.write("Test 6: search...\n")
        results = nm.search("test memory", top_k=5)
        f.write(f"  OK: {len(results)} results\n")
        
        # Test 7: encode
        f.write("Test 7: encode...\n")
        vec = nm.encode("test encoding")
        if vec:
            f.write(f"  OK: dim={len(vec)}\n")
        else:
            f.write("  FAIL: encode returned None\n")
        
        # Test 8: stats
        f.write("Test 8: stats...\n")
        stats = nm.get_stats()
        f.write(f"  OK: memories={stats.total_memories}, buffer={stats.buffer_size}\n")
        
        # Test 9: delete
        if rec:
            f.write("Test 9: delete...\n")
            ok = nm.delete(rec.id)
            if ok:
                f.write("  OK: deleted\n")
            else:
                f.write("  FAIL: delete returned False\n")
        
        f.write("\nALL TESTS COMPLETED\n")
        
    except Exception as e:
        f.write(f"\nERROR: {type(e).__name__}: {e}\n")
        f.write(traceback.format_exc())

f.close()
