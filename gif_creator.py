import os
import sys
import shutil
from datetime import datetime
import subprocess
from tqdm import tqdm


def get_capture_time(file_path):
    cmd = ["exiftool", "-DateTimeOriginal", file_path]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = proc.communicate()

    if proc.returncode != 0:
        raise ValueError(f"Error reading EXIF data for {file_path}")

    date_time_str = stdout.decode().split(": ")[-1].strip()
    return datetime.strptime(date_time_str, "%Y:%m:%d %H:%M:%S")


def process_images(output_path, folder_path):
    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(".cr3")
    ]
    files.sort(key=os.path.getmtime)

    print(f"Processing {len(files)} images...")

    gif_counter = 0
    current_sequence = []
    prev_time = None

    main_folder = os.path.join(output_path, "GIFs")
    os.makedirs(main_folder, exist_ok=True)

    raw_gif_folder = os.path.join(main_folder, "RAW_GIFs")
    os.makedirs(raw_gif_folder, exist_ok=True)

    gif_exports_folder = os.path.join(main_folder, "GIF_EXPORTS")
    os.makedirs(gif_exports_folder, exist_ok=True)

    for file in tqdm(files, unit="image", ncols=100):
        current_time = get_capture_time(file)
        if prev_time is None or (current_time - prev_time).total_seconds() <= 2:
            current_sequence.append(file)
        else:
            if len(current_sequence) >= 10:
                gif_counter += 1
                gif_folder = os.path.join(
                    raw_gif_folder, f"GIF{gif_counter} | {len(current_sequence)} images"
                )
                os.makedirs(gif_folder, exist_ok=True)

                gif_export_subfolder = os.path.join(
                    gif_exports_folder,
                    f"GIF{gif_counter} | {len(current_sequence)} images",
                )
                os.makedirs(gif_export_subfolder, exist_ok=True)

                for idx, img in enumerate(current_sequence, start=1):
                    new_name = f"frame_{idx:04d}.CR3"
                    shutil.copy(
                        os.path.join(folder_path, img),
                        os.path.join(gif_folder, new_name),
                    )
            current_sequence = [file]
        prev_time = current_time

    if len(current_sequence) >= 10:
        gif_counter += 1
        gif_folder = os.path.join(
            raw_gif_folder, f"GIF{gif_counter} | {len(current_sequence)} images"
        )
        os.makedirs(gif_folder, exist_ok=True)

        gif_export_subfolder = os.path.join(
            gif_exports_folder, f"GIF{gif_counter} | {len(current_sequence)} images"
        )
        os.makedirs(gif_export_subfolder, exist_ok=True)

        for idx, img in enumerate(current_sequence, start=1):
            new_name = f"frame_{idx:04d}.CR3"
            shutil.copy(
                os.path.join(folder_path, img), os.path.join(gif_folder, new_name)
            )

    print(f"Completed processing. Created {gif_counter} GIF sequence folders.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py [output_path] [folder_path]")
        sys.exit(1)
    output_path = sys.argv[1]
    folder_path = sys.argv[2]

    if not os.path.exists(output_path):
        print(f"The output path {output_path} does not exist.")
        sys.exit(1)

    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        sys.exit(1)

    process_images(output_path, folder_path)
