import os, json, argparse
parser = argparse.ArgumentParser()
parser.add_argument('version', metavar='VERSION', type=str, nargs=None)
args = parser.parse_args()

version_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'VERSION')

with open(version_path, 'r') as f:
    version_current = json.load(f)
    version_current['tag_val'] = args.version
    version_current = json.dumps(version_current, indent=4)
with open(version_path, 'w') as f:
    f.write(version_current)