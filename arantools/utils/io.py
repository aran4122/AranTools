import json
import os
import os.path as osp
import pickle
from typing import Any, List, Optional, Union

import cv2
import numpy as np
import yaml


def prepare_input_path(input_path: str, is_dir: bool = False) -> str:
    """准备输入路径.

    Args:
        input_path (str): 输入路径.
        is_dir (bool, optional): 输入路径是否是目录. 默认为False.

    Returns:
        str: 输入路径的绝对路径.
    """
    input_path = osp.realpath(input_path)
    assert osp.exists(input_path), f"{input_path} not exsits"
    if is_dir:
        assert osp.isdir(input_path), f"{input_path} is not a directory"
    else:
        assert osp.isfile(input_path), f"{input_path} is not a file"
    return input_path


def prepare_output_path(output_path: str) -> str:
    """准备输出路径.

    Args:
        output_path (str): 输出路径.

    Returns:
        str: 输出路径的绝对路径.
    """
    output_path = osp.realpath(output_path)
    os.makedirs(osp.dirname(output_path), exist_ok=True)
    return output_path


def read_list(
    input_path: str, strip: bool = True, delimiter: Optional[str] = None
) -> Union[List[str], List[List[str]]]:
    """读入list文件.

    Args:
        input_path (str): 输入文件路径.
        strip (bool, optional): 是否删除每行中多余的空白符. 默认为True.
        delimiter (Optional[str], optional): 行分割间隔符.
            若不为None, 则每行内容再根据该值分割为一个list. 默认为None.

    Returns:
        Union[List[str], List[List[str]]]: 读入结果.
            若delimiter为None, 输出格式为List[str]; 否则为List[List[str]].
    """
    input_path = prepare_input_path(input_path)
    with open(input_path) as f:
        ret = f.readlines()
    if strip:
        ret = [line.strip() for line in ret]
    if delimiter is not None:
        ret = [line.split(delimiter) for line in ret]
    return ret


def write_list(contents: Union[Any, List[Any]], output_path: str):
    """写入list文件.

    Args:
        contents (List[Any]): 写入内容. 若不是list, 会被转换为list.
        output_path (str): 输出文件路径.
    """
    output_path = prepare_output_path(output_path)
    if not isinstance(contents, list):
        contents = [contents]
    with open(output_path, "w") as f:
        f.writelines([f"{line}\n" for line in contents])


def read_json(input_path: str) -> Any:
    """读入json文件.

    Args:
        input_path (str): 输入文件路径.

    Returns:
        Any: 读入结果.
    """
    input_path = prepare_input_path(input_path)
    with open(input_path) as f:
        ret = json.load(f)
    return ret


def write_json(contents: Any, output_path: str, indent: Union[int, str, None] = 2):
    """写入json文件.

    Args:
        contents (Any): 写入内容.
        output_path (str): 输出文件路径.
        indent (Union[int, str, None], optional): 缩进. 默认为2.
    """
    output_path = prepare_output_path(output_path)
    with open(output_path, "w") as f:
        json.dump(contents, f, indent=indent)


def read_yaml(input_path: str) -> Any:
    """读入yaml文件.

    Args:
        input_path (str): 输入文件路径.

    Returns:
        Any: 读入结果.
    """
    input_path = prepare_input_path(input_path)
    with open(input_path) as f:
        ret = yaml.load(f, Loader=yaml.FullLoader)
    return ret


def write_yaml(contents: Any, output_path: str, indent: int = 2):
    """写入yaml文件.

    Args:
        contents (Any): 写入内容.
        output_path (str): 输出文件路径.
        indent (int, optional): 缩进. 默认为2.
    """
    output_path = prepare_output_path(output_path)
    with open(output_path, "w") as f:
        yaml.dump(contents, f, indent=indent)


def read_pickle(input_path: str) -> Any:
    """读入pickle文件.

    Args:
        input_path (str): 输入文件路径.

    Returns:
        Any: 读入结果.
    """
    input_path = prepare_input_path(input_path)
    with open(input_path, "rb") as f:
        ret = pickle.load(f)
    return ret


def write_pickle(contents: Any, output_path: str):
    """写入pickle文件.

    Args:
        contents (Any): 写入内容.
        output_path (str): 输出文件路径.
    """
    output_path = prepare_output_path(output_path)
    with open(output_path, "w") as f:
        pickle.dump(contents, f)


def read_image(input_path: str, unchanged: bool = False) -> np.ndarray:
    """读入图片文件.

    Args:
        input_path (str): 输入文件路径.
        unchanged (bool, optional): 是否使用cv2.IMREAD_UNCHANGED. 默认为False.

    Returns:
        np.ndarray: 读入结果.
    """
    input_path = prepare_input_path(input_path)
    if unchanged:
        ret = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    else:
        ret = cv2.imread(input_path)
    return ret


def write_image(contents: np.ndarray, output_path: str):
    """写入pickle文件.

    Args:
        contents (np.ndarray): 写入内容.
        output_path (str): 输出文件路径.
    """
    output_path = prepare_output_path(output_path)
    cv2.imwrite(output_path, contents)
