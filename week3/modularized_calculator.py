#! /usr/bin/python3

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


# Handle abs,int and round
def clear_commands(tokens, new_tokens, index):
    # For abs
    if tokens[index]['type'] == 'ABS':
        # If the number in abs is positive
        if tokens[index + 2]['type'] == 'NUMBER':
            for i in range(index, index + 3):
                new_tokens.pop() # pop: abs("original number")
            abs_number = abs(tokens[index + 2]['number'])
            new_tokens.append({'type': 'NUMBER', 'number': abs_number}) # append the result
        # If the number in abs is negative
        elif tokens[index + 2]['type'] == 'MINUS' and tokens[index + 3]['type'] == 'NUMBER':
            for i in range(index, index + 4):
                new_tokens.pop()
            abs_number = tokens[index + 3]['number']
            new_tokens.append({'type': 'NUMBER', 'number': abs_number})
        else:
            print('Command Error')
            exit(1)
    # For int        
    elif tokens[index]['type'] == 'INT':
        if tokens[index + 2]['type'] == 'NUMBER':
            for i in range(index, index + 3):
                new_tokens.pop()
            int_number = int(tokens[index + 2]['number'])
            new_tokens.append({'type': 'NUMBER', 'number': int_number})
        else:
            print('Command Error')
            exit(1)
    # For round
    elif tokens[index]['type'] == 'ROUND':
        if tokens[index + 2]['type'] == 'NUMBER':
            for i in range(index, index + 3):
                new_tokens.pop()
            if tokens[index + 2]['number'] - int(tokens[index + 2]['number']) > 0.5:
                round_number = int(tokens[index + 2]['number']) + 1
            else:
                round_number = int(tokens[index + 2]['number'])
            new_tokens.append({'type': 'NUMBER', 'number': round_number})
        else:
            print('Command Error')
            exit(1)
    return new_tokens

# Find out parentheses
def find_parentheses(tokens):
    while {'type': 'L_PARENTHESIS'} in tokens or  {'type': 'R_PARENTHESIS'} in tokens:
        # If there are still () in tokens, use recursion to reduce them.
        tokens = find_parentheses_rec(tokens)
    return tokens


# Recursion to find the innermost "()"
def find_parentheses_rec(tokens):
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    new_tokens = []
    parentheses_list = []
    index = 1
    while index < len(tokens):
        calculate_tokens = [] # To calculate the contents between ()
        if tokens[index]['type'] == 'L_PARENTHESIS':
            parentheses_list.append(index)
            new_tokens.append(tokens[index])

        elif tokens[index]['type'] == 'R_PARENTHESIS':
            # Check if only ")", exit
            if not parentheses_list:
                print('Invalid syntax,"()"')
                exit(1)
            parentheses_list.append(index)
            # Check if it's the innermost ()
            if tokens[parentheses_list[-2]]['type'] == 'L_PARENTHESIS':
                # Check if it's a command like abs
                if index - parentheses_list[-2] <= 3:
                    new_index = parentheses_list[-2] - 1
                    new_tokens = clear_commands(tokens, new_tokens, new_index)
                # If it's a normal ), but not a command
                else:
                    new_tokens.pop()
                    start = parentheses_list[-2] # the index of the left parenthesis
                    for i in range(start + 1, index): # calculate the formula between ()
                        calculate_tokens.append(tokens[i])
                        new_tokens.pop() # pop out the formula
                    calculated_num = evaluate_without_parenthesis(calculate_tokens)
                    new_tokens.append({'type': 'NUMBER', 'number': calculated_num}) # append the result of the formula
            else:
                new_tokens.append(tokens[index])
        else:
            new_tokens.append(tokens[index])
        index += 1
    return new_tokens


# Prioritize solving the higher-level operations
def prioritize_mul_div(tokens):
    new_tokens = []
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
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
                

def evaluate_without_parenthesis(tokens):
    tokens = prioritize_mul_div(tokens)
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
                #print(index,tokens[index],'Invalid syntax')
                exit(1)
        index += 1
    return answer


def evaluate(tokens):
    new_tokens = find_parentheses(tokens)
    answer = evaluate_without_parenthesis(new_tokens)
    return answer


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

    # Only plus and minus
    test("1+2")
    test("1.0+2.1-3")
    # Mulplication and Devision
    test("2*3/4")
    test("2.2*3.4/4.5")
    test("1+2*4-10/5*2")
    test("3*3/4.3+2-1/2")
    # Parenthesis()
    test("(3.0+4*(2-1))/5")
    test("((3.0+4)*(2-1))/5")
    test("3+(4*(5+6)*3)-1")
    test("2.5*3+(6/2)-4.2")
    test("(3.5+2.1)*4-((2-1)*5)") 
    test("3+(4*(5+6)*3)-1")
    test("2.5*3+(6/2)-4.2")
    # ABS, INT and ROUND
    test('3+abs(2)')
    test('3+abs(-5)')
    test('(12.8+(abs(-6)*2+7-abs(2))-32.4)/2')
    test('1+int(3.8)')
    test('1+round(3.8)')
    test('1+round(3.8)-int(2.3)+abs(-5.6)*2-(5+int(0.68))')

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
