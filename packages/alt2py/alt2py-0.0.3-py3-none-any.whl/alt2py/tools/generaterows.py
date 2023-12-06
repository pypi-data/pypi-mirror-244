from .Config import Config;
import pandas as pd
import re
from functools import reduce;
from .._utils import Functions, dtype_map



class GenerateRows:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"field",
                "required":True,
                "type":str,
                "field":True
            },{
                "name":"field_type",
                "required":lambda kwargs: kwargs["mode"]=="new",
                "type":str,
                "default":lambda kwargs: "String" if kwargs["mode"]=="new" else None,
                "multi_choice":list(dtype_map.keys())
            },{
                "name":"field_size",
                "required":False,
                "type":str,
                "default":None
            },{
                "name":"initialiser",
                "required":True,
                "type":str,
            },{
                "name":"on_loop",
                "required":True,
                "type":str,
            },{
                "name":"should_loop",
                "required":True,
                "type":str,
            }
        ]
        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        else:
            self.config.load(kwargs)


    def load_yxdb_tool(self,tool, execute=True):
        kwargs = {}
        xml = tool.xml;

        updateField = xml.find(".//Configuration//UpdateField").get('value')=="True"

        if updateField:
            kwargs["field"] = xml.find(".//Configuration//UpdateField_Name").text
        else:
            kwargs["field"] = xml.find(".//Configuration//CreateField_Name").text
            kwargs["field_type"] = xml.find(".//Configuration//CreateField_Type").text

        kwargs["initialiser"] = xml.find(".//Configuration//Expression_Init").text
        kwargs["should_loop"] = xml.find(".//Configuration//Expression_Cond").text
        kwargs["on_loop"] = xml.find(".//Configuration//Expression_Loop").text

        self.config.load(kwargs)

        if execute:
            if len(tool.inputs)>0:
                df = tool.get_input("Input")
                next_df = self.execute(df)
            else:
                next_df = self.execute()

            tool.data["Output"] = next_df

    def get_yxdb_mapping(self):
        return {
            "Input":"Input",
            "Output":"Output"
        }

    def applier(self,series):
        c = self.config;
        c_row = eval(c.initialiser)
        series[c.field] = c_row
        con = eval(c.should_loop)
        rows = {c.field:[]}
        while(con):
            rows[c.field].append(c_row)
            c_row = eval(c.on_loop)
            series[c.field] = c_row
            con = eval(c.should_loop)
        new_df = pd.DataFrame(rows)
        result_df = pd.DataFrame.from_records([series]*len(rows[c.field]))
        if c.field_type:
            result_df[c.field] = new_df[c.field].astype(dtype_map[c.field_type])
        else:
            result_df[c.field] = new_df[c.field]
        return result_df

    def execute(self,input_datasource=None):
        c = self.config
        print("Executing GenerateRows:")
        if input_datasource is not None:

            df = input_datasource.copy()

            c.initialiser = Functions.parse_formula(c.initialiser,column_names=[c.field]+df.columns.tolist(),df_name="series")
            c.should_loop = Functions.parse_formula(c.should_loop,column_names=[c.field]+df.columns.tolist(),df_name="series")
            c.on_loop = Functions.parse_formula(c.on_loop,column_names=[c.field]+df.columns.tolist(),df_name="series")

            df_list = df.apply(
                self.applier,
                axis=1
            )

            df_list = [df for df in df_list if not df.empty] #prevents unwanted unit conversions
            new_df = pd.concat(df_list, ignore_index=True)

        else:
            initialiser = Functions.parse_formula(c.initialiser,column_names=[c.field],df_name="series")
            should_loop = Functions.parse_formula(c.should_loop,column_names=[c.field],df_name="series")
            on_loop = Functions.parse_formula(c.on_loop,column_names=[c.field],df_name="series")

            series = {c.field:eval(initialiser)}

            con = eval(should_loop)
            rows = []
            while(con):
                rows.append(series)
                series = {c.field:eval(on_loop)}
                con = eval(should_loop)
                # runs 1 too many times
            df = pd.DataFrame(rows,dtype=dtype_map[c.field_type])
            new_df = df

        return new_df
