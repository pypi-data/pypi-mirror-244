import json
from . import basic

__version__ = __VERSION__ = '0.0.5'
__modules__ = __MODULES__ = ['basic', 'advance']
__types__ = __TYPES__ = ['list_split', 'list_line', 'list_key', 'list_value']
__type__ = __TYPE__ = [basic.list_split, basic.list_line, basic.list_key, basic.list_value]

def write(__value__: dict,fp: str, append: bool=True, encoding: str="utf-8", ensure_ascii: bool=False, indent: int=3):
    """
    Write or append data into json file,
    'W' mode mean after delete data, write data into file again.
    'A' mode mean do not delete data, append dara into end of file.
    :param __value__: You'll write data into file
    :param fp: File path
    :param append: append or write
    :param encoding: encode, such as UTF-8, GB18030, GBK
    :param ensure_ascii: decode unicode
    :param indent: indent
    :return: None
    """
    with open(fp, "r", encoding=encoding) as f:
        try:
            data = json.load(f)
        except:
            data = []
        f.close()
    if type(data) != list:
        data = [data]
    if append:
        state = True
        try:
            ori = []
            now = ''
            values = ''

            for key, value in __value__.items():
                now = key
                values = value
            for i in range(len(data)):
                for key, value in data[i].items():
                    ori.append(key)
            if now in ori:
                data[ori.index(now)][now] = values
                state = False

        except:
            pass

        finally:
            if state:
                data.append(__value__)

    else:
        data = [__value__]

    with open(fp, "w", encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)
        f.close()

def read(__content__: tuple, fp=None, encoding: str="utf-8",return_type: type=str):
    """
    Smart read the json file,
    test.json:
    [
        {"a": {
                "b": "a"
            }
        }
    ]
    main.py:
    from custom_json import read

    read(__content__=("a","b"), fp="test.json")


    :param __content__: You want to search the value's content, for example, If data=[{"a": {"b": "c"}}],
                        then __content__=('a', 'b')
    :param fp: File path
    :param encoding: encoding, such as UTF-8
    :param return_type: after read the file, return data's type
                        Python's type
                        str -> return str(data) | str
                        list -> return [data] | list
                        dict -> return {json.dumps(data)} | dict
                        int -> return len(data) | length

                        Basic's type:
                        list_split -> return list(str(data)) / ['a','b','c']
                        list_line -> ['"t": "abc"', '"t2"': "cba"]
                        list_key -> ["t", "t1"]
                        list_value -> ["abc", "cba"]
    :return: any or basic
    """
    s_type = [list, str, int, dict, basic.list_split, basic.list_line, basic.list_key, basic.list_value]
    if return_type not in s_type:
        raise basic.ReturnTypeError(f"Invalid return type: '{return_type}', only support {s_type}")
    with open(fp, "r", encoding=encoding) as f:
        try:
            data = json.load(f)
        except:
            data = []
        f.close()
    if type(data) != list:
        data = [data]
    ori = []
    for i in range(len(data)):
        for key, value in data[i].items():
            ori.append(key)
    try:
        if isinstance(__content__, tuple):
            result = data[ori.index(__content__[0])]
            for item in __content__:
                result = result[item]
            if return_type == str:
                return str(result)
            elif return_type == list:
                return [result]
            elif return_type == dict:
                return json.dumps(result)
            elif return_type == int:
                return len(result)
            elif return_type == basic.list_split:
                return list(str(result))
            elif return_type == basic.list_line:
                return json.dumps(result, indent=3).replace(" ", "").replace(",", "").split("\n")[1:-1]
            elif return_type == basic.list_key:
                return list(result)
            elif return_type == basic.list_value:
                return list(result.values())
        else:
            raise ValueError("Invalid content type, should be a tuple")
    except (KeyError, TypeError):
        raise basic.NotFoundOptionsError(f"Not found '{__content__}', please check content or cannot change the type to {return_type}")
    except IndexError:
        raise basic.EmptyFileError(f"This file {fp} is empty, please write '[]' data")

def exist(__find__: str, fp=None, encoding: str="utf-8") -> bool:
    """
    Search the key in json file,
    test.json:
    [
        {"a": {
                "b": "a"
            }
        }
    ]
    main.py:
    from custom_json import exist

    print(exist(__find__="a", fp="test.json")) # True
    print(exist(__find__="d", fp="test.json")) # False

    :param __find__: You'll find data
    :param fp: File path
    :param encoding: encoding, such as UTF-8
    :return: bool, if __find__ in json data head return True, else return False
    """
    with open(fp, "r", encoding=encoding) as f:
        try:
            data = json.load(f)
        except:
            data = []
        f.close()
    ori = []
    for i in range(len(data)):
        for key, value in data[i].items():
            ori.append(key)
    if __find__ in ori:
        return True
    else:
        return False

def revise(__content__: tuple, __value__: any, fp=None, encoding: str="utf-8", ensure_ascii=False, indent: int=3):
    """
    Revise the json file,
    before test.json:
    [
        {"a": {
                "b": "a"
            }
        }
    ]
    main.py:
    from custom_json import revise

    revise(__content__=("a',"b"),__value__="111", fp="test.json")

    after test.json:
    [
        {"a": {
                "b": "111"
            }
        }
    ]

    :param __content__: json file content
    :param __value__: You want to revise value
    :param fp: File path
    :param encoding: encoding such as UTF-8
    :param ensure_ascii: ensure_ascii
    :param indent: indent
    :return: None
    """
    with open(fp, "r", encoding=encoding) as f:
        try:
            data = json.load(f)
        except:
            data = []
        f.close()
    if type(data) != list:
        data = [data]
    ori = []
    for i in range(len(data)):
        for key, value in data[i].items():
            ori.append(key)
    if isinstance(__content__, tuple):
        for item in __content__:
            data[ori.index(__content__[0])][item] = __value__
    with open(fp, "w", encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)