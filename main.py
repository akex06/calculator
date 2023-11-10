from calculator import rpn


operation: str = "int ( sin ( 3 / 3 * 3.14 ) )"
expression = rpn.convert(operation)
print(rpn.evaluate(expression))
