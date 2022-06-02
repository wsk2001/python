import time, sys, getopt
import pyupbit

open_p = 0
high_p = 1
low_p = 2
close_p = 3


def plus_count_close(v, earn, period):
    p_count = 0
    df = pyupbit.get_ohlcv(v, count=period)
    values = df.values.tolist()

    for i in range(len(values)):
        rc = ((values[i][close_p] / values[i][open_p]) - 1) * 100.0
        if earn <= rc:
            p_count += 1

    return v[4:], p_count


def plus_count_high(v, earn, period):
    p_count = 0
    df = pyupbit.get_ohlcv(v, count=period)
    values = df.values.tolist()

    for i in range(len(values)):
        rc = ((values[i][high_p] / values[i][open_p]) - 1) * 100.0
        if earn <= rc:
            p_count += 1

    return v[4:], p_count


def main(argv):
    period = 90
    earn = 10.0
    output_count = 30
    worktype = "high"
    lst = pyupbit.get_tickers(fiat="KRW")
    pumping = [[]]
    pumping.clear()

    try:
        opts, etc_args = getopt.getopt(argv[1:], "hco:p:e:"
                                       , ["help", "output_count", "period", "earning"])

    except getopt.GetoptError:
        print(argv[0], '-p <period - days> -c (close price/high price) -o <output count> -e <earning percent>')
        print('ex) python', f'{argv[0]}', '-p 100 -c -o 30 -e 10')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(argv[0], '-p <period - days> -c (close price/high price) -o <output count> -e <earning percent>')
            print('ex) python', f'{argv[0]}', '-p 100 -c -o 30 -e 10')
            sys.exit()

        elif opt in ("-p", "--period"):
            period = int(arg.strip())

        elif opt in ("-o", "--output"):
            output_count = int(arg.strip())

        elif opt in ("-e", "--earning"):
            earn = int(arg.strip())

        elif opt in ("-c"):
            worktype = "close"

    for v in lst:
        time.sleep(0.1)
        if worktype.startswith("close"):
            arr = plus_count_close(v, earn, period)
        else:
            arr = plus_count_high(v, earn, period)

        pumping.append(list(arr))

    earns = sorted(pumping, key=lambda x : x[1], reverse=True)

    print('based on', worktype, ',작성 기준 일자', time.strftime('%Y-%m-%d %H:%M:%S'))
    print('ticker, pumping count')

    i = 0
    for e in earns:
        print(f'{e[0]},', f'{e[1]}')
        i += 1
        if output_count < i:
            break


if __name__ == "__main__":
    main(sys.argv)
