# backend/app/replay/session.py

class ReplaySession:
    def __init__(self, user_id, symbol, timeframe, start_time):
        self.user_id = user_id
        self.symbol = symbol
        self.timeframe = timeframe

        self.current_time = start_time

        self.speed = 1
        self.playing = False

        self.buffer = []