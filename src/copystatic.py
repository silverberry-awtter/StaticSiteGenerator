import os
import shutil

def copy_directory_recursive(source_dir, dest_dir):
    """
    Recursively copies all contents from source_dir into dest_dir.
    Assumes dest_dir already exists.
    """
    if not os.path.exists(dest_dir):
        print(f"Creating directory: {dest_dir}")
        os.mkdir(dest_dir)

    # List all items inside the current source directory
    for item in os.listdir(source_dir):
        src_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            # Log and copy the file
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            # Create the nested directory and recurse into it
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            copy_directory_recursive(src_path, dest_path)


def sync_static_to_public(source_dir="static", dest_dir="public"):
    """
    Cleans the target destination directory and copies everything fresh from source.
    """
    print(f"Cleaning target directory: {dest_dir}...")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    print(f"Creating fresh target directory: {dest_dir}...")
    os.mkdir(dest_dir)

    print(f"Beginning recursive copy from {source_dir} to {dest_dir}...")
    copy_directory_recursive(source_dir, dest_dir)
    print("Sync complete!")
