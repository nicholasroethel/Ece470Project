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
GA_args.add_argument("--key_len", type=int, default=5, help="Length of key to use")
GA_args.add_argument("--max_gen", type=int, default=200, help="Maximum number of generations")
GA_args.add_argument("--mutate_chance", type=float, default=.6, help="Length of key to use")
GA_args.add_argument("--survival_rate", type=float, default=.4, help="How many parents are selected to move to the next round")
GA_args.add_argument("--message_len",type=int, default=500, help="Length of message to use")
GA_args.add_argument("--bias_exponent", type=int, default=2, help="Higher number is more biased to higher fitnesses")
GA_args.add_argument("--pop_size", type=int,default=100,help="Inital size of the population to generate")
GA_args.add_argument("--convergence_number", type=int,default=4,help="Number of repeated values needed to end the GA")
GA_args.add_argument("--convergence_threshold", type=float,default=.7,help="Threshold for the fitness value to reach before it tests to end the GA")
GA_args.add_argument("--runs_per_value", type=int,default=5,help="Number of runs per value when generating a graph")



def get_config():
    config, unparsed = parser.parse_known_args()

    return config, unparsed


def print_usage():
    parser.print_usage()

#
# config.py ends here
