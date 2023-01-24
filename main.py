import random

class Hand:

    def __init__(self, dealer = False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)

    def calculate_value(self):
        self.value = 0
        has_ace = False

        for card in self.cards:
            card_value = int(card.rank["value"])
            self.value += card_value
            if card.rank["rank"] == "A":
                has_ace = True

        if has_ace and self.value > 21:
            self.value -= 10
    
    def get_value(self):
        self.calculate_value()
        return self.value

    def is_blackjack(self):
        return self.get_value() == 21

    def display(self, show_all_dealer_cards = False):

        print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_all_dealer_cards and not self.is_blackjack(): 
                print("hidden")
            else:    
                print(card)

        if not self.dealer: 
            print("Value:", self.get_value())
            print()

class Card: 

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"


class Deck:

    def __init__(self):

        self.cards = []
        suits = ["hearts", "clubs", "diamonds", "spade"] 
        cards = []

        ranks = [
        {"rank": "A", "value": 11},
        {"rank": "2", "value": 2},
        {"rank": "3", "value": 3},
        {"rank": "4", "value": 4},
        {"rank": "5", "value": 5},
        {"rank": "6", "value": 6},
        {"rank": "7", "value": 7},
        {"rank": "8", "value": 8},
        {"rank": "9", "value": 9},
        {"rank": "10", "value": 10},
        {"rank": "J", "value": 10},
        {"rank": "Q", "value": 10},
        {"rank": "K", "value": 10},
        ]

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, num):
        cards_dealt = []
        for x in range(num):
            if len(self.cards) > 0:
                card = self.cards.pop()
                cards_dealt.append(card)    
        return cards_dealt

class Game:

    def play(self):
        game_number = 0
        games_to_play = 0

        while games_to_play <= 0:
            try: 
                games_to_play = int(input("how many gmaes do you want to play"))
            except:
                print("You must enter a number.")

        while game_number < games_to_play:
            game_number += 1

            deck = Deck()
            deck.shuffle()

            players_hand = Hand()
            dealer_hand = Hand(dealer = True)

            for i in range(2):
                players_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            print()
            print("*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            players_hand.display()
            dealer_hand.display()

            if self.check_winner(players_hand, dealer_hand):
                continue

            choice = ""
            while players_hand.get_value() < 21 and choice not in ["s", "stand"]:
                choice = input("Please choose hit or stand").lower()
                print()
                while choice not in ["h", "s", "hit", "stand"]:
                    choice = input("Please enter hit or stand").lower()
                    print()                
                if choice in ["hit", "h"]:
                    players_hand.add_card(deck.deal(1))
                    players_hand.display()
            
            if self.check_winner(players_hand, dealer_hand):
                continue

            players_hand_value = players_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal())
                dealer_hand_value = dealer_hand.get_value()

            dealer_hand.display(show_all_dealer_cards=True)

            if self.check_winner(players_hand, dealer_hand):
                continue

            print("Final Results")
            print("Your hand: ", players_hand_value)
            print("Dealers hand: ", dealer_hand_value)

            self.check_winner(players_hand, dealer_hand, True)

        print("Thanks for playing!")


    def check_winner(self, players_hand, dealer_hand, game_over = False):
        if not game_over:
            if players_hand.get_value() > 21:
                print("You busted. Dealer wins!")
                return True
            elif dealer_hand.get_value() > 21:
                print("Dealer busted. You win")
                return True
            elif dealer_hand.is_blackjack() and players_hand.is_blackjack():
                print("Tie")
                return True
            elif players_hand.is_blackjack():
                print("You have blackjack you win")
                return True
            elif dealer_hand.is_blackjack():
                print("Dealer has blackjack u loose")
                return True
        else:
            if players_hand.get_value() > dealer_hand.get_value():
                print("You win!")
            elif players_hand.get_value() == dealer_hand.get_value():
                print("Tie")
            else:
                print("You loose!")
            return True
        return False

g = Game()  
g.play()