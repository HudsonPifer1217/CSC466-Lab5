import csv
import re

def parseDolphin(filename):
    nodes = set()
    inlinks = {}
    outlinks = {}

    with open(filename, newline="") as file:
        reader = csv.reader(file)
        
        for row in reader:
            dolphin1 = row[0].strip()
            dolphin2 = row[2].strip()

            add_edge(dolphin1, dolphin2, nodes, outlinks, inlinks)
            add_edge(dolphin2, dolphin1, nodes, outlinks, inlinks)

    return nodes, inlinks, outlinks

def parseLesmis(filename):
    nodes = set()
    inlinks = {}
    outlinks = {}

    with open(filename, newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            characeter1 = row[0].strip()
            characeter2 = row[2].strip()

            add_edge(characeter1, characeter2, nodes, outlinks, inlinks)
            add_edge(characeter2, characeter1, nodes, outlinks, inlinks)

    return nodes, inlinks, outlinks

def parseNCAA(filename):
    nodes = set()
    inlinks = {}
    outlinks = {}

    with open(filename, newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            team1 = row[0].strip()
            score1 = clean_score(row[1].strip())
            
            team2 = row[2].strip()
            score2 = clean_score(row[3].strip())

            if score1 > score2:
                winner = team1
                loser = team2
            elif score2 > score1:
                winner = team2
                loser = team1
            else:
                continue

            add_edge(loser, winner, nodes, outlinks, inlinks)

    return nodes, inlinks, outlinks


def clean_score(score):
    digits = re.sub(r"\D", "", score)
    return int(digits)


def add_edge(source, target, nodes, outlinks, inlinks):
    nodes.add(source)
    nodes.add(target)

    outlinks.setdefault(source, set())
    outlinks.setdefault(target, set())
    inlinks.setdefault(source, set())
    inlinks.setdefault(target, set())

    outlinks[source].add(target)
    inlinks[target].add(source)

if __name__ == "__main__":
    nodesDolphin, inlinksDolphin, outlinksDolphin = parseDolphin("data/dolphinsDir.csv")

    print("Number of nodes:", len(nodesDolphin))

    #for dolphin in outlinksDolphin:
        #print(dolphin, "->", outlinksDolphin[dolphin])

    nodesLesmis, inlinksLesmis, outlinksLesmis = parseLesmis("data/lesmisDir.csv")

    print("Number of nodes:", len(nodesLesmis))

    #for character in outlinksLesmis:
        #print(character, "->", outlinksLesmis[character])

    nodesNCAA, inlinksNCAA, outlinksNCAA = parseNCAA("data/NCAA_football.csv")

    print("Number of nodes:", len(nodesNCAA))

    for team in outlinksNCAA:
        print(team, "->", outlinksNCAA[team])
    