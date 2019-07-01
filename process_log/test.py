import argparse

def main():
    parser = argparse.ArgumentParser(description='concurrent client')

    parser.add_argument('--worker', type=int, help="Worker num")
    parser.add_argument('--ip', type=str, help="Ip address of your query frontend")
    parser.add_argument('--port', type=str, help="Port of your query frontend, for Clipper, put an arbitrary INT")
    parser.add_argument('--system', type=str, help="System name: oursystem/withoutproxy/clipper")
                       
    args = parser.parse_args()

    # Get configuration
    work_num = args.worker
    ip = args.ip
    port = args.port
    system = args.system

    print(work_num, ip, port, system)
# python test.py --worker 11 --ip 11 --port 11 --system 11



if __name__ == '__main__':
    main()
