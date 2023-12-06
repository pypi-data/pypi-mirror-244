from .Config import Config;
import pandas as pd
from datetime import datetime
import re


class DateTime:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"field",
                "required":True,
                "type":str,
                "field":True
            },{
                "name":"to_string",
                "required":False,
                "type":bool,
                "default":True
            },{
                "name":"pattern",
                "required":True,
                "type":str
            },{
                "name":"label",
                "required":True,
                "type":str
            }
        ]
        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool,execute=execute)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool,execute=True):
        xml = tool.xml;
        kwargs = {}

        kwargs["field"] = xml.find(".//Configuration//InputFieldName").text
        kwargs["to_string"] = xml.find(".//Configuration//IsFrom").get("value") == "True"
        kwargs["pattern"] = xml.find(".//Configuration//Format").text
        kwargs["label"] = xml.find(".//Configuration//OutputFieldName").text

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
    def convert_pattern(self):
        c = self.config;

        lp = "(^|[\, \-\/\:])"
        rp = "($|[\, \-\/\:])"
        c.pattern = re.sub(lp+"(d)"+rp, r"\1%-d\3", c.pattern)
        c.pattern = re.sub(lp+"(day)"+rp, r"\1%A\3", c.pattern)
        c.pattern = re.sub(lp+"(dd)"+rp, r"\1%d\3", c.pattern)
        c.pattern = re.sub(lp+"(dy)"+rp, r"\1%a\3", c.pattern)
        c.pattern = re.sub(lp+"(EEEE)"+rp, r"\1%A\3", c.pattern)
        c.pattern = re.sub(lp+"(M)"+rp, r"\1%-m\3", c.pattern)
        c.pattern = re.sub(lp+"(MM)"+rp, r"\1%m\3", c.pattern)
        c.pattern = re.sub(lp+"(MMM)"+rp, r"\1%b\3", c.pattern)
        c.pattern = re.sub(lp+"(MMMM)"+rp, r"\1%B\3", c.pattern)
        c.pattern = re.sub(lp+"(Mon)"+rp, r"\1%b\3", c.pattern)
        c.pattern = re.sub(lp+"(Month)"+rp, r"\1%B\3", c.pattern)
        c.pattern = re.sub(lp+"(yy)"+rp, r"\1%y\3", c.pattern)
        c.pattern = re.sub(lp+"(yyyy)"+rp, r"\1%Y\3", c.pattern)

        c.pattern = re.sub(lp+"(ahh)"+rp, r"\1%p\3", c.pattern)
        c.pattern = re.sub(lp+"(H)"+rp, r"\1%-H\3", c.pattern)
        c.pattern = re.sub(lp+"(HH)"+rp, r"\1%H\3", c.pattern)
        c.pattern = re.sub(lp+"(hh)"+rp, r"\1%H\3", c.pattern)
        c.pattern = re.sub(lp+"(mm)"+rp, r"\1%M\3", c.pattern)
        c.pattern = re.sub(lp+"(ss)"+rp, r"\1%S\3", c.pattern)


    def execute(self,input_datasource):
        c = self.config;
        new_df = input_datasource.copy();
        self.convert_pattern()

        if not c.to_string:
            def strpt(d):
                return datetime.strptime(d,c.pattern) if not pd.isnull(d) else d

            new_df[c.label] = new_df[c.field].apply(strpt).astype('datetime64[ns]')

        else:
            def strft(d):
                return d.strftime(c.pattern) if not pd.isnull(d) else d

            new_df[c.label] = new_df[c.field].apply(strft).astype(pd.StringDtype())

        return new_df.reset_index(drop=True)
