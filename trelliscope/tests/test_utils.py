import pytest
import os
import tempfile
import re

from trelliscope import utils

def get_error_message(text: str):
    return f"error text contains {text}"

def test_check_enum():
    utils.check_enum("trucks", ["cars", "trucks", "bikes"], get_error_message)

    with pytest.raises(ValueError, match="must be one of"):
        utils.check_enum("planes", ["cars", "trucks", "bikes"], get_error_message)

def test_check_is_list():
    utils.check_is_list(["a", "b", "c"], get_error_message)

    with pytest.raises(ValueError, match=r"Expected value .+ to be a list"):
        utils.check_is_list("a", get_error_message)

def test_check_has_variable(iris_df):
    utils.check_has_variable(iris_df, "Sepal.Length", get_error_message)

    with pytest.raises(ValueError, match="Could not find variable"):
        utils.check_has_variable(iris_df, "stuff", get_error_message)

def test_check_numeric(iris_df):
    utils.check_numeric(iris_df, "Sepal.Length", get_error_message)

    with pytest.raises(ValueError, match="must be numeric"):
        utils.check_numeric(iris_df, "Species", get_error_message)

def test_check_range(iris_df):
    utils.check_range(iris_df, "Sepal.Length", 0, 10, get_error_message)

    with pytest.raises(ValueError, match="must be in the range"):
        utils.check_range(iris_df, "Sepal.Length", 11, 15, get_error_message)

    with pytest.raises(ValueError, match="must be in the range"):
        utils.check_range(iris_df, "Sepal.Length", 0, 0.5, get_error_message)

def test_sanitize():
    actual = utils.sanitize("abc def")
    assert actual == "abc_def"

    actual = utils.sanitize("ABC def")
    assert actual == "abc_def"

    actual = utils.sanitize("ABC def", False)
    assert actual == "ABC_def"

    actual = utils.sanitize("abc?:/!@#$%^&*()<>,;:'\"|\\{}~`def")
    assert actual == "abcdef"

def test_get_jsonp_wrap_text_dict():
    json_dict = utils.get_jsonp_wrap_text_dict(False, "__abc_123")
    assert json_dict == {"start": "", "end": ""}

    jsonp_dict = utils.get_jsonp_wrap_text_dict(True, "__abc_123")
    assert jsonp_dict == {"start": "__abc_123(", "end": ")"}

def test_get_file_path():
    # TODO: Verify this path test works on windows...
    jsonp_path = utils.get_file_path("/test1/test2", "file", True)
    assert jsonp_path == "/test1/test2/file.jsonp"

    json_path = utils.get_file_path("/test1/test2", "file", False)
    assert json_path == "/test1/test2/file.json"

def test_read_jsonp():
    # From https://stackoverflow.com/a/8577226
    # using tempfile in a standard with block doesn't allow a second open
    # on Windows, hence the more complicated way here.
    
    content = """__loadAppConfig__07e09065({
        "name": "Trelliscope App",
        "data_type": "jsonp",
        "id": "07e09065"
        })"""
    
    # Note the suffix here is jsonp not json
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jsonp")
    try:
        tmp.write(content.encode("utf8"))
        tmp.close()
        dict = utils.read_jsonp(tmp.name)

        assert dict == {"name": "Trelliscope App",
                        "data_type": "jsonp",
                        "id": "07e09065"
                        }
    finally:
        tmp.close()
        os.unlink(tmp.name)

def test_read_jsonp_with_json():
    # From https://stackoverflow.com/a/8577226
    # using tempfile in a standard with block doesn't allow a second open
    # on Windows, hence the more complicated way here.
    
    content = """{
        "name": "Trelliscope App",
        "data_type": "jsonp",
        "id": "07e09065"
        }"""
    
    # Note the suffix here is json not jsonp
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    try:
        tmp.write(content.encode("utf8"))
        tmp.close()
        dict = utils.read_jsonp(tmp.name)

        assert dict == {"name": "Trelliscope App",
                        "data_type": "jsonp",
                        "id": "07e09065"
                        }
    finally:
        tmp.close()
        os.unlink(tmp.name)

def test_write_jsonp():
    # From https://stackoverflow.com/a/8577226
    # using tempfile in a standard with block doesn't allow a second open
    # on Windows, hence the more complicated way here.
    
    content = """{
        "name": "Trelliscope App",
        "data_type": "jsonp",
        "id": "07e09065"
        }"""

    expected_jsonp = """__abc_123(
        {
        "name": "Trelliscope App",
        "data_type": "jsonp",
        "id": "07e09065"
        })"""


    # Note the suffix here is jsonp not json
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jsonp")
    try:
        utils.write_json_file(tmp.name, True, "__abc_123", content)

        with open(tmp.name) as file:
            actual_content = file.read()

        actual_cleaned = re.sub(r"\s", "", actual_content)
        expected_cleaned = re.sub(r"\s", "", expected_jsonp)

        assert actual_cleaned == expected_cleaned

    finally:
        tmp.close()
        os.unlink(tmp.name)

def test_write_jsonp_with_json():
    # From https://stackoverflow.com/a/8577226
    # using tempfile in a standard with block doesn't allow a second open
    # on Windows, hence the more complicated way here.
    
    content = """{
        "name": "Trelliscope App",
        "data_type": "jsonp",
        "id": "07e09065"
        }"""

    # Note the suffix here is json not jsonp
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    try:
        utils.write_json_file(tmp.name, False, "__abc_123", content)

        with open(tmp.name) as file:
            actual_content = file.read()

        actual_cleaned = re.sub(r"\s", "", actual_content)
        expected_cleaned = re.sub(r"\s", "", content)

        assert actual_cleaned == expected_cleaned

    finally:
        tmp.close()
        os.unlink(tmp.name)