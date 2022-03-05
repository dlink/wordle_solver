
from pprint import pprint

ALL_WORDS = 'all_words'

LETTERS = 'abcdefghijklmnopqrstuvwxyz'

class Solver():

    def __init__(self):
        self.scored_words = {}
        self.scores = []
        self.num_guesses = 0
        self.initializeData()

    def run(self):
        for i in range(0, 10):
            print(self.scores[i], self.scored_words[self.scores[i]])
        print()

        quess = self.makeGuess()
        print(quess)
        
    def makeGuess(self):
        ind = 0
        done = 0
        while not done:
            score = self.scores[ind]
            break_ = 0
            for word in self.scored_words[score]:
                guess = word
                print(done, score, guess, len(set(guess)))
                if self.num_guesses != 0 or len(set(guess)) == 5:
                    done = 1
                    break_ = 1
            if break_:
                break
            ind += 1
        return guess

    def initializeData(self):
        words = self.loadWords()
        print(f'{len(words)} words')

        letter_freqs = self.getFrequency(words)
        print(letter_freqs)

        self.scored_words = self.getWordScores(words, letter_freqs)
        self.scores = sorted(list(self.scored_words.keys()), reverse=True)

    def loadWords(self):
        words = []
        for word in open(ALL_WORDS, 'r').readlines():
            word = word.strip()
            words.append(word)
        return words

    def getFrequency(self, words):
        lfreq = {}
        for letter in LETTERS:
            lfreq[letter] = 0

        for word in words:
            for letter in word:
                lfreq[letter]+=1
        return lfreq

    def getWordScores(self, words, lfreqs):
        scores = {}
        for word in words:
            score = sum([lfreqs[l] for l in word])
            #print(word, word_score)
            if score not in scores:
                scores[score] = []
            scores[score].append(word)
        return scores
    
if __name__ == '__main__':
    Solver().run()


