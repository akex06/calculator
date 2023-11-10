import math
import operator
from typing import Literal, Any
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


queue: Stack = Stack()
operator_stack: Stack = Stack()

operators: dict[str, Operator] = {
    "**": Operator("**", 4, "right", operator.pow),
    "*": Operator("*", 3, "right", operator.mul),
    "/": Operator("**", 3, "right", operator.floordiv),
    "-": Operator("**", 2, "right", operator.sub),
    "+": Operator("**", 2, "right", operator.add),
}

functions: dict[str, callable] = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "abs": abs,
    "int": int,
    "max": max,
    "min": min
}

operation: str = "sin ( max ( 2 , 3 ) / 3 * 3"
for token in operation.split():
    if token.isnumeric():
        queue.append(int(token))
        continue

    if token in functions:
        operator_stack.append(token)
        continue

    if token in operators:
        while True:
            if not operator_stack or operator_stack[-1] == "(":
                break

            o1 = operators[token]
            o2 = operators[operator_stack[-1]]
            if (
                    o2.precedence > o1.precedence
                    or (
                    o1.precedence == o2.precedence
                    and o1.associativity == "left")
            ):
                queue.append(operator_stack.pop())
                continue

            break

        operator_stack.append(token)

    if token == ",":
        while operator_stack[-1] != "(":
            queue.append(operator_stack.pop())

    if token == "(":
        operator_stack.append(token)
        continue

    if token == ")":
        while operator_stack[-1] != "(":
            assert len(operator_stack) > 0, "The operator stack is empty"
            queue.append(operator_stack.pop())

        assert operator_stack[-1] == "(", "The operator stack should have a left parenthesis at the top"
        operator_stack.pop()
        if operator_stack[-1] in functions:
            queue.append(operator_stack.pop())

queue.extend(operator_stack[::-1])
print(queue)
