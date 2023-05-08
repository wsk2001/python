import sys, argparse


def main(argv):
    parser = argparse.ArgumentParser(description='java jar file dependency checker')
    parser.add_argument('-f', '--filename', required=True, help='read file name')

    args = parser.parse_args()
    filename = args.filename

    list_jar = []
    list_jar.clear()

    with open(filename, 'r') as file_data:
        for line in file_data:
            if 'rt.jar' in line:
                continue
            if 'java.util.jar' in line:
                continue
            line = line.strip()
            line = line.replace("(", "")
            line = line.replace(")", "")
            line = line.replace("\\", " ")
            line = line[line.rfind(' '):].strip()

            if line in list_jar:
                continue
            else:
                if 0 < line.find('.jar'):
                    list_jar.append(line)

    for jar in list_jar:
        print(jar)


if __name__ == "__main__":
    main(sys.argv)

# jdeps -R -cp .;./lib/*;XFileRemoteAgent.jar XFileRemoteAgent.jar | grep ".jar" > aaa.txt
# py jar_depens.py -f aaa.txt
