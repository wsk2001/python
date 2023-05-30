import sys, argparse


def main(argv):
    parser = argparse.ArgumentParser(description='binary file to hex')
    parser.add_argument('-f', '--filename', required=True, help='read file name')

    args = parser.parse_args()
    filename = args.filename

    left_win = []
    right_win = []

    left_win.clear()
    right_win.clear()

    i = 0
    with open(filename, "rb") as f:
        while True:
            byte = f.read(1)
            left_win.append(byte.hex())

            if str(byte).isprintable():
                right_win.append(str(byte))
            else:
                right_win.append('.')
            i += 1
            if 16 <= i:
                print(left_win, right_win)
                left_win.clear()
                right_win.clear()
                i = 0


if __name__ == "__main__":
    main(sys.argv)