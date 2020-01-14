import sys
import semantic_version

if __name__ == '__main__':
    old_version = sys.argv[1]
    v = semantic_version.Version(old_version)
    sys.stdout.write(str(v.next_patch()))
