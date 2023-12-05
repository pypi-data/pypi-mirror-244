import xml.etree.ElementTree as ET;

tree = ET.parse("empty_flow.yxmd").getroot()
nodes = tree.find("Nodes")


for i in range(0,100):
    print(i,2**i);

    node = ET.SubElement(nodes,'Node')
    node.attrib['ToolID'] = str(i+1)

    gui = ET.SubElement(node,'GuiSettings')
    gui.attrib['Plugin'] = "AlteryxBasePluginsGui.TextToColumns.TextToColumns"

    pos = ET.SubElement(gui,'Position')

    pos.attrib['x'] = str(50)
    pos.attrib['y'] = str(50*i)

    props = ET.SubElement(node,'Properties')
    config = ET.SubElement(props,'Configuration')
    flags = ET.SubElement(config,'Flags')
    flags.attrib['value'] = str(i)

    es = ET.SubElement(node,"EngineSettings")

    es.attrib['EngineDll'] = "AlteryxBasePluginsEngine.dll"
    es.attrib['EngineDllEntryPoint'] = "AlteryxTextToColumns"

tree = ET.ElementTree(tree)

print(tree)

with open('test.yxmd', 'wb') as f:
    tree.write(f, encoding='utf-8')


# def create_node_with_parent(toolid, plugin_attribute, configuration_child):
#     # Create the root node
#     root = ET.Element('Root')
#
#     # Create the parent node with toolid
#     parent = ET.SubElement(root, 'Parent')
#     parent.attrib['toolid'] = toolid
#
#     # Create the GuiSettings node with Plugin attribute
#     guisettings = ET.SubElement(parent, 'GuiSettings')
#     guisettings.attrib['Plugin'] = plugin_attribute
#
#     # Create the properties node
#     properties = ET.SubElement(guisettings, 'Properties')
#
#     # Create the configuration child node
#     configuration = ET.SubElement(properties, 'Configuration')
#     configuration.append(configuration_child)
#
#     # Create the ElementTree and return
#     tree = ET.ElementTree(root)
#     return tree
