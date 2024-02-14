import random, math
import pomeloabc_OI.Generator.Utils as utils

class Graph():
    class Edge():
        def __init__(self, u, v, w):
            self.u = u
            self.v = v
            self.w = w
    
    def __add_edge(g, u, v, w):
        g.append(Graph.Edge(u, v, w))

    def graph(self, node_size, edge_size, directed = False, self_loop = False, repeat_edges = False, weight_limit = None):
        if weight_limit == None:
            weight_gen = None
        elif utils.basicdt_like(weight_limit):
            weight_gen = weight_limit
        else:
            weight_gen = lambda: random.randint(weight_limit[0], weight_limit[1])
        
        graph, used_edges, cnt = list(), set(), 0

        if 0 <= edge_size <= int(node_size * math.log2(node_size)):
            while cnt < edge_size:
                u, v = random.randint(1, node_size), random.randint(1, node_size)

                if (not self_loop and u == v) or (not repeat_edges and (u, v) in used_edges):
                    continue
                
                if weight_gen == None or utils.basicdt_like(weight_gen):
                    Graph.__add_edge(graph, u, v, weight_gen)
                else:
                    Graph.__add_edge(graph, u, v, weight_gen())

                if not repeat_edges:
                    used_edges.add((u, v))
                    if not directed:
                        used_edges.add((v, u))

                cnt += 1

        elif int(node_size * math.log2(node_size)) < edge_size <= node_size * (node_size - 1) // 2:
            unused_edges = [(i, j) for i in range(1, node_size + 1) for j in range(1, node_size + 1) if not self_loop and i != j]
            random.shuffle(unused_edges)

            for edge in unused_edges:
                if cnt >= edge_size:
                    break

                u, v = edge[0], edge[1]

                if (not self_loop and u == v) or (not repeat_edges and (u, v) in used_edges):
                    continue

                if weight_gen == None or utils.list_like(weight_gen):
                    Graph.__add_edge(graph, u, v, weight_gen)
                else:
                    Graph.__add_edge(graph, u, v, weight_gen())

                if not repeat_edges:
                    used_edges.add((u, v))
                    if not directed:
                        used_edges.add((v, u))

                cnt += 1

        return [(node_size, edge_size), graph]
    
    def tree(self, node_size, chain = False, flower = False, directed = False, self_loop = False, repeat_edges = False, weight_limit = None):
        if weight_limit == None:
            weight_gen = None
        elif utils.basicdt_like(weight_limit):
            weight_gen = weight_limit
        else:
            weight_gen = lambda: random.randint(weight_limit[0], weight_limit[1])

        graph = list()
        chain_cnt, flower_cnt = int((node_size - 1) * chain), int((node_size - 1) * flower)
        
        if chain_cnt > node_size - 1:
            chain_cnt = node_size - 1
        if chain_cnt + flower_cnt > node_size - 1:
            flower_cnt = node_size - 1 - chain_cnt
        rand_cnt = node_size - 1 - chain_cnt - flower_cnt
        
        for i in range(2, chain_cnt + 2):
            if weight_gen == None or utils.basicdt_like(weight_gen):
                Graph.__add_edge(graph, i - 1, i, weight_gen)
            else:
                Graph.__add_edge(graph, i - 1, i, weight_gen())
        
        for i in range(chain_cnt + 2, chain_cnt + flower_cnt + 2):
            if weight_gen == None or utils.basicdt_like(weight_gen):
                Graph.__add_edge(graph, 1, i, weight_gen)
            else:
                Graph.__add_edge(graph, 1, i, weight_gen())
        
        for i in range(node_size - rand_cnt + 1, node_size + 1):
            u = random.randrange(1, i)

            if weight_gen == None or utils.basicdt_like(weight_gen):
                Graph.__add_edge(graph, u, i, weight_gen)
            else:
                Graph.__add_edge(graph, u, i, weight_gen())
        
        return [(node_size, node_size - 1), graph]
    
    def chain(self, node_size, directed = False, self_loop = False, repeat_edges = False, weight_limit = None):
        return Graph.tree(node_size, True, False, directed = directed, self_loop = self_loop, repeat_edges = repeat_edges, weight_limit = weight_limit)
    
    def flower(self, node_size, directed = False, self_loop = False, repeat_edges = False, weight_limit = None):
        return Graph.tree(node_size, False, True, directed = directed, self_loop = self_loop, repeat_edges = repeat_edges, weight_limit = weight_limit)
    
    def format(self, data):
        res = "{} {}\n".format(data[0][0], data[0][1])

        for edge in data[1]:
            u, v, w = edge.u, edge.v, edge.w

            if w != None:
                res += "{} {} {}\n".format(u, v, w)
            else:
                res += "{} {}\n".format(u, v)

        return res[:-1]