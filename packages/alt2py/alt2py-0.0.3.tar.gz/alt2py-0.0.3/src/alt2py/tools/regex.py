from .Config import Config;
import pandas as pd
import re
from functools import reduce;
from .._utils import Functions,dtype_map


class RegEx:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        # LOAD DEFAULTS
        INPUT_CONSTRAINTS = [
            {
                "name":"field",
                "required":True,
                "type":str,
                "field":True
            },
            {
                "name":"pattern",
                "required":True,
                "type":str
            },
            {
                "name":"case_insensitive",
                "required":False,
                "type":bool,
                "default":True
            },
            {
                "name":"method",
                "required":False,
                "type":str,
                "default":"match",
                "multi_choice":["match","parse","tokenize","replace"]
            },
            {
                "name":"replace_pattern",
                "required":lambda kwargs:kwargs["method"]=="replace",
                "type":str,
                "default":None
            },
            {
                "name":"copy_unmatched",
                "required":False,
                "type":bool,
                "default":False
            },
            {
                "name":"to_rows",
                "required":False,
                "type":bool,
                "default":False
            },
            {
                "name":"root_name",
                "required":
                    lambda kwargs: kwargs["method"]=="tokenize" and
                                   (("to_rows" not in kwargs) or
                                    not kwargs["to_rows"]),
                "type":str,
                "default":None
            },
            {
                "name":"num_fields",
                "required":
                    lambda kwargs: kwargs["method"]=="tokenize" and
                                   (("to_rows" not in kwargs) or
                                    not kwargs["to_rows"]),
                "type":int,
                "default":None
            },
            {
                "name":"on_error",
                "required":False,
                "type":str,
                "default":"Ignore",
                "multi_choice":["Warn","Ignore","Error"]
            },
            {
                "name":"new_fields",
                "required":lambda kwargs: kwargs["method"]=="parse",
                "type":list,
                "default":None
            },
            {
                "name":"new_fields.field",
                "required":True,
                "type":str
            },
            {
                "name":"formulae.size",
                "required":False,
                "type":str
            },
            {
                "name":"formulae.type",
                "required":False,
                "type":str,
                "default":"String",
                "multi_choice":list(dtype_map.keys())
            },
        ]
        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        else:
            self.config.load(kwargs)


    def load_yxdb_tool(self,tool,execute=True):
        xml = tool.xml

        kwargs = {}
        config = xml.find('Properties/Configuration')

        kwargs["field"] = config.find("Field").text
        kwargs["pattern"] = config.find("RegExExpression").get("value")
        kwargs["case_insensitive"] = config.find("CaseInsensitve").get("value")=="True"
        kwargs["method"] = config.find("Method").text

        if kwargs["method"]=="Replace":
            kwargs["method"]="replace"
            replace_config = config.find("Replace")
            kwargs["replace_pattern"] = replace_config.get("expression")
            kwargs["copy_unmatched"] = replace_config.find("CopyUnmatched").get("value")=="True"
        elif kwargs["method"]=="ParseSimple":
            kwargs["method"]="tokenize"
            parse_config = config.find("ParseSimple")
            kwargs["to_rows"] = parse_config.find("SplitToRows").get("value")=="True"
            if not kwargs["to_rows"]:
                kwargs["root_name"] = parse_config.find("RootName").text;
                kwargs["num_fields"] =  int(parse_config.find("NumFields").get("value"))
                kwargs["on_error"] = parse_config.find("ErrorHandling").text #Warn Ignore Error
        elif kwargs["method"]=="ParseComplex":
            kwargs["method"]="parse"
            parse_config = config.find("ParseComplex")
            kwargs["new_fields"] = [{
                "field":f.get("field"),
                "type":f.get("type"),
                "size":f.get("size")
            } for f in parse_config.findall("Field")]
        elif kwargs["method"]=="Match":
            kwargs["method"]="match"
            match_config = config.find("Match")
            kwargs["new_fields"] = [{"field":match_config.find("Field").text}]

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
    def regex_parse(self,text):
        c = self.config
        flags = re.IGNORECASE if c.case_insensitive else 0;

        matches = re.search(c.pattern, text,flags=flags)
        out = []

        for i,f in enumerate(c.new_fields):
            if matches:
                out.append(matches.group(i+1))
            else:
                out.append(None)
        return out

    def regex_replace(self,text):
        c = self.config

        flags = re.IGNORECASE if c.case_insensitive else 0;
        compiled_pattern = re.compile(c.pattern,flags=flags)
        match = compiled_pattern.search(text)

        if match:
            # Replace the matched text using the replacement string and dollar signs
            replaced_text = compiled_pattern.sub(c.replace_pattern.replace("$","\\"), text)
            return replaced_text
        else:
            # Return the input string as-is if no matches found
            return text if c.copy_unmatched else "";

    def regex_to_columns(self,text):
        c = self.config

        flags = re.IGNORECASE if c.case_insensitive else 0;
        out = []
        match = re.search(c.pattern, text,flags=flags)
        print(c.pattern,text)
        ##c.num_fields = 2
        while match and (c.num_fields is None or len(out)<c.num_fields):
            out.append(match.group(0))
            text = text[match.end():]
            match = re.search(c.pattern, text,flags=flags)

        if c.num_fields is not None and match:
            out.append(text[match.start():])
        return out

    def execute(self,input_datasource):
        new_df = input_datasource.copy();
        c = self.config;
        print(c)
        if c.method=="replace":
            new_df[c.field] = new_df[c.field].apply(self.regex_replace)

        elif c.method=="tokenize":
            new_cols = new_df[c.field].apply(self.regex_to_columns)
            new_cols = pd.DataFrame(new_cols.tolist())
            if c.root_name is not None:
                new_cols.columns = [c.root_name+str(col+1) for col in new_cols.columns]
            new_df = pd.concat([new_df,new_cols], axis=1)

            if c.to_rows:
                new_df = new_df.reset_index().rename(columns={'index': 'order_index'})
                new_df = new_df.melt(id_vars=input_datasource.columns.tolist()+['order_index'])
                new_df['variable'] = new_df['variable'].astype(int)
                new_df.sort_values(by=['order_index', 'variable'], ascending=[True, True],inplace=True)
                new_df.drop([c.field,'variable','order_index'], axis=1, inplace=True)
                new_df.rename(columns={'value':c.field},inplace=True)
                new_df.reset_index(drop=True,inplace=True)
                new_df = new_df[new_df[c.field].notna()]

        elif c.method=="parse":
            new_cols = new_df[c.field].apply(self.regex_parse)
            new_cols = pd.DataFrame(new_cols.tolist())
            new_cols.columns = [f["field"] for f in c.new_fields]
            new_df = pd.concat([new_df,new_cols], axis=1)

        elif c.method=="match":
            print(c.new_fields)
            new_df = new_df.assign(**{c.new_fields[0]["field"]: new_df[c.field].str.match(c.pattern)})

        return new_df
