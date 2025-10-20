import ast

def load_matches(path='matches.txt'):
    coord_list = []
    with open(path) as file:
        for line in file:
            line = line.strip('\n')
            clean_list = ast.literal_eval(line)
            coord_list.append(clean_list)
    return coord_list