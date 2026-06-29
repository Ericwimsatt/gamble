class gameStats:
    stats = {}
    def __init__(self):
        self.stats ={
            'units_won_total': 0,
            'player_wins': 0,
            'dealer_wins': 0,
            'pushes': 0,
            'dealer_qualifies': 0,
            'play_bet_total': 0,
            'ante_bet_total': 0,
            'player_win_play_bet_total': 0,
            'dealer_win_play_bet_total': 0,
            'push_play_bet_total': 0,
            'blind_payout_total': 0,
            'folds': 0,
            'bad_folds': 0,
            'game_count': 0
        }

    def accumulate(self, new_game_stats):
        for key in self.stats.keys():
            self.stats[key] += new_game_stats.stats[key]

    def set_field(self, field, value):
        self.stats[field] = value
    
    def average_units_won(self):
        if self.stats['game_count'] == 0:
            return 0
        return self.stats['units_won_total'] / self.stats['game_count']
        
    def __str__(self):
        out_str = "Game Stats:\n"
        for key in self.stats.keys():
            out_str += "{}: {}\n".format(key, self.stats[key])
        return out_str

    
    def average_str(self):
        if self.stats['game_count'] == 0:
            return "No games played"
        out_str = "Average Game Stats:\n"
        for key in self.stats.keys():
            out_str += "{}: {}\n".format(key, self.stats[key] / self.stats['game_count'])
        return out_str
