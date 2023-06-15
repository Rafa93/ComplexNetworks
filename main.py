import os
import pandas as pd

def load_graph(path):
    files = load_ods(path)


def load_ods(path):
    ls = os.listdir(path)
    files = []
    for file in ls:
        if file.__contains__('.ods'):
            real_path = path + "//" + file
            files.append(real_path)
            print(real_path)

            #load ODS file
            pd.read_excel(real_path, engine='odf')

    return files

if __name__ == '__main__':
    g_path = "D:\pythonProject1\libro de recetas"
    graphs = {}

    print('Welcome, availables options are: load_recipes, load_graph, exit')
    while(True):
        str = input('Type a command\n')
        line = str.split(" ")
        command = line[0]
        path = "None"
        if len(line) > 1:
            path = line[1]

        if (command == "exit"):
            break
        if (command == "load_recipes"):
            print('Path: Internal')
            if (path == "None"):
                load_graph(g_path)
            else:
                load_graph(path)
            continue
        if (command == "load_graph"):
            load_graph(g_path)
            continue

        print('Invalid command')


