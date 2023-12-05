#Import packages/modules. Don't Remove.
from .Config import Config;
import pandas as pd;

#RENAME CLASS
class Limit:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        INPUT_CONSTRAINTS = [
            {
                "name":"groupings",
                "required":False,
                "type":list,
                "sub_type":str,
                "default":[],
                "field":True
            },
            {
                "name":"sample_size",
                "required":True,
                "type":int
            },
            {
                "name":"mode",
                "required":False,
                "type":str,
                "default":[],
                "multi_choice":["First","Last"]
            }
        ]
        self.config = Config(INPUT_CONSTRAINTS);

        # self.yxdb_mapping is used for mapping connections from a yxdb file:
        # It should be a dict that contains 2 keys, Input and Output.
        # for input:
        #     if there is only a single input, set the value to the input anchor name
        #     if there are multiple inputs, set the value to a list of input anchornames
        #     IN THE OTHER THAT THEY ARE PASSED TO execute
        # for output
        #     if there is only a single input, set the value to the output anchor name
        #     if there are multiple inputs, set the value to a dict with
        #     keys as the yxdb anchor names and values as the name of the instance attributes defined above.
        #Eg for join.
        # self.yxdb_mapping = {
        #     "Input":["Left","Right"],
        #     "Output":{
        #         "Left":"left",
        #         "Join":"inner",
        #         "Right":"Right"
        #     }
        # }
        self.yxdb_mapping = {
            "Input":"Input",
            "Output":"Output"
        }
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool,execute=execute)
        else:
            self.config.load(kwargs) #Loads the key word arguments into the config object.


    def get_yxdb_mapping(self):
        return self.yxdb_mapping

    def load_yxdb_tool(self,yxdb_tool,execute=True):
        # This function is used when our new tool is called from the ReadYXDB.Workflow object.

        #yxdb_tool has the following properties:
        # yxdb_tool.name = the alteryx name of the tool
        # yxdb_tool.xml = the xml of the node Node in the yxdb file. as an xml.etree.ElementTree:
        # https://docs.python.org/3/library/xml.etree.elementtree.html#elementinclude-functions
        #to get the configuration node, use xml.find(".//Configuration")
        # yxdb_tool.dir = The directory of the workflow the node was in.

        xml = yxdb_tool.xml;
        kwargs = {}
        config_xml = xml.find(".//Configuration")

        kwargs["mode"] = config_xml.find("Mode").text
        kwargs["sample_size"] = int(config_xml.find("N").text)

        kwargs["groupings"] = []

        group_fields = config_xml.find("GroupFields")
        for field in group_fields:
            kwargs["groupings"].append(field.get("name"))

        self.config.load(kwargs)

        if execute:
            # HERE IS
            df = yxdb_tool.get_input("Input")
            next_df = self.execute(df)
            yxdb_tool.data["Output"] = next_df


    #ADD ADDITIONAL INPUT DATASOURCES TO THE EXECUTE ARGUEMENTS IF NECESARRY
    def execute(self,input_datasource):
        c = self.config;
        print(self.config)

        new_df = input_datasource.copy()

        if len(c.groupings) > 0:
            new_df = new_df.groupby(c.groupings)

        if c.mode == "First":
            new_df = new_df.head(c.sample_size)
        elif c.mode == "Last":
            new_df = new_df.tail(c.sample_size)

        print(new_df)

        return new_df
