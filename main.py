import random

class Card(object):
    def __init__(self, name, value, suit, symbol):
        self.name = name
        self.value = value
        self.suit = suit
        self.symbol = symbol
        self.showing = False

    def __repr__(self):
        if self.showing:
            return self.symbol
        else: #Hiding deck (facedown) so all cards of deck can't be seen by player
            return "Card"

class Deck (list):
    def __init__(self):
        self.cards = []
        values = {"Two":2,
                  "Three":3,
                  "Four":4,
                  "Five":5,
                  "Six":6,
                  "Seven":7,
                  "Eight":8,
                  "Nine":9,
                  "Ten":10,
                  "Jack":11,
                  "Queen":12,
                  "King":13,
                  "Ace":14}
        suits = {"Hearts":"♥","Diamonds":"♦","Clubs":"♣","Spades":"♠"}

        for name in values:
            for suit in suits:
                symbolIcon = suits[suit]
                if values[name] < 11:
                  symbol = str(values[name]) + symbolIcon
                else:
                  symbol = name[0] + symbolIcon #anything above a Ten will display as the first letter in name
                self.cards.append(Card(name, values[name], suit, symbol))

    def shuffle(self, times=1): 
        random.shuffle(self.cards) 
        print("Deck shuffled")

    def deal(self):
        return self.cards.pop()

    def __repr__(self):
        return "Cards remaining: " + str(len(self.cards))

class Player(object):
    def __init__(self):
        #self.name = name
        self.cards = []

    def cardCount(self):
        return len(self.cards)

    def addCard(self, card):
      self.cards.append(card)
      
    def __repr__(self):
        print(self.cards)

class Scorer(object):
    def __init__(self, cards):
        self.cards = cards

    def suitCount(self): #Gives list of individual suits in player's hand
        suits = [card.suit for card in self.cards]
        return len(set(suits))

    def checkForFive(self):
        return len(self.cards) == 5

    def cardValues(self):
        values = [card.value for card in self.cards]
        return sorted(values)

    def checkIsConsecutive(self): 
        values = self.cardValues()
        return sorted(values) == list(range(min(values), max(values)+1))
    
    #Testing for different hands
    #Highest value hand to lowest value hand
    def royalFlush(self):
        values = self.cardValues()
        if self.flush() and values[0]==10 and values[1]==11 and values[2]==12 and values[3]==13 and values[4]==14:
            return True
        return False
    
    def straightFlush(self):
        if self.straight() and self.flush():
            return True
        return False

    def fourOfAKind(self): 
        values = self.cardValues()
        if (values[0]==values[1]==values[2]==values[3] or 
           values[1]==values[2]==values[3]==values[4]):
            return True
        return False
    
    def fullHouse(self):
        values = self.cardValues()
        if (values[0]==values[1]==values[2] and values[3]==values[4] or
            values[2]==values[3]==values[4] and values[0]==values[1]):
            return True
        return False

    def flush(self):
        if self.suitCount()==1:
            return True
        return False
        
    def straight(self):
        if self.checkForFive() and self.checkIsConsecutive():
            return True
        return False
    
    def threeOfAKind(self):
        values = self.cardValues()
        if (values[0]==values[1]==values[2] or
            values[1]==values[2]==values[3] or
            values[2]==values[3]==values[4]):
            return True
        return False

    def twoPair(self): 
        values = self.cardValues()
        if len(set(values))==3:
            return True
        return False
    
    def pair(self):
        values = self.cardValues()
        if len(set(values)) == 4:
            return True
        return False
    
    def highCard(self):
        values = self.cardValues()
        return values[4]

def play():
  print()
  print("You start with $100 and each hand costs $5 to play.")
  print()
  print()
  player = Player()
  #Initial amount
  dollars = 100
  #Cost per hand
  handCost = 5

  end = False
  while not end:
    dollars -= handCost
    print("You have " + str(dollars) + " dollars" )
    print()
    
    #Create deck
    deck = Deck() #new deck will be created and shuffled after
    deck.shuffle()
    
    #Deal out
    for i in range(5):
      player.addCard(deck.deal())
    
    #Make palyer's hand visible
    for card in player.cards:
      card.showing = True

    print(player.cards)

    validInput = False
    while not validInput:
      print("Which card positions do you want to get rid of? (ie: 1, 2, 3)")
      print("*Just hit return to hold all.")
      inputString = input()
      if inputString=="":
          validInput=True
          break
      try:   
        inputList = [int(inp.strip()) for inp in inputString.split(",")]

        for inp in inputList:
          if inp > 6:
            continue

        for inp in inputList: #replacing cards that were discarded
          player.cards[inp-1] = deck.deal()
          player.cards[inp-1].showing = True
        
        validInput = True
      except:
        print("Input Error: use commas to seperate the cards you want to hold")
        print()
        print(player.cards)
    print()
    print(player.cards)

    #Score
    score = Scorer(player.cards)

    #Royal Flush
    if score.royalFlush():
      print("Royal Flush!!!")
      print("+ $500")
      dollars += 500
    #Straight flush
    elif score.straightFlush():
      print("Straight Flush!")
      print("+ $250")
      dollars += 250
    #4 of a kind
    elif score.fourOfAKind():
      print("Four of a kind!")
      print("+ $100")
      dollars += 100
    #Full house
    elif score.fullHouse():
      print("Full House!")
      print("+ $50")
      dollars += 50 
    #Flush
    elif score.flush():
      print("Flush!")
      print("+ $25")
      dollars += 25
    #Straight
    elif score.straight():
      print("Straight!")
      print("+ $20")
      dollars += 20
    #3 of a kind
    elif score.threeOfAKind():
      print("Three of a kind!")
      print("+ $15")
      dollars += 15
    #2 pair
    elif score.twoPair():
      print("Two pair!")
      print("+ $10")
      dollars += 10
    #pair
    elif score.pair():
      print("Pair!")
      print("+ $5")
      dollars += 5
    #highest card
    elif score.highCard () >= 11:
      print("Jacks or better!")
      print("+ $1")
      dollars += 1
    else:
      print("This is not a good hand :(")

    player.cards = []

    print()
    print()

    if dollars >= 250:
        print("Good job! You were able to make money.")
        end =True
        break
    elif dollars <= 0:
        print("Unfortunately you've lost all your money, you need more practice to learn the poker hands.")
        end =True
        break

play()