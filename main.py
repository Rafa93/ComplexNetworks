import itertools
import networkx as nx
import matplotlib.pyplot as plt
from utils import *


def build_matrix_tfidf(graph):

    ingredients_nodes = [n for n, d in graph.nodes(data=True) if d["bipartite"] == 1]
    recipes_nodes = [n  for n, d in graph.nodes(data=True) if d["bipartite"] == 0]

    matrix_tf_idf = {}  # given a ingredient return a similarity vector
    for ing in ingredients_nodes:
        matrix_tf_idf[ing] = {}
        for ing2 in ingredients_nodes:
            matrix_tf_idf[ing][ing2] = 0

    # por cada receta actualizar la matrix de similaridad
    for recipe in recipes_nodes:
        neihbors = [node for node in graph.neighbors(recipe)]
        n = len(neihbors)
        i, j = 0, 0
        for ing in neihbors:
            for ing2 in neihbors:
                if ing != ing2:
                    matrix_tf_idf[ing][ing2] += 1
                    matrix_tf_idf[ing2][ing] += 1
            continue
    return matrix_tf_idf



#type 1 = ingredients
#type 0 = recipes
def rank_and_print_ingr(graph, n, type):

    ingredients_nodes = {(n, graph.degree[n]) for n, d in graph.nodes(data=True) if d["bipartite"] == type}
    ingredients_nodes = sorted(ingredients_nodes, key= lambda x:x[1], reverse=True)
    print(ingredients_nodes[:n])

    x = range(1, 11)
    x = [x for (x,y) in ingredients_nodes]
    degrees = [y for (x, y) in ingredients_nodes]

    if type ==1:
        plt.title('Rank of ' + format(n) + ' most frequently ingredients used in recipes')
    else:
        plt.title('Rank of ' + format(n) + ' biggest recipes')
    plt.plot(x[:n], degrees[:n])
    plt.show()



if __name__ == '__main__':

    g_path = "D:\pythonProject1\libro de recetas"
    graphs = {}
    nx_graph = None
    top_nodes = None
    bottom_nodes = None
    matrix_tf_idf = None
    recipes_and_categories = {}

    print('Welcome, availables options are:')
    print('General commands: load_graph, categories, subcategories, recipes, ingredients, exit')
    print('Class 2 node-centralities: degree, closeness, eigenvector, betweenneess, pagerank, closeness_vitality')
    print('Class 2 edge-centralities: edge_betwenness')
    print('Class 5 community detection: girvan_newman, asyn_fluidc, asyn_lpa, k_clique, kernighan_lin')
    print('Others: ingredient_similarity X, recipe_similarity X')
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
            matrix_tf_idf = build_matrix_tfidf(nx_graph) # CREA LA MATRIZ

            # Separate by group
            l, r = nx.bipartite.sets(nx_graph)
            pos = {}

            # Update position for node from each group
            pos.update((node, (1, index)) for index, node in enumerate(l))
            pos.update((node, (2, index)) for index, node in enumerate(r))

            nx.draw_networkx(nx_graph, pos=pos, with_labels=False, node_size=20)
            plt.show()

            top_nodes = {n for n, d in nx_graph.nodes(data=True) if d["bipartite"]==0} # recetas
            bottom_nodes = set(nx_graph) - top_nodes # ingredientes
            nx.draw_networkx(nx_graph, node_size=20, with_labels=False)
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
            rank_and_print_ingr(nx_graph, 5, 0)
            print(top_nodes)
            continue
        if (command == "ingredients"):
            # ranking de los ingredientes mas importantes
            print('Count of Ingredients: ', len(bottom_nodes))
            rank_and_print_ingr(nx_graph, 10, 1)
            continue

        # Clase 2
        if (command == "degree"):
            c= nx.degree_centrality(nx_graph)
            degree = sorted(c.items(), key=lambda x: x[1], reverse=True)
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

        # Ideas mias
        if (command == "ingr_similarity"):
            # Dado la matriz tf-idf de ingredientes

            # dos propuestas
            # la 1ra, quitar X
            # El maximo de alguien es X? Seria el candidato ideal, deriva en
            # encontrar el maximo X en alguien, o lo q es lo mismo
            # buscar en el vector X el maximo
            # el maximo de cada vector indicara el ingrediente sustituto
            # proponer ese/esos  ingrediente/s

            # quien puede romper esta idea, los ingredientes q aparecen 1 vez o pocas veces.
            #porque todos con los q apareciste son posibles candidatos,
            #cuando es bueno aplicar esta idea, cuando el ingrediente aparece las "suficientes veces"
            # por eso hablar de un "coeficiente de desestimacion" de ingredientes candidatos

            x = path
            if x in matrix_tf_idf.keys():
                y = matrix_tf_idf[x]
                y = sorted(y.items(), key= lambda x:x[1], reverse=True)
                print(y[:3])
            else:
                print(x, ' this ingredient do not exists')

            continue
        if (command == "recipes_similarity"):
            continue

        if (command == "exit"):
            break
        print('Invalid command')
