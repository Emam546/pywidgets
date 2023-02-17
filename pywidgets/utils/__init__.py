from pycv2.img.utils import closest_node_index
def closest_node(node, nodes,maxdistance=float("inf")):
    close=closest_node_index(node, nodes,maxdistance)
    if close!=None:
        return nodes[close[0]]