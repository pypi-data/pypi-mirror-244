#Import packages/modules. Don't Remove.
from .Config import Config;
import pandas as pd;

#RENAME CLASS

#IMPORT THIS CLASS TO __INIT__.py in this folder and add it to the
#tool_name_map dictionary in ReadYXDB.py.


class Limit:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # Input your constraints:
        # {
        #     "name": The key word argument you are setting constraints on.
        #     if the type of the argument is a dict: you can also specify a constraint
        #     on an element of that dict by you using [argument_name].[key]
        #     eg, if you have an argument called `expression` which you expect to contain a value with the key `field`
        #     use "name":"expression.field" to add constrains on that dict element.
        #
        #     "required": Whether or not this argument is required.
        #     Also accepts a function, that takes a dictionary of arguments and returns
        #     True or False, which is useful for when an arguments requirements is dependent
        #     on the values of other arguments
        #
        #
        #     "type": The expected python type for the argument: (str,list,bool,int,float,dict,list)
        #
        #     "sub_type": If type is list, what is the type you expect the elements to be.
        #
        #     "default": What to set the value if no argument is passed.
        #
        #     "multi_choice": A list of possible values that can be used.
        #
        #     "field": Whether or not this element is required to be in a dataframe passed to execute()
        # }
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
                "type":int,
            },
            {
                "name":"mode",
                "required":False,
                "type":String,
                "multi_choice": ["First", "Last"],
                "default": "First"
            }
        ]
        self.config = Config(INPUT_CONSTRAINTS);

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

        #ADD YOUR KEY WORD ARGUMENTS INTO KWARGS HERE.

        self.config.load(kwargs)

        if execute:
            # HERE IS
            df = tool.get_input("Input")
            next_df = self.execute(df)
            tool.data["Output"] = next_df

    #ADD ADDITIONAL INPUT DATASOURCES TO THE EXECUTE ARGUEMENTS IF NECESARRY
    def execute(self,input_datasource):
        c = self.config;
        # c will now have all of the key word arguments that were loaded.
        # if you loaded a kwarg named groupings, access that kwarg with c.groupings.


        # Create a copy of the input. You don't want to change the
        new_df = input_datasource.copy()

        #ADD LOGIC HERE

        return new_df
