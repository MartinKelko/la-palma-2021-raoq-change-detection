import os
import re
import glob
import shutil
import processing

from qgis.core import QgsVectorLayer


# ============================================================
# INPUTS
# ============================================================

# path to your validation points file
points = (
    r"path\to\your\validation\points\file"
)

# path to your RaoQ MD binary map folder
folders = [
    r"path\to\your\RaoQ\MD\binary\map\folder",
]

# path to your RaoQ MD binary map output folder
final_out = (
    r"path\to\your\RaoQ\MD\binary\map\output\folder"
)

# path to your temp folder
temp_dir = (
    r"path\to\your\temp\folder"
)


# ============================================================
# CLEAN OUTPUTS
# ============================================================

if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)

os.makedirs(temp_dir, exist_ok=True)

if os.path.exists(final_out):
    os.remove(final_out)


# ============================================================
# PREFIX HELPER FOR RAOQ MULTIDIMENSIONAL
# ============================================================

def make_prefix(path):
    name = os.path.splitext(os.path.basename(path))[0]

    # remove BINARY_
    name = re.sub(r"^BINARY_", "", name)

    # accept only RaoQ multidimensional rasters
    if not (
        name.startswith("RaoQ_multidimensional_")
        or name.startswith("RaoQ_MULTIDIM_")
    ):
        return None

    # match:
    # ..._PRE_1_20210910_20210910_TO_POST_1_20220113_20220113_TRIANGLE
    # ..._PRE_2_20210826_20210826_TO_POST_2_20220113_20220113_TRIANGLE
    pair = re.search(
        r"_PRE_([12])_(.*?)_TO_POST_\1_(.*?)_TRIANGLE$",
        name
    )

    if pair is None:
        return None

    pair_id = pair.group(1)

    # remove pair/date suffix
    variable = re.sub(
        r"_PRE_[12]_(.*?)_TO_POST_[12]_(.*?)_TRIANGLE$",
        "",
        name
    )

    # shorten column prefix
    variable = variable.replace("RaoQ_multidimensional_", "RaoQ_MD_")
    variable = variable.replace("RaoQ_MULTIDIM_", "RaoQ_MD_")

    return f"BIN_{variable}_{pair_id}"


# ============================================================
# COLLECT RASTERS
# ============================================================

rasters = []

for folder in folders:
    rasters.extend(
        glob.glob(
            os.path.join(folder, "**", "*.tif"),
            recursive=True
        )
    )

rasters = sorted(rasters)


# ============================================================
# BUILD SAMPLING JOBS
# ============================================================

jobs = []

for r in rasters:
    prefix = make_prefix(r)

    if prefix is not None:
        jobs.append((r, prefix))

print("Rasters found:", len(rasters))
print("Rasters selected:", len(jobs))

for r, prefix in jobs:
    print(prefix, os.path.basename(r))


# ============================================================
# SAFETY CHECK
# ============================================================

if len(jobs) == 0:
    raise RuntimeError(
        "No RaoQ multidimensional binary rasters selected. "
        "Check folder path and file naming."
    )


# ============================================================
# ITERATIVE RASTER SAMPLING
# ============================================================

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


# ============================================================
# SAVE FINAL OUTPUT
# ============================================================

processing.run(
    "native:savefeatures",
    {
        "INPUT": current,
        "OUTPUT": final_out
    }
)

print("\nDONE")
print(final_out)