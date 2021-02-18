from graphs.graph import Graph


def read_graph_from_file(filename):
    """
    Read in data from the specified filename, and create and return a graph
    object corresponding to that data.

    Arguments:
    filename (string): The relative path of the file to be processed

    Returns:
    Graph: A directed or undirected Graph object containing the specified
    vertices and edges
    """

    # Use 'open' to open the file
    with open(filename) as graph_file:
        graph_file_lines = graph_file.readlines()

    # Use the first line (G or D) to determine whether graph is directed 
    # and create a graph object
    direction = graph_file_lines[0].strip()
    if direction != 'G' and direction != 'D':
        raise ValueError('File is in an imporper format')
    graph = Graph(is_directed=direction is 'D')

    # Use the second line to add the vertices to the graph
    for vertex in graph_file_lines[1].strip().split(','):
        graph.add_vertex(vertex)

    # Use the 3rd+ line to add the edges to the graph
    for edge in graph_file_lines[2:]:
        edge = edge.strip().split(',')
        graph.add_edge(edge[0][1], edge[1][0])

    graph_file.close()
    return graph


read_graph_from_file('./test_files/graph_small_directed.txt')