import sys
from pkg.calculator import Calculator
from pkg.render import format_json_output


def main():
    """
    Main function to run the calculator application.
    It parses command-line arguments, evaluates the expression, and prints the result.
    """
    calculator = Calculator()
    # Check if any arguments are provided. If not, print usage instructions.
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    # Join all command-line arguments to form the expression string.
    expression = " ".join(sys.argv[1:])

    try:
        # Evaluate the expression using the Calculator.
        result = calculator.evaluate(expression)
        # If the result is not None, format and print the output.
        if result is not None:
            to_print = format_json_output(expression, result)
            print(to_print)
        else:
            # Handle cases where the expression is empty or contains only whitespace.
            print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        # Catch any exceptions during evaluation and print an error message.
        print(f"Error: {e}")


if __name__ == "__main__":
    # Ensure main() is called only when the script is executed directly.
    main()
