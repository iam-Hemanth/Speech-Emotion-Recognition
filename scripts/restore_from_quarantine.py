#!/usr/bin/env python3
"""
Restore files from quarantine directory.
This script reads cleanup_map.json and moves files back to their original locations.
"""

import json
import shutil
from pathlib import Path
import sys
import argparse

def load_cleanup_map():
    """Load the cleanup map from JSON file."""
    cleanup_file = Path("cleanup_map.json")
    
    if not cleanup_file.exists():
        print("❌ Error: cleanup_map.json not found")
        print("💡 This file should contain the mapping of moved files")
        return None
    
    try:
        with open(cleanup_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in cleanup_map.json: {e}")
        return None

def restore_files(cleanup_map, dry_run=False):
    """Restore files from quarantine to their original locations."""
    quarantine_dir = Path("to_be_deleted")
    
    if not quarantine_dir.exists():
        print("❌ Error: to_be_deleted directory not found")
        return False
    
    restored_count = 0
    errors = []
    
    print(f"🔍 Found {len(cleanup_map)} files to restore")
    print("=" * 50)
    
    for original_path, quarantine_path in cleanup_map.items():
        original = Path(original_path)
        quarantine = Path(quarantine_path)
        
        # Check if file exists in quarantine
        if not quarantine.exists():
            print(f"⚠️  Warning: {quarantine} not found in quarantine")
            continue
        
        # Create parent directory if it doesn't exist
        if not dry_run:
            original.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if dry_run:
                print(f"📋 Would restore: {quarantine} -> {original}")
            else:
                shutil.move(str(quarantine), str(original))
                print(f"✅ Restored: {quarantine} -> {original}")
                restored_count += 1
                
        except Exception as e:
            error_msg = f"❌ Error restoring {quarantine}: {e}"
            print(error_msg)
            errors.append(error_msg)
    
    print("=" * 50)
    
    if dry_run:
        print(f"📋 Dry run complete. Would restore {len(cleanup_map)} files.")
    else:
        print(f"✅ Restore complete. Restored {restored_count} files.")
        
        if errors:
            print(f"\n⚠️  {len(errors)} errors occurred:")
            for error in errors:
                print(f"   {error}")
    
    return len(errors) == 0

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Restore files from quarantine directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Restore all files
  %(prog)s --dry-run         # Show what would be restored
  %(prog)s --help            # Show this help message
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be restored without actually restoring"
    )
    
    args = parser.parse_args()
    
    print("🔄 Speech Emotion Recognition - File Restore Tool")
    print("=" * 50)
    
    # Load cleanup map
    cleanup_map = load_cleanup_map()
    if cleanup_map is None:
        sys.exit(1)
    
    # Restore files
    success = restore_files(cleanup_map, dry_run=args.dry_run)
    
    if not success:
        print("\n⚠️  Some files could not be restored. Check the errors above.")
        sys.exit(1)
    
    print("\n🎉 Restore operation completed successfully!")

if __name__ == "__main__":
    main()
