from pathlib import Path
import subprocess
import os
import sys
from pic_template.config import get_config

# Load configuration
config = get_config()
drc_config = config["drc"]
gds_config = config["gds"]

GDS = Path(gds_config["top"]).resolve()
RULES = Path(drc_config["rules"]).resolve()
REPORT = Path(drc_config["report"]).resolve()
LOG = Path(drc_config["log"]).resolve()
SUMMARY = Path(drc_config["summary_script"]).resolve()

FAIL_ON_VIOLATIONS = drc_config.get("fail_on_violations", False)


def run():
    if not GDS.exists():
        raise FileNotFoundError(f"GDS not found: {GDS}")
    if not RULES.exists():
        raise FileNotFoundError(f"DRC rules not found: {RULES}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "klayout",
        "-b",
        "-r", str(RULES),
        "-rd", f"input={GDS}",
        "-rd", f"report={REPORT}",
        "-rd", f"log={LOG}",
    ]

    try:
        res = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if res.stdout:
            print(res.stdout, end="")
        if res.stderr:
            print(res.stderr, end="", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print("KLayout DRC failed")
        print("STDOUT:\n" + (e.stdout or ""))
        print("STDERR:\n" + (e.stderr or ""))
        raise

    if not REPORT.exists():
        raise RuntimeError(f"DRC report not created at {REPORT}")

    print(f"✔ DRC finished. Report: {REPORT}")

    if SUMMARY.exists():
        print('Summary exists, running summary script...')
        res = subprocess.run(
            ["klayout", "-b", "-r", str(SUMMARY)],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "REPORT": str(REPORT)},
        )
        # Always show summary output
        if res.stdout:
            print(res.stdout.rstrip())
        if res.stderr:
            print(res.stderr.rstrip(), file=sys.stderr)

        if FAIL_ON_VIOLATIONS and res.returncode != 0:
            # Let CI fail if summary script signals violations (e.g. exit 2)
            sys.exit(res.returncode)


    OPEN = os.environ.get("OPEN", "") not in ("", "0", "false", "False")
    CI = os.environ.get("CI", "") != ""

    # after summary, if violations exist:
    if OPEN and not CI:
        subprocess.Popen(["klayout", str(GDS), "-m", str(REPORT)])




if __name__ == "__main__":
    run()
