from .Config import Config;
import pandas as pd;
import numpy as np;
import re;


# IF A CONSTRAINT IS REQUIRED YOU SHOULD NOT SET A DEFAULT
# IF A CONSTRAINT IS NOT REQUIRED YOU MUST SET A DEFAULT

class Clean:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS

        INPUT_CONSTRAINTS = [
        {
            "name":"fields",
            "required":False,
            "type":list,
            "sub_type":str,
            "default":[]
        },
        {
            "name":"filter_na_cols",
            "required":False,
            "type":bool,
            "default":False
        },
        {
            "name":"filter_na_rows",
            "required":False,
            "type":bool,
            "default":False
        },
        {
            "name":"replace_na_blank",
            "required":False,
            "type":bool,
            "default":False
        },
        {
            "name":"replace_na_zero",
            "required":False,
            "type":bool,
            "default":False
        },
        {
            "name":"trim_whitespace",
            "required":False,
            "type":bool,
            "default":False
        },
        {
            "name":"remove_dup_space",
            "required":False,
            "type":bool,
            "default":False
        },
        {
            "name":"remove_all_space",
            "required":False,
            "type":bool,
            "default":False
        },
        {
            "name":"remove_letters",
            "required":False,
            "type":bool,
            "default":False
        },
        {
            "name":"remove_numbers",
            "required":False,
            "type":bool,
            "default":False
        },
        {
            "name":"remove_numbers",
            "required":False,
            "type":bool,
            "default":False
        },
        {
            "name":"modify",
            "required":False,
            "type":bool,
            "default":None,
            "multi_choice":["title","upper","lower"]
        }]
        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool,execute=execute)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool,execute=True):
        xml = tool.xml;
        kwargs = {}

        values = {int(re.sub(r"[\(\)]",'', v.get("name").split(" ")[-1])):v.text for v in xml.find(".//Configuration")}
        kwargs["fields"] = re.sub('^\"|\"$',"",values[11]).split('","')
        if len(kwargs["fields"])==1 and kwargs["fields"][0] == "":
            kwargs["fields"] = []
        kwargs["filter_na_cols"] = values[135]=="True"
        kwargs["filter_na_rows"] = values[136]=="True"
        kwargs["replace_na_blank"] = values[84]=="True"
        kwargs["replace_na_zero"] = values[117]=="True"
        kwargs["trim_whitespace"] = values[15]=="True"
        kwargs["remove_dup_space"] = values[109]=="True"
        kwargs["remove_all_space"] = values[122]=="True"
        kwargs["remove_letters"] = values[53]=="True"
        kwargs["remove_numbers"] = values[58]=="True"
        kwargs["remove_punctuation"] = values[70]=="True"
        kwargs["modifier"] = values[81] if values[77]=="True" else None;

        self.config.load(kwargs)

        if execute:
            df = tool.get_input("Input2")
            next_df = self.execute(df)
            tool.data["Output"] = next_df

    def get_yxdb_mapping(self):
        return {
            "Input":"Input2",
            "Output":"Output"
        }

    def execute(self,input_datasource):
        c = self.config;
        # c.check_field_constraints(input_datasource)
        new_df = input_datasource.copy();

        if c.fields is None:
            c.fields = input_datasource.columns.tolist();

        if c.filter_na_cols:#APPLIES TO ALL COLUMNS
            new_df = new_df.dropna(axis=1, how='all')
            c.fields = [item for item in c.fields if item in new_df.columns]

        if c.filter_na_rows:
            new_df = new_df.dropna(axis=0, how='all')

        string_columns = new_df[c.fields].select_dtypes(include=[pd.StringDtype()]).columns.tolist()
        numeric_columns = new_df[c.fields].select_dtypes(include=np.number).columns.tolist()

        if c.replace_na_blank:
            new_df[string_columns] = new_df[string_columns].replace({pd.NA: ''})

        if c.replace_na_zero:
            new_df[numeric_columns] = new_df[numeric_columns].replace({pd.NA: 0})

        if c.remove_letters:
            new_df[string_columns] = new_df[string_columns].apply(lambda x: x.str.replace(r'[a-zA-Z]+', '',regex=True))

        if c.remove_numbers:
            new_df[string_columns] = new_df[string_columns].apply(lambda x: x.str.replace(r'[0-9]+', '',regex=True))

        if c.remove_punctuation:
            new_df[string_columns] = new_df[string_columns].apply(lambda x: x.str.replace(r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', '',regex=True))

        if c.trim_whitespace:
            new_df[string_columns] = new_df[string_columns].apply(lambda x: x.str.strip())

        if c.remove_dup_space:
            new_df[string_columns] = new_df[string_columns].apply(lambda x: x.str.replace(r'\s+', ' ',regex=True))

        if c.remove_all_space:
            new_df[string_columns] = new_df[string_columns].apply(lambda x: x.str.replace(r'\s+', '',regex=True))

        if c.modifier:
            if c.modifier=="title":
                new_df[string_columns] = new_df[string_columns].apply(lambda x: x.str.title())
            elif c.modifier=="upper":
                new_df[string_columns] = new_df[string_columns].apply(lambda x: x.str.upper())
            elif c.modifier=="lower":
                new_df[string_columns] = new_df[string_columns].apply(lambda x: x.str.lower())
            else:
                raise Exception("Unknown modifier")

        return new_df
