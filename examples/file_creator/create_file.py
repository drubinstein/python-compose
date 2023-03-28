import argparse
import pathlib

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=pathlib.Path)
    args = parser.parse_args()

    with open(args.file_path, "w") as f:
        f.write("hello")
