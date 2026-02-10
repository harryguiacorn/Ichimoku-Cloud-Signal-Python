import argparse
import os
import shutil
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--simulate-changes", action="store_true", help="Create a simulated change to commit")
args = parser.parse_args()

repo = os.path.abspath(os.getcwd())
workdir = tempfile.mkdtemp(prefix="ci-dryrun-")
print("Original repo:", repo)
print("Cloning into temporary dir:", workdir)

try:
    # Clone the repo into temp dir
    r = subprocess.run(["git", "clone", repo, workdir], check=True, capture_output=True, text=True)
    print(r.stdout)

    os.chdir(workdir)
    # Ensure we have master branch checked out
    subprocess.run(["git", "checkout", "master"], check=False)

    if args.simulate_changes:
        # Create a simulated change
        fname = os.path.join(workdir, "SIMULATED_CHANGE.txt")
        with open(fname, "w", encoding="utf-8") as f:
            f.write("This is a simulated change for dry-run.\n")
        print("Created simulated change:", fname)

    # Configure git user locally in clone
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
    subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)

    # Stage all
    subprocess.run(["git", "add", "--all"], check=True)

    # Check for staged changes
    diff = subprocess.run(["git", "diff", "--staged", "--name-only"], check=True, capture_output=True, text=True)
    if not diff.stdout.strip():
        print("No changes to commit. Exiting cleanly.")
        sys.exit(0)

    print("Staged changes:\n", diff.stdout)

    # Commit
    commit = subprocess.run(["git", "commit", "-m", "Simulated CI commit - dry run"], capture_output=True, text=True)
    print(commit.stdout)
    if commit.returncode != 0:
        print("Commit failed:\n", commit.stderr)
        sys.exit(commit.returncode)

    # Fetch origin/master
    fetch = subprocess.run(["git", "fetch", "origin", "master"], capture_output=True, text=True)
    print("Fetch output:\n", fetch.stdout, fetch.stderr)

    # Try rebase
    rebase = subprocess.run(["git", "rebase", "origin/master"], capture_output=True, text=True)
    print("Rebase stdout:\n", rebase.stdout)
    if rebase.returncode != 0:
        print("Rebase failed (this simulates a conflict). Aborting rebase and not pushing.")
        subprocess.run(["git", "rebase", "--abort"], check=False)
        print("Would run: git push --force-with-lease origin HEAD:master")
        print("Dry-run: skipping actual push to avoid modifying remotes.")
        sys.exit(0)

    print("Rebase successful (or was fast-forward). Now simulating push with --dry-run:")
    push = subprocess.run(["git", "push", "--dry-run", "origin", "HEAD:master"], capture_output=True, text=True)
    print(push.stdout)
    print(push.stderr)
    print("Dry-run complete. No remote was modified.")

finally:
    try:
        os.chdir(repo)
    except Exception:
        pass
    # Clean up the temp dir
    try:
        shutil.rmtree(workdir)
    except Exception:
        pass
