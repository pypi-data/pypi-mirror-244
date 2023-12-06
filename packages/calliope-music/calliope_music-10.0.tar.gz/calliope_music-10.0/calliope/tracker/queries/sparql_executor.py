from gi.repository import Tracker

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process TrackerSparql with file and parameters")
    parser.add_argument("--file", help="Specify the file", required=True)
    parser.add_argument("--parameters", nargs='+', help="Specify parameters in key=type:value format", required=True)

    args = parser.parse_args()

    main(args.file, args.parameters)
