import util
from util import Config as c

def task() -> None:
    if not c.isValid:
        print("Config isn't valid!")

    print(f"Extensions: {c.hxxExtension}, {c.cxxExtension}")

    for bin in c.binaries:
        print(f"Name: {bin.name}")
        print(f"Filename: {bin.filename}")
        print(f"Type: {bin.type}")
        print(f"SrcDir: {bin.sourceDirectory}")
        print("Sources:")
        for src in bin.sources:
            print(f"  {src}")
        print("__________\n")
#task()