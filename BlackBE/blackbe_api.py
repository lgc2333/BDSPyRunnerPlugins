import traceback
from typing import Optional, List, Union

import pkghelper

while True:
    try:
        from pydantic import BaseModel
        import requests
    except:
        print('[BlackBEAPI] 未发现所需第三方库，正在通过PkgHelper自动安装')
        pkghelper.install('pydantic')
        pkghelper.install('requests')
    else:
        break


class BlackBEReturnDataInfo(BaseModel):
    uuid: Optional[str]
    name: Optional[str]
    black_id: Optional[str]
    xuid: Optional[str]
    info: Optional[str]
    level: Optional[int]
    qq: Optional[int]


class BlackBEReturnData(BaseModel):
    exist: bool
    info: List[Optional[BlackBEReturnDataInfo]]


class BlackBEReturn(BaseModel):
    success: bool
    status: int
    message: str
    version: str
    codename: str
    time: str
    data: Union[BlackBEReturnData, List[None]]


def get_simple_info(token='', **kwargs):
    headers = {}
    if token:
        headers = {'Authorization': f'Bearer {token}'}
    try:
        with requests.session() as s:
            ret = s.get('https://api.blackbe.xyz/openapi/v3/check',
                        params=kwargs, headers=headers).json()
        return BlackBEReturn(**ret)
    except:
        exc = traceback.format_exc()
        print(f'[BlackBEAPI] 访问接口出现错误\n{exc}')
        return exc


__version__ = '3.0.0'
