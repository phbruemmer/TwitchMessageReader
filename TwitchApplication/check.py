import random


def check_numbers():
    nums = set()
    multiples = 0

    with open("numbers.txt", "r") as file:
        for line in file:
            num = int(line)

            if num in nums:
                multiples += 1
            nums.add(num)

    print("# # #")
    print(f"Total guesses:\t\t{len(nums)}")
    print(f"Multiple guesses:\t{multiples}")

    random_num = random.randint(0, 9999)
    while random_num in nums:
        random_num = random.randint(0, 9999)

    print(f"Recommended guess:\t{random_num}")
    print("# # #")

    return random_num


# Deletes last line in a file
def clean_file():
    with open("numbers.txt", "r") as file:
        lines = file.readlines()
    if lines:
        lines.pop()
    with open("numbers.txt", "w") as file:
        file.writelines(lines)


def extract(msg):
    if "This command is currently on cooldown" in msg:
        clean_file()

    msg_extract = msg.split()

    if not msg_extract[0] == '!safe':
        return

    try:
        num = int(msg_extract[1])
    except Exception:
        return

    with open('numbers.txt', 'a') as file:
        file.write(f'{num}\n')

    check_numbers()


def check_num(num: int):
    with open("numbers.txt", "r") as file:
        data = file.read()
        if str(num) in data:
            print("Number found.")
        else:
            print("Number not found.")


if __name__ == '__main__':
    clean_file()
