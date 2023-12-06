import xml.etree.ElementTree as ET;
import os;

workflow_to_convert = r"input_converter.yxmd"

tree = ET.parse(workflow_to_convert)
root = tree.getroot()
nodes = root.find("Nodes")

inputs_to_conv = {}

ids = []

for node in nodes:
    id = node.get("ToolID")
    ids.append(int(id))
    toolType = node.find("GuiSettings").get("Plugin")

    if toolType=="AlteryxBasePluginsGui.DbFileInput.DbFileInput":
        spatialFields = node.findall("Properties/MetaInfo/RecordInfo/Field[@type='SpatialObj']")
        if len(spatialFields)>0:
            print(id,spatialFields)
            inputs_to_conv[id] = {
                'spatialFields': [s.get('name') for s in spatialFields],
                'x':node.find("GuiSettings/Position").get('x'),
                'y':node.find("GuiSettings/Position").get('y'),
                "Connections":[]
            }

example_select = """
    <Node ToolID="66">
      <GuiSettings Plugin="AlteryxBasePluginsGui.AlteryxSelect.AlteryxSelect">
        <Position x="438" y="258" />
      </GuiSettings>
      <Properties>
        <Configuration>
          <OrderChanged value="False" />
          <CommaDecimal value="False" />
          <SelectFields>
          </SelectFields>
        </Configuration>
        <Annotation DisplayMode="0">
          <Name />
          <DefaultAnnotationText />
          <Left value="False" />
        </Annotation>
      </Properties>
      <EngineSettings EngineDll="AlteryxBasePluginsEngine.dll" EngineDllEntryPoint="AlteryxSelect" />
    </Node>
"""

example_field = """<SelectField field="Centroid" selected="True" type="V_String" size="2147483647" />"""

example_con = """
    <Connection>
        <Origin ToolID="0" Connection="Output" />
        <Destination ToolID="0" Connection="Input" />
    </Connection>
"""

# <MetaInfo connection="Output">
# <RecordInfo>
# <Field name="BUSINESS NAME" size="30" source="Calgary:Field: D:\Data Products\US\Calgary\AP_DB_Q4_2013\DB_BUS_CAL_Q4_2013.cydb" type="V_String" />
# <Field name="City" size="50" source="Calgary:Field: D:\Data Products\US\Calgary\AP_DB_Q4_2013\DB_BUS_CAL_Q4_2013.cydb" type="V_String" />
# <Field name="SALES VOLUME" source="Formula: RAND()*1000000" type="Int64" />
# <Field name="Centroid" size="2147483647" source="CreatePoints: x=LONGITUDE y=LATITUDE" type="SpatialObj" />
# <Field name="Store Name" size="64" source="Formula: [StoreID2]+[City]" type="String" />
# <Field name="StoreID" source="RecordID: Starting Value=101" type="Int32" />
# <Field name="Store Sales" source="Formula: (RAND())*10000000" type="Double" />
# <Field name="Universe_CENTROID" size="2147483647" source="Calgary:Field: D:\Data Products\US\Calgary\AP_DB_Q4_2013\DB_BUS_CAL_Q4_2013.cydb" type="SpatialObj" />
# <Field name="SpatialObject_TradeArea" size="2147483647" source="TradeArea: Source=CENTROID Radius=3.0 Units=Miles" type="SpatialObj" />
# <Field name="SpatialObject_TradeArea2" size="2147483647" source="TradeArea: Source=CENTROID RadiusField=Distance Units=Minutes GuzzlerDataSet=Latest:TeleAtlas_US" type="SpatialObj" />
# </RecordInfo>
# </MetaInfo>

con_nodes = root.find("Connections")
cons_to_remove = []

for i,con in enumerate(con_nodes):
    con = con_nodes[i]
    origin = con.find("Origin")
    dest = con.find("Destination")

    print(origin.get("ToolID"),dest.get("ToolID"))

    if origin.get("ToolID") in inputs_to_conv:
        print("removed",origin.get("ToolID"),dest.get("ToolID"))
        inputs_to_conv[origin.get("ToolID")]["Connections"].append({
            "orig_id":origin.get("ToolID"),
            "dest_id":dest.get("ToolID"),
            "orig_con":origin.get("Connection"),
            "dest_con":dest.get("Connection"),
        })
        cons_to_remove.append(con)

for con in cons_to_remove:
    print(con.find("Origin").get("ToolID"),con.find("Destination").get("ToolID")," REMOVED")
    con_nodes.remove(con)
print(inputs_to_conv)

toolId=max(ids)+1

for inputid in inputs_to_conv:
    inp = inputs_to_conv[inputid]
    x = int(inp["x"])+75
    y = int(inp["y"])
    print(spatialFields)
    spatialFields = inp['spatialFields']

    new_select = ET.ElementTree(ET.fromstring(example_select)).getroot()
    selectFields = new_select.find("Properties/Configuration/SelectFields")
    print(selectFields)

    for sp in spatialFields:
        print(sp)
        new_field = ET.ElementTree(ET.fromstring(example_field)).getroot()
        new_field.set("field",sp)
        selectFields.append(new_field)

    selectFields.append(ET.ElementTree(ET.fromstring('<SelectField field="*Unknown" selected="True" />')).getroot())

    for c in inp["Connections"]:
        c["select"] = toolId

    new_select.set("ToolID",str(toolId))
    new_select.find("GuiSettings/Position").set("x",str(x))
    new_select.find("GuiSettings/Position").set("y",str(y))
    nodes.append(new_select)

    for c in inp["Connections"]:
        c1 = ET.ElementTree(ET.fromstring(example_con)).getroot()
        c2 = ET.ElementTree(ET.fromstring(example_con)).getroot()

        c1.find("Origin").set("ToolID",c["orig_id"])
        c1.find("Origin").set("Connection",c["orig_con"])
        c1.find("Destination").set("ToolID",str(toolId))
        c1.find("Destination").set("Connection","Input")

        c2.find("Origin").set("ToolID",str(toolId))
        c2.find("Origin").set("Connection","Output")
        c2.find("Destination").set("ToolID",c["dest_id"])
        c2.find("Destination").set("Connection",c["dest_con"])

        con_nodes.append(c1)
        con_nodes.append(c2)


    toolId+=1

print(len(con_nodes))

with open(r"input_convert_spatial.yxmd", 'wb') as f:
    tree.write(f, encoding='utf-8')
