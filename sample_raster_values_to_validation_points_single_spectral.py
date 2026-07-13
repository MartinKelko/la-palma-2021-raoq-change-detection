import os
import re
import glob
import shutil
import processing

from qgis.core import QgsVectorLayer

# path to your validation points file
points = (
    r"path\to\your\validation\points\file"
)

# path to your single spectral binary map folder
folders = [
    r"path\to\your\single\spectral\binary\map\folder",
]

# path to your single spectral binary map output folder
final_out = (
    r"path\to\your\single\spectral\binary\map\output\folder"
)

# path to your temp folder
temp_dir = (
    r"path\to\your\temp\folder"
)

if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)

os.makedirs(temp_dir, exist_ok=True)

if os.path.exists(final_out):
    os.remove(final_out)


def make_prefix(path):
    name = os.path.splitext(os.path.basename(path))[0]

    # remove BINARY_
    name = re.sub(r"^BINARY_", "", name)

    # keep only PRE_1->POST_1 or PRE_2->POST_2 pair number
    pair = re.search(r"_PRE_([12])_\d+_TO_POST_\1_\d+", name)

    if pair is None:
        return None

    pair_id = pair.group(1)

    variable = re.sub(r"_PRE_[12]_\d+_TO_POST_[12]_\d+_TRIANGLE$", "", name)

    variable = variable.replace("S1_ARD_VV_DESCENDING", "S1_VV")
    variable = variable.replace("S1_ARD_VH_DESCENDING", "S1_VH")

    return f"BIN_{variable}_{pair_id}"


rasters = []

for folder in folders:
    rasters.extend(glob.glob(os.path.join(folder, "**", "*.tif"), recursive=True))

rasters = sorted(rasters)

jobs = []

for r in rasters:
    prefix = make_prefix(r)

    if prefix is not None:
        jobs.append((r, prefix))

print("Rasters found:", len(rasters))
print("Rasters selected:", len(jobs))

for r, prefix in jobs:
    print(prefix, os.path.basename(r))


current = points

for i, (raster, prefix) in enumerate(jobs, start=1):

    out = os.path.join(temp_dir, f"sample_step_{i:03d}.gpkg")

    print(f"\n[{i}/{len(jobs)}] Sampling:")
    print("Raster:", os.path.basename(raster))
    print("Prefix:", prefix)

    processing.run(
        "native:rastersampling",
        {
            "INPUT": current,
            "RASTERCOPY": raster,
            "COLUMN_PREFIX": prefix,
            "OUTPUT": out
        }
    )

    current = out


processing.run(
    "native:savefeatures",
    {
        "INPUT": current,
        "OUTPUT": final_out
    }
)

print("\nDONE")
print(final_out)