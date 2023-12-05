from .Config import Config;
import pandas as pd;
from .._utils import Functions

INPUT_CONSTRAINTS = [
    {
        "name":"expression",
        "required":True,
        "type":str
    },
]

class Filter:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        self.config = Config(INPUT_CONSTRAINTS);
        self.true = None;
        self.false = None;
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool,execute=True):
        xml = tool.xml;
        kwargs = {}

        if  xml.find(".//Configuration//Mode").text != "Custom":
            raise Exception("Filter tool must use custom expression! Simply open the WF and change the filter type to a custom expression.")

        kwargs['expression'] = xml.find(".//Configuration//Expression").text

        self.config.load(kwargs)

        if execute:
            df = tool.get_input("Input")
            out = self.execute(df)
            tool.data["True"] = out.true
            tool.data["False"] = out.false


    def get_yxdb_mapping(self):
        return {
            "Input":"Input",
            "Output":{"True":"true","False":"false"}
        }

    def applier(self,series):
        c = self.config
        return eval(c.expression)

    def execute(self,input_datasource):
        c = self.config;
        new_df = input_datasource.copy();
        if isinstance(c.expression,str):
            c.expression = Functions.parse_formula(c.expression,column_names=new_df.columns,df_name='series')

        mask = new_df.apply(self.applier,axis=1)

        self.true = new_df[mask].reset_index(drop = True)
        self.false = new_df[~mask].reset_index(drop = True)
        return self
