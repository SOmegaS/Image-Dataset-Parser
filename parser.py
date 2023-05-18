import sys
from parsers.base_parser import Parser
from parsers.burst import Burst
from parsers.google import Google
from parsers.unsplash import Unsplash
from parsers.openverse import Openverse
from parsers.vecteezy import Vecteezy
from parsers.wikimedia import Wikimedia


def main(percent, query):
    path = "images/"
    path_for_save = "save/"
    parsers = [Burst(path, path_for_save),
               Openverse(path, path_for_save),
               Unsplash(path, path_for_save), Wikimedia(path, path_for_save), Vecteezy(path, path_for_save)]
    amount_const = len(parsers)
    perc = 1 / amount_const
    Parser.make_dirs(query, path, path_for_save, amount_const)
    for i in range(0, amount_const):
        parsers[i].parse(query, perc, i + 1)


if __name__ == "__main__":
    percent = int(sys.argv[1])
    query = dict(zip(sys.argv[2::2], map(int, sys.argv[3::2])))
    main(percent, query)
