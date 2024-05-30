#! /usr/bin/python3


'''

    This is the read part. 
    Use it to read string.

    read_xxx(line, index) -> (token, index)

    function: A cluster of functions to read line and convert them to corresponded types.

    xxx := [number(int), alphabet(char), operators(+, -, *, /), symbol('(', ')')]

    Args:
        line: input string.
        index: the index of the input string, which used to specify char in current position

    Returns:
        token: a dictionary to indicate parsed types. i.e, {'type': xxx }
        index: the index of the input string, which used to specify char for next read function.

    
'''


def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_alphabet(line, index):
    alpha = []
    while index < len(line) and line[index].isalpha():
        alpha.append(line[index])
        index += 1
    alpha = ''.join(alpha)
    if alpha == 'abs':
        token = {'type': 'ABS'}
    elif alpha == 'int':
        token = {'type': 'INT'}
    elif alpha == 'round':
        token = {'type': 'ROUND'}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_multiplication(line, index):
    token = {'type': 'MULTIPLICATION'}
    return token, index + 1


def read_division(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1


def read_left_parenthesis(line, index):
    token = {'type': 'L_PARENTHESIS'}
    return token, index + 1


def read_right_parenthesis(line, index):
    token = {'type': 'R_PARENTHESIS'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index].isalpha():
            (token, index) = read_alphabet(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiplication(line, index)
        elif line[index] == '/':
            (token, index) = read_division(line, index)
        elif line[index] == '(':
            (token, index) = read_left_parenthesis(line, index)
        elif line[index] == ')':
            (token, index) = read_right_parenthesis(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


'''
    This is the real working parts for calculation

    evaluate_xxx(tokens) -> (new_tokens)
    except for: evaluate_plus_and_divide(tokens) -> (answer)

    function: Each function calculates different symbols and functionalities respectively.

    Args:
        tokens: A list of tokens representing the arithmetic expression.

    Returns:
        A list of tokens with all parentheses evaluated and removed.
    '''


def evaluate_brackets(tokens):
    #This function finds the innermost parentheses, evaluates the expression within them, and replaces the parentheses and their content with the evaluated result.
    while True:
        R = -1
        for i in range(len(tokens)):
            if tokens[i]['type'] == 'R_PARENTHESIS':
                R = i
                break
        if R == -1:
            return tokens
        
        L = -1
        for j in range(R, -1, -1):
            if tokens[j]['type'] == 'L_PARENTHESIS':
                L = j
                break
        if L == -1:
            raise ValueError("Mismatched parentheses in expression")
        
        new_number = evaluate(tokens[L + 1: R])
        new_tokens = tokens[:L] + [{'type': 'NUMBER', 'number': new_number}] + tokens[R + 1:]
        tokens = new_tokens


def evaluate_functions(tokens):
    # This function evaluates specific functions (absolute value, integer conversion, and rounding) within the tokens.
    index = 0
    new_tokens = []
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'ABS':
                new_tokens.pop()
                tokens[index]['number'] = abs(tokens[index]['number'])
            elif tokens[index - 1]['type'] == 'INT':
                new_tokens.pop()
                tokens[index]['number'] = int(tokens[index]['number'])
            elif tokens[index - 1]['type'] == 'ROUND':
                new_tokens.pop()
                tokens[index]['number'] = round(tokens[index]['number'])
        new_tokens.append(tokens[index])
        index += 1
    return new_tokens


def evaluate_multiply_and_division(tokens):
    # This function evaluates multiplication and division within the tokens.
    new_tokens = []
    new_tokens = []
    index = 0
    while index < len(tokens):
        # If found * or /
        if tokens[index]['type'] == 'MULTIPLICATION' or tokens[index]['type'] == 'DIVISION':
            prev_number = new_tokens.pop() # pop the number before * or / and save it as prev_number
            current_number = tokens[index + 1]['number'] # the number after * or /
            if tokens[index]['type'] == 'MULTIPLICATION':
                new_number = prev_number['number'] * current_number
            elif tokens[index]['type'] == 'DIVISION':
                new_number = prev_number['number'] / current_number
            new_tokens.append({'type': 'NUMBER', 'number': new_number})
            index += 2
        else:
            new_tokens.append(tokens[index])
            index += 1
    return new_tokens
                

def evaluate_plus_and_divide(tokens):
    # This function evaluates addition and subtraction within the tokens.
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print(index,tokens[index],'Invalid syntax')
                exit(1)
        index += 1
    return answer


'''

    This is the general calculate part. 
    evaluate(tokens) -> (answer)
    
'''


def evaluate(tokens):

    # Firstly solve the parenthesis
    tokens = evaluate_brackets(tokens)#inner bracket range
    tokens = evaluate_functions(tokens)
    # solve the mul and div
    tokens = evaluate_multiply_and_division(tokens)
    # Finally calculate the add ans sub
    answer  = evaluate_plus_and_divide(tokens)
    return answer


'''
    This is the test part.
'''


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")

    print("\n","== Only plus and minus tests start ==")
    test("12")
    test("-1.4")
    test("1+2")
    test("1.0+2.1-5")

    print("\n","== Mulplication and Devision tests start ==")
    test("2*3/4")
    test("2.2*3.4/4.5")
    test("1+2*4-10/5*2")
    test("3*3/4.3+2-1/2")

    print("\n","== Parenthesis() tests start ==")
    test("1+(-2)")
    test("(3.0+4*(2-1))/5")
    test("((3.0+4)*(1-3))/5")
    test("3+(4*(5+6)*3)-1")
    test("2.5*3+(6/2)-4.2")
    test("(3.5+2.1)*4-((2-1)*5)") 
    test("3+(4*(5+6)*3)-1")
    test("2.5*3+(6/2)-4.2")

    print("\n","== Function(abs, int and round) tests start ==")
    test('3+abs(2)')
    test('3+abs(-5)')
    test('(12.8+(abs(-6)*2+7-abs(2))-32.4)/2')
    test('1+int(3.8+2)')
    test('1+round(3.8-1)')
    test('1+abs(round(-3.8))-int(2.3)+int(abs(-5.6)*2)-(5+int(0.68))')

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
