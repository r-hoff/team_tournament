import csv
import random
from time import sleep

sleepVal = 0.5


class Format:
    GREEN = ''
    RED = ''
    BOLD = ''
    UNDERLINE = ''
    END = ''


class Team:
    def __init__(self, city, mascot):
        self.city = city
        self.mascot = mascot
        self.score = 0

    def __repr__(self):
        return f"{self.city} {self.mascot}"


class Match:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.scoreboard = f"{self.team1}: {self.team1.score}, {self.team2}: {self.team2.score}"
        self.winner = None
        self.loser = None

    def __repr__(self):
        return f"{self.team1} vs. {self.team2}"

    def clearScores(self):
        self.team1.score = 0
        self.team2.score = 0

    def simulateDrive(self):
        scores = [0, 3, 7]
        return scores[random.randrange(0, 3)]

    def updateScoreboard(self):
        self.scoreboard = f"{self.team1}: {self.team1.score}, {self.team2}: {self.team2.score}"

    def overtimeRound(self):
        print(Format.BOLD + "Overtime round begins!" + Format.END)

        # add dramatic effect
        sleep(sleepVal)
        print(".", flush=True, end='')
        sleep(sleepVal)
        print(".", flush=True, end='')
        sleep(sleepVal)
        print(". ", flush=True, end='')

        self.team1.score += self.simulateDrive()
        self.team2.score += self.simulateDrive()
        self.updateScoreboard()
        print(self.scoreboard)
        print("")
        if self.team1.score != self.team2.score:
            return False
        return True

    def startMatch(self):

        # play the game
        for qtr in range(4):

            print(f"Qtr {qtr + 1} ", end='')
            # add dramatic effect
            sleep(sleepVal)
            print(".", flush=True, end='')
            sleep(sleepVal)
            print(".", flush=True, end='')
            sleep(sleepVal)
            print(".", flush=True, end='')
            sleep(sleepVal)
            print(".", flush=True, end='')
            sleep(sleepVal)
            print(". ", flush=True, end='')

            for drive in range(1):
                self.team1.score += self.simulateDrive()
                self.team2.score += self.simulateDrive()
            self.updateScoreboard()
            print(self.scoreboard)
        print("\nEnd of regulation.\n")

        if self.team1.score == self.team2.score:
            while self.team1.score == self.team2.score:
                self.overtimeRound()

        print(Format.UNDERLINE + "Final Score:" + Format.END +
              Format.BOLD + f"\n{self.team1}: {self.team1.score}\n{self.team2}: {self.team2.score}\n" + Format.END)

        # return winner
        if self.team1.score > self.team2.score:
            self.clearScores()
            self.winner = self.team1
            self.loser = self.team2
            return
        self.clearScores()
        self.winner = self.team2
        self.loser = self.team1
        return


class Tournament:
    def __init__(self, block1=None, block2=None):
        self.teams = []
        self.availableTeams = []
        self.matches = []
        self.isOver = False
        self.winner = None

        with open('teams.csv', newline='') as file:
            rows = csv.reader(file, delimiter=',')
            for row in rows:
                if block1 is None and block2 is None:
                    self.teams.append(Team(row[0], row[1]))
                elif block1 is not None:
                    if row[1].lower() != block1.lower():
                        if block2 is not None:
                            if row[1].lower() != block2.lower():
                                self.teams.append(Team(row[0], row[1]))
            self.availableTeams = self.teams.copy()

    def getRandomTeam(self):
        return self.availableTeams.pop(random.randrange(0, len(self.availableTeams)))

    def generateMatches(self):
        self.matches.clear()
        matchNum = int(len(self.availableTeams) / 2)
        for match in range(matchNum):
            current = Match(self.getRandomTeam(), self.getRandomTeam())
            current.clearScores()
            self.matches.append(current)

    def setWinner(self, team):
        self.winner = team

    def startRound(self):
        i = 1
        for match in self.matches:
            print(Format.UNDERLINE + f"Match {i}: {match.team1} vs {match.team2}" + Format.END + "\n")
            match.startMatch()
            winner = match.winner
            loser = match.loser
            print(Format.GREEN + f"The winner is the {winner}!" + Format.END)
            print(Format.RED + f"The {loser} have been eliminated.\n" + Format.END)
            self.availableTeams.append(winner)
            i += 1
            input("Press enter to continue\n")
        if len(self.availableTeams) == 1:
            self.isOver = True
            self.setWinner(winner)


def main(block1=None, block2=None):
    tourney = Tournament(block1, block2)
    i = 1
    while not tourney.isOver:
        tourney.generateMatches()

        print("\n" + Format.UNDERLINE + f"Round {i} Matchups:" + Format.END + "\n")
        for match in range(len(tourney.matches)):
            print(f"Match {match + 1}:\t" + str(tourney.matches[match]))
        input(f"\nPress enter to begin round {i}")
        print("")
        tourney.startRound()
        i += 1

    print(Format.BOLD + f"\nYour new team is the {tourney.winner}!" + Format.END)


if __name__ == '__main__':

    teams = ["Cardinals","Falcons","Ravens","Bills","Panthers","Bears","Bengals","Browns","Cowboys",
             "Broncos","Lions","Packers","Texans","Colts","Jaguars","Chiefs","Raiders","Chargers",
             "Rams","Dolphins","Vikings","Patriots","Saints","Giants","Jets","Eagles","Steelers",
             "49ers","Seahawks","Buccaneers","Titans","Commanders"]

    import sys
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "-f":
            Format.GREEN = '\033[92m'
            Format.RED = '\033[91m'
            Format.BOLD = '\033[1m'
            Format.UNDERLINE = '\033[4m'
            Format.END = '\033[0m'

    block1 = None
    block2 = None

    block = input("Block two teams (y/n)? ")
    if block == "y":
        print("\nEnter blocks (team name without city, ex: seahawks)")
        while block1 is None:
            team = input("First block: ")
            if team.title() not in teams:
                team = input("Team not found, try again: ")
            block1 = team
        while block2 is None:
            team = input("Second block: ")
            if team.title() not in teams:
                team = input("Team not found, try again: ")
            block2 = team

    main(block1, block2)
