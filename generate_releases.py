#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""
Release generator for documentation templates.

This script finds all folders with manifest.json files that have publish=true,
creates release folders for each, and copies all dependencies recursively
while preserving folder structure and modifying relative import paths.
"""

import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


class ReleaseGenerator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.releases_dir = repo_root / "releases"
        
    def find_manifest_files(self) -> List[Path]:
        """Find all manifest.json files in the repository."""
        manifest_files = []
        for root, dirs, files in os.walk(self.repo_root):
            # Skip .git and releases directories
            if '.git' in Path(root).parts or 'releases' in Path(root).parts:
                continue
            if 'manifest.json' in files:
                manifest_files.append(Path(root) / 'manifest.json')
        return manifest_files
    
    def load_manifest(self, manifest_path: Path) -> Dict:
        """Load and parse a manifest.json file."""
        try:
            with open(manifest_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not load {manifest_path}: {e}")
            return {}
    
    def get_publishable_folders(self) -> List[Tuple[Path, Dict]]:
        """Get all folders with manifest.json files where publish=true."""
        publishable = []
        manifest_files = self.find_manifest_files()
        
        for manifest_path in manifest_files:
            manifest = self.load_manifest(manifest_path)
            if manifest.get('publish', False):
                folder_path = manifest_path.parent
                publishable.append((folder_path, manifest))
        
        return publishable
    
    def validate_dependency_path(self, dep: str, manifest_folder: Path) -> None:
        """Validate that a dependency path is relative to the manifest folder."""
        # Check if the dependency path starts with absolute indicators
        if dep.startswith('/') or (len(dep) > 2 and dep[1] == ':'):
            raise ValueError(
                f"Dependency '{dep}' in manifest at {manifest_folder} uses an absolute path. "
                f"Dependencies must be relative to the manifest.json location."
            )
        
        # Check if the dependency path goes to the project root or uses project-relative paths
        if dep.startswith('common/') or dep.startswith('./common/'):
            raise ValueError(
                f"Dependency '{dep}' in manifest at {manifest_folder} appears to be relative to the project root. "
                f"Dependencies must be relative to the manifest.json location. "
                f"Use '../../../common/...' to reference files in the common directory."
            )

    def resolve_dependencies_recursive(self, folder_path: Path, manifest: Dict, 
                                     resolved: Set[Path]) -> Set[Path]:
        """Recursively resolve all dependencies for a folder."""
        if folder_path in resolved:
            return set()
        
        resolved.add(folder_path)
        all_deps = set()
        
        # Add dependencies from current manifest
        dependencies = manifest.get('dependencies', [])
        for dep in dependencies:
            # Validate that the dependency path is properly formatted
            self.validate_dependency_path(dep, folder_path)
            
            # Resolve relative path from the folder containing the manifest
            dep_path = (folder_path / dep).resolve()
            
            # If the exact path doesn't exist, try adding common file extensions
            if not dep_path.exists():
                for ext in ['.tex', '.cls', '.sty', '.png', '.jpg', '.pdf', '.bib']:
                    dep_path_with_ext = (folder_path / f"{dep}{ext}").resolve()
                    if dep_path_with_ext.exists():
                        dep_path = dep_path_with_ext
                        break
                        
            if dep_path.exists():
                all_deps.add(dep_path)
                
                # Check if this dependency has its own manifest
                dep_folder = dep_path.parent
                dep_manifest_path = dep_folder / 'manifest.json'
                if dep_manifest_path.exists():
                    dep_manifest = self.load_manifest(dep_manifest_path)
                    # Recursively resolve sub-dependencies
                    sub_deps = self.resolve_dependencies_recursive(
                        dep_folder, dep_manifest, resolved
                    )
                    all_deps.update(sub_deps)
            else:
                raise FileNotFoundError(
                    f"Dependency not found: '{dep}' (from manifest at {folder_path}). "
                    f"Ensure the path is correct and relative to the manifest.json location."
                )
        
        return all_deps
    
    def copy_file_to_release(self, src_path: Path, release_folder: Path, 
                           common_folder: Path, source_folder: Path):
        """Copy a file to the release folder, preserving relative structure."""
        # Determine if this should go in common/ or stay in the release root
        try:
            # Check if the source is under the repo root
            rel_path = src_path.relative_to(self.repo_root)
            
            # If the dependency is in the same folder as the main template, 
            # copy it to the release root instead of common/
            if src_path.parent == source_folder:
                dest_path = release_folder / src_path.name
            # If it's in common/, preserve the structure under common/
            elif rel_path.parts[0] == 'common':
                dest_path = common_folder / Path(*rel_path.parts[1:])
            else:
                # Otherwise copy to release root
                dest_path = release_folder / rel_path.name
                
        except ValueError:
            # If we can't make it relative to repo root, just use filename
            dest_path = release_folder / src_path.name
        
        # Create destination directory
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy the file
        shutil.copy2(src_path, dest_path)
        print(f"  Copied: {src_path} -> {dest_path}")
    
    def get_main_file(self, folder_path: Path) -> Path:
        """Get the main file for a folder (same name as folder)."""
        folder_name = folder_path.name
        
        # Look for files with the same name as the folder
        for ext in ['.tex', '.cls', '.sty']:
            main_file = folder_path / f"{folder_name}{ext}"
            if main_file.exists():
                return main_file
        
        # If no main file found, return the first .tex/.cls/.sty file
        for ext in ['.tex', '.cls', '.sty']:
            for file_path in folder_path.glob(f"*{ext}"):
                return file_path
        
        raise FileNotFoundError(f"No main file found in {folder_path}")
    
    def modify_imports_in_file(self, file_path: Path, release_folder: Path):
        """Modify relative import paths in a file to use the release folder as root."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # This is a simplified approach - for a full implementation,
            # you might want to use regex or LaTeX parsing
            # For now, we'll just replace common patterns
            
            # Replace relative paths that go up directories
            import re
            
            # Pattern for \documentclass{../common/...} -> \documentclass{common/...}
            content = re.sub(
                r'\\documentclass\{(\.\./)+common/([^}]*)\}',
                r'\\documentclass{common/\2}',
                content
            )
            
            # Pattern for \subimport{../common/path/}{file} -> \subimport{common/path/}{file}
            content = re.sub(
                r'\\subimport\{(\.\./)+common/([^}]*)/\}\{([^}]*)\}',
                r'\\subimport{common/\2/}{\3}',
                content
            )
            
            # Pattern for \input{../common/path/file} -> \input{common/path/file}
            content = re.sub(
                r'\\input\{(\.\./)+common/([^}]*)\}',
                r'\\input{common/\2}',
                content
            )
            
            # Pattern for \include{../common/path/file} -> \include{common/path/file}
            content = re.sub(
                r'\\include\{(\.\./)+common/([^}]*)\}',
                r'\\include{common/\2}',
                content
            )
            
            # Update \graphicspath entries that reference ../common/
            content = re.sub(
                r'\{(\.\./)+common/([^}]*)\}',
                r'{common/\2}',
                content
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  Modified imports in: {file_path}")
            
        except Exception as e:
            print(f"Warning: Could not modify imports in {file_path}: {e}")
    
    def generate_releases(self):
        """Generate release folders for all publishable templates."""
        # Create releases directory
        if self.releases_dir.exists():
            shutil.rmtree(self.releases_dir)
        self.releases_dir.mkdir()
        
        publishable_folders = self.get_publishable_folders()
        
        print(f"Found {len(publishable_folders)} publishable folders:")
        for folder_path, _ in publishable_folders:
            print(f"  - {folder_path.relative_to(self.repo_root)}")
        
        for folder_path, manifest in publishable_folders:
            folder_name = folder_path.name
            print(f"\nProcessing: {folder_name}")
            
            try:
                # Create release folder
                release_folder = self.releases_dir / folder_name
                release_folder.mkdir()
                
                # Create common folder
                common_folder = release_folder / "common"
                common_folder.mkdir()
                
                # Resolve all dependencies
                resolved = set()
                dependencies = self.resolve_dependencies_recursive(
                    folder_path, manifest, resolved
                )
                
                print(f"  Found {len(dependencies)} dependencies")
            except (ValueError, FileNotFoundError) as e:
                print(f"  ERROR: {e}")
                print(f"  Skipping {folder_name} due to manifest errors.")
                # Remove the partially created folder
                if release_folder.exists():
                    shutil.rmtree(release_folder)
                continue
            
            # Copy main file to release root
            try:
                main_file = self.get_main_file(folder_path)
                main_dest = release_folder / main_file.name
                shutil.copy2(main_file, main_dest)
                print(f"  Copied main file: {main_file} -> {main_dest}")
                
                # Modify imports in main file
                self.modify_imports_in_file(main_dest, release_folder)
                
            except FileNotFoundError as e:
                print(f"  Warning: {e}")
            
            # Copy all dependencies
            for dep_path in dependencies:
                self.copy_file_to_release(dep_path, release_folder, common_folder, folder_path)
            
            # Copy other important files from the source folder
            for file_name in ['README.md', 'test.tex']:
                src_file = folder_path / file_name
                if src_file.exists():
                    dest_file = release_folder / file_name
                    shutil.copy2(src_file, dest_file)
                    print(f"  Copied: {src_file} -> {dest_file}")
                    
                    # Also modify imports in test.tex if it exists
                    if file_name == 'test.tex':
                        self.modify_imports_in_file(dest_file, release_folder)
        
        print(f"\nRelease generation complete! Check the '{self.releases_dir}' folder.")


def main():
    """Main entry point."""
    # Get repository root (directory containing this script)
    script_dir = Path(__file__).parent
    
    generator = ReleaseGenerator(script_dir)
    generator.generate_releases()


if __name__ == "__main__":
    main()