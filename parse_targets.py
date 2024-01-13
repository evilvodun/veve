import argparse
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", help='File containing combinations', required=False)
    parser.add_argument("--delimiter", help="Delimiter to use", required=False, default=":")
    parser.add_argument("--length", help="Length of the elememnts", required=False, default=2, type=int)

    return parser.parse_args()

def get_targets(targets):
    with open(targets, 'r', encoding='utf-8') as fp:
        lines = fp.read().splitlines()
        logging.info("targets to be parsed: %s", len(lines))

    return lines

def parse_target(target, delimiter, length):
    return len(target.split(delimiter)) == length

def main():
    args = options()
    targets = get_targets(args.targets)


if __name__ == "__main__":
    main()
