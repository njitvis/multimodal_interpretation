#######################################################
#                                                     #
# Source: https://github.com/kdavila/CHART_Info_2024  #
#                                                     #
#######################################################

import os
import shutil
from pathlib import Path

PATH_BASE = '<PATH_TO_PROJECT>/train_yolo/datasets/'
DESTINATION = f"{PATH_BASE}output_dataset/"
TRAIN_SOURCE = f"{PATH_BASE}input_charts/CHARTINFO_2024_Train/"
TEST_SOURCE = f"{PATH_BASE}input_charts/CHARTINFO_2024_Test/"

def copy_files(src, proportion_to_move, destination):
  os.makedirs(destination, exist_ok=True)
  files = os.listdir(src)
  total_files = len(files)

  num_files_to_move = int(proportion_to_move * total_files)

  files_to_move = sorted(files)[:num_files_to_move]

  for file_name in files_to_move:
      src_path = os.path.join(src, file_name)
      shutil.move(src_path, destination)

  print(f"Moved {num_files_to_move} out of {total_files} files from {src} to {destination}.")

def parse_path_copy(path, destination, amount):
  if path.is_dir():
      subdirs = [d for d in path.iterdir() if d.is_dir()]
      if subdirs:
          for subdir in subdirs:
            copy_files(subdir, amount, destination)
      else:
          copy_files(path, amount, destination);
  else:
      print(f"The path '{path}' is not a valid directory.")

## MOVE 80% of train images and 100% of test images
path = Path(f"{TRAIN_SOURCE}/images/")
parse_path_copy(path, f"{DESTINATION}images/train", 0.8)
path = Path(f"{TEST_SOURCE}/images/")
parse_path_copy(path, f"{DESTINATION}images/test", 1)

print("\n")
print("=" * 100)
print("\n")

## MOVE 80% of train annotation and 100% of test annotation
path = Path(f"{TRAIN_SOURCE}/annotations_JSON/")
parse_path_copy(path, f"{DESTINATION}labels/train", 0.8)
path = Path(f"{TEST_SOURCE}/annotations_JSON/")
parse_path_copy(path, f"{DESTINATION}labels/test", 1)

print("\n")
print("=" * 100)
print("\n")

## MOVE remaining train images to validation
path = Path(f"{TRAIN_SOURCE}/images/")
parse_path_copy(path, f"{DESTINATION}images/val", 1)

print("\n")
print("=" * 100)
print("\n")

## MOVE remaining train annotations to validation
path = Path(f"{TRAIN_SOURCE}/annotations_JSON/")
parse_path_copy(path, f"{DESTINATION}labels/val", 1)

print("\n")
print("=" * 100)
print("\n")

### Validate copy
path = Path("<PATH_TO_PROJECT>/train_yolo/output_dataset")
if path.is_dir():
      print(f"- {path}")
      subdirs = [d for d in path.iterdir() if d.is_dir()]
      if subdirs:
          for subdir in subdirs:
            print(f"\t|-> {subdir}")
            if subdir.is_dir():
                sds = [d for d in subdir.iterdir() if d.is_dir()]
                for sd in sds:
                    files = os.listdir(sd)
                    print(f"\t\t|-> {sd} ({len(files)})")
            else:
                files = os.listdir(subdir)
                print(f"\t|-> {subdir} ({len(files)})")
      else:
            files = os.listdir(path)
            print(f"\t|-> {path} ({len(files)})")
else:
  print(f"The path '{path}' is not a valid directory.")

print("\n")
print("=" * 100)
print("\n")
