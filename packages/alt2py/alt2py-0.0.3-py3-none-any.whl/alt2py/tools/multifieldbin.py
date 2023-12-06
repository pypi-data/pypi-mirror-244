from .Config import Config;
import pandas as pd;


class MultiFieldBin:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        INPUT_CONSTRAINTS = [
            {
                "name":"fields",
                "required":True,
                "type":list,
                "sub_type":str,
                "field":True
            },{
                "name":"mode",
                "required":False,
                "type":str,
                "multi_choice":["count","interval"],
                "default":"count"
            },{
                "name":"bins",
                "required":True,
                "type":int
            },{
                "name":"prefix",
                "required":False,
                "type":str,
                "default":""
            },{
                "name":"suffix",
                "required":False,
                "type":str,
                "default":"_Tile_Num"
            }
        ]
        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool,execute=True):
        kwargs = {}
        xml = tool.xml;
        values = {v.get("name"):v.text for v in xml.find(".//Configuration")}

        field_statements = values["List Box (297)"].split(',')
        kwargs['fields'] = [f.split("=")[0] for f in field_statements if f.split("=")[1]=="True"]
        kwargs['mode'] = "count" if values["Radio Button (299)"]=="True" else "interval"#count
        kwargs['bins'] = int(values["Numeric Up Down (298)"]) if values["Radio Button (299)"]=="True" else int(values["Numeric Up Down (300)"])
        kwargs['suffix'] = "_Tile_Num"

        self.config.load(kwargs)

        if execute:
            df = tool.get_input("Input")
            next_df = self.execute(df)
            tool.data["Output"] = next_df

    def get_yxdb_mapping(self):
        return {
            "Input":"Input",
            "Output":"Output"
        }
        
    def execute(self,input_datasource):
        c = self.config;

        new_df = input_datasource.copy()
        if c.mode == "count":
            for f in c.fields:
                new_df[c.prefix + f + c.suffix], bins = pd.qcut(new_df[f], q=c.bins, labels=range(c.bins,0,-1),retbins=True)
                print(bins)
        elif c.mode == "interval":
            for f in c.fields:
                new_df[c.prefix + f + c.suffix] = pd.cut(new_df[f], bins=c.bins, labels=range(1,c.bins+1),precision=10)
        else:
            raise Exception("mode must be set to 'count' or 'interval'.")

        return new_df
