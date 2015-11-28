# Maybe we should just use a standard logger.
# In theory, we could customize this one if we needed it.

# LEVELS
# 1: reserved
# 2: used for multi-game runs
# 3: used for a single-game run
class Logger:
    def __init__(self, level=3):
        self.level = level

    def log(self, message, level=3):
        if level <= self.level:
            print(message)
