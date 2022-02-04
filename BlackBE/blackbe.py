# coding=utf-8
import json
import os.path
import threading

import mc
from blackbe_api import *

default_conf = {
    'token': '',
    'kick_message': '§c你TNND之前作过案上云黑了还想进服？'
}
conf = {}


def event_listener(event: str):
    """设置监听器的装饰器函数"""

    def function(func):
        mc.setListener(event, func)
        return func

    return function


def command_listener(cmd: str, desc: str):
    """设置指令监听器的装饰器函数"""

    def function(func):
        mc.registerCommand(cmd, func, desc)
        return func

    return function


def logout(txt):
    print(f'[BlackBE] {txt}')


def tellraw(content: str, target='@a'):
    json_txt = json.dumps({'rawtext': [{'text': content}]})
    mc.runCommand(f'tellraw {target} {json_txt}')


def get_conf(key):
    value = conf.get(key)
    if not value:
        value = default_conf[key]
        logout(f'配置文件中未发现键 "{key}" ，使用默认值')
    return value


def parse_lvl(lvl: int):
    if lvl == 1:
        msg = '有作弊行为，但未对其他玩家造成实质上损害'
        color = 'e'
    elif lvl == 2:
        msg = '有作弊行为，且对玩家造成一定的损害'
        color = '6'
    elif lvl == 3:
        msg = '严重破坏服务器，对玩家和服务器造成较大的损害'
        color = 'c'
    else:
        msg = '未知'
        color = 'r'
    return f'§{color}等级§l {lvl} §r§{color}（{msg}）'


def parse_info(info: BlackBEReturnDataInfo):
    return (f'§2玩家ID§r：§l§d{info.name}§r\n'
            f'§2危险等级§r：{parse_lvl(info.level)}\n'
            f'§2记录原因§r：§b{info.info}\n'
            f'§2XUID§r：§b{info.xuid}\n'
            f'§2库来源§r：§b{info.black_id}\n'
            f'§2记录UUID§r：§b{info.uuid}\n'
            f'§2玩家QQ§r：§b{info.qq}')


def send_arg_empty_tip(player: mc.Entity):
    player.sendText('§c指令格式：/blackbe <XboxID/QQ号/XUID>\n'
                    '§6请谨慎使用XUID查询：由于历史遗留和XUID采集本身存在难度，导致大部分条目没有记录XUID，'
                    '所以不推荐依赖XUID来判断玩家是否存在于黑名单', 0)


def thread_player_join(player: mc.Entity):
    ret = get_simple_info(get_conf('token'), name=player.getName(), xuid=player.getXuid())
    if isinstance(ret, BlackBEReturn):
        if ret.data.exist:
            player.disconnect(get_conf('kick_message'))
            tellraw(f'§6[BlackBE] §c发现尝试进服的玩家 §l§a{player.getName()} §r§c存在违规记录\n'
                    f'§l已将该玩家踢出游戏！\n'
                    f'§r§2-=-=-=详细信息=-=-=-\n'
                    f'{parse_info(ret.data.info[0])}')
            logout(f'玩家 {player.getName()} 存在BlackBE云黑记录，已踢出并全服通报\n'
                   f'库来源：{ret.data.info[0].black_id}')


def thread_get_blacklist_and_send_form(player: mc.Entity, query: str):
    ret = get_simple_info(get_conf('token'), name=query, qq=query, xuid=query)
    if isinstance(ret, BlackBEReturn):
        if ret.success:
            if ret.data.exist:
                li = ret.data.info
                tmp_li = [f'§a为您查询到关于 §l§2{query} §r§a的 §l§e{len(li)} §r§a条相关记录：']
                for i in li:
                    tmp_li.append('§r-=-=-=-=-=-=-=-=-=-=-=-=-=-')
                    tmp_li.append(parse_info(i))
                form_text = '\n'.join(tmp_li)
            else:
                form_text = (f'§a未查询到 §l§b{query} §r§a的记录§r：'
                             f'[§6{ret.status}§r] §d{ret.message}')
        else:
            form_text = f'§c查询失败：§r[§6{ret.status}§r] §d{ret.message}'
    else:
        form_text = f'§c抱歉，查询时发生错误：\n{ret}'
    player.sendCustomForm(json.dumps({
        "content": [{"type": "label", "text": form_text}],
        "type": "custom_form", "title": "§bBlackBE §a查询结果"
    }), lambda _, __: None)


@command_listener('blackbe', '查询玩家BlackBE违规记录')
def cmd_blackbe(player: mc.Entity):
    send_arg_empty_tip(player)


@event_listener('onJoin')
def onJoin(data):
    """
    玩家加入服务器监听

    为什么不用onPreJoin？ 因为用onPreJoin时无法显示踢出信息
    """
    player = data["Player"]
    threading.Thread(
        target=thread_player_join, args=(player,)
    ).start()


@event_listener('onPlayerCmd')
def onPlayerCmd(data):
    """
    玩家输入指令监听
    """
    player: mc.Entity = data["Player"]
    command: str = data["Command"]

    if command.startswith('blackbe '):
        arg = command.replace('blackbe ', '', 1).strip()
        if arg.startswith('"') and arg.endswith('"'):
            arg = arg[1:-1]

        if arg:
            threading.Thread(
                target=thread_get_blacklist_and_send_form, args=(player, arg)
            ).start()
        else:
            send_arg_empty_tip(player)

        return False  # 拦截此事件


def startup():
    global conf
    path = os.path.split(__file__)[0] + '/blackbe.json'
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(default_conf, f)
            conf = default_conf
        logout(f'未发现配置文件，自动创建 {path}')
    else:
        with open(path, encoding='utf-8') as f:
            conf = json.load(f)
        logout(f'已读取配置文件 {path}')


startup()
logout('插件加载完毕 插件编写：student_2333 BlackBE站长：Nyan-Cat\n'
       '赞助链接：https://afdian.net/@BlackBE')

__version__ = '3.0.0'
