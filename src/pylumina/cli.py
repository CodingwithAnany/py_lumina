"""
pylumina CLI — run simulation scripts from the terminal.

Usage:
    pylumina run simulation.py
    pylumina run simulation.py --output ./results
    pylumina run simulation.py --format vtk
    pylumina run simulation.py --output ./results --format vtk
"""

import argparse
import sys
import os
import runpy


def main():
    parser = argparse.ArgumentParser(
        prog="pylumina",
        description="pylumina — High-performance physics simulation engine",
    )
    subparsers = parser.add_subparsers(dest="command")

    # ── run sub-command ──────────────────────────────────────────
    run_parser = subparsers.add_parser(
        "run",
        help="Run a simulation script",
    )
    run_parser.add_argument(
        "script",
        help="Path to the simulation script (.py)",
    )
    run_parser.add_argument(
        "--output", "-o",
        default="output",
        help="Output directory for exported data (default: ./output)",
    )
    run_parser.add_argument(
        "--format", "-f",
        choices=["hdf5", "vtk"],
        default="hdf5",
        dest="fmt",
        help="Export format: hdf5 or vtk (default: hdf5)",
    )
    run_parser.add_argument(
        "--no-export",
        action="store_true",
        help="Skip auto-export after simulation",
    )

    args = parser.parse_args()

    if args.command != "run":
        parser.print_help()
        print()
        print("Example:")
        print("  pylumina run simulation.py")
        print("  pylumina run simulation.py --output ./results --format vtk")
        sys.exit(1)

    if not os.path.isfile(args.script):
        print(f"Error: file '{args.script}' not found.")
        sys.exit(1)

    # ── run the simulation ───────────────────────────────────────
    print(f"🚀 pylumina — running {args.script}")
    print(f"   output : {os.path.abspath(args.output)}/")
    print(f"   format : {args.fmt}")
    print("─" * 50)

    # Enable recording on the global environment before the script runs
    import pylumina
    pylumina.env.sim.enable_recording()

    # Clean argv so the script sees itself as the main script
    sys.argv = [args.script]
    script_vars = runpy.run_path(args.script, run_name="__main__")

    # ── auto-export ──────────────────────────────────────────────
    if not args.no_export:
        # Try to find a simulation in the script's global variables
        from pylumina import Simulation
        sim = None
        for obj in script_vars.values():
            if isinstance(obj, Simulation) and obj.history:
                sim = obj
                break
        
        # Fallback to the global environment simulation
        if sim is None and pylumina.env.sim.history:
            sim = pylumina.env.sim

        if sim and sim.history:
            history = sim.history
            print()
            print("─" * 50)
            print(f"📦 Exporting {len(history)} frames to {args.fmt.upper()}...")

            result = sim.export(
                output_dir=args.output,
                fmt=args.fmt,
                basename="simulation",
            )

            if isinstance(result, list):
                print(f"   ✅ Wrote {len(result)} files to {args.output}/")
                if len(result) <= 5:
                    for p in result:
                        print(f"      {p}")
                else:
                    print(f"      {result[0]}")
                    print(f"      ...")
                    print(f"      {result[-1]}")
            else:
                print(f"   ✅ Wrote {result}")
        else:
            print()
            print("⚠  No recorded history to export.")
            print("   Tip: call sim.enable_recording() before sim.run()")


if __name__ == "__main__":
    main()
