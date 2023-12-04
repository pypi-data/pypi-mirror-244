from pathlib import Path


def run():
    collection_root = Path(r"E:\data\manga\test_pages")

    mokuro_files = list(collection_root.glob("**/*.mokuro"))
    print(mokuro_files)


if __name__ == '__main__':
    run()