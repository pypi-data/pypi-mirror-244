from .Config import Config;
import pandas as pd;
import numpy as np;
from .select import Select


class Join:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):

        INPUT_CONSTRAINTS = [
            {
                "name":"how",
                "type":str,
                "default":"key",
                "multi_choice":["cross","key","position"]
            },{
                "name":"left_keys",
                "required":lambda kwargs: kwargs["how"]=="key",
                "required_error_msg": "left_keys is required when using how=key",
                "type":list,
                "sub_type":str,
                "field":True
            },{
                "name":"right_keys",
                "required":lambda kwargs: kwargs["how"]=="key",
                "required_error_msg": "left_keys is required when using how=key",
                "type":list,
                "sub_type":str,
                "field":True
            }
        ]
        self.config = Config(INPUT_CONSTRAINTS);
        self.left = None;
        self.inner = None;
        self.right = None;
        self.xml = None;
        self.yxdb_mapping = {
            "Input":["Left","Right"],
            "Output":{
                "Left":"left",
                "Join":"inner",
                "Right":"Right"
            }
        }
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool,execute=execute)
        else:
            self.config.load(kwargs)

    def load_yxdb_tool(self,tool, execute=True):
        if tool.name[-1] == "AppendFields":
            self.yxdb_mapping = {
                "Input":["Targets","Source"],
                "Output":"Output"
            }
            self.load_yxdb_tool_append(tool, execute = execute)
        else:
            self.load_yxdb_tool_join(tool, execute = execute)

    def load_yxdb_tool_append(self,tool, execute=True):
        xml = tool.xml
        self.xml = xml
        kwargs = {"how":"cross"}
        self.config.load(kwargs)

        if execute:
            left = tool.get_input("Targets")
            right = tool.get_input("Source")
            self.inner = self.execute(left,right)
            tool.data["Output"] = self.inner

    def load_yxdb_tool_join(self,tool, execute=True):
        xml = tool.xml
        self.xml = xml
        kwargs = {}

        node_type = xml.find(".//GuiSettings").get("Plugin").split(".")[-1]
        if node_type == "AppendFields":
            kwargs["how"] = "cross"
        else:
            kwargs["how"] = "position" if xml.find(".//Properties//Configuration").get("joinByRecordPos")=="True" else "key"

            if kwargs["how"]=="key":
                left_infos = xml.find(".//Properties//Configuration//JoinInfo[@connection='Left']")
                right_infos = xml.find(".//Properties//Configuration//JoinInfo[@connection='Right']")

                kwargs["left_keys"] = [i.get('field') for i in left_infos]
                kwargs["right_keys"] = [i.get('field') for i in right_infos]

        self.config.load(kwargs)
        if execute:
            left = tool.get_input("Left")
            right = tool.get_input("Right")
            out = self.execute(left,right)

            tool.data["Left"] = out.left
            tool.data["Join"] = out.inner
            tool.data["Right"] = out.right

    def get_yxdb_mapping(self):
        return self.yxdb_mapping

    def get_renames(self,left_df,right_df):
        c = self.config;
        renames = {}
        renames_back = {}
        prefix = "Right_"
        if c.how=="cross":
            for i, name1 in enumerate(left_df.columns):
                renames_back["Target_"+name1] = name1
            for j, name2 in enumerate(right_df.columns):
                if "Target_"+name2 in renames_back:
                    renames[name2] = "Source_" + name2
                else:
                    renames_back["Source_" + name2] = name2


        else:
            for i, name1 in enumerate(left_df.columns):
                for j, name2 in enumerate(right_df.columns):
                    if name1 == name2:
                        renames[name2] = prefix+name2
                        renames_back[prefix+name2] = name2
        return (renames,renames_back)

    def join_by_pos(self,left_df,right_df,renames,renames_back):
        join_df = pd.concat([left_df, right_df], axis=1)

        leftover_dir = len(left_df) - len(right_df)
        if leftover_dir > 0:
            out_inner_df = join_df.head(len(join_df) - leftover_dir)
            out_left_df = left_df.tail(leftover_dir)
            out_right_df = right_df.head(0)

        elif leftover_dir < 0:
            out_inner_df = join_df.head(len(join_df) + leftover_dir)
            out_left_df = left_df.head(0)
            out_right_df = right_df.tail(-leftover_dir)
            out_right_df = out_right_df.rename(columns = renames_back)
        else:
            out_inner_df = join_df
            out_left_df = left_df.head(0)
            out_right_df = right_df.head(0)

        self.left = out_left_df;
        self.inner = out_inner_df;
        self.right = out_right_df;

    def join_by_key(self,left_df,right_df,renames,renames_back):
        c = self.config;
        df_merged = pd.merge(
            left_df,
            right_df,
            left_on=c.left_keys,
            right_on=[renames[i] if i in renames else i for i in c.right_keys],
            how="outer",
            sort=True,
            indicator=True
        )

        out_left_df = df_merged[df_merged['_merge'] == 'left_only']
        out_join_df = df_merged[df_merged['_merge'] == 'both']
        out_right_df = df_merged[df_merged['_merge'] == 'right_only']

        out_left_df = out_left_df.drop(columns = right_df.columns.tolist() + ['_merge']).sort_values(by=c.left_keys, na_position='first')
        out_join_df = out_join_df.drop(columns = '_merge').sort_values(by=c.left_keys, na_position='first')
        out_right_df = out_right_df.drop(columns = left_df.columns.tolist() + ['_merge']).sort_values(by=[renames[i] if i in renames else i for i in c.right_keys], na_position='first')

        self.left = out_left_df;
        self.inner = out_join_df;
        self.right = out_right_df;

    def join_by_cross(self,left_df,right_df,renames,renames_back):
        target_names = {}
        source_names = {}
        for i, name1 in enumerate(left_df.columns):
            target_names[name1] = "Target_"+name1
        for j, name2 in enumerate(right_df.columns):
            source_names[name2] = "Source_"+name2

        df_merged = pd.merge(
            left_df.rename(columns=target_names),
            right_df.rename(columns=source_names),
            how="cross"
        )
        self.inner=df_merged

    def execute(self,left_datasource,right_datasource):
        c = self.config;
        print("Executing Join:")
        left_df = left_datasource.copy();
        right_df = right_datasource.copy();

        renames,renames_back = self.get_renames(left_df,right_df);

        if len(renames) and c.how!="cross":
            right_df.rename(columns = renames, inplace=True)

        if c.how=="cross":
            self.join_by_cross(left_df,right_df,renames,renames_back)
            right_df.rename(columns = renames, inplace=True)
        elif c.how=="position":
            self.join_by_pos(left_df,right_df,renames,renames_back)
        else:
            self.join_by_key(left_df,right_df,renames,renames_back)
        if c.how!="cross":
            self.right = self.right.rename(columns=renames_back)

            self.left.reset_index(drop = True,inplace = True)
            self.inner.reset_index(drop = True,inplace = True)
            self.right.reset_index(drop = True,inplace = True)
        if self.xml:
            # if c.how=="cross":
            #     self.inner = self.inner.rename(columns=renames)
            self.inner = Select(xml = self.xml.find(".//SelectConfiguration")).execute(self.inner)
            if c.how=="cross":
                self.inner = self.inner.rename(columns=renames_back)
        return self if c.how!="cross" else self.inner.astype(left_df.dtypes+right_df.dtypes)
