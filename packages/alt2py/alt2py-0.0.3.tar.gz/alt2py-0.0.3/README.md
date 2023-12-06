# alt2py
alt2py is a python package that provides tools for data preperation, blending and extraction using pandas. This package provides tools similar to Alteryx Designer, so Alteryx users can carry some of their Alteryx skills over to python. Alternatively, use this package to parse yxdb files and create similar logic that can be run entirely in Python.

# Tools
The main components of this package are called "Tools". Each tool is a python Class that can be passed keyword arguments to set up the configuration of the tool. Each tool also has an execute function that accepts the pandas dataframe/s that you want to perform that tools functionality on. Tools execute functions do not alter input dataframes.

If the tool only has a single output, the execute function will return the altered_dataframe:

## Single Output Tools

from alt2py.tools import [Tool_Name]

altered_df = Tool_Name(
    key_word1 = "value",
    key_word2 = "value"
).execute(input_dataframe1,input_dataframe2)


## Multiple Output Tools

from alt2py.tools import [Tool_Name]

class_instance = Tool_Name(
    key_word1 = "value",
    key_word2 = "value"
).execute(input_dataframe1,input_dataframe2) //returns the instance of the class with the outputs added to new attributes

output_df1 = class_instance.output1
output_df2 = class_instance.output2


## Sample ("Random Sample" and Create Samples)
**Key word arguments:**
> **train: float or int, default=1**
>> If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the train split. If int, represents the absolute number of train samples. If None, the value is automatically set to the complement of the validate size.

> **validate: float or int, default=1**
>> If float, should be between 0.0 and 1.0 and represent the proportion of the dataset to include in the validate split. If int, represents the absolute number of validate samples. If None, the value is automatically set to the complement of the train size.If *train* is also None, it will be set to 0.25.

> **shuffle: bool, default=True**
>> Whether or not shuffling is applied to the data before applying the split.

> **seed: int, default=None**
>> Controls the shuffling applied to the data before applying the split. Pass an int for reproducible output across multiple function calls.

**Returns:**
self, with 3 new instance attributes: *self.train*, *self.validate* and *self.hold*

## Clean (Data Cleansing)
**Key word arguments:**
> **filter_na_cols: boolean, default=False**
>> When True, this tool will filter any column that only contains ps.NA.

> **filter_na_rows: boolean, default=False**
>> When True, this tool will filter any column that only contains ps.NA.

> **fields: list, default=[all columns]**
>> Fields to apply the cleaning to (excluding params above).

> **replace_na_blank: boolean, default=False**
>> If True, this tool will replace pd.NA with an empty string. Only applies to String type columns.

> **replace_na_zero: boolean, default=False**
>> If True, this tool will replace pd.NA with a 0. Only applies to numeric type columns.

> **trim_whitespace: boolean, default=False**
>> Remove leading and trailing whitespace.

> **remove_dup_space: boolean, default=False**
>> Replace any occurrence of whitespace with a single space, including line endings, tabs, multiple spaces, and other consecutive whitespaces.

> **remove_all_space: boolean, default=False**
>> Remove any occurrences of whitespace.

> **remove_letters: boolean, default=False**
>> Remove any occurences of letters.

> **remove_numbers: boolean, default=False**
>> Remove any occurences of Numbers. Only applies to String type columns.

> **remove_punctuation: boolean, default=False**
>> Remove these characters: ! " # $ % & ' ( ) * + , \ - . / : ; < = > ? @ [ / ] ^ _ ` { | } ~

> **modify_case: boolean, default=False**
>> If True, apply the modifier (below) to all String type columns.

> **modifier: string, default=title, accepts="title"|"upper"|"lower"**
>> - **upper**: Capitalise all letters in a string.
>> - **lower**: Convert all letters in a string to lowercase.
>> - **title**: Capitalize the 1st letter of all words in a string.

**Returns:**
Altered Dataframe

## Filter
**Key word arguments:**
> **expression: str or function, default="True"**
>> Pass a string to use Alteryx syntax for filtering. Alternatively pass a Python function that returns a boolean.

**Returns:**
self, with 2 new instance attributes: *self.train*, *self.false*

## Formula
**Key word arguments:**
> **formulae: [{field,type,size,expression}], default=[]**
>> A list of Python dictionaries

> **field: str, required**
>> The name of the field. If this field already exists, it will be updated. If the field doesn't exist, it will be created.

> **type: str, required if the field is new. defaults to the type of the original field if the field already exists**
>> The data type for the field.

> **size: str, default=None**
>> The size of the data.

> **expression: str or function, required**
>> Pass a string to use Alteryx syntax for the expression. Alternatively pass a Python function that returns the value.

## Imputer
Use Imputation to replace a specified value within one or more numeric data fields with another specified value.

A typical use case is to replace all pd.NA values with the average of the remaining values for fields Q1_Sales and Q2_Sales so the pd.NA values do not affect the final outcome of their forecasting model.
**Key word arguments:**
> **fields: [str], required**
>> The fields to apply the imputation to.

> **impute_value: Number or pd.NA, default=pd.NA**
>> The value that you want to be replaced with imputation.

> **impute_fn: str[Agg], default=None**
>> A string that references an Aggregator.

> **impute_static: number, default=None**
>> An int of float to be used as the replacement value. This parameter is only used if there is no *impute_fn*.

> **indicator: bool, default=False**
>> If True, add a new column of booleans for each selected field to flag that records that were imputed.

> **add_fields: bool, default=False**
>> If True, maintain the original fields and add a new column with imputed data. If False, update the original fields to contain the imputed data.

> **new_prefix: str, default=""**
>> prefix to add to the column name of the added fields.

> **new_suffix: str, default="_imputed"**
>> suffix to add to the column name of the added fields.

> **indicator_prefix: str, default=""**
>> prefix to add to the column name of the indicator fields.

> **indicator_suffic: str, default="_indicator"**
>> prefix to add to the column name of the indicator fields.


## MultiFieldBin
Use Multi-Field Binning to replicate some of the functionality of the Tile tool—additional features allow the data to be binned on multiple fields. Built primarily for the predictive toolset, Multi-Field Binning only accepts numeric fields for binning. You can bin fields on either equal records or equal intervals.
**Key word arguments:**
> **fields: [str], required**
>> A list of numeric fields that are used to determine the bins.

> **mode: str, default="count", accepts="count"|"interval"**
>> - **count**: Bins will be created such that there are an equal number of records in each bin.
>> - **interval**: The minimum and maximum values of the selected fields are determined. The range is split into equal-sized sub-ranges. Records are assigned to bins based on these ranges.

> **bins: int, required**
>> Number of bins to split the data into.

> **prefix: str, default=""**
>> prefix to add the field_name for the new column.

> **suffix: str, default="_Tile"**
>> suffix to add the field_name for the new column.


## MultiFieldFormula
Use Multi-Field Formula to create or update multiple fields using a single expression.
**Key word arguments:**
> **fields: [str], required**
>> A list of the field names to apply the formula to.

> **expression: str or fn, default="count"**
>> The expression to apply to selected fields. If a string is passed, it will be parsed as an Alteryx expression. Alternatively, you can pass a normal Python function.

> **type: int, required**
>> The type to change the new fields to.

> **size: str, default=None**
>> The size to change the new fields to.

> **prefix: str, default=""**
>> The prefix to add to the field_name as a new column. If both prefix and suffix are empty, update the selected field instead of creating a new one.

> **suffix: str, default=""**
>> The suffix to add to the field_name as a new column. If both prefix and suffix are empty, update the selected field instead of creating a new one.

## MultiRowFormula
Use Multi-Row Formula to take the concept of the Formula tool a step further. This tool allows you to use row data as part of the formula creation and is useful for parsing complex data, and creating running totals, averages, percentages, and other mathematical calculations.

The Multi-Row Formula tool can only update one field per tool instance. If you would like to update multiple fields, you need to add a Multi-Row Formula tool for each field to be updated.

**Key word arguments:**
> **field: str, required**
>> The field to update or add. If the field name already exists in the dataframe, perform an update on that field. If the field doesn't already exist in.

> **groupings: [str], default=[]**
>> The field/s to group each iteration by.

> **expression: str or fn, required**
>> The expressions to apply on each iteration. If a string is passed, it will be passed, it will be parsed as an Alteryx expression. Alternatively, you can pass a normal Python function.

> **num_rows: int, default=1**
>> The number of rows to lookup backwards and forwards from the current iterations row. #TODO: this parameter can be parsed from the expression. get rid of it.

> **type: int, required**
>> The type to assign to the updated/new column.

> **size: str, default=None**
>> The size to assign to the updated/new column.

> **unknown: str or pd.NA, default=pd.NA, accepts="null"|"empty"|"nearest"|pd.NA**
>> The value to apply to non existent rows.


## OverSample
 This tool is used to create a new sample for analysis that has an elevated percentage of a certain value (often a 50-50 split of positive and negative responses is used).
**Key word arguments:**
> **field: str, required**
>> The field to oversample in the data.

> **value: field_type, required**
>> The value of the field to oversample.

> **sample: int, default=50**
>> The percentage (between 1 and 100) of records that should have the desired value in the field of interest


## RecordID
Use Record ID to create a new column in the data and assign a unique identifier that increments sequentially for each record in the data. The Record ID tool generates unique identifiers with numeric values or string values, based on the data type you select.
**Key word arguments:**
> **field: str, required**
>> The field name to assign to the new column.

> **start: int, default=1**
>> The ID to be assigned to the first record in the dataframe.

> **type: str, default="Int", accepts: "Int"|"String"**
>> The type to be assigned to the new column.

> **size: str, default=None**
>> The size to be assigned to the new column.

> **position: bool, default=False**
>> If True, the new field will be the first columm in the dataframe.


## Select
**Key word arguments:**
> **selected: [str], required**
>> A list of all of the columns to keep in the dataframe.

> **deselected: [str], default=[]**
>> A list of all of the columns to remove from the dataframe.

> **keep_unknown: str, default=False**
>> If True, any columns that are in the dataframe, but not in *selected* or *deselected*, will be kept in the dataframe.

> **types: {*field_name*: *type*}, default={}**
>> A dictionary with field_names as keys and the type to remap that field to as the values.

> **renames: {*field_name*: *new_name*}, default={}**
>> A dictionary with field_names as keys and the new field name to remap that field to as the values.

> **reorder: bool, default=True**
>> If True, the columns will be reordered to match the *selected* list. If False, the original order will be maintained.


## SelectRecords
**Key word arguments:**
> **conditions: [str], required**
>> Enter the records or range of records to return.
>> - A single digit returns only the entered row. For example, "3" returns only row 3.
>> - A minus sign before a number returns row 1 through the entered row. For example, "-2" returns rows 1 and 2.
>> - A range of numbers returns the rows in the range, including the entered rows. For example, "17-20" returns rows 17, 18, 19, and 20.
>> - A number followed by a plus sign returns the entered row through the last row. For example, "50+" returns row 50 through the last row.
>> - Any combination can be used at the same time by entering the ranges as seperate list entries.

> **index: int, default=0, load_xml default=1**
>> The base index of the source data. In Pandas, this will usually be 0-based indexing so use index=0. In Alteryx, this will be 1-based indexing, so if the ranges originate from Alteryx, use index=1.


## Sort
**Key word arguments:**
> **fields: [str], required**
>> A list of fields to sort the dataframe by, in order of priority.

> **order: [bool], required**
>> This list **MUST** be the same length as the *fields* parameter. If the nth entry of order is True, the dataframe will be sorted by the nth entry of fields in ascending order. If false, the order will be descending.

> **handle_alpha_numeric: [bool], default=False**
>> If False, numeric strings are sorted left to right, character by character. eg. "22" will be *before* "4". If True, numeric strings are sorted from the smallest to the largest number. eg. "22" will be *after* "4".


## Tile
Use Tile to assign a value (tile) based on ranges in the data. The tool does this based on the user specifying one of 5 methods. 2 fields are added to the data:
- Tile number is the assigned tile of the record.
- Tile sequence number is the record number of the record's position within the Tile.

**Key word arguments:**
> **mode: str, required, accepts: "records"|"sum"|"smart"|"manual"|"unique"**
>>  The type of tiling to use:
>> - records: Input records are divided into the specified amount of tiles so that each tile is assigned the same amount of records.
>> - sum: Assigns tiles to cover a range of values where each tile has the same total of the Sum field based on the sort order of the incoming records.
>> - smart:Creates tiles based on the Standard Deviation of the values in the specified field. The tiles assigned indicate whether the record's value falls within the average range (=0), above the average (1), or below the average (-1), etc.
>> - manual:The user can specify the cutoffs for the tiles by typing a value on a new line for each range.
>> - unique: For every unique value in a specified field or fields, a unique tile is assigned. If multiple fields are specified, a tile is assigned based on that combination of values.

> **field: str, required**
>> The field to perform tiling on.

> **num_tiles: int, default=None**
>> The amount of tiles to be created. **MUST** be specified for *mode*="records"|"sum". **IGNORED** otherwise.

> **no_split: str, default=None**
>> A tile is not split across this field if selected. **IGNORED** if *mode* is not "records".

> **manual: [int], default=False**
>> the upper limit of each manually defined tile. **IGNORED** if *mode* is not "manual".

> **tile_name: str, default="Tile_Num"**
>> The field name for the tile number of the record.

> **seq_name: str, default="Tile_SequenceNum"**
>> The field name for the record number of the record's position within the Tile

> **smart_tile_name: str, default="SmartTile_Name"**
>> The field name for the smart tile description ranging from *Extremely Low* to *Extremely High*.


## Unique
Use Unique to distinguish whether a data record is unique or a duplicate by grouping on one or more specified fields, then sorting on those fields.

**Key word arguments:**
> **fields: [str], required**
>> The combination of fields that you want to test for uniqueness.

**Returns:**
self, with 2 new instance attributes: *self.unique* and *self.duplicates*.


## Join
Use Join to combine 2 inputs based on common fields between the 2 dataframes. You can also Join 2 data streams based on record position. This tool can also do a cartesean join (append in alteryx).

**Key word arguments:**
> **how: string, default="cross", accepts="cross"|"position"**
>> If cross, the tool will do a join by keys, if position the tool will do a join by record position.

> **left_keys: [str], default=None**
>> The field names from the left (first) dataframe. **IGNORED** when *how*="position".

> **right_keys: [str], default=None**
>> The field names from the right (second) dataframe. **IGNORED** when *how*="position". **MUST** be the same length as *left_keys*

**Returns:**
self, with 3 new instance attributes: *self.left*, *self.right* and *self.inner*.


## JoinMultiple
Use JoinMultiple to combine 2 or more inputs based on a commonality between the input dataframes. By default, the tool outputs a full outer join. Visit Join Tool for more information.

**Key word arguments:**
> **fields: [[str]], default=[]**
>> A list of lists of keys. The number of sub-lists must be equal to the number of dataframes passed to execute. The length of each sub-list must be equal. **IGNORED** if by_position is True.

>**names: [str], default=["#1","#2"...]**
>> The name of each dataframe passed to execute. This is used for renaming columns that have duplicated names.

> **by_position: bool, default=False**
>> If False, the tool will do a join by keys. If True, the tool will do a join by record position.

> **inner: bool, default=False**
>> If False, returns a full outer join of all the dataframes. If True, only return the inner join of the dataframes.

**Returns:**
Joined Dataframe.

## Union
Use Union to combine 2 or more datasets on column names or positions. In the output, each column contains the rows from each input.

**Key word arguments:**
> **mode: str, default="position", accepts="position"|"name"|"manual"**
>> - **position:** Stack data by the column order in the dataframes.
>> - **name:** Stack data by column name.
>> - **manual:**  Allows you to manually specify how to stack data. When you choose this method, the manual parameter is **REQUIRED**

>**subset: bool, default=True**
>> If true, only output the fields that match. If False, keep all fields from all dataframes and populate missing data with *pd.NA*.

> **manual: [], default=[]**
>>  A list of lists of field_names. The number of sub-lists must be equal to the number of dataframes passed to execute. The length of each sub-list must also be equal, this will contain the order of each dataframe to stack.

**Returns:**
Unioned Dataframe.

## DateTime
Use DateTime to transform date-time data to and from a variety of formats, including both expression-friendly and human-readable formats. You can also specify the language of your date-time data. When carrying operations with 2 date-time data of different precision, the higher precision prevails. To format more precise date-time formats as strings, you need to insert a Select tool before you write to a database.

**Key word arguments:**
>**to_string: bool, default=False**
>> If False, convert a DateTime object to a String. If False, convert a String to a DateTime object.

>**field: str, default=True**
>> The name of the field that you want to convert.

>**label: str, default=""**
>> The name of the newly added field.

>**pattern: str, default=True**
>> The pattern to use with the conversion.

**Day, Month and Year Formats**
- **d:** Day of the month as digits, without leading zeros for single-digit days.

- **day:** The full name of the day of the week.

- **dd:** Day in 2 digits, with leading zeros for single-digit days. On input, leading zeros are optional.

- **dy:** Day of the week as a 3-letter abbreviation. On input, full names are accepted but Alteryx doesn't check that the day of the week agrees with the rest of the date.

- **EEEE:** The full name of the day of the week.

- **M:** A single-digit month, without a leading zero.

- **MM:** Month as digits, with leading zeros for single-digit months. On input, leading zeros are optional.

- **MMM:** The abbreviated name of the month.

- **MMMM:** The name of the month spelled out.

- **Mon:** A 3-letter abbreviation of the name of the month. On input, full names are also accepted.

- **Month:** Name of the Month. On input, abbreviations are also accepted.

- **yy:** Year represented only by the last two digits. When converting from a string, two-digit years are mapped into the range from the current year, minus 66 years to the current year, plus 33 years. For example, in 2016, a two-digit year will be mapped into the range: 1950 to 2049. On input, four digits are also be accepted.

- **yyyy:** Year represented by the full 4 digits. On input, 2 digits will also be accepted and mapped as done for the “yy” pattern.s

**Hour, Minute and Seconds Formats**
- **ahh:** AM/PM (Simplified Chinese only).

- **H:** Hour, with no leading zeros for single-digit hours (24-hour clock).

- **HH or hh:** Hours, with leading zeros for single-digit hours (24-hour clock).

- **mm:** Minutes, with leading zeros for single-digit minutes.

- **ss:** Seconds, with leading zeros for single-digit seconds.

**Seperators**

On output, separators in the date/time format are used exactly. On input...

- \- and / are accepted as equivalent.

- White space is ignored.

- : and , must match exactly.

**Returns:**
Altered Dataframe.

## Regex
Use RegEx (Regular Expression) to leverage regular expression syntax to parse, match, or replace data.

**Key word arguments:**
>**field: str, default=None, Required**
>> The name of the column to parse.

>**pattern: str, default=None, Required**
>> The Regex expression to be used on the selected field.

>**case_insensitive: bool, default=True**
>> Whether or not the regex expression should be sensitive to case.

>**method: str, default=match, accepts="match"|"parse"|"tokenize"|"replace"**
>> The method to use to parse the text.
>> - **match:** Add a column containing a number: 1 if the expression matched, 0 if it did not.
>> - **parse:** Add a column containing a number: 1 if the expression matched, 0 if it did not.

**Returns:**
Altered Dataframe.


## CrossTab
Use Cross Tab to pivot the orientation of data in a table by moving vertical data fields onto a horizontal axis and summarizing data where specified.

**Key word arguments:**
>**groupings: [str], default=[]**
>> A list of  field names that should be used to group the data. Data with identical values are grouped together into a single row.

>**header: str, Required**
>>  A field name to get the new headers. A new column is created for each unique value in the selected column.

>**value_field: str, Required**
>> A field name for the column that contains the values used to populate the new columns.

>**method: str,accepts="Sum"|"Average"|"Count"|"CountWithNulls"|"First"|"Last"|"Concat", Required**
>> The method for Aggregating values for combining multiple values in a field

>**sep: str,default="," when method is Concat,  Required**
>> TThe seperator to use for concatenation of multiple fields






>**method: str, default=match, accepts="match"|"parse"|"tokenize"|"replace"**
>> The method to use to parse the text.
>> - **match:** Add a column containing a number: 1 if the expression matched, 0 if it did not.
>> - **parse:** Add a column containing a number: 1 if the expression matched, 0 if it did not.

**Returns:**
Altered Dataframe.
