#this script reads a one tool at a time workflow and adds outputs to each individual
#test, the we can simply run the workflow to get outputs for testing

import xml.etree.ElementTree as ET;


wf_paths = {
    "TextToColumns":"\TextToColumns\Text_To_Columns",
    "AlteryxSelect":"\AlteryxSelect\Select",
    "GenerateRows":"\GenerateRows\Generate_Rows",
    "Join":"\Join\Join",
    "Tile":"\Tile\Tile",
    "Summarize":"\Summarize\Summarize",
    "Formula":"\Formula\Formula",
    "RegEx":"\RegEx\RegEx",
    "MultiFieldFormula":"\MultiFieldFormula\MultiFieldFormula",
    "MultiRowFormula":"\MultiRowFormula\MultiRowFormula",
    "RecordID":"\RecordID\RecordID",
    "RandomSample":"\RandomSample\RandomSample",
    "SelectRecords":"\SelectRecords\SelectRecords",
    "Sort":"\Sort\Sort",
    "Unique":"\\Unique\\Unique",
    "JoinMultiple":"\JoinMultiple\JoinMultiple",
    "Union":"\\Union\\Union",
    "Filter":"\\Filter\\Filter",
    "CrossTab":"\\CrossTab\\CrossTab",
    "Transpose":"\\Transpose\\Transpose",
    "Cleaner":"\\Cleaner\\Cleaner",
    "Impute":"\\Impute\\Impute",
    "MultiFieldBin":"\\MultiFieldBin\\MultiFieldBin",
    "OverSample":"\\OverSample\\OverSample",
    "XMLParse":"\\XMLParse\\XMLParse",
    "DateTime":"\\DateTime\\DateTime",
    "DateTime":"\\DateTime\\DateTime",
    "AppendFields":"\\AppendFields\\AppendFields",
}

def extend_OTaaT(testing):
    path = wf_paths[testing]
    print("One Tool At A Time - Testing" + path + '.yxmd')
    tree = ET.parse("One Tool At A Time - Testing" + path + '.yxmd')
    root = tree.getroot()
    nodes = root.find("Nodes")

    # Store all tool IDs that have inputs or outputs
    tool_ids = set();

    for node in root.iter('Node'):
        tool_id = node.attrib.get('ToolID')
        tool_ids.add(tool_id)

    inputs = [];
    test_tools = [];
    texts = [];

    # Create tools
    for node in root.iter('Node'):
        tool_id = node.attrib.get('ToolID')
        tool_name = None
        gui_settings = node.find('GuiSettings')

        if gui_settings is None:
            continue;

        tool_name = gui_settings.attrib.get('Plugin')
        pos = gui_settings.find('Position')
        x = int(pos.attrib.get('x'))
        y = int(pos.attrib.get('y'))

        print(tool_name)
        if tool_name is None:
            tool_name = node.find("EngineSettings").get("Macro").replace(".yxmc","")
            tool_name = tool_name.replace("Cleanse","Cleaner")
            tool_name = tool_name.replace("Imputation_v3","Impute")
            tool_name = tool_name.replace("MultiFieldBinning_v2","MultiFieldBin")
            tool_name = tool_name.replace("Predictive Tools\Oversample_Field","OverSample")
            tool_name = tool_name.replace("RandomRecords","RandomSample")


            print("ASDFIASLDFN",tool_name)
        if tool_name.split('.')[-1]=='TextBox':
            height = pos.attrib.get('height')
            width = pos.attrib.get('width')
            print(width)
            text = node.find("Properties").find("Configuration").find('Text').text
            print(height,width,x)
            if height == '24' and x == 270:
                texts.append({
                    'id':tool_id,
                    'y':y,
                    'x':x,
                    'text':text
                })
                print("HERHERHERHERHERH")
        print(tool_name.split('.')[-1],testing)
        if tool_name.split('.')[-1]==testing:
            test_tools.append({
                'id':tool_id,
                'y':y,
                'x':x,
                'node':node
            })
        if tool_name.split('.')[-1]=='DbFileInput':
            file = node.find("Properties").find("Configuration").find("File")
            file.set("FileFormat","48")
            file.text = file.text[:-5] + ".avro"
            inputs.append({
                'id':tool_id,
                'y':y,
                'x':x,
                'node':node
            })

    for i in inputs:
        node_to_edit = i['node'].find("Properties").find("Configuration").find('File');
        filename = node_to_edit.text.replace('..\..\..\data\OneToolData', '..\OneToolData');
        node_to_edit.text = filename;


    example_out = """ <Node ToolID="161">
          <GuiSettings Plugin="AlteryxBasePluginsGui.DbFileOutput.DbFileOutput">
            <Position x="894" y="186" />
          </GuiSettings>
          <Properties>
            <Configuration>
              <File MaxRecords="" FileFormat="0">./Split to Columns - 1 delimiter.csv</File>
              <Passwords />
              <FormatSpecificOptions>
                <LineEndStyle>CRLF</LineEndStyle>
                <Delimeter>,</Delimeter>
                <ForceQuotes>False</ForceQuotes>
                <HeaderRow>True</HeaderRow>
                <CodePage>28591</CodePage>
                <WriteBOM>True</WriteBOM>
              </FormatSpecificOptions>
              <MultiFile value="False" />
            </Configuration>
            <Annotation DisplayMode="0">
              <Name />
              <DefaultAnnotationText>Out</DefaultAnnotationText>
              <Left value="False" />
            </Annotation>
            <Dependencies>
              <Implicit />
            </Dependencies>
          </Properties>
          <EngineSettings EngineDll="AlteryxBasePluginsEngine.dll" EngineDllEntryPoint="AlteryxDbFileOutput" />
        </Node> """

    example_in ="""<Node ToolID="10004">
          <GuiSettings Plugin="AlteryxBasePluginsGui.DbFileInput.DbFileInput">
            <Position x="54" y="786" />
          </GuiSettings>
          <Properties>
            <Configuration>
              <Passwords />
              <File OutputFileName="" FileFormat="48" SearchSubDirs="False" RecordLimit="">151 - Generating Rows as a Standalone Dataset.avro</File>
              <FormatSpecificOptions />
            </Configuration>
            <Annotation DisplayMode="0">
              <Name />
              <DefaultAnnotationText>151 - Generating Rows as a Standalone Dataset.avro</DefaultAnnotationText>
              <Left value="False" />
            </Annotation>
            <Dependencies>
              <Implicit />
            </Dependencies>
          </Properties>
          <EngineSettings EngineDll="AlteryxBasePluginsEngine.dll" EngineDllEntryPoint="AlteryxDbFileInput" />
        </Node> """

    example_con = """
    <Connection>
      <Origin ToolID="141" Connection="Output" />
      <Destination ToolID="142" Connection="Input" />
    </Connection>"""

    id = 9999

    print("len(texts)",len(texts))
    print("len(test_tools)",len(test_tools))

    for i in range(len(texts)):
        print(texts[i])
        new_node = ET.ElementTree(ET.fromstring(example_out)).getroot()
        new_node_in = ET.ElementTree(ET.fromstring(example_in)).getroot()
        new_node.set('ToolID',str(id))
        new_node_in.set('ToolID',str(id+1))
        print("DFKLUGNKDUFNGKDFUNGDG")
        print(texts[i])
        new_node.find("Properties").find("Configuration").find('File').text = test_tools[i]["id"] + ' - ' +texts[i]["text"].replace('/',' ') + ".avro"
        new_node_in.find("Properties").find("Configuration").find('File').text = test_tools[i]["id"] + ' - ' +texts[i]["text"].replace('/',' ') + ".avro"
        new_node.find("Properties").find("Configuration").find('File').set('FileFormat','48')
        new_node_in.find("Properties").find("Configuration").find('File').set('FileFormat','48')
        pos = new_node.find("GuiSettings").find("Position")
        pos_in = new_node_in.find("GuiSettings").find("Position")
        pos.set('x', str(test_tools[i]['x']+500))
        pos.set('y', str(test_tools[i]['y']))
        pos_in.set('x', str(test_tools[i]['x']+700))
        pos_in.set('y', str(test_tools[i]['y']))

        nodes.append(new_node)
        nodes.append(new_node_in)
        new_con = ET.ElementTree(ET.fromstring(example_con)).getroot()

        connections = root.find("Connections")

        new_con.find("Origin").set("ToolID",test_tools[i]["id"])
        new_con.find("Destination").set("ToolID",str(id))

        connections.append(new_con)

        id+=2;

    print("One Tool At A Time - Testing"+path + "_edit.yxmd")
    with open("One Tool At A Time - Testing"+path+ "_edit.yxmd", 'wb') as f:
        tree.write(f, encoding='utf-8')

    print(sorted(inputs, key=lambda x: x['y']),len(inputs))
    print(sorted(texts, key=lambda x: x['y']),len(texts))
    print(sorted(test_tools, key=lambda x: x['y']),len(test_tools))


extend_OTaaT("AppendFields")
