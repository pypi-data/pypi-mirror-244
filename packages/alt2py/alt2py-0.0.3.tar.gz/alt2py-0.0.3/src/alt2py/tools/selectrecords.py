from .Config import Config;
import pandas as pd
import re


class SelectRecords:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"conditions",
                "required":True,
                "type":list,
                "sub_type":str
            },
            {
                "name":"index",
                "required":False,
                "type":int,
                "default":0
            },
        ]
        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        else:
            self.config.load(kwargs)

    def parse_range_expressions(self,text_list,df_name="new_df"):
        c = self.config;
        out_list = []
        for text in c.conditions:
            out = ""
            pattern = re.compile("[^\d\+\s-]")
            match = pattern.match(text);
            if match:
                raise Exception("Range Expression Can't Contain Words!")
            if "-" in text:
                pattern = re.compile("(\d*)\s*-\s*(\d*)")
                match = pattern.match(text);
                m1 = match.group(1)
                m2 = match.group(2)

                if m1:
                    out+=f"({df_name}.index + {c.index} >= {m1})"
                if m2:
                    if m1:
                        out += " & "
                    out+=f"({df_name}.index + {c.index} <= {m2})"
            elif "+" in text:
                pattern = re.compile("(\d*)\+")
                match = pattern.match(text);
                m1 = match.group(1)
                out = f"{df_name}.index + {c.index} >= {m1}"
            else:
                pattern = re.compile("(\d*)")
                match = pattern.match(text);
                m1 = match.group(1)
                out = f"{df_name}.index + {c.index} == {m1}"
            out_list.append(f"({out})")
        return out_list

    def load_yxdb_tool(self,tool,execute=True):
        xml = tool.xml
        kwargs = {}
        kwargs['index'] = 1
        kwargs['conditions'] = []
        values = xml.find(".//Configuration//Value").text.split("\n")
        for v in values:
            kwargs['conditions'].append(v)
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

        print(c)

        new_df = input_datasource.copy();

        joined_conditions = " | ".join(self.parse_range_expressions(c.conditions))
        new_df = eval(f"new_df[{joined_conditions}]")
        return new_df.reset_index(drop=True)
