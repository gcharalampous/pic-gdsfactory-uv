#!/usr/bin/env python3
"""Initialize a new PIC project from the template.

This script renames 'pic_template' to your project name throughout the codebase,
reinitializes git for a clean slate, and prepares the project for development.

Usage:
    python scripts/init.py
    # Follow the prompts to enter your project name
"""

from __future__ import annotations
import re
import shutil
import subprocess
import sys
from pathlib import Path


def validate_project_name(name: str) -> bool:
    """Validate that project name is a valid Python package name.
    
    Parameters
    ----------
    name : str
        Project name to validate
    
    Returns
    -------
    bool
        True if valid Python package name
    """
    # Must start with letter or underscore, contain only alphanumerics and underscores
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, name))


def get_project_name() -> str:
    """Prompt user for project name with validation.
    
    Returns
    -------
    str
        Validated project name (snake_case)
    """
    print("\n" + "=" * 70)
    print("PIC Template Initialization")
    print("=" * 70)
    print("\nThis script will rename the template to your project name.")
    print("Project name should be lowercase with underscores (e.g., my_photonic_design)\n")
    
    while True:
        try:
            name = input("Enter your project name: ").strip()
        except EOFError:
            print("\n❌ No input provided. Aborting.")
            sys.exit(1)
        
        if not name:
            print("❌ Project name cannot be empty")
            continue
        
        if not validate_project_name(name):
            print("❌ Invalid name. Use only letters, numbers, and underscores (start with letter)")
            continue
        
        if name == "pic_template":
            print("❌ Please choose a different name (not 'pic_template')")
            continue
        
        # Confirm
        print(f"\n✓ Project name: {name}")
        try:
            confirm = input("Continue with this name? (y/n): ").strip().lower()
        except EOFError:
            confirm = "y"  # Default to yes if piped
        
        if confirm == "y" or confirm == "":
            return name
        print("Please try again.\n")


def find_files_to_update() -> list[Path]:
    """Find all files that need updating (exclude .git, __pycache__, build).
    
    Returns
    -------
    list[Path]
        List of file paths to update
    """
    root = Path.cwd()
    exclude_dirs = {".git", "__pycache__", ".pytest_cache", "build", ".venv", ".ruff_cache"}
    
    files = []
    for file_path in root.rglob("*"):
        # Skip excluded directories
        if any(excl in file_path.parts for excl in exclude_dirs):
            continue
        
        # Only process files (not directories)
        if not file_path.is_file():
            continue
        
        # Skip binary files
        if file_path.suffix in {".pyc", ".gds", ".lyrdb"}:
            continue
        
        # Include text files likely to contain references
        if file_path.suffix in {
            ".py", ".toml", ".yaml", ".yml", ".md", ".txt", 
            ".sh", ".makefile", "", ".json", ".lock"
        } or file_path.name in {"Makefile", "pyproject.toml", "README.md"}:
            files.append(file_path)
    
    return files


def replace_in_file(file_path: Path, old_name: str, new_name: str) -> bool:
    """Replace old project name with new name in a file.
    
    Parameters
    ----------
    file_path : Path
        File to update
    old_name : str
        Old project name (pic_template)
    new_name : str
        New project name
    
    Returns
    -------
    bool
        True if file was modified
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return False
    
    original_content = content
    
    # Replace pic_template (snake_case)
    content = content.replace(old_name, new_name)
    
    # Replace pic-template (kebab-case) → converted to snake_case with underscores
    kebab_old = old_name.replace("_", "-")
    kebab_new = new_name.replace("_", "-")
    content = content.replace(kebab_old, kebab_new)
    
    # Replace PIC_TEMPLATE (uppercase) if relevant
    content = content.replace(old_name.upper(), new_name.upper())
    
    if content == original_content:
        return False
    
    file_path.write_text(content, encoding="utf-8")
    return True


def rename_directories(old_name: str, new_name: str) -> None:
    """Rename src/pic_template/ to src/{new_name}/.
    
    Parameters
    ----------
    old_name : str
        Old directory name
    new_name : str
        New directory name
    """
    old_src = Path("src") / old_name
    new_src = Path("src") / new_name
    
    if old_src.exists():
        old_src.rename(new_src)
        print(f"✓ Renamed src/{old_name}/ → src/{new_name}/")


def reinit_git() -> None:
    """Remove .git and reinitialize for clean repo."""
    git_dir = Path(".git")
    
    if git_dir.exists():
        shutil.rmtree(git_dir)
        print("✓ Removed old git history")
    
    # Initialize new repo
    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "you@example.com"], check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Your Name"], check=True, capture_output=True)
    
    # Create initial commit
    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True, capture_output=True)
    print("✓ Initialized new git repository")


def main():
    """Run the initialization process."""
    old_name = "pic_template"
    
    # Validate we're in the right directory
    if not Path("scripts/init.py").exists() or not Path("src/pic_template").exists():
        print("❌ Error: This script must be run from the project root directory")
        print("   (where scripts/ and src/ directories exist)")
        sys.exit(1)
    
    # Get project name
    new_name = get_project_name()
    
    print("\n" + "-" * 70)
    print("Starting initialization...\n")
    
    # Find and update files
    files_to_update = find_files_to_update()
    updated_count = 0
    
    for file_path in files_to_update:
        if replace_in_file(file_path, old_name, new_name):
            updated_count += 1
    
    print(f"✓ Updated {updated_count} files")
    
    # Rename directories
    rename_directories(old_name, new_name)
    
    # Reinitialize git
    try:
        reinit_git()
    except subprocess.CalledProcessError as e:
        print(f"⚠ Warning: Git reinitialization incomplete: {e}")
        print("  You can manually run: git init && git add . && git commit -m 'Initial commit'")
    
    print("\n" + "=" * 70)
    print("✓ Initialization Complete!")
    print("=" * 70)
    print(f"\nYour project '{new_name}' is ready for development.")
    print("\nNext steps:")
    print("  1. Update README.md with your project description")
    print(f"  2. Review and customize src/{new_name}/ components")
    print("  3. Start designing: make build && make verify")
    print("  4. Push to your repository")
    print("\n")


if __name__ == "__main__":
    main()
