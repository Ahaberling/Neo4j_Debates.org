from graph_tool.all import *

'''
    with open("Output.txt", "w") as text_file:
    print("explo", file=text_file)
'''


g = graph_tool.Graph()
v1 = g.add_vertex()
v2 = g.add_vertex()
e = g.add_edge(v1, v2)

graph_draw(g, vertex_text=g.vertex_index, output="two-nodes.pdf")

print(v1.out_degree())
print(e.source(), e.target())
print(e.source(), e.target())

vlist = g.add_vertex(10)
print(len(list(vlist)))

print(g)

v = g.add_vertex()
print(g.vertex_index[v])

print(int(v))
