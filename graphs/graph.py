from collections import deque


class Graph:
    """ Graph Class
    Represents a directed or undirected graph.
    """
    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.vertex_dict = {} # id -> list of neighbor ids
        self.is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key.
        
        Parameters:
        vertex_id (string): The unique identifier for the new vertex.
        """
        self.vertex_dict[vertex_id] = []

    def add_edge(self, start_id, end_id):
        """
        Add an edge from vertex with id `start_id` to vertex with id `end_id`.

        Parameters:
        start_id (string): The unique identifier of the first vertex.
        end_id (string): The unique identifier of the second vertex.
        """
        self.vertex_dict[start_id].append(end_id)
        # if not self.is_directed:
        #     self.vertex_dict[end_id].append(start_id)

    def contains_vertex(self, vertex_id):
        """Return True if the vertex is contained in the graph."""
        return vertex_id in self.vertex_dict

    def contains_edge(self, start_id, end_id):
        """
        Return True if the edge is contained in the graph from vertex `start_id`
        to vertex `end_id`.

        Parameters:
        start_id (string): The unique identifier of the first vertex.
        end_id (string): The unique identifier of the second vertex."""
        return end_id in self.vertex_dict[start_id]

    def get_vertices(self):
        """
        Return all vertices in the graph.
        
        Returns:
        list<string>: The vertex ids contained in the graph.
        """
        return list(self.vertex_dict.keys())

    def get_neighbors(self, start_id):
        """
        Return a list of neighbors to the vertex `start_id`.

        Returns:
        list<string>: The neigbors of the start vertex.
        """
        if self.is_directed:
            return self.vertex_dict[start_id]

        neighbors = []
        for vertex in self.vertex_dict:
            if start_id in self.vertex_dict[vertex]:
                neighbors.append(vertex)
        neighbors.extend(self.vertex_dict[start_id])
        return neighbors

    def __str__(self):
        """Return a string representation of the graph."""
        graph_repr = [f'{vertex} -> {self.vertex_dict[vertex]}' 
            for vertex in self.vertex_dict.keys()]
        return f'Graph with vertices: \n' +'\n'.join(graph_repr)

    def __repr__(self):
        """Return a string representation of the graph."""
        return self.__str__()

    def bfs_traversal(self, start_id):
        """
        Example of traversing the graph using breadth-first search.
        """
        if start_id not in self.vertex_dict:
            raise KeyError("The start vertex is not in the graph!")

        # Keep a set to denote which vertices we've seen before
        seen = set()
        seen.add(start_id)

        # Keep a queue so that we visit vertices in the appropriate order
        queue = deque()
        queue.append(start_id)

        while queue:
            current_vertex_id = queue.popleft()

            # Process current node
            print('Processing vertex {}'.format(current_vertex_id))

            # Add its neighbors to the queue
            for neighbor_id in self.get_neighbors(current_vertex_id):
                if neighbor_id not in seen:
                    seen.add(neighbor_id)
                    queue.append(neighbor_id)

        return # everything has been processed

    def find_shortest_path(self, start_id, target_id):
        """
        Find and return the shortest path from start_id to target_id.

        Parameters:
        start_id (string): The id of the start vertex.
        target_id (string): The id of the target (end) vertex.

        Returns:
        list<string>: A list of all vertex ids in the shortest path, from start to end.
        """
        if start_id not in self.vertex_dict:
            raise KeyError("The start vertex is not in the graph!")

        path_dict = {start_id: [start_id]}
        queue = deque()
        queue.append(start_id)

        while len(queue) > 0:
            vertex = queue.popleft()

            if vertex == target_id:
                break
            
            for neighor_id in self.get_neighbors(vertex):
                if neighor_id not in path_dict:
                    path_dict[neighor_id] = list(path_dict[vertex])
                    path_dict[neighor_id].append(neighor_id)
                    queue.append(neighor_id)

        return path_dict[target_id]


    def find_vertices_n_away(self, start_id, target_distance):
        """
        Find and return all vertices n distance away.
        
        Arguments:
        start_id (string): The id of the start vertex.
        target_distance (integer): The distance from the start vertex we are looking for

        Returns:
        list<string>: All vertex ids that are `target_distance` away from the start vertex
        """
        if start_id not in self.vertex_dict:
            raise KeyError("The start vertex is not in the graph!")

        target_vertcies = []
        distance = {start_id: 0}
        queue = deque([start_id])

        while len(queue) > 0:
            vertex = queue.popleft()

            # Process Vertext
            if distance[vertex] == target_distance:
                target_vertcies.append(vertex)
            elif distance[vertex] > target_distance:
                break

            for neighbor in self.get_neighbors(vertex):
                if neighbor not in distance:
                    distance[neighbor] = distance[vertex] + 1
                    queue.append(neighbor)

        return target_vertcies

    def is_bipartite(self):
        """
        Return True if the graph is bipartite, and False otherwise.
        """
        start_id = list(self.vertex_dict.keys())[0]

        # Keep a set to denote which vertices we've seen before and their color (0, 1)
        vertex_colors = {start_id: True}

        # Keep a queue so that we visit vertices in the appropriate order
        queue = deque()
        queue.append(start_id)

        while queue:
            vertex = queue.popleft()

            # Add its neighbors to the queue
            for neighbor in self.get_neighbors(vertex):
                if neighbor not in vertex_colors:
                    vertex_colors[neighbor] = not vertex_colors[vertex]
                    queue.append(neighbor)
                elif vertex_colors[neighbor] == vertex_colors[vertex]:
                    return False

        return True

    def find_connected_components(self):
        """
        Return a list of all connected components, with each connected component
        represented as a list of vertex ids.
        """
        components = []
        not_visited = list(self.vertex_dict.keys())
        
        while not_visited:
            start_id = not_visited.pop()
            
            # Keep a set to denote which vertices we've seen before
            seen = set()
            seen.add(start_id)

            # Keep a queue so that we visit vertices in the appropriate order
            queue = deque()
            queue.append(start_id)

            while queue:
                current_vertex_id = queue.popleft()

                # Add its neighbors to the queue
                for neighbor_id in self.get_neighbors(current_vertex_id):
                    if neighbor_id not in seen:
                        seen.add(neighbor_id)
                        not_visited.remove(neighbor_id)
                        queue.append(neighbor_id)
            components.append(list(seen))
            
        return components

    def dfs_traversal(self, start_id):
        """Visit each vertex, starting with start_id, in DFS order."""

        visited = set() # set of vertices we've visited so far

        def dfs_traversal_recursive(start_vertex):
            print(f'Visiting vertex {start_vertex.get_id()}')

            # recurse for each vertex in neighbors
            for neighbor in start_vertex.get_neighbors():
                if neighbor.get_id() not in visited:
                    visited.add(neighbor.get_id())
                    dfs_traversal_recursive(neighbor)
            return

        visited.add(start_id)
        dfs_traversal_recursive(start_id)

    def find_path_dfs_iter(self, start_id, target_id):
        """
        Use DFS with a stack to find a path from start_id to target_id.
        """
        if start_id not in self.vertex_dict:
            raise KeyError("The start vertex is not in the graph!")

        # Keep a set to denote which vertices we've seen before and the path up to them
        path_dict = {start_id: [start_id]}

        # Keep a queue so that we visit vertices in the appropriate order
        stack = list()
        stack.append(start_id)

        while stack:
            vertex = stack.pop()

            if vertex == target_id:
                return path_dict[target_id]

            # Add its neighbors to the queue
            for neighbor in self.get_neighbors(vertex):
                if neighbor not in path_dict:
                    path_dict[neighbor] = path_dict[vertex]
                    path_dict[neighbor].append(neighbor)
                    stack.append(neighbor)

    def contains_cycle(self):
        """
        Return True if the directed graph contains a cycle, False otherwise.
        """
        
        not_visited = list(self.vertex_dict.keys())

        while not_visited:
            start_id = not_visited.pop()
            current_path = set()
            
            def dfs_traversal_recursive(start_vertex):
                contains_cycle = False

                # recurse for each vertex in neighbors
                for neighbor in self.get_neighbors(start_vertex):
                    if neighbor in not_visited:
                        not_visited.remove(neighbor) # This operation is O(n) where n is the vertices in the not_visited.
                        # The above operation makes this algorith slower rather than using a set for visited and fillin it
                        # but is better for space because its only creating one array rather than a set for the visted and
                        # an array of arrays for the different connected components possible in the graph.
                        current_path.add(neighbor)
                        contains_cycle = dfs_traversal_recursive(neighbor)
                    elif neighbor in current_path:
                        return True
                current_path.remove(start_vertex)
                return contains_cycle

            current_path.add(start_id)
            return dfs_traversal_recursive(start_id)
        

    def topological_sort(self):
        """
        Return a valid ordering of vertices in a directed acyclic graph.
        If the graph contains a cycle, throw a ValueError.
        """
        if self.contains_cycle():
            return ValueError('Graph contains cycle and cannot be sorted.')
        
        # Create a stack to hold the vertex ordering.
        stack = list()
        
        # For each unvisited vertex, execute a DFS from that vertex.
        not_visited = list(self.vertex_dict.keys())

        while not_visited:
            start_id = not_visited.pop()

            def dfs_traversal_recursive(start_vertex):
                # recurse for each vertex in neighbors
                for neighbor in self.get_neighbors(start_vertex):
                    if neighbor in not_visited:
                        not_visited.remove(neighbor)
                        dfs_traversal_recursive(neighbor)
                # On the way back up the recursion tree, add the vertex to the stack.
                stack.append(start_vertex)

            dfs_traversal_recursive(start_id)

        # Reverse the contents of the stack and return it as a valid ordering.
        return list(reversed(stack))

