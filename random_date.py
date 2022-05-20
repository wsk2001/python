from time import sleep
import random, sys, getopt, datetime


def main(argv):

    select_count = 25

    day = datetime.datetime(2021, 1, 1)
    day_list = random.sample(range(365), select_count)
    for i in day_list:
        print(day + datetime.timedelta(days=i))


if __name__ == "__main__":
    main(sys.argv)
