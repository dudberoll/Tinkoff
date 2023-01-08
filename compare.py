import argparse


# Helper function for determining the distance
def m(str1: str, str2: str, i: int, j: int):
    if str1[i - 1] != str2[j - 1]:
        return 1
    else:
        return 0


# Levinshtein distance
def Distance(str1: str, str2: str):
    lev_array = [[0 for j in range(len(list(str2)) + 1)]
                 for i in range(len(list(str1)) + 1)]
    if min(len(str1), len(str2)) == 0:
        return max(len(str1), len(str2))
    else:
        for i in range(len(str1) + 1):
            for j in range(len(str2) + 1):
                if j == 0 and i > 0:
                    lev_array[i][j] = i
                if i == 0 and j > 0:
                    lev_array[i][j] = j
                if i > 0 and j > 0:
                    lev_array[i][j] = min(lev_array[i][j - 1] + 1, lev_array[i - 1][j] + 1,
                                          lev_array[i - 1][j - 1] + m(str1, str2, i, j))
        return lev_array[len(str1)][len(str2)]


parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, help='Input plagiat list')
parser.add_argument('output', type=str, help='Output plagiat scores')
args = parser.parse_args()


def result():
    # Удаляем содержимое файла
    open(args.output, 'w')

    with open(args.input) as f:
        input_lines = list(f)

    for i in range(len(input_lines)):
        current_line = input_lines[i].replace('\n', '').split()

        with open(current_line[0]) as f:
            arg1 = f.read()

        with open(current_line[1]) as f:
            arg2 = f.read()

        current_score = round((len(arg1) - Distance(arg1, arg2)) / len(arg1), 2)
        with open(args.output, 'a') as f:
            f.write(str(current_score) + '\n')
    return


result()
