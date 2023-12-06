from .common import Union, datetime


def input_int(print_str: str) -> int:
    """
    int入力

    Parameters
    ----------
    print_str : str
        表示文字列

    Returns
    -------
    int
        入力数字
    """
    return _input(print_str=print_str, type=int)


def input_float(print_str: str) -> float:
    """
    float入力

    Parameters
    ----------
    print_str : str
        表示文字列

    Returns
    -------
    float
        入力数字
    """
    return _input(print_str=print_str, type=float)


def input_str(print_str: str) -> str:
    """
    文字列出力

    Parameters
    ----------
    print_str : str
        表示文字列

    Returns
    -------
    str
        入力文字列
    """
    return _input(print_str=print_str, type=str)


def input_min_sec(print_str: str) -> datetime:
    """
    入力時間からdatetimeオブジェクトを出力

    Parameters
    ----------
    print_str : str
        表示文字列

    Returns
    -------
    int
        _description_
    """
    return _input(print_str=print_str, type=datetime)


def _input(
    print_str: str,
    type: Union[int, str, float, datetime],
    over_count: int = 1024,
) -> Union[int, str, float, datetime]:
    """
    コンソール入力処理

    Parameters
    ----------
    print_str : str
        表示文字列
    type : Union[int, str, float, datetime]
        出力タイプ
    over_count : int
        オーバーフロー回数 by default 1024

    Returns
    -------
    Union[int, str, float]
        入力されたデータ

    Raises
    ------
    TypeError
        予期しないタイプ
    OverflowError
        無限ループ対策
    """
    for _ in range(over_count):
        try:
            data: str | int | float = input(print_str + "入力:")
            if type == int:
                data = int(data)
            elif type == float:
                data = float(data)
            elif type == str:
                pass
            elif type == datetime:
                data = datetime.strptime(data, "%M:%S")
            else:
                raise TypeError
            if input(print_str + f":{data}[Yn]:").lower() == "y":
                break
        except ValueError:
            pass
    else:
        raise OverflowError
    return data
