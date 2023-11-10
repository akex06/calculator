import math
import operator
from typing import Literal, Any, Union
from collections.abc import MutableSequence


class Stack(list):
    def __init__(self) -> None:
        super().__init__()

    def popto(self, mutable_sequence: MutableSequence) -> Any:
        mutable_sequence.append(self.pop())


class Operator:
    def __init__(
            self,
            operator: str,
            precedence: int,
            associativity: Literal["left", "right"],
            method: callable
    ) -> None:
        self.operator = operator
        self.precedence = precedence
        self.associativity = associativity
        self.method = method

    def __repr__(self) -> str:
        return f"Operator({self.operator=})"


operators: dict[str, Operator] = {
    "**": Operator("**", 4, "right", operator.pow),
    "*": Operator("*", 3, "right", operator.mul),
    "/": Operator("/", 3, "right", operator.truediv),
    "-": Operator("-", 2, "right", operator.sub),
    "+": Operator("+", 2, "right", operator.add),
}

functions: dict[str, callable] = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "abs": abs,
    "int": int,
    "ceil": math.ceil,
    "floor": math.floor
}


def convert(operation: str) -> list[Union[int, str]]:
    queue: Stack = Stack()
    operator_stack: Stack = Stack()
    for token in operation.split():
        try:
            queue.append(float(token))
        except ValueError:
            pass

        if token in functions:
            operator_stack.append(functions[token])
            continue

        if token in operators:
            while True:
                if not operator_stack:
                    break

                if operator_stack[-1] == "(":
                    break

                if not isinstance(operator_stack[-1], Operator):
                    break
                o1 = operators[token]
                o2 = operator_stack[-1]
                if (
                        o2.precedence > o1.precedence
                        or (
                        o1.precedence == o2.precedence
                        and o1.associativity == "left")
                ):
                    operator_stack.popto(queue)
                    continue

                break

            operator_stack.append(operators[token])

        if token == ",":
            while operator_stack[-1] != "(":
                operator_stack.popto(queue)

        if token == "(":
            operator_stack.append(token)
            continue

        if token == ")":
            while operator_stack[-1] != "(":
                assert len(operator_stack) > 0, "The operator stack is empty"
                operator_stack.popto(queue)

            assert operator_stack[-1] == "(", "The operator stack should have a left parenthesis at the top"
            operator_stack.pop()
            if operator_stack[-1] in functions:
                operator_stack.popto(queue)

    queue.extend(operator_stack[::-1])
    return queue


def evaluate(expression: list[Union[int, str, callable, Operator]]) -> Union[float, int]:
    i = 0
    while len(expression) > 1:
        token = expression[i]
        if isinstance(token, int):
            i += 1
            continue

        if isinstance(token, Operator):
            expression[i - 2] = token.method(*expression[i - 2:i][::-1])
            expression.pop(i - 1)
            expression.pop(i - 1)
            i -= 1
            continue
        if callable(token):
            expression[i - 1] = token(expression[i - 1])
            expression.pop(i)
            continue

        i += 1
    return expression[0]
