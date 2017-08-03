#!/usr/bin/env python
# coding: utf-8
# @File Name: lrcplayer.py
# @Author: Joshua Liu
# @Email: liuchaozhenyu@gmail.com
# @Create Date: 2017-08-03 10:08:10
# @Last Modified: 2017-08-03 15:08:21
# @Description:
import os
import time
import curses
from curses.textpad import Textbox
from threading import Timer

class Player:

    def __init__(self, lyrics, mode='default'):
        self.lyrics = lyrics
        self.mode = mode
        self.current = 0
        self.win = None
        self.timer = Timer(10, self._tick)
        self.timer.start()
        curses.wrapper(self.show)

    def _tick(self):
        if not self.win:
            return
        text = os.popen('cmus-remote -Q').read()
        position, title, artist, album = self._parse_cmus(text)
        for i, (k, _) in enumerate(self.lyrics):
            if k > position:
                self.scroll(self.win, i)
                break

    def _parse_cmus(self, text):
        '''
        status playing
        file /Users/liuchaozhen/Downloads/海阔天空_beyond h 黄家驹 .mp3
        duration 328
        position 61
        tag artist Beyond
        tag album 海阔天空
        tag title 海阔天空
        tag date 1993-09-01
        tag tracknumber 0
        '''
        position = 0
        album = ''
        artist = ''
        title = ''
        lines = text.split('\n')
        for line in lines:
            if 'position' in line:
                position = int(line.split(' ')[1])
            elif 'tag artist' in line:
                artist = line.split(' ')[2]
            elif 'tag album' in line:
                album = line.split(' ')[2]
            elif 'tag title' in line:
                title = line.split(' ')[2]

        return position, title, artist, album

    def show(self, screen):
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        h, w = screen.getmaxyx()
        win = curses.newwin(h, w, 0, 0)
        self.win = win
        textbox = Textbox(win)
        self.scroll(win, 0)
        while True:
            ch = win.getch()
            if ord('q') == ch:
                break
            elif curses.KEY_UP == ch:
                self.scroll(win, 0)
            elif curses.KEY_DOWN == ch:
                self.scroll(win, 0)
            elif curses.KEY_RESIZE == ch:
                self.scroll(win, 0)

    def scroll(self, win, cur):
        '''
        @param cur: 当前播放的行数，相对于 self.lyrics
        '''
        if cur < len(self.lyrics) and cur >= 0:
            self.current = cur
        else:
            return

        if cur == self.current and cur != 0:
            return

        win.clear()
        h, w = win.getmaxyx()
        begin = self.current - int(h * 0.4)

        try:
            for i in range(0, h):
                if i + begin < 0 or i + begin > len(self.lyrics) - 1:
                    win.addstr(i, 0, '')
                else:
                    k, v = self.lyrics[i + begin]
                    if i + begin == self.current:
                        win.addstr(i, (w-len(v))//2, v, curses.color_pair(6))
                    else:
                        win.addstr(i, (w-len(v))//2, v)
            win.refresh()
        except Exception as e:
            pass


if __name__ == '__main__':
    import lrcpaser
    player = Player(lrcpaser.parse('./sample.lrc'))

