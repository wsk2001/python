from time import sleep
import random, sys, getopt, datetime


def main(argv):

    select_count = 25
    start = 1
    end = 84

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hc:s:e:", ["count=", "start=", "end"])

    except getopt.GetoptError:
        print(argv[0], '-c <extract count> -s <start range> -e <end range>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-c <extract count> -s <start range> -e <end range>')
            sys.exit()

        elif opt in ("-c", "--count"):
            select_count = int(arg.strip())

        elif opt in ("-s", "--start"):
            start = int(arg.strip())

        elif opt in ("-e", "--end"):
            end = int(arg.strip())

    for i in range(1, select_count):
        print(random.randint(start, end))
        sleep(0.3)


if __name__ == "__main__":
    main(sys.argv)
