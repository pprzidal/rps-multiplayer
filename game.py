

class RockPaperScissors:
    _ROCK = 0 # TODO hide better
    _PAPER = 1
    _SCISSORS = 2

    def __init__(self):
        """
        Sets all the values to default
        :param opponent: Which Opponent to use
        """
        self._player_score = 0
        self._computer_score = 0
        self._playerLast = 0
        self._computerLast = 0
        self._round = 0

    def play(self, players_choice: int, dchoice=-1) -> tuple:
        """
        Play a new game
        :param players_choice: a number betweeen
        :param dchoice: DO NOT TOUCH only for test purpuses
        :return: tuple with current round, player score, computer score, computer last and player's last pick
        """
        self._playerLast = players_choice
        ochoice = self._opponent.choice() if dchoice == -1 else dchoice
        self._computerLast = ochoice
        won = None
        if players_choice - 1 == ochoice or (players_choice == self._ROCK and ochoice == self._SCISSORS):
            self._player_score += 1
            won = "player"
        elif players_choice != ochoice:
            self._computer_score += 1
            won = "computer"
        self._round += 1
        #self._opponent.addToHistory({"player": self.toString(players_choice), "computer": self.toString(ochoice), "won": won if won is not None else "tie"})
        #return self.stats()
        return won

    def reset(self) -> None:
        """
        Resets all the values
        :return: nothing
        """
        self._player_score = 0
        self._computer_score = 0
        self._round = 0

    def stats(self) -> tuple:
        """
        Returns the current stats as a tuple
        :return: tuple with current round, player score, computer score, computer last and player's last pick
        """
        #TODO not so clean i guess
        return (self._round, self._player_score, self._computer_score, self._computerLast, self._playerLast)

    def toString(self, a: int) -> str:
        """
        To map a number to the corresponding string
        :param a: between -1 and 3
        :return: the according String to the number
        """
        return ["Rock", "Paper", "Scissors"][a]

    def toInt(self, message: str) -> int:
        if message == "rock":
            return 0
        elif message == "paper":
            return 1
        elif message == "scissors":
            return 2
        #e = {"rock": 0, "paper": 1, "scissors": 2}
        #print(message + " TO " + e[message])
        return -1


if __name__ == "__main__":
    # Test is kinda shitty
    rps = RockPaperScissors()
    for players_choice in range(3):
        for ochoice in range(3):
            print(f"Player: {rps.toString(players_choice)}, Opponent: {rps.toString(ochoice)}")
            rps.play(players_choice, ochoice)
            if rps._player_score == 1: print("Player won")
            elif rps._computer_score == 1: print("Opponent won")
            else: print("Tie")
            rps.reset()