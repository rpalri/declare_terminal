#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import itertools
import random

vals = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
suits = ['spades', 'clubs', 'hearts', 'diamonds']

orig_deck = [list(tup) for tup in itertools.product(vals, suits)]
deck = orig_deck[:]

player_count = int(input("Enter the number of players: "))
game_count = int(input("Enter the number of games you want to play: "))


# In[ ]:


def shuffle_deck(deck):
    random.shuffle(deck)
    return deck


# In[ ]:


def player_names(player_count):
    players = {}
    for i in range(player_count):
        players.update({input("Enter name of Player {}: ".format(str(i+1))) : []})
    names = list(players.keys())
    
    game_points = {}
    for i in players:
        game_points.update({i : int()})
    
    return names, players, game_points


# In[ ]:


def deal_cards(player_count, players, deck):
    dead_deck = []
    for p in players:
        players.update({p : []})
    for i in range(4):
        for j in players:
            players[j].append(deck[0])
            deck.pop(0)
            players[j].sort()
    return deck, players


# In[ ]:


def open_game(start_player, deck, players, names):
    open_cards = []
    for i in range(2):
        print((i+1), "=", deck[0])
        open_cards.append(deck[0])
        deck.pop(0)
    print("\n\n{}'s turn".format(names[start_player]))
    joker_select = int(input("Pick a Joker from the above two cards (Press 1 or 2 to select the card): "))
    joker = open_cards[joker_select-1]
    open_cards.pop(joker_select-1)
    top_card = open_cards[0]
    print("\n\nJoker for the game is:", joker[0])
    print("Top card is:", top_card)
    return joker, top_card, deck

#joker, top_card = open_game()


# In[ ]:


def calc_points(joker, players):
    points = {}
    for i in players:
        points.update({i : int()})
    card_point = {'ace' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, '10' : 10, 'jack' : 10, 'queen' : 10, 'king' : 10}
    card_point.update({joker[0] : 0})
    for i in players:
        for j in players[i]:
            points[i] += card_point[j[0]]
    return points


# In[ ]:


def same_cards(play_card, players, player, names):
    same = []
    face = players[names[player]][play_card-1][0]
    for i in range(len(players[names[player]])):
        if players[names[player]][i][0] == str(face):
            same.append(players[names[player]][i])
    for j in range(len(same)):
        players[names[player]].remove(same[j])
    return same, players


# In[ ]:


def display_hand(players, names, player):
    print("Cards in {}'s hand:".format(names[player]))
    for card in range(len(players[names[player]])):
        print((card+1), "=", players[names[player]][card])


# In[ ]:


def declare(points, player, names):
    for i in names:
        if points[i] < points[names[player]]:
            print("{} has less points than {}. You lose! BAD DECLARE!!".format(i, names[player]))
            input("Press Enter to continue...")
            return i
    return player


# In[ ]:


def round_points(result, player, points, players, game_points, names):
    if result == player:
        for i in players:
            if i != names[player]:
                game_points[i] += points[i]
        game_points[names[player]] += 0
        print("\n\n**********\n{} won the round!\n**********\nWHAT A DECLARE!!\n**********".format(names[player]))
        input("Press Enter to continue...")
        return game_points
    else:
        for i in players:
            game_points[i] += 0
        game_points[names[player]] += sum(points.values())
        return game_points


# In[ ]:


def disp_game_points(game, players, game_points):
    print("\n\nTally after Round {}:".format(game+1))
    for i in players:
        print("{} has {} points".format(i, game_points[i]))
    input("Press Enter to continue...")

def rotate(lst, x=1):
    lst[:] =  lst[-x:] + lst[:-x]
    return lst
# In[ ]:


def game_play(game_count=game_count, orig_deck=orig_deck, player_count=player_count):
    names, players, game_points = player_names(player_count)
    #start_player = -1
    for game in range(game_count):
        deck = orig_deck[:]
        deck = shuffle_deck(deck)
        deck, players = deal_cards(player_count, players, deck)
        print("\n\nRound {}".format(game+1))
        joker, top_card, deck = open_game(-1, deck, players, names)
        declare_decision = ""
        while declare_decision != "Y":
            for player in range(player_count):
                print("\n\n{}'s turn".format(names[player]))
                points = calc_points(joker, players)
                print("You have {} points.".format(points[names[player]]))
                display_hand(players, names, player)
                print("Top card is:", top_card)
                if points[names[player]] < 10:
                    declare_decision = input("You have {} points. You are eligible to Declare. Do you want to Declare? [Y/N]\n".format(points[names[player]])).upper()
                    if declare_decision == "Y":
                        print("{} declared...".format(names[player]))
                        result = declare(points, player, names)
                        game_points = round_points(result, player, points, players, game_points, names)
                        break
                play_card = int(input("Select a card to play from the cards in your hand: "))
                temp_card, players = same_cards(play_card, players, player, names)
                pick = int(input("What would you like to pick?\n1 = A card from the deck\n2 = the top card {}\n".format(top_card)))
                if pick == 1:
                    players[names[player]].append(deck[0])
                    deck.pop(0)
                elif pick == 2:
                    players[names[player]].append(top_card)
                if len(temp_card) > 1:
                    top_card = temp_card[0]
                else:
                    top_card = temp_card[0]
        print("\n\nFinal hands:\n")
        for player in range(player_count):
            display_hand(players, names, player)
        input("Press Enter to continue...")
        disp_game_points(game, players, game_points)
        names = rotate(names)
        #start_player += 1
    print("\n\nGAME OVER\n\nFinal Tally:")
    for i in players:
        print("{} has {} points".format(i, game_points[i]))
    print("\n\n!!!!!!!!!!\n**********\n\n{}\nWON THE GAME\n\n**********\n\n!!!!!!!!!!".format(min(game_points, key=game_points.get)))


# In[ ]:


game_play()


# In[ ]:





# In[ ]:




