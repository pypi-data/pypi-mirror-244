from .Config import Config;
import pandas as pd;
import os;

class FileOutput:
    def __init__(self,yxdb_tool=None,execute=True,**kwargs):
        INPUT_CONSTRAINTS = [
            {
                "name":"base_dir",
                "required":False,
                "type":str,
                "default":None
            },
            {
                "name":"file_path",
                "required":True,
                "type":str
            }
        ]
        self.config = Config(INPUT_CONSTRAINTS);
        if yxdb_tool:
            self.load_yxdb_tool(yxdb_tool, execute=execute)
        else:
            self.config.load(kwargs)

    def set_dir(self,dir):
        self.config.base_dir = dir
        return self

    def get_yxdb_mapping(self):
        return {
            "Input":"Input",
            "Output":"Output"
        }

    def load_yxdb_tool(self,tool, execute=True):
        kwargs = {};
        xml = tool.xml;
        config = xml.find("Properties").find("Configuration");
        file = config.find("File");
        kwargs['file_path'] = file.text
        new_base_dir = os.path.join(tool.dir,"..\\")
        kwargs['base_dir'] = os.path.normpath(new_base_dir)
        self.config.load(kwargs)
        if execute:
            input_df = tool.get_input("Input")
            next_df = self.set_dir(self.config.base_dir).execute(input_df)

    def write_csv(self,df):
        c = self.config;
        df.to_csv(path_or_buf = c.file_path, index = False)

    def execute(self,input_datasource):
        c = self.config
        print("Executing FileOutput: ",c.file_path)
        file_type = c.file_path.split(".")[-1]
        if c.base_dir:
            new_path = os.path.join(c.base_dir, c.file_path)
            # Normalize the path to handle any '..' or '.' segments. if C.file_name is a full path, it will ignore the rest.
            new_path = os.path.normpath(new_path)
            c.file_path = new_path
        if file_type=="csv":
            new_df = self.write_csv(input_datasource)
        else:
            raise Exception(f"File type: {file_type} not supported.")
        return self
