from Game import Game
from RunnerLoop import RunnerLoop


if __name__ == '__main__':
    game = Game() #Make game just for training
    game.Mike.loadModelForMode(True)
    runner = RunnerLoop(game, tick_hz=60)
    print("freal time");
    runner.trainStart()