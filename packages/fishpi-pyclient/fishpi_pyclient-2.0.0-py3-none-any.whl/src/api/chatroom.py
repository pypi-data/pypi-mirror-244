# -*- coding: utf-8 -*-
import json
import random

import requests

from src.api import Base
from src.utils import HOST, UA
from src.utils.version import __version__

from .redpacket import *


class ChatRoomAPI(Base):

    def __init__(self, last_msg_id=None):
        self.last_msg_id = last_msg_id

    def more(self, page: int = 1) -> None | dict:
        if self.api_key == '':
            return None
        resp = requests.get(f"{HOST}/chat-room/more?page={page}",
                            headers={'User-Agent': UA})
        return json.loads(resp.text)

    def send(self, message: str) -> None:
        if self.api_key == '':
            return None
        params = {'apiKey': self.api_key, 'content': message,
                  'client': f'Python/客户端v{__version__}'}
        ret = requests.post(f'{HOST}/chat-room/send',
                            json=params, headers={'User-Agent': UA})
        ret_json = json.loads(ret.text)
        if ('code' in ret_json and ret_json['code'] == -1):
            print(ret_json['msg'])

    def revoke(self, msg_id: str) -> None:
        if self.api_key == '':
            return None
        params = {'apiKey': self.api_key,
                  'client': f'Python/客户端v{__version__}'}
        ret = requests.delete(f'{HOST}/chat-room/revoke/{msg_id}',
                              json=params, headers={'User-Agent': UA})
        ret_json = json.loads(ret.text)
        if ('code' in ret_json and ret_json['code'] == -1):
            print(ret_json["msg"])
        else:
            print('撤回成功')

    def send_redpacket(self, redpacket: RedPacket = RedPacket('最后的发', 128, 5, RedPacketType.RANDOM)) -> None:
        content = f'[redpacket]{json.dumps(redpacket.__json__())}[/redpacket]'
        self.send(content)

    def open_redpacket(self, red_packet_id) -> dict:
        params = {
            'apiKey': self.api_key,
            'oId': red_packet_id
        }
        resp = requests.post(
            f"{HOST}/chat-room/red-packet/open", json=params, headers={'User-Agent': UA})
        return json.loads(resp.text)

    def open_rock_paper_scissors_redpacket(self, red_packet_id, gesture: int = -1) -> dict:
        if gesture not in [0, 1, 2]:
            gesture = random.choice([0, 1, 2])
        params = {
            'apiKey': self.api_key,
            'oId': red_packet_id,
            'gesture': gesture
        }
        resp = requests.post(
            f"{HOST}/chat-room/red-packet/open", json=params, headers={'User-Agent': UA})
        return json.loads(resp.text)
