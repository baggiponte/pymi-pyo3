import argparse

from pymi_pyo3 import sum_as_string  # ignore

def main():

    # create the parser object
    parser = argparse.ArgumentParser(description='Add two numbers but return them as a string.')

    # add the arguments to the parser
    parser.add_argument('num1', type=int, help='The first number to add.')
    parser.add_argument('num2', type=int, help='The second number to add.')

    # parse the arguments
    args = parser.parse_args()

    print(sum_as_string(args.num1, args.num2))


if __name__ == "__main__":
    main()
