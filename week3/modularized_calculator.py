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


# Find out parentheses
def find_parentheses(tokens):
    while {'type': 'L_PARENTHESIS'} in tokens or  {'type': 'R_PARENTHESIS'} in tokens:
         #print("递归前",tokens,'\n')
         tokens = find_parentheses_rec(tokens)
         #print("递归后",tokens)
    return tokens


# Recursion to find the innermost "()"
def find_parentheses_rec(tokens):
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    new_tokens = []
    parentheses_list = []
    index = 1
    while index < len(tokens):
        calculate_tokens = []
        if tokens[index]['type'] == 'L_PARENTHESIS':
            parentheses_list.append(index)
            new_tokens.append(tokens[index])

        elif tokens[index]['type'] == 'R_PARENTHESIS':

            # Check if only ")"
            if not parentheses_list:
                print('Invalid syntax,"()"')
                return
            parentheses_list.append(index)
            if tokens[parentheses_list[-2]]['type'] == 'L_PARENTHESIS':
                new_tokens.pop()
                start = parentheses_list[-2]
                #1print("start",start,index)

                for i in range(start + 1, index):
                    calculate_tokens.append(tokens[i])
                    new_tokens.pop()
                calculated_num = evaluate_without_parenthesis(calculate_tokens)
                new_tokens.append({'type': 'NUMBER', 'number': calculated_num})
            #print("右括号发现",parentheses_list, new_tokens, "\n","值calculated_num",calculated_num)
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
            prev_number = new_tokens.pop()
            current_number = tokens[index + 1]['number']
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
    test("(3.5+2.1)*4-((2-1)*5)")
    test("(1+2)*(3+4)/5")
    test("(2+3)*(5.5-1.5)/(2*3)")
    test("((2.5+3.5)*2-1)/3")
    test("2.5*(4+(3-2))/1.5")
    test("6/(2*(1+2))-3.5")

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
