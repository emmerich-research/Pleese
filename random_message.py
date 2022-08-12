import random

class Reminder:
    def __init__(self):
        self.languages = []
        self.shortkeys = []
        self.messages = {}
        self.index = 0
        
        with open("messages/conf.txt", 'r') as f:
            msg = f.read().split('\n')[:-1]
            for confs in msg:
                conf = confs.split('-')
                self.languages.append(conf[0])
                self.shortkeys.append(conf[1])

        for lang in self.languages:
            key = self.shortkeys[self.languages.index(lang)]
            with open(f"messages/message-{lang}.txt", 'r') as f:
                msg = f.read().split('\n')[:-1]
                self.messages[key] = msg

    def getMessage(self, lang, index):
        return self.messages[lang][index]
    
    def getAllMessage(self, lang):
        return self.messages[lang]
    
    def getRandom(self, lang):
        return random.choice(self.messages[lang])
    
    def getRandomIndexed(self, lang):
        return self.getMessage(lang, self.index)

    def randomIndex(self):
        self.index = random.randint(0,2)

    def getAvailable(self):
        return self.languages


if __name__ == "__main__":
    rem = Reminder()
    choosen = input("which language:")
    if choosen in rem.getAvailable():
        choosen = rem.shortkeys[rem.languages.index(choosen)]
        for message in rem.getAllMessage(choosen):
            print(message)
