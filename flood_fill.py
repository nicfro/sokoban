W = "#"
E = " "

class Node(object):
    def __init__(self, i, j):
        self.con = []  # Box can move from here to connected nodes
        self.i = i
        self.j = j
        
    def __repr__(self):
        return "Node(%d, %d)" % (self.i, self.j)
        
def fix_map(m):
    nm = m
    m = []
    for row in nm:
        m.append(list(row))
    m.insert(0, [W]*len(m[0]))
    m.append([W]*len(m[0]))
    for row in m:
        row.insert(0, W)
        row.append(W)
    return m

def fill_map(m):

    m = fix_map(m)
    
    # Create nodes for all empty cells
    nodes = {}
    for i, row in enumerate(m):
        for j, cell in enumerate(row):
            if cell == E:
                n = Node(i, j)
                nodes[(i,j)] = n
                
    # Find connections
    # TODO: see if the player can actually get to both cells when box is on the node
    for (i, j), node in nodes.items():
        if (i-1, j) in nodes:
            node.con.append(nodes[(i-1, j)])
        if (i+1, j) in nodes:
            node.con.append(nodes[(i+1, j)])
        if (i, j-1) in nodes:
            node.con.append(nodes[(i, j-1)])
        if (i, j+1) in nodes:
            node.con.append(nodes[(i, j+1)])
    
    groups = []
    group = []
    nodestack = list(nodes.values())
    
    def find_connected(group, n):
        """
        Adds to group all nodes that are connected both ways (chained)
        """
        for c in n.con:
            if c not in group and (c in n.con or n in c.con):
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
            
    biggest_area = []
    for group in groups:
        if len(group) > len(biggest_area):
        biggest_area = group

    field = []
    for cell in biggest_area:
    field.append([cell.i,cell.j])

    for i, row in enumerate(m):
        for j, cell in enumerate(row):
            if cell == E and [i,j] not in field:
                m[i][j] = W