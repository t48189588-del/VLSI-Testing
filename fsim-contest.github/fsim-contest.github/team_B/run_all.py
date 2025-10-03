import subprocess
from pathlib import Path

bench_dir = Path("data.nogit")
all_output_file = Path("all_out.sp")

with open(all_output_file, "w") as all_out:
    for bench_file in bench_dir.glob("*.bench"):
        name = bench_file.stem  # 例如 c17
        tests_file = bench_dir / f"{name}.tests"
        
        if not tests_file.exists():
            print(f"[SKIP] {tests_file} not found")
            continue
        
        print(f"[RUN] {bench_file} with {tests_file}")
        
        # 先寫個標題分隔方便辨識

        
        subprocess.run(
            ["python", "3_stuck_at_fault_simulator.py", str(bench_file), str(tests_file)],
            stdout=all_out
        )
 
