import os

SCHEDULERS = {
    "pct3": ['--scheduler=pct', '--num-switch-points=3'],
    "pct15": ['--scheduler=pct', '--num-switch-points=15'],
    "pos": ['--scheduler=pos'],
    "surw": ['--scheduler=surw'],
    "random": ['--scheduler=random'],
}

FRAY_VERSION = "0.4.4-SNAPSHOT"
FRAY_PATH = os.environ["FRAY_PATH"]
SCRIPT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
PROJECT_PATH = os.path.join(SCRIPT_PATH, "..")
ARTIFACTS_PATH = os.path.join(PROJECT_PATH, "bms")
ASSETS_PATH = os.path.join(SCRIPT_PATH, "assets")
OUTPUT_PATH = os.path.join(PROJECT_PATH, "output")
TOOL_PATH = os.path.join(PROJECT_PATH, "tools")
HELPER_PATH = os.path.join(PROJECT_PATH, "helpers")
RR_PATH = os.path.join(TOOL_PATH, "rr")
JPF_PATH = os.path.join(TOOL_PATH, "jpf-core")
PERF_ITER = 5000
PERF_TRIALS = 10
