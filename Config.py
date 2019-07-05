import argparse

arg_lists = []
parser = argparse.ArgumentParser()

def str2bool(v):
    return v.lower() in ("true", "1")


def add_argument_group(name):
    arg = parser.add_argument_group(name)
    arg_lists.append(arg)
    return arg

GA_args = parser.add_argument_group("GA")
GA_args.add_argument("--crib", type=str, default="potato",help="Know string to encode with plaintext")
GA_args.add_argument("--key_len", type=int, default=10, help="Length of key to use")
GA_args.add_argument("--message_len",type=int, default=40, help="Length of message to use")
GA_args.add_argument("--hamming_weight", type=float, default=1.0, help="Weight for the hamming score")
GA_args.add_argument("--corr_weight",type=float,default=1.0,help="Weight for the correlation score")
GA_args.add_argument("--pop_size", type=int,default=100,help="Inital size of the population to generate")


def get_config():
    config, unparsed = parser.parse_known_args()

    return config, unparsed


def print_usage():
    parser.print_usage()

#
# config.py ends here
