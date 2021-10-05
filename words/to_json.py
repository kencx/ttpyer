import os
import json


def to_json(filename):
    d = {}

    with open(filename, "r") as f:
        for line in f:
            word = line.strip()
            d[word] = 1

    raw_filename = os.path.splitext(os.path.basename(filename))[0]
    output_file = open(f"{raw_filename}.json", "w")
    json.dump(d, output_file, indent=4, sort_keys=False)
    output_file.close()
