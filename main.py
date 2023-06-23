import itertools
import os
from pandas_ods_reader import read_ods
import networkx as nx
import matplotlib.pyplot as plt


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

if __name__ == '__main__':

    g_path = "D:\pythonProject1\libro de recetas"
    graphs = {}
    nx_graph = None
    top_nodes = None
    bottom_nodes = None

    recipes_and_categories = {}

    print('Welcome, availables options are:')
    print('General commands: load_graph, categories, subcategories, recipes, ingredients, exit')
    print('Class 2 node-centralities: degree, closeness, eigenvector, betweenneess, pagerank, closeness_vitality')
    print('Class 2 edge-centralities: edge_betwenness')
    print('Class 5 community detection: girvan_newman, asyn_fluidc, asyn_lpa, k_clique, kernighan_lin')
    while(True):
        str = input('Type a command\n')
        line = str.split(" ")
        command = line[0]
        path = "None"
        if len(line) > 1:
            path = line[1]


        if (command == "load_graph"):
            if (path == "None"):
                path = g_path
            files = load_graph(path)
            nx_graph, recipes_and_categories = ods_to_graph(files) #CARGA EL GRAFO
            nx.write_graphml(nx_graph, "recipes.graphml")  #SALVA EL GRAFO

            top_nodes = {n for n, d in nx_graph.nodes(data=True) if d["bipartite"]==0}
            bottom_nodes = set(nx_graph) - top_nodes

            nx.draw(nx_graph)
            plt.show()
            continue

        if (command == "categories"):
            print_cat(recipes_and_categories)
            continue
        if (command == "subcategories"):
            print_subcat(recipes_and_categories)
            continue
        if (command == "recipes"):
            print('Count of recipes: ', len(top_nodes))
            print(top_nodes)
            continue
        if (command == "ingredients"):
            print('Count of Ingredients: ', len(bottom_nodes))
            continue


    # Clase 2

        if (command == "degree"):
            c= nx.degree_centrality(nx_graph)
            degree = sorted(c.items(), key=lambda x:x[1], reverse=True)
            print('Degree centrality for nodes ', degree)
            paint_graph(nx_graph, degree)
            continue

        if (command == "closeness"):
            c = nx.closeness_centrality(nx_graph,distance=None)
            degree = sorted(c.items(), key=lambda x: x[1], reverse=True)
            print('Closeness centrality for nodes ', degree)
            paint_graph(nx_graph, degree)
            continue

        if (command == "eigenvector"):
            c= nx.eigenvector_centrality(nx_graph)
            degree = sorted(c.items(), key=lambda x:x[1], reverse=True)
            print('Eigenvector centrality ', degree)
            paint_graph(nx_graph, degree)
            continue

        if (command == "betweenness"):
            c =nx.betweenness_centrality(nx_graph)
            degree = sorted(c.items(), key=lambda x: x[1], reverse=True)
            print('Betweenness ', degree)
            paint_graph(nx_graph, degree)
            continue

        if (command == "pagerank"):
            c =nx.pagerank(nx_graph)
            degree = sorted(c.items(), key=lambda x: x[1], reverse=True)
            print('Pagerank ', degree)
            paint_graph(nx_graph, degree)
            continue

        if (command == "closeness_vitality"): #en el nodo, en el curso sale respecto a la arista
            c =nx.closeness_vitality(nx_graph,node=None)
            degree = sorted(c.items(), key=lambda x: x[1], reverse=True)
            print('Closeness vitality ', degree)
            paint_graph(nx_graph, degree)
            continue

        if (command == "edge_betwenness"):
            c =nx.edge_betweenness_centrality(nx_graph)
            degree = sorted(c.items(), key=lambda x: x[1], reverse=True)
            paint_edged_graph(nx_graph, c)
            print('edge betweenness ', degree)
            continue

        #Clase 5
        if (command == "girvan_newman"):
            comp = nx.community.girvan_newman(nx_graph)
            k=4
            limited = itertools.takewhile(lambda c: len(c) <= k, comp)
            for comunities in limited:
                print(tuple(sorted(c) for c in comunities))
            continue

        if (command=="asyn_fluidc"):
            comp = nx.community.asyn_fluidc(nx_graph, 4)
            for comunities in comp:
                print(comunities)
            continue
        if (command=="asyn_lpa"):
            comp = nx.community.asyn_lpa_communities(nx_graph)
            k=4
            for f in comp:
                print(f)
            continue

        if (command=="k_clique"):
            cmp = nx.community.k_clique_communities(nx_graph, 2) # con K>2 da solucion vacia
            for f in cmp:
                print(f)
            continue

        if (command== "kernighan_lin"):
            (a,b) = nx.community.kernighan_lin_bisection(nx_graph, max_iter=100)
            print(a)
            print(b)
            continue

        if (command == "exit"):
            break
        print('Invalid command')


