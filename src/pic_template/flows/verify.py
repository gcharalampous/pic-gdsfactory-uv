"""Enhanced verification flow with comprehensive reporting.

This script runs both KLayout DRC and Python geometry checks, then generates
a unified verification report.
"""

from __future__ import annotations
from pathlib import Path
import subprocess
import sys
from pic_template.config import get_config
from pic_template.flows.geometry_check import GeometryChecker
from pic_template.chips.top import top


def run_enhanced_drc(use_enhanced_rules: bool = False) -> dict:
    """Run KLayout DRC with specified ruleset.
    
    Parameters
    ----------
    use_enhanced_rules : bool
        If True, use enhanced DRC rules, otherwise use simple rules
    
    Returns
    -------
    dict
        DRC execution results
    """
    config = get_config()
    drc_config = config["drc"]
    build_config = config["build"]
    gds_config = config["gds"]
    
    # Construct paths
    gds_dir = build_config["gds_dir"]
    gds_filename = gds_config["filename"]
    gds_path = (Path(gds_dir) / gds_filename).resolve()
    
    # Select rules
    if use_enhanced_rules and "enhanced_rules" in drc_config:
        rules_path = Path(drc_config["enhanced_rules"]).resolve()
        report_path = Path("build/reports/drc_enhanced_report.lyrdb").resolve()
        log_path = Path("build/reports/drc_enhanced_run.log").resolve()
    else:
        rules_path = Path(drc_config["rules"]).resolve()
        report_path = Path(drc_config["report"]).resolve()
        log_path = Path(drc_config["log"]).resolve()
    
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check files exist
    if not gds_path.exists():
        return {
            "success": False,
            "error": f"GDS not found: {gds_path}",
            "violations": None
        }
    
    if not rules_path.exists():
        return {
            "success": False,
            "error": f"DRC rules not found: {rules_path}",
            "violations": None
        }
    
    # Run DRC
    cmd = [
        "klayout",
        "-b",
        "-r", str(rules_path),
        "-rd", f"input={gds_path}",
        "-rd", f"report={report_path}",
        "-rd", f"log={log_path}",
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "rules_used": str(rules_path),
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": f"DRC failed: {e}",
            "stdout": e.stdout,
            "stderr": e.stderr
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "klayout not found - is it installed?",
            "violations": None
        }


def run_geometry_checks() -> dict:
    """Run Python geometry verification on top-level chip.
    
    Returns
    -------
    dict
        Geometry check results
    """
    try:
        chip = top()
        checker = GeometryChecker(chip)
        results = checker.run_all_checks(is_top_level=True)  # Top chip may not have ports
        return {
            "success": True,
            "results": results
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def generate_verification_report(drc_results: dict, geometry_results: dict) -> str:
    """Generate unified verification report.
    
    Parameters
    ----------
    drc_results : dict
        DRC check results
    geometry_results : dict
        Geometry check results
    
    Returns
    -------
    str
        Formatted report
    """
    lines = []
    lines.append("=" * 80)
    lines.append("COMPREHENSIVE VERIFICATION REPORT")
    lines.append("=" * 80)
    lines.append("")
    
    # DRC Results
    lines.append("─" * 80)
    lines.append("DRC (Design Rule Check) Results")
    lines.append("─" * 80)
    
    if drc_results["success"]:
        lines.append("✓ DRC completed successfully")
        lines.append(f"  Rules used: {drc_results.get('rules_used', 'N/A')}")
        lines.append(f"  Report: {drc_results.get('report_path', 'N/A')}")
    else:
        lines.append("✗ DRC failed")
        lines.append(f"  Error: {drc_results.get('error', 'Unknown error')}")
    
    lines.append("")
    
    # Geometry Check Results
    lines.append("─" * 80)
    lines.append("Python Geometry Verification Results")
    lines.append("─" * 80)
    
    if geometry_results["success"]:
        results = geometry_results["results"]
        lines.append(f"Component: {results['component_name']}")
        lines.append("")
        lines.append("Checks:")
        
        for check_name, passed in results["checks"].items():
            status = "✓" if passed else "✗"
            lines.append(f"  {status} {check_name}: {'PASS' if passed else 'FAIL'}")
        
        lines.append("")
        
        if results["violations"]:
            lines.append(f"Violations found: {len(results['violations'])}")
            for violation in results["violations"]:
                lines.append(f"  - {violation}")
        else:
            lines.append("✓ No geometry violations found")
        
        lines.append("")
        overall = "PASS" if results["passed"] else "FAIL"
        lines.append(f"Overall: {overall}")
    else:
        lines.append("✗ Geometry checks failed")
        lines.append(f"  Error: {geometry_results.get('error', 'Unknown error')}")
    
    lines.append("")
    lines.append("=" * 80)
    
    return "\n".join(lines)


def main(use_enhanced_drc: bool = False):
    """Run comprehensive verification flow.
    
    Parameters
    ----------
    use_enhanced_drc : bool
        Use enhanced DRC rules instead of simple rules
    """
    print("Running comprehensive verification...")
    print("")
    
    # Run DRC
    print("1. Running DRC...")
    drc_results = run_enhanced_drc(use_enhanced_rules=use_enhanced_drc)
    
    # Run geometry checks
    print("2. Running geometry checks...")
    geometry_results = run_geometry_checks()
    
    # Generate report
    print("")
    report = generate_verification_report(drc_results, geometry_results)
    print(report)
    
    # Save report
    report_path = Path("build/reports/verification_summary.txt")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)
    print(f"\nReport saved to: {report_path}")
    
    # Exit with error if checks failed
    if not drc_results["success"] or not geometry_results["success"]:
        sys.exit(1)
    
    if geometry_results["success"] and not geometry_results["results"]["passed"]:
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run comprehensive PIC verification")
    parser.add_argument("--enhanced", action="store_true", 
                       help="Use enhanced DRC rules")
    args = parser.parse_args()
    
    main(use_enhanced_drc=args.enhanced)
