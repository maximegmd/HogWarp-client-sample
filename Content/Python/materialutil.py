import unreal
import MaterialExpressions
MEL = unreal.MaterialEditingLibrary

def create_named_parameter(mat, name, ty, x, y):
    node = MEL.create_material_expression(mat, ty, x, y)
    node.set_editor_property("ParameterName", name)
    return node 

def create_parameter_array(mat, name, ty, num, originX = 0, originY = 0, X_SPACE=0, Y_SPACE=250):
    nodes = [
        create_named_parameter(mat, f"{name}[{i}]", ty, originX + X_SPACE * i, originY + Y_SPACE * i)
        for i in range(1, num + 1)
    ]
    return nodes

def getScalarOutput(node):
    if isinstance(node, (MaterialExpressions.TextureSampleParameter2D, MaterialExpressions.VectorParameter)):
        return "R"

    return ""
    

def connectNodesUntilSingle(mat, _nodes : list):
    nodes = [*_nodes]

    y = 0

    while len(nodes) > 1:
        nodeA, nodeB = nodes[:2]
        nodes = nodes[2:]
        connector = MEL.create_material_expression(mat, MaterialExpressions.Add, 200, y)
        MEL.connect_material_expressions(nodeA, getScalarOutput(nodeA), connector, "A")
        MEL.connect_material_expressions(nodeB, getScalarOutput(nodeB), connector, "B")
        nodes.append(connector)
        y += 75


    return nodes[0]