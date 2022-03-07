# Wordle Solver

ALL_WORDS_FILE = 'all_words'
LETTERS = 'abcdefghijklmnopqrstuvwxyz'
DEBUG = 0

class Solver():

    def __init__(self):
        self.scored_words = {}
        self.scores = []
        self.num_guesses = 0
        self.score_ind = -1

        self.clues = {'matches': [],
                      'hits': [],
                      'misses': []}

        self.initializeData()

    def run(self):
        '''Solve a wordle puzzle.
           Make guesses, request clues based on guesses
           until it guesses the word.
        '''
        # show score_words in order
        #for score in self.scores:
        #    print(score, self.scored_words[score])

        guesses = []
        done = 0
        while not done:
            guess = self.makeGuess()
            guesses.append(guess)
            print(f'\nGuess {self.num_guesses}: {guess}')
            while 1:
                response = input('Correct (C)? or new clues? ')
                if(self.responseValid(response)):
                   break
            if response.lower() == 'c':
                print('Solved!')
                done = 1
                break
            self.updateClues(guess, response)
        print(guess)

    def makeGuess(self):
        '''Run through the words in score order and
           Return the first one that satifies all known clues
        '''
        found = 0
        while not found:
            self.score_ind += 1
            score = self.scores[self.score_ind]
            for guess in self.scored_words[score]:
                if DEBUG:
                    print(score, guess, len(set(guess)))

                # eliminations

                # repeat letters on first guess
                if self.num_guesses == 0 and len(set(guess)) != 5:
                    if DEBUG:
                        print('   repeat letters on first guess')
                    break

                # must use letter matches
                mismatch = 0
                for match in self.clues['matches']:
                    m = match[0]
                    p = int(match[1])-1
                    if guess[p] != m:
                        mismatch = 1
                        if DEBUG:
                            print('   must use letter matches')
                        break
                if mismatch:
                    break

                # must use letter hits
                non_hit = 0
                hit_same_spot = 0
                for hit in self.clues['hits']:
                    h = hit[0]
                    p = int(hit[1])-1
                    if guess[p] == h:
                        hit_same_spot = 1
                        if DEBUG:
                            print('   hit same spot')
                        break
                    frag = guess[0:p] + guess[p+1:]
                    if h not in frag:
                        non_hit = 1
                        if DEBUG:
                            print('   has non hit letter')
                        break
                if hit_same_spot or non_hit:
                    break

                # do not use letter misses
                has_misses = 0
                for l in guess:
                    if l in self.clues['misses']:
                        has_misses = 1
                        if DEBUG:
                            print('   has letter misses')
                        break
                if has_misses:
                    break

                # guess looks good:
                found = 1
                break

        self.num_guesses += 1
        return guess

    def responseValid(self, response):
        '''User resonse should be 'C' for correct or
           A five digit number of 0s,1s, or 2s only
        '''
        if response.lower() == 'c':
            return 1

        if len(response) != 5:
            return 0

        # only contains 0, 1, or 2
        for c in response:
            if c not in ['0','1','2']:
                return 0
        return 1

    def updateClues(self, guess, response):
        '''Convert response hints (0s,1s, and 2s)
           in to clues and add them to our clue structure

           clues = {0: [<letter_n>, ...],
                    1: [<letter_n><position_n>, ...],
                    2: [<letter_n><position_n>, ...]}

           Example:

              clues = { 0: ['a'],   # no 'a's
                        1: ['t1'],  # there is a 't' but not in position 1
                        2: ['s2']}  # there is an 's' in position 1

           Positions are start at 1 (not 0)
        '''
        for i, c in enumerate(response):
            if c == '2':
                self.clues['matches'].append(guess[i] + str(i+1))
            elif c == '1':
                self.clues['hits'].append(guess[i] + str(i+1))

        # separate loop after we've collected all matches
        for i, c in enumerate(response):
            if c == '0':
                match_letters = [a[0] for a in self.clues['matches']]
                hit_letters = [a[0] for a in self.clues['hits']]
                if guess[i] not in match_letters and\
                   guess[i] not in hit_letters:
                    self.clues['misses'].append(guess[i])

        if DEBUG:
            print('clues:', self.clues)
            pause = input('pause.')

    # Initialization Code ----------------

    def initializeData(self):
        '''Create a dict self.scored_words as {score: list of word}

           { 23060: ['esses'],
             22474: ['asses'],
             22414: ['eases'],
             21334: ['erses', 'seers', 'seres'],
             21274: ['resee'],
             21112: ['sises'],
             21052: ['seise'],
             20864: ['leses', 'seels'],
             20814: ['oases'],
             ...
           }

           The score is calculated as the sum of each of a words
           letter's letter_frequency_score
        '''

        words = self.loadWords()
        print(f'{len(words)} words in repository')

        letter_freqs = self.getFrequency(words)
        #print(letter_freqs)

        self.scored_words = self.getWordScores(words, letter_freqs)
        self.scores = sorted(list(self.scored_words.keys()), reverse=True)

    def loadWords(self):
        '''Read words from file'''
        words = []
        for word in open(ALL_WORDS_FILE, 'r').readlines():
            word = word.strip()
            words.append(word)
        return words

    def getFrequency(self, words):
        '''Return dict letter_frequency as {letter: score}
             where score is number of times that letter shows
             up in the list of words
        '''
        lfreq = {}
        for letter in LETTERS:
            lfreq[letter] = 0

        for word in words:
            for letter in word:
                lfreq[letter]+=1
        return lfreq

    def getWordScores(self, words, lfreqs):
        '''Give a list of words and the letter_requencey dict
           return a dict scores of the form {score: word_list}
        '''
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
