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

def save_target(target, output):
    with open(output, 'w', encoding='utf-8') as fp:
        fp.write(target + "\n")

def main():
    args = options()
    targets = get_targets(args.targets)
    parsed_targets = []
    wrong_targets = []
    
    logging.info("Using delimiter: %s", args.delimiter)
    logging.info("Using length: %s", args.length)

    for target in targets:
        if parse_target(target, args.delimiter, args.length):
            logging.info("%s", target)
            parsed_targets.append(target)
        else:
            logging.info("Target %s does not match the pattern", target)
            wrong_targets.append(target)

    logging.info("Parsed targets: %s", len(parsed_targets))
    logging.info("Wrong targets: %s", len(wrong_targets))

    save_target("\n".join(parsed_targets), "./parsed_targets.txt")
    save_target("\n".join(wrong_targets), "./wrong_targets.txt")


if __name__ == "__main__":
    main()
