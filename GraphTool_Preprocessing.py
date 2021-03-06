import graph_tool.all as gt
import numpy as np
#import matplotlib.pyplot as plt
#import scipy.stats as stats
import sys


######################
### Initialization ###
######################

np.set_printoptions(threshold=sys.maxsize)

g_raw = gt.load_graph('debate.org_with_issues_mod.graphml', fmt='graphml')
# DO NOT USE g_raw FOR ASSORTATIVITY ANALYSIS! It contains uni- and bilateral FRIENDS_WITH relations.
# This is intentional due to the optional privacy setting of friendships in debate.org. See report for details.
# g_raw contains nodes: User, Issues
# g_raw contains edges: FRIENDS_WITH, GIVES_ISSUES

approach1_bool = True
approach2_bool = True           # relies on results from approach 1
approach3_bool = True           # relies on results from approach 2
summary_bool = True


###########################
### Graph Preprocessing ###
###########################

# There are 3 kind of User nodes that are handled differently by each of the following approaches.
# The kind of User nodes in focus:
# A: User nodes with friendship visibility setting on PRIVATE AND     being nominated as friend by any other User node (jusitfied unidirectional edge)
# B: User nodes with friendship visibility setting on PRIVATE AND NOT being nominated as friend by any other User node (private isolated)
# C: User nodes with friendship visibility setting on PUBLIC  AND     being nominated as friend by any other User node AND and empty friends list
#    (User contains UNJUSTIFIED unidirectional edge - this is faulty. These 331 edges must not exist. I assume this is caused by faulty data
#    crawling/scraping, see Report)

g_raw_friend = gt.GraphView(g_raw, vfilt=lambda v: g_raw.vp.userID[v] != "")
# g_raw_friend contains nodes: Users; edges: FRIENDS_WITH

g_raw_issues = gt.GraphView(g_raw, vfilt=lambda v: g_raw.vp.issuesID[v] != "")
# g_raw_issues contains nodes: Users, Issues; edges: GIVES_ISSUES


#--- Approach 1: Keep all User nodes AND make A & C bidirectional ---#

if approach1_bool == True:
    print("\n\nApproach 1 - Keep all User nodes AND make A & C bidirectional\n")

    g_ap1 = g_raw
    tuplelist = list(map(tuple, g_raw_friend.get_edges()))

    no_e_before = len(g_ap1.get_edges())        # Number of edges before applying approach 1

    c = 0
    c_newE = 0                                  # Counter for number of edges created following approach 1
    c_max = len(g_raw_friend.get_edges())

    for e in g_raw_friend.get_edges():
        c = c + 1
        source = e[0]
        target = e[1]

        if (target, source) not in tuplelist:   # target and source switched to create the missing edge in the opposite direction
            c_newE = c_newE + 1
            g_ap1.add_edge(target, source)

        if c % 10000 == 0:
            print(c, "/", c_max)

    print(c_max, "/", c_max)

    print("Unidirectional friend edges made bidirectional: ", c_newE)                                           #  45135
    print("Number of edges (Friendship & Issues) before making A & C bidirectional: ", no_e_before)             # 188965
    print("Number of edges (Friendship & Issues) after  making A & C bidirectional: ", len(g_ap1.get_edges()))  # 234100

    g_ap1.save("Graph_Preprocessed_Approach1.graphml")

    g_ap1_friend = gt.GraphView(g_ap1, vfilt=lambda v: g_ap1.vp.userID[v] != "")
    g_ap1_issues = gt.GraphView(g_ap1, vfilt=lambda v: g_ap1.vp.issuesID[v] != "")

    print("\nApproach 1 - Keep all User nodes AND make A & C bidirectional - done\n")


#--- Approach 2: Remove B AND make A & C bidirectional ---#

if approach2_bool == True:
    print("\nApproach 2 - Remove B AND make A & C bidirectional\n")

    g_ap2 = g_ap1

    vprop_approach2 = g_ap2.new_vertex_property("bool")
    g_ap2.vp.approach2 = vprop_approach2

    for v in g_ap2.get_vertices():
        g_ap2.vp.approach2[v] = True

    c = 0
    c_max = len(g_ap1_friend.get_vertices())

    for v in g_ap1_friend.get_vertices():
        c = c + 1
        if len(g_ap1_friend.get_all_neighbors(v)) <= 0:         # or "==False"
            if g_ap1_friend.vp.friend_privacy[v] == True:
                g_ap2.vp.approach2[v] = False

        if c % 10000 == 0:
            print(c, "/", c_max)

    print(c_max, "/", c_max)

    no_v_before = len(g_ap2.get_vertices())                     # Number of vertices before applying approach 2 ontop of ap 2
    no_e_before = len(g_ap2.get_edges())                        # Number of edges    before applying approach 2 ontop of ap 2

    g_ap2 = gt.GraphView(g_ap2, vfilt=lambda v: g_ap2.vp.approach2[v] == True)

    print("Number of nodes removed: ", no_v_before - len(g_ap2.get_vertices()))                     #   5648 (User)
    print("Number of edges removed: ", no_e_before - len(g_ap2.get_edges()))                        #   5648 (GIVES_ISSUES)
    print("Number of nodes (User & Issues)       before removing B: ", no_v_before)                 #  90696
    print("Number of edges (Friendship & Issues) before removing B: ", no_e_before)                 # 234100
    print("Number of nodes (User & Issues)       after removing B: ", len(g_ap2.get_vertices()))    #  85048
    print("Number of edges (Friendship & Issues) after removing B: ", len(g_ap2.get_edges()))       # 228452

    g_ap2.save("Graph_Preprocessed_Approach2.graphml")

    g_ap2_friend = gt.GraphView(g_ap2, vfilt=lambda v: g_ap2.vp.userID[v] != "")
    g_ap2_issues = gt.GraphView(g_ap2, vfilt=lambda v: g_ap2.vp.issuesID[v] != "")

    print("\nApproach 2 - Remove B AND make A & C bidirectional - done\n")


#--- Approach 3: Remove B & C AND make A bidirectional ---#

if approach3_bool == True:
    print("\nApproach 3 - Remove B & C AND make A bidirectional\n")

    g_ap3 = g_ap2

    vprop_approach3 = g_ap3.new_vertex_property("bool")
    g_ap3.vp.approach3 = vprop_approach3

    for v in g_ap3.get_vertices():
        g_ap3.vp.approach3[v] = True

    g_raw_friend_noPriv = gt.GraphView(g_raw_friend, vfilt=lambda v: g_raw.vp.friend_privacy[v] == False)  # 311 edges regarding C
    tuplelist = list(map(tuple, g_raw_friend_noPriv.get_edges()))

    c = 0
    c_badE = 0                                          # Counter for number of faulty edges
    c_max = len(g_raw_friend_noPriv.get_edges())

    for e in g_raw_friend_noPriv.get_edges():
        c = c + 1
        source = e[0]
        target = e[1]

        if (target, source) not in tuplelist:
            c_badE = c_badE + 1
            g_ap3.vp.approach3[target] = False          # This results in 187 "faulty" nodes labeled as False and later on excluded in the Graphimage regarding approach 3.
                                                        # Some of the 311 identified invalide edges (c_badE) refere to the same "target", hence the number of
                                                        # faulty nodes is < 311 (some nodes are labeled False multiple times)
        if c % 10000 == 0:
            print(c, "/", c_max)

    print(c_max, "/", c_max)

    print("Number of edges identified as belonging to C: ", c_badE)                                 # 331

    no_v_before = len(g_ap3.get_vertices())
    no_e_before = len(g_ap3.get_edges())

    g_ap3 = gt.GraphView(g_ap3, vfilt=lambda v: g_ap3.vp.approach3[v] == True)

    print("Number of nodes (User & Issues)       before removing C: ", no_v_before)                 #  85048
    print("Number of edges (Friendship & Issues) before removing C: ", no_e_before)                 # 228452
    print("Number of nodes (User & Issues)       after removing C: ", len(g_ap3.get_vertices()))    #  84861
    print("Number of edges (Friendship & Issues) after removing C: ", len(g_ap3.get_edges()))       # 227603

    # 228452 - 227603 = 849
    # Why 849 edges removed? Because:
    #   311 (unjustified unidirectional friendship)
    # + 311 (made bidirectional in approach A)
    # + 187 (GIVES_ISSUES relation, since 187 nodes where removed)

    g_ap3.save("Graph_Preprocessed_Approach3.graphml")

    g_ap3_friend = gt.GraphView(g_ap3, vfilt=lambda v: g_ap3.vp.userID[v] != "")
    g_ap3_issues = gt.GraphView(g_ap3, vfilt=lambda v: g_ap3.vp.issuesID[v] != "")

    print("\nApproach 3 - Remove B & C AND make A bidirectional - done\n")

    # Issues nodes of respective user nodes deleted in approach B and C are still part of the saved Graphs
    # Graph_Preprocessed_Approach2.graphml & Graph_Preprocessed_Approach3.graphml
    # -> These Issue nodes are best handled later on, by deleting them as well


#--- Summary ---#

if approach1_bool == True:

    print("\nSummary\n")

    print(g_ap1)                                                                                            # 90696 vertices and 234100 edges
    print(g_ap2)                                                                                            # 85048 vertices and 228452 edges
    print(g_ap3)                                                                                            # 84861 vertices and 227603 edges

    print("AP1 - Number of nodes (User): ", len(g_ap1_friend.get_vertices()))                               #  45348
    print("AP1 - Number of edges (Friends): ", len(g_ap1_friend.get_edges()))                               # 188752

    print("\n AP2 - Number of nodes (User): ", len(g_ap2_friend.get_vertices()))                            #  39700
    print("AP2 - Number of edges (Friends): ", len(g_ap2_friend.get_edges()))                               # 188752

    print("\n AP3 - Number of nodes (User): ", len(g_ap3_friend.get_vertices()))                            #  39513
    print("AP3 - Number of edges (Friends): ", len(g_ap3_friend.get_edges()))                               # 188090


    print("\n AP1 - Number of nodes (Issues): ", len(g_ap1_issues.get_vertices()))                          # 45348
    print("AP1 - Number of edges (gives_Issues): ", len(g_ap1.get_edges())-len(g_ap1_friend.get_edges()))   # 45348

    print("\n AP2 - Number of nodes (Issues): ", len(g_ap2_issues.get_vertices()))                          # 45348
    print("AP2 - Number of edges (gives_Issues): ", len(g_ap2.get_edges())-len(g_ap2_friend.get_edges()))   # 39700

    print("\n AP3 - Number of nodes (Issues): ", len(g_ap3_issues.get_vertices()))                          # 45348
    print("AP3 - Number of edges (gives_Issues): ", len(g_ap3.get_edges())-len(g_ap3_friend.get_edges()))   # 39513

    print("\nSummary - done\n")
    print("\nGraphTool_Preprocessing.py - done\n")