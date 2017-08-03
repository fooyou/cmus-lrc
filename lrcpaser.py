#!/usr/bin/env python
# coding: utf-8
# @File Name: lrcpaser.py
# @Author: Joshua Liu
# @Email: liuchaozhenyu@gmail.com
# @Create Date: 2017-08-02 16:08:20
# @Last Modified: 2017-08-03 11:08:02
# @Description:

import re

def parse(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    lyrics = {}
    re_lyric = re.compile(r'\[\d\d:\d\d.\d\d\]')
    for line in lines:
        line = line.strip()
        matchs = re.findall(re_lyric, line)
        value = re.sub(re_lyric, '', line)
        for match in matchs:
            lyrics[_get_time(match)] = value

    return sorted(lyrics.items(), key=lambda i: i[0])


def _get_time(match):
    minutes = int(match[1:3])
    seconds = int(match[4:6])
    miliseconds = int(match[7:9])
    return minutes * 60 + seconds + miliseconds / 100.0

if __name__ == '__main__':
    print(parse('./sample.lrc'))
