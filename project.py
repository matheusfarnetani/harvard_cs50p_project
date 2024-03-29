import argparse

from models.accessible_ramp import AccessibleRamp

OPTIONS = ["COM-A", "COM-B", "COM-C", "EXP-A", "EXP-B"]
MAX_HEIGHT_START = 1
MAX_HEIGHT_INCREMENT = 0.5
MAX_SLOPE_START = 5
MAX_SLOPE_INCREMENT = 0.2


def main() -> None:
    args = arguments()
    
    height: float = args.height if args.height else get_float("Height: ")
    width:float = args.width if args.width else get_float("Width: ")
    slope: float = args.slope if args.slope else get_float("Slope: ")
    option: str = args.opt if args.opt else input("Option: ").upper()

    print("\nMax Possible Height:\n")
    if slope > 6.25:
        max_height = max_possible_height(slope, MAX_HEIGHT_START, MAX_HEIGHT_INCREMENT)
        print(f"In a total, {len(max_height)} ramps were calculated.",
            f"\nThe count started from {MAX_HEIGHT_START:.2f}m and was incremented, within each loop, by {MAX_HEIGHT_INCREMENT:.2f}m"
            f"\nThe last ramp calculated, with a slope of {slope:.2f}%, has a height of {max_height[-1].height:.2f}m"
        )
    else:
        print(f"For a slope less than 6.25% there is no max possible height, if you have the space :)")

    print("\nMax Possible Slope:\n")
    max_slope = max_possible_slope(height, MAX_SLOPE_START, MAX_SLOPE_INCREMENT)
    print(f"In a total, {len(max_slope)} ramps were calculated.",
          f"\nThe count started from {MAX_SLOPE_START:.2f}% and was incremented, within each loop, by {MAX_SLOPE_INCREMENT:.2f}%",
          f"\nThe last ramp calculated, with a height of {height:.2f}m, has a slope of {max_slope[-1].slope:.2f}%"
    )

    print("\nOther Options:\n")
    options = other_options(height, width)
    print(f"Calculated {len(options)}/{len(OPTIONS)} options.",
          f"\nA ramp of height={height:.2f}m, could have the following slopes:")
    for o in options:
        print(f"slope={o.slope:.2f}% and length={o.length:.2f}m")

    ar = AccessibleRamp(height, width, option, slope)

    print("\n", ar)


def other_options(height: float, width: float) -> list:
    results: list = list()
    for i in OPTIONS:
        try:
            results.append(AccessibleRamp(height, width, i))
        except ValueError:
            pass
    return results


def max_possible_height(slope: float, start: float, increment: float) -> list:
    results: list = list()
    height: float = start
    while True:
        try:
            results.append(AccessibleRamp(height=height, width=1.2, slope=slope))
        except ValueError:
            break
        height += increment
    return results


def max_possible_slope(height: float, start: float, increment: float) -> list:
    results: list = list()
    slope: float = start
    while True:
        try:
            results.append(AccessibleRamp(height=height, width=1.2, slope=slope))
        except ValueError:
            break
        slope += increment
    return results


def arguments():
    parser = argparse.ArgumentParser(
        description="Calculates values for a accessible ramp, following the standard ABNT NBR 9050:2020"
    )
    parser.add_argument(
        "-v, --version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    parser.add_argument(
        "-o, --option",
        type=str,
        help=" See ABNT NBR 9050:2020 6.6.2.1 and 6.6.2.2. 'COM' means 'common' and, 'exp', 'exception'. The default is 'COM-C'",
        choices=OPTIONS,
        dest="opt"
    )
    parser.add_argument(
        "--height",
        type=float,
        help="define value for height",
        dest="height"
    )
    parser.add_argument(
        "-w, --width",
        type=float,
        help="define value for width",
        dest="width"
    )
    parser.add_argument(
        "-s, --slope",
        type=float,
        help="define value for slope",
        dest="slope"
    )

    return parser.parse_args()


def get_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            pass


if __name__ == "__main__":
    main()
