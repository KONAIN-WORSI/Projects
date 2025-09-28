print('Welcome to simple Calculator!')
print('='*30)



def calculator():
    while True:
        try:
            expr = input('Enter expression (or exit to quit): ')

            if expr.lower() == 'exit':
                print('Exiting Calculator.')
                break

            if '/' in expr:
                parts = expr.split('/')
                if len(parts) == 2 and parts[1].strip() == '0':
                    print('Error: Division by Zero is not allowed.')
                    continue

            result = eval(expr)
            print(f'The result of {expr} is: {result}')
        except Exception as e:
            print(f'Error: {e}. please enter a valid expression.')


if __name__ == '__main__':
    calculator()

