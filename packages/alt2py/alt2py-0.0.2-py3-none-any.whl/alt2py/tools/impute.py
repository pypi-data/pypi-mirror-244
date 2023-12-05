from .Config import Config;
import pandas as pd;
import re
from .._utils import dtype_map, Aggregators as Agg


class Impute:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"fields",
                "required":True,
                "type":list,
                "sub_type":str,
                "field":True
            },{
                "name":"impute_value",
                "default":pd.NA,
                "type":(type(pd.NA),int,float)
            },{
                "name":"impute_fn",
                "required":lambda kwargs: "impute_static" not in kwargs,
                "required_error_msg": "either impute_static or impute_fn is required",
                "type":str,
                "multi_choice":["Average","Median","Mode"]
            },{
                "name":"impute_static",
                "required":False,
                "type":(int,float),
            },{
                "name":"indicator",
                "required":False,
                "type":bool,
                "default":False
            },{
                "name":"add_fields",
                "required":False,
                "type":bool,
                "default":False
            },{
                "name":"new_prefix",
                "required":False,
                "type":str,
                "default":""
            },{
                "name":"indicator_prefix",
                "required":False,
                "type":str,
                "default":""
            },{
                "name":"new_suffix",
                "required":False,
                "type":str,
                "default":"_ImputedValue"
            },{
                "name":"indicator_suffix",
                "required":False,
                "type":str,
                "default":"_Indicator"
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

        kwargs['fields'] = re.sub('^\"|\"$',"",values["listbox Select Incoming Fields"]).split('","')
        kwargs['impute_value'] = pd.NA if values["radio Null Value"]=="True" else values["updown User Replace Value"]
        kwargs['impute_fn'] = "Average" if values["radio Mean"]=="True" else "Median"  if values["radio Median"]=="True" else "Mode" if values["radio Mode"]=="True" else None;
        kwargs['impute_static'] = values["updown User Replace With Value"] if not kwargs['impute_fn'] else None
        kwargs['indicator'] = values["checkbox Impute Indicator"]=="True"
        kwargs['add_fields'] = values["checkbox Imputed Values Separate Field"]=="True"
        kwargs['new_suffix'] = "_ImputedValue"
        kwargs['indicator_suffix'] = "_Indicator"
        kwargs['impute_static'] = None if kwargs['impute_static'] is None else float(kwargs['impute_static']) if '.' in kwargs['impute_static'] else int(kwargs['impute_static'])
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
        print(c)

        if c.impute_fn:
            print(Agg.get_by_name(c.impute_fn))
            replacement = new_df[c.fields].apply(Agg.get_by_name(c.impute_fn))
        else:
            replacement = c.impute_static

        if c.indicator:
            print(replacement)
            indicators = (new_df[c.fields] == replacement)
            indicators = indicators.fillna(True)
            indicators = indicators.astype(dtype_map["Int"])
            indicators.columns = [c.indicator_prefix + col + c.indicator_suffix for col in indicators.columns]
            new_df = pd.concat([new_df,indicators],axis=1)

        if c.impute_fn:
            replacement = replacement.to_dict()
            print(replacement)

            for f  in c.fields:
                print(str(new_df[f].dtype))
                if "Int" in str(new_df[f].dtype):
                    print("HERE")
                    replacement[f] = int(round(replacement[f]))

            added_df = new_df[c.fields].replace(to_replace=pd.NA,value = replacement)
            print(added_df)
        else:
            added_df = new_df[c.fields].replace({pd.NA:replacement})

        if c.add_fields:
            added_df.columns = [c.new_prefix + col + c.new_suffix for col in added_df.columns]
            new_df = pd.concat([new_df,added_df],axis=1)
        else:
            print(replacement)
            print(new_df[c.fields])

            new_df[c.fields] = added_df
            print(new_df[c.fields])

        return new_df.reset_index(drop=True)
