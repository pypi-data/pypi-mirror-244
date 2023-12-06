import pandas as pd;
import re;
import math;
from datetime import datetime, timedelta;
import random;

units = {
    "yea":"years",
    "year":"years",
    "years":"years",
    "mon":"months",
    "mont":"months",
    "month":"months",
    "months":"months",
    "day":"days",
    "days":"days",
    "hou":"hours",
    "hour":"hours",
    "hours":"hours",
    "min":"minutes",
    "minu":"minutes",
    "minut":"minutes",
    "minute":"minutes",
    "minutes":"minutes",
    "sec":"seconsd",
    "seco":"seconds",
    "secon":"seconds",
    "second":"seconds",
    "seconds":"seconds",
    "1":"deciseconds",
    "ds":"deciseconds",
    "dsec":"deciseconds",
    "dsecs":"deciseconds",
    "decisecond":"deciseconds",
    "deciseconds":"deciseconds",
    "2":"centiseconds",
    "cs":"centiseconds",
    "csec":"centiseconds",
    "csecs":"centiseconds",
    "centisecond":"centiseconds",
    "centiseconds":"centiseconds",
    "3":"milliseconds",
    "ms":"milliseconds",
    "msec":"milliseconds",
    "msecs":"milliseconds",
    "millisecond":"milliseconds",
    "milliseconds":"milliseconds",
    "6":"microseconds",
    "us":"microseconds",
    "usec":"microseconds",
    "usecs":"microseconds",
    "microsecond":"microseconds",
    "microseconds":"microseconds",
    "9":"nanoseconds",
    "ns":"nanoseconds",
    "nsec":"nanoseconds",
    "nsecs":"nanoseconds",
    "nanosecond":"nanoseconds",
    "nanoseconds":"nanoseconds",
    # "12":"picosecond",
    # "ps":"picosecond",
    # "psec":"picosecond",
    # "psecs":"picosecond",
    # "picosecond":"picosecond",
    # "picoseconds":"picosecond",
    # "15":"femtosecond",
    # "fs":"femtosecond",
    # "fsec":"femtosecond",
    # "fsecs":"femtosecond",
    # "femtosecond":"femtosecond",
    # "femtoseconds":"femtosecond",
    # "18":"attosecond",
    # "as":"attosecond",
    # "asec":"attosecond",
    # "asecs":"attosecond",
    # "attosecond":"attosecond",
    # "attoseconds":"attosecond",
}

class Functions:
    @staticmethod
    def parse_formula(text,df_name="df",column_names=[]):
        column_names = sorted(column_names, key=lambda x: len(x), reverse=True)

        def parse_if_else(formulaText):
            ifelsePattern = "(?i)(?:^|[^\w])(?:If|ElseIf)[^\w]+(\!)*(.*?)\sThen\s(.*?)(?=\sElseIf|\sElse|\n)|Else\s+(.*?)(?:\n| Endif)"

            newText = formulaText;


            matches = re.findall(ifelsePattern, newText)

            ifStatement = ""

            if len(matches)==0:
                return text; #RETURN NONE AND JUST USE THE ORIGINAL EXPRESSION
            for index, (negation,condition, ifExpression, elseExpression) in enumerate(matches):
                condition = condition.replace("=","==")

                negation.replace("!"," not ")

                condition = f"(False if pd.isna({negation}{condition}) else ({negation}{condition}))" if condition!="" else "" #pd.NA is ambiguous, this solves the ambiguity
                if index==0:
                    ifStatement+= ifExpression + " if " + condition
                elif condition!="":
                    ifStatement += " else "+ifExpression +" if "+ condition
                else:
                    ifStatement += " else "+elseExpression
            return ifStatement;

        def format_formula(text, df_name):
            def replace_column(match):
                column_name = match.group(1)
                return f"{df_name}['{column_name}']"

            def title_fns(match):
                return "Functions." + match.group(1).title()

            commentPattern = "\/\/.*?\n+"

            formatted_str = re.sub(commentPattern," ",text)
            formatted_str = re.sub(r'\[([^\[\]]+)\]', replace_column, formatted_str)
            formatted_str = re.sub(r'\b([\w_]+)\b(?=\()', title_fns, formatted_str)
            formatted_str = re.sub(r'\!', "not ", formatted_str)
            formatted_str = re.sub(r'\s', " ", formatted_str)
            formatted_str = re.sub(r'\sand\s', " and ", formatted_str, flags = re.IGNORECASE)
            formatted_str = re.sub(r'\sor\s', " or ", formatted_str, flags = re.IGNORECASE)
            return formatted_str

        def wrap_column_names(text, column_names):
            for item in column_names:
                pattern = re.compile(rf'(?<=[\s\[]){re.escape(item)}(?=[\s\]])', re.IGNORECASE)
                text = pattern.sub(item, text)

            for item in column_names:
                pattern = re.compile(rf'(?<!\[)(?<=[\s\[]){re.escape(item)}(?=[\s\]])(?!\])(?![^\[]*\])', re.IGNORECASE)
                text = pattern.sub(f'[{item}]', text)

            #being very lazy here
            for item in column_names:
                pattern = re.compile(rf'^{re.escape(item)}[^\w]', re.IGNORECASE)
                text = pattern.sub(f'[{item}]', text)

            return text

        text = wrap_column_names(text,column_names)
        text = format_formula(text,df_name)
        text = parse_if_else(text)
        return text

    @staticmethod
    def format_field_formula(text, field):
        text = text.replace("_CurrentField_",field)
        text = text.replace("[_CurrentFieldName_]",f'"{field}"')
        text = text.replace("_CurrentFieldName_",f'"{field}"')
        return text

    @staticmethod
    def Datetimeadd(dt,i,u):
        out = dt;
        unit = units[u.lower()]

        dur_dict = {
            "years":0,
            "months":0,
            "days": 0 ,
            "hours":0,
            "minutes":0,
            "seconds":0,
            "milliseconds":0,
            "microseconds":0,
            "nanoseconds":0
        }
        dur_dict[unit] += i;

        duration = pd.DateOffset(
            years=dur_dict["years"],
            months=dur_dict["months"],
            days=dur_dict["days"],
            hours=dur_dict["hours"],
            minutes=dur_dict["minutes"],
            seconds=dur_dict["seconds"],
            milliseconds=dur_dict["milliseconds"],
            microseconds=dur_dict["microseconds"],
            nanoseconds=dur_dict["nanoseconds"]
        )

        out = out + duration;

        return out

    @staticmethod
    def get_timedelta_units(diff,u):

        if u=="years":
            return diff.years
        if u=="months":
            return diff.months
        if u=="days":
            return diff.days
        if u=="hours":
            return diff.hours
        if u=="minutes":
            return diff.minutes
        if u=="seconds":
            return diff.total_seconds()
        return "WOW"

    @staticmethod
    def Datetimediff(dt1,dt2,u):
        diff = dt1 - dt2
        if pd.isna(diff):
            diff=pd.NA
        else:
            diff = Functions.get_timedelta_units(diff,units[u.lower()])

        return diff

    @staticmethod
    def Trim(str,sep=" "):
        if pd.isna(str):
            return str
        return str.strip(sep)

    @staticmethod
    def Isnull(obj):
        if isinstance(obj,pd.Series):
            return obj.isna()
        return pd.isnull(obj)

    @staticmethod
    def Null():
        return pd.NA

    @staticmethod
    def Titlecase(str):
        return str.title()

    @staticmethod
    def Startswith(str,start):
        return str.startswith(start)

    @staticmethod
    def Datetimeparse(dt,format):
        return datetime.strptime(dt,format)

    @staticmethod
    def Todate(dt):
        return pd.Timestamp(dt)

    @staticmethod
    def Datetimetoday():
        now =  pd.Timestamp.now()
        now = Functions.Datetimeformat(now,"%Y-%m-%d")
        return now

    @staticmethod
    def Datetimeformat(dt,format):
        return datetime.strptime(datetime.strftime(dt,format),format)

    @staticmethod
    def Datetimenow():
        return pd.Timestamp.now()

    @staticmethod
    def Round(num,acc):
        if acc == 0:
            raise ValueError("The round argument cannot be zero.")
        if num/acc - int(num)==0.5:
            return math.ceil(num/acc) * acc
        return round(num/acc) * acc

    @staticmethod
    def Average(*args):
        return sum(args) / len(args)

    @staticmethod
    def Uppercase(str):
        return str.upper()

    @staticmethod
    def Regex_Match(str,pattern):
        match = re.match(pattern,str,flags=re.IGNORECASE)
        if match:
            return True
        return False

    @staticmethod
    def Randint(size):
        return random.randint(0, size)

    @staticmethod
    def Rand():
        return random.random()

    @staticmethod
    def Log(num):
        if num>0:
            return math.log(num)
        return pd.NA

    @staticmethod
    def Iif(con,v1,v2):
        return v1 if con else v2
