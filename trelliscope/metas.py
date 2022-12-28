import json
import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

class Meta():
    """
    The base class for all Meta variants.
    """
    def __init__(self, type: str, varname: str, filterable: bool, sortable: bool, label: str = None, tags: list = None):
        # TODO: Should filterable and sortable have default values?
        
        # Note: We are specifically *NOT* using an underscore in these
        # variable names so the default JSON serialization using __dict__ works
        # as expected and produced the correctly named output.
        # This also makes sense in that this class is essentially a struct or a dict
        # with a few extra features.
        self.type = type
        self.varname = varname
        self.filterable = filterable
        self.sortable = sortable
        self.label = label
        self.tags = []
        
        if tags is None:
            # TODO: Verify this behavior, it's slightly different than what is done in R
            self.tags = []
        elif isinstance(tags, str):
            self.tags = [tags]
        elif isinstance(tags, list):
            self.tags = tags
        else:
            raise ValueError("Tags is an unrecognized type.")

        if label is None:
            # TODO: Verify this behavior. It seems to be expected by
            # a unit test, but was not present in the R code...
            self.label = varname

    def get_error_message(self, error_text: str):
        return f"While defining a `{self.type}` meta variable for the variable `{self.varname}`: `{error_text}`"

    def get_data_error_message(self, error_text: str):
        return f"While checking meta variable definition for variable `{self.varname}` against the data: `{error_text}`"

    def to_json(self, pretty: bool = True):
        indent_value = None

        if pretty:
            indent_value = 2

        return json.dumps(self, default=lambda o: o.__dict__, indent=indent_value)

    def check_varname(self, df: pd.DataFrame):
        if not self.varname in df.columns:
            raise ValueError(self.get_error_message("Could not find variable {self.varname} is in the list of columns"))

    def check_variable(self, df: pd.DataFrame):
        # To be overridden by sub classes
        pass

    def check_with_data(self, df: pd.DataFrame):
        self.check_varname(df)
        self.check_variable(df)


class NumberMeta(Meta):
    def __init__(self, varname: str, label: str = None, tags: list = None, digits: int = None, locale: bool = True):
        super().__init__(type="number", varname=varname, label=label, tags=tags,
            filterable=True, sortable=True)

        if digits is not None and not isinstance(digits, int):
            raise TypeError("Digits must be an integer")

        if locale is not None and not isinstance(locale, bool):
            raise TypeError("Locale must be logical (boolean)")

        self.digits = digits
        self.locale = locale

    def check_variable(self, df: pd.DataFrame):
        if not is_numeric_dtype(df[self.varname]):
            raise ValueError(self.get_data_error_message("Data type must be numeric"))



class CurrencyMeta(Meta):
    def __init__(self):
        super().__init__()
        raise NotImplementedError()


class StringMeta(Meta):
    def __init__(self, varname: str, label: str = None, tags: list = None):
        super().__init__(type="string", varname=varname, label=label, tags=tags,
            filterable=True, sortable=False)
        
    def check_variable(self, df: pd.DataFrame):
        if not is_string_dtype(df[self.varname]):
            raise ValueError(self.get_data_error_message("Data type is not a string"))

    # TODO: Add a cast variable method

class FactorMeta(Meta):
    def __init__(self):
        super().__init__()
        raise NotImplementedError()


class DateMeta(Meta):
    def __init__(self):
        super().__init__()
        raise NotImplementedError()


class DatetimeMeta(Meta):
    def __init__(self):
        super().__init__()
        raise NotImplementedError()


class GraphMeta(Meta):
    def __init__(self):
        super().__init__()
        raise NotImplementedError()


class GeoMeta(Meta):
    def __init__(self):
        super().__init__()
        raise NotImplementedError()


class HrefMeta(Meta):
    def __init__(self):
        super().__init__()
        raise NotImplementedError()
