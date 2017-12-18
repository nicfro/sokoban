from mapGeneration import 

W = "#"
E = " "

class Node(object):
    def __init__(self, i, j):
        self.con = []  # Box can move from here to connected nodes
        self.i = i
        self.j = j
        
    def __repr__(self):
        return "Node(%d, %d)" % (self.i, self.j)

def find_deadlocks(m):
    m = fix_map(m)
    
    # Create nodes for all empty cells
    nodes = {}
    empty_fields = []
    for i, row in enumerate(m):
        for j, cell in enumerate(row):
            if cell == E:
                n = Node(i, j)
                nodes[(i,j)] = n
                empty_fields.append([i,j])
                
    # Find connections
    # TODO: see if the player can actually get to both cells when box is on the node
    for (i, j), node in nodes.items():
        if (i-1, j) in nodes and (i+1, j) in nodes:
            node.con.append(nodes[(i-1, j)])
            node.con.append(nodes[(i+1, j)])
        if (i, j-1) in nodes and (i, j+1) in nodes:
            node.con.append(nodes[(i, j-1)])
            node.con.append(nodes[(i, j+1)])
    
    groups = []
    group = []
    nodestack = list(nodes.values())
    
    def find_connected(group, n):
        """
        Adds to group all nodes that are connected both ways (chained)
        """
        for c in n.con:
            if c not in group and c in n.con and n in c.con:
                group.append(c)
                nodestack.remove(c)
                find_connected(group, c)
    
    # Group all nodes that are connected
    while len(nodestack) > 0:
        n = nodestack.pop()
        group.append(n)
        find_connected(group, n)
        groups.append(group)
        group = []
        
    def find_group(node):
        """
        Return the group node is in
        """
        for group in groups:
            if node in group:
                return group
        
    # Find deadlocks
    deadlocks = []
    for group in groups:
        if len(group) == 1:
            node = group[0]
            deadlocks.append((node.i, node.j))
        else:
            # If the group only connects to single cell groups
            # all nodes in it are also considered a deadlock
            deadlock = True
            for node in group:
                for c in node.con:
                    if c not in group and len(find_group(c)) > 1:
                        deadlock = False
            if deadlock:
                for node in group:
                    deadlocks.append((node.i, node.j))
                    
    available_fields = []
    for field in empty_fields:
        if field not in deadlocks:
            available_field.append(field)
            
    return available_fields