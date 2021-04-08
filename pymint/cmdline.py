import argparse
from pathlib import Path
from pymint import MINTDevice
import os
import json


def main():

    # do the arg parsing here
    parser = argparse.ArgumentParser()

    parser.add_argument("input", help="This is the file thats used as the input ")
    parser.add_argument(
        "--outpath", type=str, default="out/", help="This is the output directory"
    )
    parser.add_argument(
        "-c",
        "--convert",
        action="store_true",
        help="Sets the flag to only convert the design and nothing else",
    )

    args = parser.parse_args()
    OUTPUT_DIR = Path(args.outpath).resolve()
    file_path = str(Path(args.input).resolve())

    current_device = MINTDevice.from_mint_file(file_path)

    tt = os.path.join(OUTPUT_DIR, "{}.json".format(current_device.name))
    with open(tt, "w") as f:
        json.dump(current_device.to_parchmint_v1(), f)


if __name__ == "__main__":
    main()
