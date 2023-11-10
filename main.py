import operator
from typing import Literal

queue: list = list()
operator_stack: list = list()


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


operators: dict[str, Operator] = {
    "**": Operator("**", 4, "right", operator.pow),
    "*": Operator("*", 3, "right", operator.mul),
    "/": Operator("**", 3, "right", operator.floordiv),
    "-": Operator("**", 2, "right", operator.sub),
    "+": Operator("**", 2, "right", operator.add),
}

operation: str = "3 + 4 - 5 / 6"
for token in operation.split():
    if token.isnumeric():
        queue.append(int(token))
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

queue.extend(operator_stack[::-1])
print(queue)
