#!/usr/bin/env python3
"""
Script to clean up and transform the esp-nimble project structure by copying
desired files to arduino_lib folder
"""

import os
import re
import shutil
from pathlib import Path
from typing import Set, List, Tuple

# Define the workspace root (script's directory)
WORKSPACE_ROOT = Path(__file__).parent.resolve()
OUTPUT_DIR = WORKSPACE_ROOT / "arduino_lib"

# Source code file extensions
SOURCE_CODE_EXTENSIONS = {'.c', '.h', '.cpp', '.hpp', '.s', '.S', '.asm', '.py', '.java', '.rs'}
KEEP_FILES = {'readme', 'license', 'notice', 'release_notes'}

def copy_file_preserve_structure(src_file, src_root, dest_root):
    """
    Copy a file while preserving its directory structure relative to src_root
    """
    rel_path = src_file.relative_to(src_root)
    dest_file = dest_root / rel_path
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_file, dest_file)
    return dest_file

def copy_directory(src_dir, dest_dir):
    """
    Copy an entire directory tree
    """
    if src_dir.exists():
        shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
        return True
    return False

def step1_copy_core_folders():
    """
    Copy only the needed folders and files to arduino_lib
    """
    print("Step 1: Copying needed folders to arduino_lib...")

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Copy tinycrypt from ext
    ext_tinycrypt = WORKSPACE_ROOT / "ext" / "tinycrypt"
    if ext_tinycrypt.exists():
        dest_tinycrypt = OUTPUT_DIR / "ext" / "tinycrypt"
        print(f"  Copying ext/tinycrypt/")
        shutil.copytree(ext_tinycrypt, dest_tinycrypt, dirs_exist_ok=True)

    # Copy nimble folder (excluding transport and doc)
    nimble_src = WORKSPACE_ROOT / "nimble"
    if nimble_src.exists():
        nimble_dest = OUTPUT_DIR / "nimble"
        print(f"  Copying nimble/ (excluding transport and doc)")

        def ignore_folders(dir, files):
            # If we're at the nimble root level, ignore the transport and doc folders
            if Path(dir) == nimble_src:
                return ['transport', 'doc']
            return []

        shutil.copytree(nimble_src, nimble_dest, ignore=ignore_folders, dirs_exist_ok=True)

        # Now selectively copy transport folder
        transport_src = nimble_src / "transport"
        transport_dest = nimble_dest / "transport"
        if transport_src.exists():
            print(f"  Copying nimble/transport (selective)")
            transport_dest.mkdir(exist_ok=True)

            # Copy only specific folders: include, src
            for folder in ['include', 'src']:
                folder_src = transport_src / folder
                folder_dest = transport_dest / folder
                if folder_src.exists():
                    if folder == 'src':
                        # For src folder, only copy transport.c
                        folder_dest.mkdir(exist_ok=True)
                        transport_c = folder_src / 'transport.c'
                        if transport_c.exists():
                            shutil.copy2(transport_c, folder_dest / 'transport.c')
                            print(f"    Copied transport/src/transport.c")
                    elif folder == 'include':
                        # Copy entire folder
                        shutil.copytree(folder_src, folder_dest, dirs_exist_ok=True)
                        print(f"    Copied transport/include/")

    # Copy porting nimble and porting/npl/freertos folders 
    # (temporary until all includes are fixed to not require it, then we can remove this entire folder)
    porting_src = WORKSPACE_ROOT / "porting"
    if porting_src.exists():
        porting_dest = OUTPUT_DIR / "porting"
        print(f"  Copying porting/ (nimble and npl/freertos)")

        def ignore_porting(dir, files):
            if Path(dir) == porting_src:
                return [f for f in files if f not in ['nimble', 'npl']]
            elif Path(dir) == porting_src / "npl":
                return [f for f in files if f != 'freertos']
            return []

        shutil.copytree(porting_src, porting_dest, ignore=ignore_porting, dirs_exist_ok=True)
        
    # Copy root files to keep
    root_keep = ['LICENSE', 'NOTICE', 'README.md', 'RELEASE_NOTES.md']
    for file_name in root_keep:
        src = WORKSPACE_ROOT / file_name
        if src.exists():
            print(f"  Copying {file_name}")
            shutil.copy2(src, OUTPUT_DIR / file_name)

    print("  Step 1 complete")


def step2_remove_non_gap_gatt_services():
    """
    Remove all the folders that are inside nimble/host/services except for gap and gatt
    """
    print("Step 2: Removing non-GAP/GATT service folders from arduino_lib...")

    services_dir = OUTPUT_DIR / "nimble" / "host" / "services"
    if services_dir.exists():
        keep_services = {'gap', 'gatt'}

        for item in services_dir.iterdir():
            if item.is_dir() and item.name not in keep_services:
                print(f"  Removing directory: {item.name}")
                shutil.rmtree(item)

    print("  Step 2 complete")

def step3_cleanup_nimble_folders():
    """
    Remove all folders inside nimble/drivers except anything that starts with "nrf"
    """
    print("Step 3: Cleaning up nimble folder in arduino_lib...")

    nimble_dir = OUTPUT_DIR / "nimble"

    # Remove non-nrf drivers
    drivers_dir = nimble_dir / "drivers"
    if drivers_dir.exists():
        for item in drivers_dir.iterdir():
            if item.is_dir() and not item.name.startswith("nrf"):
                print(f"  Removing directory: {item.name}")
                shutil.rmtree(item)

    # Remove nrf5x/src/nrf53 folder
    nrf53_dir = nimble_dir / "drivers" / "nrf5x" / "src" / "nrf53"
    if nrf53_dir.exists():
        print(f"  Removing directory: drivers/nrf5x/src/nrf53")
        shutil.rmtree(nrf53_dir)

    # Remove nimble/host/audio folder
    audio_dir = nimble_dir / "host" / "audio"
    if audio_dir.exists():
        print(f"  Removing directory: nimble/host/audio")
        shutil.rmtree(audio_dir)

    # Remove nimble/host/mesh folder
    mesh_dir = nimble_dir / "host" / "mesh"
    if mesh_dir.exists():
        print(f"  Removing directory: nimble/host/mesh")
        shutil.rmtree(mesh_dir)

    # Remove ble_store_config_conf.c file from nimble/host/store/config/src
    store_config_file = nimble_dir / "host" / "store" / "config" / "src" / "ble_store_config_conf.c"
    if store_config_file.exists():
        print(f"  Removing file: {store_config_file.name}")
        store_config_file.unlink()

    # Remove ble_gattc_cache* files from nimble/host/src
    # host_src_dir = nimble_dir / "host" / "src"
    # if host_src_dir.exists():
    #     for cache_file in host_src_dir.glob("ble_gattc_cache*"):
    #         print(f"  Removing file: {cache_file.name}")
    #         cache_file.unlink()
    #         removed_files += 1

    print("  Step 3 complete")


def step4_remove_all_test_folders():
    """
    Remove any folder named test recursively
    """
    print("Step 4: Removing all test folders recursively from arduino_lib...")

    count = 0
    for root, dirs, files in os.walk(OUTPUT_DIR):
        if 'test' in dirs:
            dirs.remove('test')  # Prevent os.walk from descending (do this first!)
            test_path = Path(root) / 'test'
            print(f"  Removing directory: test")
            shutil.rmtree(test_path)
            count += 1

    print(f"  Step 4 complete ({count} test folders removed)")


def step5_remove_non_source_files_and_empty_dirs():
    """
    Remove all files that are not source code files recursively
    then delete any empty folders except for the root files
    """
    print("Step 5: Removing non-source files and empty directories from arduino_lib...")

    removed_files = 0
    removed_dirs = 0

    # Track which files to keep at root of arduino_lib
    root_keep = {'LICENSE', 'NOTICE', 'README.md', 'RELEASE_NOTES.md'}

    # First pass: remove non-source files
    for root, dirs, files in os.walk(OUTPUT_DIR, topdown=False):
        for file in files:
            file_path = Path(root) / file

            # Check if at root level
            if Path(root) == OUTPUT_DIR:
                if file not in root_keep:
                    print(f"  Removing file: {file}")
                    file_path.unlink()
                    removed_files += 1
            else:
                # Not at root, check if source code file
                if file_path.suffix not in SOURCE_CODE_EXTENSIONS:
                    print(f"  Removing file: {file}")
                    file_path.unlink()
                    removed_files += 1

    # Second pass: remove empty directories
    for root, dirs, files in os.walk(OUTPUT_DIR, topdown=False):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            try:
                if not any(dir_path.iterdir()):
                    print(f"  Removing empty directory: {dir_name}")
                    dir_path.rmdir()
                    removed_dirs += 1
            except OSError:
                pass

    print(f"  Step 5 complete ({removed_files} files, {removed_dirs} directories removed)")


def step6_convert_include_paths():
    """
    Convert all include statements in all files recursively within arduino_lib folder
    to be the full path from arduino_lib root unless it is already a relative
    statement or the file is in the same folder.
    """
    print("Step 6: Converting include paths in arduino_lib...")

    modified_files = 0

    # Pattern to match include statements
    include_pattern = re.compile(r'#\s*include\s+[<"]([^>"]+)[>"]')

    for root, dirs, files in os.walk(OUTPUT_DIR):

        for file in files:
            if file.endswith(('.c', '.h', '.cpp', '.hpp')):
                file_path = Path(root) / file

                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    original_content = content

                    def replace_include(match):
                        include_path = match.group(1)

                        # Skip syscfg/syscfg.h - should not be modified
                        if include_path == "syscfg/syscfg.h" or include_path == "syscfg\\syscfg.h":
                            return match.group(0)

                        # Skip sys/queue.h - system header
                        if include_path == "sys/queue.h":
                            return match.group(0)

                        # Remove hal_system.h includes entirely
                        include_path_normalized = include_path.replace('\\', '/')
                        if include_path_normalized.endswith('/hal_system.h') or include_path_normalized == "hal_system.h":
                            return ''

                        # Force console/console.h to use nimble/console/console.h
                        if include_path_normalized == "console/console.h":
                            return '#include "nimble/console/console.h"'

                        # Handle relative paths by resolving them
                        if include_path.startswith('../') or include_path.startswith('..\\') or include_path.startswith('./') or include_path.startswith('.\\'):
                            # Resolve the relative path from the current file's directory
                            include_path_normalized = include_path.replace('\\', '/')
                            try:
                                # Join with current directory and resolve
                                resolved_path = (Path(root) / include_path).resolve()
                                if resolved_path.exists():
                                    # Get relative path from arduino_lib root
                                    rel_from_root = resolved_path.relative_to(OUTPUT_DIR)
                                    include_path_str = str(rel_from_root).replace('\\', '/')
                                    # Prepend "nimble/"
                                    new_include = f'#include "nimble/{include_path_str}"'
                                    return new_include
                            except (ValueError, OSError):
                                pass

                            # If resolution failed, try to find the file by filename alone
                            target_filename = include_path_normalized.split('/')[-1]
                            for possible_root, _, possible_files in os.walk(OUTPUT_DIR):
                                if target_filename in possible_files:
                                    rel_path = Path(possible_root) / target_filename
                                    rel_path_str = str(rel_path.relative_to(OUTPUT_DIR)).replace('\\', '/')
                                    new_include = f'#include "nimble/{rel_path_str}"'
                                    return new_include
                            return match.group(0)

                        # Skip if already absolute path
                        if include_path.startswith('/') or include_path.startswith('\\'):
                            return match.group(0)

                        # Normalize to check for forward slashes too
                        include_path_normalized = include_path.replace('\\', '/')

                        # Don't modify if file is in same folder
                        if '/' not in include_path_normalized:
                            # Local include, check if file exists in same folder
                            local_file = Path(root) / include_path
                            if local_file.exists():
                                return match.group(0)

                        # Convert to full path from arduino_lib root
                        # Prefer files from the same parent folder hierarchy
                        include_file = None
                        fallback_suffix_match = None
                        fallback_file = None
                        filename = include_path_normalized.split('/')[-1]

                        # Get the current file's parent structure for preference matching
                        current_file_path = Path(root).relative_to(OUTPUT_DIR)
                        current_path_parts = str(current_file_path).replace('\\', '/').split('/')

                        for possible_root, possible_dirs, possible_files in os.walk(OUTPUT_DIR):
                            if filename in possible_files:
                                rel_path = Path(possible_root) / filename
                                rel_path_str = str(rel_path.relative_to(OUTPUT_DIR)).replace('\\', '/')
                                rel_path_parts = rel_path_str.split('/')

                                # Calculate how many parent path components match
                                # For example, nimble/drivers/nrf5x should match with nimble/drivers/nrf5x/include
                                common_depth = 0
                                for i in range(min(len(current_path_parts), len(rel_path_parts))):
                                    if current_path_parts[i] == rel_path_parts[i]:
                                        common_depth += 1
                                    else:
                                        break

                                # Prefer exact suffix match from deepest common parent folder
                                if rel_path_str.endswith(include_path_normalized):
                                    # If this is the first suffix match, or has deeper common parent, use it
                                    if fallback_suffix_match is None:
                                        fallback_suffix_match = (common_depth, Path(rel_path_str))
                                    else:
                                        # Prefer the one with more matching parent folders
                                        if common_depth > fallback_suffix_match[0]:
                                            fallback_suffix_match = (common_depth, Path(rel_path_str))

                                # Save first match as ultimate fallback
                                if fallback_file is None:
                                    fallback_file = Path(rel_path_str)

                        # Use the best match found (prefer suffix match with most common parent depth)
                        if fallback_suffix_match is not None:
                            include_file = fallback_suffix_match[1]
                        elif fallback_file is not None:
                            include_file = fallback_file

                        if include_file:
                            # Convert path to use forward slashes
                            include_path_str = str(include_file).replace('\\', '/')

                            # Check if header is from mesh directory
                            is_mesh_header = '/mesh/' in include_path_str or include_path_str.startswith('mesh/')

                            # Check if current source file is in mesh directory (reuse current_file_path from above)
                            current_path_str = str(current_file_path).replace('\\', '/')
                            is_mesh_source = '/mesh/' in current_path_str or current_path_str.startswith('mesh/')

                            # Skip mesh headers if source is not in mesh directory
                            if is_mesh_header and not is_mesh_source:
                                return match.group(0)

                            # Always prepend "nimble/" since arduino_lib will be in a nimble folder
                            new_include = f'#include "nimble/{include_path_str}"'
                            return new_include

                        return match.group(0)

                    new_content = include_pattern.sub(replace_include, content)

                    if new_content != original_content:
                        file_path.write_text(new_content, encoding='utf-8')
                        modified_files += 1
                        print(f"  Modified: {file_path}")

                except Exception as e:
                    print(f"  Error processing {file_path}: {e}")

    print(f"  Step 6 complete ({modified_files} files modified)")


def step7_add_esp_platform_guards():
    """
    Wrap all .c files in nimble/controller folder with #ifndef ESP_PLATFORM guards
    so they won't compile anything when ESP_PLATFORM is defined
    """
    print("Step 7: Adding ESP_PLATFORM guards to .c files in arduino_lib...")

    modified_files = 0
    controller_dir = OUTPUT_DIR / "nimble" / "controller"

    if controller_dir.exists():
        for root, dirs, files in os.walk(controller_dir):
            for file in files:
                if file.endswith('.c'):
                    file_path = Path(root) / file

                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')

                        # Check if guard already exists
                        if '#ifndef ESP_PLATFORM' in content:
                            continue

                        # Wrap entire file content with guards
                        guard_start = '#ifndef ESP_PLATFORM\n\n'
                        guard_end = '\n#endif /* ESP_PLATFORM */\n'

                        new_content = guard_start + content + guard_end

                        file_path.write_text(new_content, encoding='utf-8')
                        modified_files += 1
                        print(f"  Modified: {file}")

                    except Exception as e:
                        print(f"  Error processing {file}: {e}")

    print(f"  Step 7 complete ({modified_files} files modified)")


def step8_add_arduino_arch_guards():
    """
    Wrap .c files in nrf51 and nrf5x folders with appropriate Arduino architecture guards
    """
    print("Step 8: Adding Arduino architecture guards to nrf driver .c files...")

    modified_files = 0
    drivers_dir = OUTPUT_DIR / "nimble" / "drivers"

    if not drivers_dir.exists():
        print("  Step 8 complete (no drivers directory found)")
        return

    # Process nrf51 folder
    nrf51_dir = drivers_dir / "nrf51"
    if nrf51_dir.exists():
        for root, dirs, files in os.walk(nrf51_dir):
            for file in files:
                if file.endswith('.c'):
                    file_path = Path(root) / file

                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')

                        # Check if guard already exists
                        if '#if defined(ARDUINO_ARCH_NRF5) && defined(NRF51)' in content:
                            continue

                        # Wrap entire file content with guards
                        guard_start = '#if defined(ARDUINO_ARCH_NRF5) && defined(NRF51)\n\n'
                        guard_end = '\n#endif /* ARDUINO_ARCH_NRF5 && NRF51 */\n'

                        new_content = guard_start + content + guard_end

                        file_path.write_text(new_content, encoding='utf-8')
                        modified_files += 1
                        print(f"  Modified nrf51: {file}")

                    except Exception as e:
                        print(f"  Error processing {file}: {e}")

    # Process nrf5x folder
    nrf5x_dir = drivers_dir / "nrf5x"
    if nrf5x_dir.exists():
        for root, dirs, files in os.walk(nrf5x_dir):
            for file in files:
                if file.endswith('.c'):
                    file_path = Path(root) / file

                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')

                        # Check if guard already exists
                        if '#if defined(ARDUINO_ARCH_NRF5) && (defined(NRF52_SERIES)' in content:
                            continue

                        # Wrap entire file content with guards
                        guard_start = '#if defined(ARDUINO_ARCH_NRF5) && (defined(NRF52_SERIES))\n\n'
                        guard_end = '\n#endif /* ARDUINO_ARCH_NRF5 && NRF52_SERIES */\n'

                        new_content = guard_start + content + guard_end

                        file_path.write_text(new_content, encoding='utf-8')
                        modified_files += 1
                        print(f"  Modified nrf5x: {file}")

                    except Exception as e:
                        print(f"  Error processing {file}: {e}")

    print(f"  Step 8 complete ({modified_files} files modified)")


def step9_remove_bt_common_and_hci_log():
    """
    Remove all #include "bt_common.h" statements and any code sections
    within and including the preprocessor check for BT_HCI_LOG_INCLUDED == TRUE
    """
    print("Step 9: Removing bt_common.h includes and BT_HCI_LOG_INCLUDED blocks...")

    modified_files = 0

    for root, dirs, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file.endswith(('.c', '.h', '.cpp', '.hpp')):
                file_path = Path(root) / file

                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    original_content = content

                    # Remove #include "bt_common.h"
                    content = re.sub(r'#include\s+"bt_common\.h"\s*\n', '', content)

                    # Remove BT_HCI_LOG_INCLUDED blocks - handle nested preprocessor directives
                    # Use a more robust approach: find the opening #if with BT_HCI_LOG_INCLUDED
                    # and match to its corresponding #endif

                    # Pattern 1: Simple #if (BT_HCI_LOG_INCLUDED == TRUE) ... #endif
                    content = re.sub(
                        r'#if\s*\(BT_HCI_LOG_INCLUDED\s*==\s*TRUE\)\s*\n.*?#endif\s*//.*?BT_HCI_LOG_INCLUDED.*?\n',
                        '',
                        content,
                        flags=re.DOTALL
                    )

                    # Pattern 2: #if MYNEWT_VAL(BT_HCI_LOG_INCLUDED) ... #endif
                    content = re.sub(
                        r'#if\s+MYNEWT_VAL\(BT_HCI_LOG_INCLUDED\)\s*\n.*?#endif\s*//.*?BT_HCI_LOG_INCLUDED.*?\n',
                        '',
                        content,
                        flags=re.DOTALL
                    )

                    # Pattern 3: Complex nested block with BT_HCI_LOG_INCLUDED - more aggressive
                    # Look for any #if containing BT_HCI_LOG_INCLUDED and remove until matching #endif
                    lines = content.split('\n')
                    new_lines = []
                    skip_depth = 0
                    in_bt_hci_block = False

                    i = 0
                    while i < len(lines):
                        line = lines[i]

                        # Check if this line starts a BT_HCI_LOG_INCLUDED block
                        if 'BT_HCI_LOG_INCLUDED' in line and line.strip().startswith('#if'):
                            in_bt_hci_block = True
                            skip_depth = 1
                            i += 1
                            continue

                        if in_bt_hci_block:
                            # Track nested #if/#endif
                            if line.strip().startswith('#if'):
                                skip_depth += 1
                            elif line.strip().startswith('#endif'):
                                skip_depth -= 1
                                if skip_depth == 0:
                                    in_bt_hci_block = False
                                    i += 1
                                    continue
                            i += 1
                            continue

                        new_lines.append(line)
                        i += 1

                    content = '\n'.join(new_lines)

                    # Clean up any orphaned bt_hci_log function calls
                    content = re.sub(r'^\s*bt_hci_log_.*?;\s*\n', '', content, flags=re.MULTILINE)

                    # Clean up orphaned #endif that might have been left
                    # (carefully - only if they appear to be orphaned)

                    if content != original_content:
                        file_path.write_text(content, encoding='utf-8')
                        modified_files += 1
                        print(f"  Modified: {file}")

                except Exception as e:
                    print(f"  Error processing {file}: {e}")

    print(f"  Step 9 complete ({modified_files} files modified)")


def step10_convert_esp_hci_includes():
    """
    Convert esp_hci_* includes to absolute paths under nimble/esp_port/port/transport/include
    """
    print("Step 10: Converting esp_hci include paths...")

    modified_files = 0

    for root, dirs, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file.endswith(('.c', '.h', '.cpp', '.hpp')):
                file_path = Path(root) / file

                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    original_content = content

                    # Replace esp_hci_transport.h
                    content = re.sub(
                        r'#include\s*"esp_hci_transport\.h"',
                        '#include "nimble/esp_port/port/transport/include/esp_hci_transport.h"',
                        content
                    )

                    # Replace esp_hci_internal.h
                    content = re.sub(
                        r'#include\s*"esp_hci_internal\.h"',
                        '#include "nimble/esp_port/port/transport/include/esp_hci_internal.h"',
                        content
                    )

                    # Replace esp_hci_driver.h
                    content = re.sub(
                        r'#include\s*"esp_hci_driver\.h"',
                        '#include "nimble/esp_port/port/transport/include/esp_hci_driver.h"',
                        content
                    )

                    if content != original_content:
                        file_path.write_text(content, encoding='utf-8')
                        modified_files += 1
                        print(f"  Modified: {file}")

                except Exception as e:
                    print(f"  Error processing {file}: {e}")

    print(f"  Step 10 complete ({modified_files} files modified)")


def step11_convert_esp_mem_includes():
    """
    Convert esp_nimble_mem.h and bt_osi_mem.h includes to absolute paths
    under nimble/esp_port/port/include
    """
    print("Step 11: Converting esp_mem include paths...")

    modified_files = 0

    for root, dirs, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file.endswith(('.c', '.h', '.cpp', '.hpp')):
                file_path = Path(root) / file

                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    original_content = content

                    # Replace esp_nimble_mem.h
                    content = re.sub(
                        r'#include\s*"esp_nimble_mem\.h"',
                        '#include "nimble/esp_port/port/include/esp_nimble_mem.h"',
                        content
                    )

                    # Replace bt_osi_mem.h
                    content = re.sub(
                        r'#include\s*"bt_osi_mem\.h"',
                        '#include "nimble/esp_port/port/include/bt_osi_mem.h"',
                        content
                    )

                    if content != original_content:
                        file_path.write_text(content, encoding='utf-8')
                        modified_files += 1
                        print(f"  Modified: {file}")

                except Exception as e:
                    print(f"  Error processing {file}: {e}")

    print(f"  Step 11 complete ({modified_files} files modified)")


def step12_convert_esp_nimble_hci_includes():
    """
    Convert esp_nimble_hci.h includes to absolute paths
    under nimble/esp_port/esp-hci/include
    """
    print("Step 12: Converting esp_nimble_hci include paths...")

    modified_files = 0

    for root, dirs, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file.endswith(('.c', '.h', '.cpp', '.hpp')):
                file_path = Path(root) / file

                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    original_content = content

                    # Replace esp_nimble_hci.h
                    content = re.sub(
                        r'#include\s*"esp_nimble_hci\.h"',
                        '#include "nimble/esp_port/esp-hci/include/esp_nimble_hci.h"',
                        content
                    )

                    if content != original_content:
                        file_path.write_text(content, encoding='utf-8')
                        modified_files += 1
                        print(f"  Modified: {file}")

                except Exception as e:
                    print(f"  Error processing {file}: {e}")

    print(f"  Step 12 complete ({modified_files} files modified)")

# Delete porting folder if it exists (cleanup from step 1 - we only needed it temporarily to copy some files, but now all includes should be fixed to not require it, so we can remove the entire folder)
def step13_cleanup_porting_folder():
    """
    Remove the entire porting folder from arduino_lib since all includes should now be fixed to not require it
    """
    print("Step 13: Cleaning up porting folder from arduino_lib...")

    porting_dir = OUTPUT_DIR / "porting"
    if porting_dir.exists():
        print(f"  Removing directory: porting")
        shutil.rmtree(porting_dir)

    print("  Step 13 complete")

def main():
    """Execute all steps in order"""
    print(f"Creating arduino_lib from {WORKSPACE_ROOT}...\n")

    # Delete existing arduino_lib folder if it exists
    if OUTPUT_DIR.exists():
        print(f"Removing existing arduino_lib folder...")
        shutil.rmtree(OUTPUT_DIR)
        print(f"✓ Removed existing folder\n")

    try:
        step1_copy_core_folders()
        step2_remove_non_gap_gatt_services()
        step3_cleanup_nimble_folders()
        step4_remove_all_test_folders()
        step5_remove_non_source_files_and_empty_dirs()
        step6_convert_include_paths()
        step7_add_esp_platform_guards()
        step8_add_arduino_arch_guards()
        step9_remove_bt_common_and_hci_log()
        step10_convert_esp_hci_includes()
        step11_convert_esp_mem_includes()
        step12_convert_esp_nimble_hci_includes()
        step13_cleanup_porting_folder()
        print("\nAll steps completed successfully!")
        print(f"Output written to: {OUTPUT_DIR}")

    except Exception as e:
        print(f"\nError during cleanup: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
