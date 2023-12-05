import xml.etree.ElementTree as ET;


import os

# Replace 'your_folder_path' with the path to the folder you want to search
folder_path = r"One Tool At A Time - Testing\OneToolData"
# Get all filenames in the folder
filenames = os.listdir(folder_path)
# Filter filenames that end with '.yxdb'
yxdb_files = [filename for filename in filenames if filename.endswith('.yxdb')]

# Print the list of filenames with the '.yxdb' extension
print(yxdb_files)

input = """
 <Node ToolID="1">
      <GuiSettings Plugin="AlteryxBasePluginsGui.DbFileInput.DbFileInput">
        <Position x="102" y="78" />
      </GuiSettings>
      <Properties>
        <Configuration>
          <Passwords />
          <File OutputFileName="" FileFormat="19" SearchSubDirs="False" RecordLimit="">.\One Tool At A Time - Testing\OneToolData\Address_Sale_Data_Narrow.yxdb</File>
          <FormatSpecificOptions />
        </Configuration>
        <Annotation DisplayMode="0">
          <Name />
          <DefaultAnnotationText></DefaultAnnotationText>
          <Left value="False" />
        </Annotation>
        <Dependencies>
          <Implicit />
        </Dependencies>
      </Properties>
      <EngineSettings EngineDll="AlteryxBasePluginsEngine.dll" EngineDllEntryPoint="AlteryxDbFileInput" />
    </Node>
"""

output = """
    <Node ToolID="2">
      <GuiSettings Plugin="AlteryxBasePluginsGui.DbFileOutput.DbFileOutput">
        <Position x="204" y="54" />
      </GuiSettings>
      <Properties>
        <Configuration>
          <File FileFormat="48" MaxRecords="">.\One Tool At A Time - Testing\OneToolData\\Address_Sale_Data_Narrow.avro</File>
          <Passwords />
          <FormatSpecificOptions>
            <EnableCompression>True</EnableCompression>
            <SupportNullValues>True</SupportNullValues>
          </FormatSpecificOptions>
          <MultiFile value="False" />
        </Configuration>
        <Annotation DisplayMode="0">
          <Name />
          <DefaultAnnotationText>Address_Sale_Data_Narrow.avro</DefaultAnnotationText>
          <Left value="False" />
        </Annotation>
        <Dependencies>
          <Implicit />
        </Dependencies>
      </Properties>
      <EngineSettings EngineDll="AlteryxBasePluginsEngine.dll" EngineDllEntryPoint="AlteryxDbFileOutput" />
    </Node>
"""

connection = """
    <Connection>
      <Origin ToolID="1" Connection="Output" />
      <Destination ToolID="2" Connection="Input" />
    </Connection>
"""

tree = ET.parse("empty_flow.yxmd")
root = tree.getroot()
nodes = root.find("Nodes")

connections_node = root.find("Connections")

id = 1

base_location = r".\One Tool At A Time - Testing\OneToolData"

for i,filename in enumerate(yxdb_files):
    print(i,filename[:-5])

    new_in_node = ET.ElementTree(ET.fromstring(input)).getroot()
    new_in_node.set('ToolID',str(id))

    new_in_node.find("Properties").find("Configuration").find('File').text = base_location + r"\\" + filename

    pos = new_in_node.find("GuiSettings").find("Position")
    pos.set('x', str(50))
    pos.set('y', str(50 + i*50))


    new_out_node = ET.ElementTree(ET.fromstring(output)).getroot()
    new_out_node.set('ToolID',str(id+1))

    new_out_node.find("Properties").find("Configuration").find('File').text = base_location + r"\\" + filename[:-5]+'.avro'

    pos = new_out_node.find("GuiSettings").find("Position")
    pos.set('x', str(200))
    pos.set('y', str(50 + i*50))

    con_node = ET.Element("Connection")

    origin = ET.Element("Origin")
    origin.set('ToolID',str(id))
    origin.set('Connection',"Output")
    dest = ET.Element("Destination")
    dest.set('ToolID',str(id+1))
    dest.set('Connection',"Input")

    nodes.append(new_in_node)
    nodes.append(new_out_node)

    con_node.append(origin)
    con_node.append(dest)
    connections_node.append(con_node)

    id+=2;

root.append(connections_node)

with open("input_converter.yxmd", 'wb') as f:
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
