import os
if not os.path.isfile('../TOKEN.txt'):
    TOKEN = input("Token: ")
    print('Want to save?(Y/N)')
    chose = input()
    if chose.lower() == 'y':
        with open('../TOKEN.txt', 'w') as f:
            f.write(TOKEN)
else:
    with open('../TOKEN.txt', 'r') as f:
        TOKEN = f.read()