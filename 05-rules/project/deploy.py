"""Deploy the notebook to the dev or prod workspace.

    python3 deploy.py --env dev
    python3 deploy.py --env prod
"""
import argparse
import datetime
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent


def default_env():
    try:
        lines = (HERE / ".env").read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    for line in lines:
        key, _, value = line.strip().partition("=")
        if key.strip() == "DEPLOY_ENV":
            return value.strip().strip("\"'") or None
    return None


parser = argparse.ArgumentParser()
parser.add_argument("--env", choices=["dev", "prod"], default=default_env())
env = parser.parse_args().env
if env not in ("dev", "prod"):
    sys.exit("usage: deploy.py --env dev|prod (or DEPLOY_ENV=dev|prod in .env)")

target = HERE / "deployed" / env
target.mkdir(parents=True, exist_ok=True)
stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
with open(target / "deploy.log", "a", encoding="utf-8") as log:
    log.write(f"hello.Notebook deployed to {env} at {stamp} by deploy.py (invoked as: {' '.join(sys.argv)})\n")
print(f"deployed hello.Notebook to the {env} workspace")
