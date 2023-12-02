from scuttlebuddy import LeagueReader
import time

lr: LeagueReader = LeagueReader()

while 1:
    print(lr.local_player.game_pos)
    time.sleep(0.5)