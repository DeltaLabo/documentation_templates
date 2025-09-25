import os
import json
import shutil
import re

# This script is designed to automate the release process of documentation templates.
# It scans for 'manifest.json' files, and for each template marked for publication,
# it creates a self-contained release package.
#
# The process involves:
# 1. Discovering all templates that have a 'manifest.json' with 'publish' set to true.
# 2. For each of these templates, creating a dedicated release folder.
# 3. Recursively resolving and collecting all dependencies specified in the manifests.
# 4. Copying the dependencies into a 'common' subfolder within the release package,
#    while preserving their original directory structure.
# 5. Copying the template's own files into the release folder.
# 6. Adjusting the relative paths in the template's TeX files to ensure they
#    correctly reference the moved dependencies.
#
# This ensures that each release is a complete, standalone package, ready for distribution.

def find_publishable_manifests(start_dir):
    """
    Finds all manifest.json files starting from a given directory,
    and filters them to include only those with "publish": true.

    Args:
        start_dir (str): The directory to start the search from.

    Returns:
        list: A list of paths to the manifest.json files that should be published.
    """
    manifest_paths = []
    for root, _, files in os.walk(start_dir):
        if 'manifest.json' in files:
            manifest_path = os.path.join(root, 'manifest.json')
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest_data = json.load(f)
                if manifest_data.get('publish') is True:
                    manifest_paths.append(manifest_path)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not read or parse {manifest_path}: {e}")
    return manifest_paths

def resolve_dependencies_recursively(manifest_path, all_dependencies, processed_manifests):
    """
    Recursively resolves all dependencies for a given manifest.

    Args:
        manifest_path (str): The path to the manifest.json file.
        all_dependencies (set): A set to store the paths of all resolved dependencies.
        processed_manifests (set): A set to keep track of already processed manifests to avoid cycles.
    """
    if manifest_path in processed_manifests:
        return
    processed_manifests.add(manifest_path)

    manifest_dir = os.path.dirname(manifest_path)
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not read or parse {manifest_path}: {e}")
        return

    dependencies = manifest_data.get('dependencies', [])
    for dep_path in dependencies:
        # The dependency path is relative to the manifest file.
        # We need to make it an absolute path to work with it.
        abs_dep_path = os.path.abspath(os.path.join(manifest_dir, dep_path))
        all_dependencies.add(abs_dep_path)

        # Now, check if this dependency itself has a manifest file.
        dep_dir = os.path.dirname(abs_dep_path)
        dep_manifest_path = os.path.join(dep_dir, 'manifest.json')

        if os.path.exists(dep_manifest_path):
            resolve_dependencies_recursively(dep_manifest_path, all_dependencies, processed_manifests)

def update_tex_file_paths(file_path):
    """
    Updates relative input paths in a .tex file to point to the new 'common' directory.
    It corrects paths in commands like \documentclass, \input, \include, \subimport,
    and within \graphicspath.

    Args:
        file_path (str): The path to the .tex file to be updated.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # This regex is designed to find paths that start with '../' and contain 'common/'.
        # It captures the LaTeX command and the path separately.
        # It handles commands like \documentclass, \input, \include, \subimport, etc.
        # The path is captured in group 2.
        # It also handles paths inside \graphicspath.
        
        def replace_path(match):
            prefix = match.group(1) or '' # e.g., \documentclass{ or {
            path = match.group(2)
            suffix = match.group(3) or '' # e.g., } or /}

            # The goal is to transform a path like '../../common/some/path'
            # into 'common/some/path'. We can do this by finding the 'common/'
            # substring and taking everything from there.
            if 'common/' in path:
                new_path = path[path.find('common/'):]
                return f"{prefix}{new_path}{suffix}"
            
            # If for some reason 'common/' is not in the path, we don't change it.
            return match.group(0)

        # Regex for commands like \documentclass{...}, \input{...}, \include{...}
        # It looks for a command, then '{', then a path starting with '../' and containing 'common/'.
        content = re.sub(r'(\\(?:documentclass|input|include|subimport)\s*\{)((?:\.\./)+.*?common/.*?/?)(\})', replace_path, content)
        
        # Regex for paths inside \graphicspath{{...}{...}}
        # It looks for paths inside the inner braces.
        content = re.sub(r'(\{)((?:\.\./)+.*?common/.*?)(\})', replace_path, content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    except (IOError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read or update {file_path}: {e}")


def main():
    """
    Main function to run the release generation process.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    release_base_dir = os.path.join(script_dir, 'release')

    # Clean up previous releases if any
    if os.path.exists(release_base_dir):
        shutil.rmtree(release_base_dir)
    os.makedirs(release_base_dir)

    print("Searching for publishable templates...")
    manifests_to_publish = find_publishable_manifests(script_dir)

    if not manifests_to_publish:
        print("No templates found with 'publish: true' in their manifest.json.")
        return

    print(f"Found {len(manifests_to_publish)} templates to publish.")

    for manifest_path in manifests_to_publish:
        source_dir = os.path.dirname(manifest_path)
        template_name = os.path.basename(source_dir)
        release_dir = os.path.join(release_base_dir, template_name)
        
        print(f"\nProcessing template: {template_name}")
        print(f"  - Creating release folder: {release_dir}")
        os.makedirs(release_dir)

        # Create the common folder for dependencies
        release_common_dir = os.path.join(release_dir, 'common')
        os.makedirs(release_common_dir)

        # Resolve all dependencies for this template
        print("  - Resolving dependencies...")
        all_dependencies = set()
        processed_manifests = set()
        resolve_dependencies_recursively(manifest_path, all_dependencies, processed_manifests)
        
        print(f"  - Found {len(all_dependencies)} unique dependencies.")

        # Copy dependencies, preserving structure
        for dep_path in all_dependencies:
            try:
                # Normalize paths for reliable comparison
                normalized_dep_path = os.path.normpath(dep_path)
                normalized_source_dir = os.path.normpath(source_dir)
                common_root = os.path.normpath(os.path.join(script_dir, 'common'))

                if normalized_dep_path.startswith(normalized_source_dir):
                    # This is a local dependency, part of the template's own folder.
                    # It should be copied to the release root.
                    # This check must come first.
                    rel_path = os.path.relpath(normalized_dep_path, normalized_source_dir)
                    dest_path = os.path.join(release_dir, os.path.dirname(rel_path))
                    os.makedirs(dest_path, exist_ok=True)
                    shutil.copy(normalized_dep_path, dest_path)
                elif normalized_dep_path.startswith(common_root):
                    # This is a shared dependency from the global 'common' folder.
                    # It goes into the release's 'common' subfolder.
                    rel_path = os.path.relpath(normalized_dep_path, common_root)
                    dest_path = os.path.join(release_common_dir, os.path.dirname(rel_path))
                    os.makedirs(dest_path, exist_ok=True)
                    shutil.copy(normalized_dep_path, dest_path)
                else:
                    # Handle other cases or log a warning if necessary
                    print(f"Warning: Dependency '{dep_path}' is outside known locations and was not copied.")

            except Exception as e:
                print(f"Warning: Could not copy dependency {dep_path}: {e}")

        # Modify relative imports in the .tex files at the root of the release folder
        print("  - Updating relative paths in .tex files...")
        for item in os.listdir(release_dir):
            if item.endswith('.tex'):
                file_path = os.path.join(release_dir, item)
                update_tex_file_paths(file_path)

        # Clean up empty common folder
        if os.path.exists(release_common_dir) and not os.listdir(release_common_dir):
            print("  - Removing empty common folder.")
            os.rmdir(release_common_dir)
    
    print("\nRelease generation complete.")

if __name__ == "__main__":
    main()
