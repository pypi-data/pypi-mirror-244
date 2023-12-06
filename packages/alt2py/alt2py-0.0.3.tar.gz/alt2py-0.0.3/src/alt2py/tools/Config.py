import pandas as pd
class Config:
    def __init__(
        self,
        constraints
    ):
        self._constraints = constraints

    def load(self,kwargs):
        self.check_load_constraints(kwargs)
        self.__dict__.update(**kwargs)

    def check_load_constraints(self,kwargs):
        ## TODO: This was pretty rushed, could use a rework to make it more readable.
        for con in self._constraints:
            if con["name"] in kwargs and kwargs[con["name"]] is not None:
                if "validate" in con:
                    if not con["validate"]["validator"](kwargs):
                        raise TypeError(f"{con['validate']['error_msg']}")
                if "type" in con:
                    if not isinstance(kwargs[con["name"]],con["type"]):
                        raise TypeError(f"{con['name']} must be of type: {str(con['type'])}")
                if "sub_type" in con:
                    if isinstance(kwargs[con["name"]],list):
                        for k in kwargs[con["name"]]:
                            if not isinstance(k,con["sub_type"]):
                                raise TypeError(f"{con['name']} must only contain values of type: {str(con['sub_type'])}")
                if "multi_choice" in con:
                    if kwargs[con["name"]] not in con["multi_choice"]:
                        raise TypeError(f"{con['name']} must be one of the following values: {', '.join(con['multi_choice'])}")

            elif "." in con["name"] and con["name"].split(".")[0] in kwargs:
                [name,sub_name] = con["name"].split(".")
                to_test = kwargs[name]
                if not isinstance(to_test,list):
                    if to_test is None:
                        continue
                    to_test = [to_test]

                for dct in to_test:
                    if sub_name in dct and dct[sub_name] is not None:
                        if "multi_choice" in con:
                            if dct[sub_name] not in con["multi_choice"]:
                                raise TypeError(f"{con['name']} must be one of the following values: {', '.join(con['multi_choice'])}")

                        if not isinstance(dct[sub_name],con["type"]):
                            raise TypeError(f"{con['name']} must be of type: {str(con['type'])}")
                        if isinstance(dct[sub_name],list):
                            for k in dct[sub_name]:
                                if not isinstance(k,con["sub_type"]):
                                    raise TypeError(f"{con['name']} must only contain values of type: {str(con['sub_type'])}")
                        if "multi_choice" in con:
                            if dct[sub_name] not in con["multi_choice"]:
                                raise TypeError(f"{con['name']} must be one of the following values: {', '.join(con['multi_choice'])}")
                    else:
                        if "required" in con:
                            if con["required"]==True:
                                if "required_error_msg" in con:
                                    raise TypeError(con['required_error_msg'])
                                raise TypeError(f"{con['name']} is required")
                            elif hasattr(con["required"], "__call__") and con["required"](kwargs):
                                if "required_error_msg" in con:
                                    raise TypeError(con['required_error_msg'])
                                raise TypeError(f"{con['name']} is required")
                            else:
                                if "default" in con:
                                    if hasattr(con["default"], "__call__"):
                                        dct[sub_name] = con["default"](kwargs)
                                    else:
                                        dct[sub_name] = con["default"]
                                else:
                                    dct[sub_name] = None;
                        else:
                            if "default" in con:
                                if hasattr(con["default"], "__call__"):
                                    dct[sub_name] = con["default"](kwargs)
                                else:
                                    dct[sub_name] = con["default"]
                            else:
                                dct[sub_name] = None;

            else:
                if "required" in con:
                    if con["required"]==True:
                        if "required_error_msg" in con:
                            raise TypeError(con['required_error_msg'])
                        raise TypeError(f"{con['name']} is required")
                    elif hasattr(con["required"], "__call__") and con["required"](kwargs):
                        if "required_error_msg" in con:
                            raise TypeError(con['required_error_msg'])
                        raise TypeError(f"{con['name']} is required")
                if "default" in con:
                    if hasattr(con["default"], "__call__"):
                        kwargs[con["name"]] = con["default"](kwargs)
                    else:
                        kwargs[con["name"]] = con["default"]
                else:
                    kwargs[con["name"]] = None;

    def check_field_constraints():
        print("fields")

    def get_required_kwargs(self):
        attributes = vars(self)

        all_attrs = {}

        for attribute, value in attributes.items():
            if attribute == "_constraints":
                continue;
            else:
                all_attrs[attribute] = value
        ordered_filtered_attrs = []
        for con in self._constraints:
            if con["name"] in all_attrs:
                    ordered_filtered_attrs.append({
                        "key":con["name"],
                        "value":all_attrs[con["name"]]
                    })
        for k in all_attrs:
            if k not in [dct["name"] for dct in self._constraints]:
                ordered_filtered_attrs.append({
                    "key":k,
                    "value":all_attrs[k]
                })

        return ordered_filtered_attrs



    def __str__(self):
        attributes = vars(self)
        out=""
        max_spacing = max([len(attr) for attr,_ in attributes.items()])

        for attribute, value in attributes.items():
            space = " "*(max_spacing - len(attribute))
            newline = '\n' if len(out) else ''
            out +=(f"{newline}{attribute}: {space}{{{value}}}")
        return out
