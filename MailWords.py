try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle
import email
import smtplib
import unidecode

Word_Lists = ["WordsEasy.txt", "WordsMedium.txt", "WordsHard.txt"]
WordsSent = "WordsSent.txt"
WordsPerList = 7 #7 from every word list for every day.
EmailList = ['ss9131@nyu.edu', 'rabailmotihar@gmail.com']

class WordsForTheDay():
    def __init__(self):
        self.words_covered = set()
        self.words_for_the_day = ''
        with open("Words.json", 'rb') as f:
            self.words_objects = pickle.load(f)
        self.TotalCount = 0
        
    
    def parse_words_for_day_helper(self, word_list):
        Count = 0
        TotalCount = 0
        with open(word_list, 'r') as f:
            for word in f:
                self.TotalCount += 1
                if word not in self.words_covered:
                    break
                self.words_covered.add(word)
                Word_Definition = self.words_objects[word.strip()]["Definition"]
                Word_Mnemonics = self.words_objects[word.strip()]["Mnemonic"]
                Word_Sentences = self.words_objects[word.strip()]["Sentences"]
                self.words_for_the_day += "\n\n\n" + str(self.TotalCount) + '. ' + word
                #print(Word_Definition)
                #TODO multiple definitions | Currently a list of only 1 definition. 
                #TODO Synonyms support. 
                self.words_for_the_day += "Definition: " + Word_Definition[0] + '\n'                
                self.words_for_the_day += "\nMnemonics: \n" 
                #print(Word_Sentences)

                for mnemonic_index in range(0, len(Word_Mnemonics)):
                    self.words_for_the_day += str(mnemonic_index+1) + ". " + Word_Mnemonics[mnemonic_index] + '\n'
                self.words_for_the_day += "\nSentences: \n" 
                for sentence_index in range(0, len(Word_Sentences)):
                    self.words_for_the_day += str(sentence_index+1) + ". " + Word_Sentences[sentence_index] + '\n'
                Count += 1
                if Count == WordsPerList:
                    print(unidecode.unidecode(self.words_for_the_day))
                    return 
                    


    def parse_words_for_day(self):
        with open("WordsSent.txt", 'r') as f:
            for word in f:
                self.words_covered.add(word.strip())
        for word_list in Word_Lists:
            self.parse_words_for_day_helper(word_list)
        with open("WordsSent.txt", 'a') as f:
            for word in self.words_covered:
                f.write(word.strip() + '\n')



if __name__ == "__main__":
    Word_Object = WordsForTheDay()
    Word_Object.parse_words_for_day()
    
    msg = email.message_from_string(unidecode.unidecode(Word_Object.words_for_the_day))
    #msg = email.message_from_string("HELLO\n")
    msg['From'] = 'shikhar394@hotmail.com'
    
    msg['Subject'] = 'Words for the day'

    server = smtplib.SMTP("smtp.live.com", 587)
    server.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    server.starttls() #Puts connection to SMTP server in TLS mode
    server.ehlo()
    server.login("email", "pass") #
    for email in EmailList:
        msg['To'] = email
        server.sendmail("senderEmail", email, msg.as_string())
    server.quit()

    