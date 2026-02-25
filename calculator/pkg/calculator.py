class Calculator:
    """A simple calculator class that evaluates arithmetic expressions."""

    def __init__(self):
        """Initializes the Calculator with supported operators and their precedence."""
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        """
        Evaluates an arithmetic expression given as a string.
        Supports addition, subtraction, multiplication, and division.
        Handles operator precedence.

        Args:
            expression (str): The arithmetic expression to evaluate.

        Returns:
            float or None: The result of the expression, or None if the expression is empty/whitespace.

        Raises:
            ValueError: If the expression is invalid (e.g., invalid tokens, not enough operands).
        """
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()  # Split the expression into tokens.
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        """
        Evaluates an infix expression using the shunting-yard algorithm.

        Args:
            tokens (list): A list of tokens (numbers and operators) from the expression.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression is invalid.
        """
        # Implementation of the shunting-yard algorithm to handle operator precedence
        values = []  # Stack to store numerical values
        operators = []  # Stack to store operators

        for token in tokens:
            if token in self.operators:
                # Process operators based on precedence
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                # Token is a number, convert to float and push to values stack
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        # Apply remaining operators in the stack to the values
        while operators:
            self._apply_operator(operators, values)

        # The final result should be the only element left in the values stack
        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        """
        Applies the top operator from the operators stack to the top two values from the values stack.

        Args:
            operators (list): The stack of operators.
            values (list): The stack of numerical values.

        Raises:
            ValueError: If there are not enough operands for the operator.
        """
        if not operators:
            return

        operator = operators.pop() # Get the top operator
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        # Pop two operands, apply the operator, and push the result back to values stack
        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))
