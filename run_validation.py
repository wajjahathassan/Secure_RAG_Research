import sys
import subprocess
import os
import platform


def run_command(command, description):
    print("")
    print(f"[{description}]")
    print(f"Running: {' '.join(command)}")
    try:
        # 'shell=True' should only be used on Windows for internal commands like 'dir' or 'echo' if needed
        # 'shell=False' is safer and cross-platform compatible for python scripts
        subprocess.check_call(command, shell=False)
        print("✅ PASS")
    except subprocess.CalledProcessError:
        print("❌ FAIL")
        sys.exit(1)


def main():
    print("==========================================")
    print("   SECURE RAG - REPRODUCIBILITY SUITE")
    print("==========================================")

    # 1. Setup
    run_command([sys.executable, "-m", "pip", "install", "-r",
                "requirements.txt"], "Setup: Checking Requirements")

    # 2. Synthetic Test
    run_command([sys.executable, "src/experiment.py"],
                "Test 1: Isometry Verification (Synthetic)")

    # 3. Public Data Test
    # Must explicitly add the project root to PYTHONPATH for this subprocess
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()

    print("")
    print("[Test 2: Real-World Validation (MS MARCO)]")
    try:
        subprocess.check_call([sys.executable, "tools/validate_public.py",
                              "--out", "logs/public_report.json"], env=env)
        print("✅ PASS")
    except subprocess.CalledProcessError:
        print("❌ FAIL")
        sys.exit(1)

    # 4. Printing Report
    run_command([sys.executable, "tools/print_report.py",
                "logs/public_report.json"], "Summary Report")

    print("")
    print("[Done] Verification Complete.")


if __name__ == "__main__":
    main()
