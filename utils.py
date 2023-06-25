import os
from pandas_ods_reader import read_ods
import networkx as nx
import matplotlib.pyplot as plt

#####------- LOAD GRAPH METHODS --------------------
def load_graph(path):
    files = load_ods(path)
    return files

def load_ods(path):
    ls = os.listdir(path)
    files = []
    for file in ls:
        if file.__contains__('.ods'):
            real_path = path + "//" + file
            print(real_path)

            #load ODS file
            ods_file = read_ods(real_path, 1, columns=['Ingrediente', 'Modificador', 'Cantidad', 'Medida', 'Medida Exacta',
                                                       'Opcional',    'Receta',      'Categoria','Subcategoria', 'Preparacion'])
            files.append(ods_file)
        break
    return files


def ods_to_graph(ods_files):

    B = nx.Graph()
    recipes_set = set() #LLave Receta, Valor: lista de ingredientes
    ingredients_set = set()
    categories_sub_recipes = {}

    # Iterar por cada columna del fichero ODS
    for i in ods_files:
        length = len(i['Ingrediente'])
        for j in range(length):
            ing = i['Ingrediente'][j]
            m = i['Modificador'][j]
            c = i['Cantidad'][j]
            me = i['Medida'][j]
            mee = i['Medida Exacta'][j]
            o = i['Opcional'][j]
            rec = i['Receta'][j]
            cat = i['Categoria'][j]
            subcat = i['Subcategoria'][j]
            pre = i['Preparacion'][j]

            # UTILIZAR Ingredientes y Recetas
            if ing not in ingredients_set:
                ingredients_set.add(ing)
                B.add_nodes_from([ing], bipartite=1)

            # las recetas pertenecen a una categoria y subcategoria
            if rec not in recipes_set:
                recipes_set.add(rec)
                B.add_nodes_from([rec], bipartite=0)

                if cat not in categories_sub_recipes.keys(): #categoria nueva
                    categories_sub_recipes[cat] = {}

                if subcat not in categories_sub_recipes[cat].keys(): #subcategoria nueva
                    categories_sub_recipes[cat][subcat] = []

                categories_sub_recipes[cat][subcat].append(rec)



            #Añadir arista
            B.add_edges_from([(ing, rec)])

    return B, categories_sub_recipes



######--------------- PRINT GRAPHS METHODS ----------------------------------

def print_cat(categories):

    cate = len(categories.keys())
    print('Count of Categories: ', cate)
    i = 1
    for cat in categories.keys():
        print(i, ' - ', cat)
        i+=1

def print_subcat(categories):
    sum = 0
    names = []

    for cat in categories.keys():
        names.append(categories[cat].keys())
        sum += len(categories[cat].keys())
    print('Count of SubCategories: ', sum)
    print(names)

def paint_graph(graph, val_map):

    values = [value for key,value in val_map]
    nx.draw(graph, cmap=plt.get_cmap('viridis'),node_size=90, node_color=values, with_labels=False, font_color='white')
    plt.show()

def paint_edged_graph(graph, edge_weights):

    for u,v, d in graph.edges(data=True):
        d['weight'] = edge_weights[(u,v)]

    edges, weights = zip(*nx.get_edge_attributes(graph, 'weight').items())
    nx.draw(graph, node_color='w', node_size=70, edge_color= weights)
    plt.show()
