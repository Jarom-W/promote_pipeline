from pathlib import Path
import sys
import yaml
import subprocess
import os


def run(cmd, cwd):
    """Small wrapper so every git call is deterministic."""
    subprocess.run(cmd, cwd=cwd, check=True)


def main():
    if len(sys.argv) != 3:
        print("Usage: promote.py <source_env> <target_env>")
        sys.exit(1)

    source = sys.argv[1]   # dev
    dest = sys.argv[2]     # staging

    # Always anchor to GitHub workspace
    repo_root = Path(os.environ.get("GITHUB_WORKSPACE", Path.cwd()))

    source_file = repo_root / f"environments/http_service/{source}/http-service.yaml"
    dest_file = repo_root / f"environments/http_service/{dest}/http-service.yaml"

    if not source_file.exists():
        raise FileNotFoundError(f"Source file not found: {source_file}")

    if not dest_file.exists():
        raise FileNotFoundError(f"Destination file not found: {dest_file}")

    # Read source image tag
    with open(source_file) as f:
        source_values = yaml.safe_load(f)

    tag = source_values["image"]["tag"]

    print(f"Promoting image {tag} from {source} → {dest}")

    # Configure git identity
    run(["git", "config", "user.name", "github-actions[bot]"], repo_root)
    run(
        ["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"],
        repo_root
    )

    # Create branch
    branch = f"promote-{source}-to-{dest}-{tag}"

    run(["git", "checkout", "-b", branch], repo_root)

    # Update destination values.yaml
    with open(dest_file) as f:
        dest_values = yaml.safe_load(f)

    dest_values["image"]["tag"] = tag

    with open(dest_file, "w") as f:
        yaml.safe_dump(dest_values, f, sort_keys=False)

    # Commit changes
    run(["git", "add", str(dest_file)], repo_root)
    run(["git", "commit", "-m", f"promote {tag} {source} → {dest}"], repo_root)

    # Push branch
    run(["git", "push", "-u", "origin", branch], repo_root)

    print("\n✅ Promotion complete")
    print(f"Branch: {branch}")
    print(f"Source: {source} → Target: {dest}")
    print(f"Image tag: {tag}")
    print("\nNext step: open PR into main")


if __name__ == "__main__":
    main()
