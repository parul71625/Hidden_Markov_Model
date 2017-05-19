import sys

class HMMlearn:

    TransProbDict = {}
    EmissionProbDict = {}
    WordTagDict = {}
    ListOfTags = []


    def createListOfTags(self, trainingFile):
        with open(trainingFile, "r", encoding="utf8") as file:
            for line in file:
                line = line.rstrip()
                wordsWithTag = line.split(' ')
                start = 1
                for pair in wordsWithTag:
                    word_tag = pair.rsplit('/', 1)
                    word = word_tag[0]
                    tag = word_tag[1]

                    if tag not in self.ListOfTags:
                        self.ListOfTags.append(tag)



    def readTrainFile(self, trainingFile):

        self.createListOfTags(trainingFile)
        #print(len(self.ListOfTags))


        with open(trainingFile, "r", encoding="utf8") as file:
            for line in file:
                line = line.rstrip()
                wordsWithTag = line.split(' ')
                start = 1
                for pair in wordsWithTag:
                    word_tag = pair.rsplit('/', 1)
                    word = word_tag[0]
                    tag = word_tag[1]

                    #Transition Probabilities
                    if start == 1:
                        prevTag = "q0"

                    if prevTag in self.TransProbDict.keys():
                        dictOfSuccTags = self.TransProbDict[prevTag]
                        if tag in dictOfSuccTags.keys():
                            dictOfSuccTags[tag] = dictOfSuccTags[tag] + 1
                        else:
                            dictOfSuccTags[tag] = 1
                    else:
                        dictOfSuccTags = {}
                        dictOfSuccTags[tag] = 1
                        self.TransProbDict[prevTag] = dictOfSuccTags
                    prevTag = tag
                    start = 0


                    #Emission Probabilities
                    if tag in self.EmissionProbDict.keys():
                        dictOfWords = self.EmissionProbDict[tag]
                        if word in dictOfWords.keys():
                            dictOfWords[word] = dictOfWords[word] + 1
                        else:
                            dictOfWords[word] = 1
                        self.EmissionProbDict[tag] = dictOfWords
                    else:
                        dictOfWords = {}
                        dictOfWords[word] = 1
                        self.EmissionProbDict[tag] = dictOfWords


                    #TagsRelatedToWords
                    if word in self.WordTagDict:
                        listOfTags = self.WordTagDict[word]
                        if tag not in listOfTags:
                            listOfTags.append(tag)
                    else:
                        listOfTags = [tag]
                        self.WordTagDict[word] = listOfTags

            #print(self.TransProbDict)
            #print(self.EmissionProbDict)

            self.applySmoothing()

            for masterTag in self.TransProbDict.keys():
                dictOfTags = self.TransProbDict[masterTag]
                sum = 0
                for eachTag in dictOfTags:
                    sum = sum + dictOfTags[eachTag]
                #dictOfTags["Total"] = sum
                for eachTag in dictOfTags:
                    dictOfTags[eachTag] = dictOfTags[eachTag]/sum
                self.TransProbDict[masterTag] = dictOfTags

            for tag in self.EmissionProbDict.keys():
                dictOfWords = self.EmissionProbDict[tag]
                sum = 0
                for word in dictOfWords:
                    sum = sum + dictOfWords[word]
                #dictOfWords["Total"] = sum
                for word in dictOfWords:
                    dictOfWords[word] = dictOfWords[word]/sum
                self.EmissionProbDict[tag] = dictOfWords


            self.printModelFile()



    def applySmoothing(self):
        for tag in self.ListOfTags:
            if tag not in self.TransProbDict.keys():
                self.TransProbDict[tag] = {}

        for masterTag in self.TransProbDict.keys():
            dictOfTags = self.TransProbDict[masterTag]
            for childTag in dictOfTags.keys():
                num = dictOfTags[childTag]
                num = num + 1
                dictOfTags[childTag] = num

            for tag in self.ListOfTags:
                if tag not in dictOfTags.keys():
                    dictOfTags[tag] = 1


    def printModelFile(self):
        with open("hmmmodel.txt", "w") as text_file:
            outputDict = {}
            outputDict["TransitionProb"] = self.TransProbDict
            text_file.write(str(outputDict))
            text_file.write("\n")
            outputDict = {}
            outputDict["EmissionProb"] = self.EmissionProbDict
            text_file.write(str(outputDict))
            text_file.write("\n")
            outputDict = {}
            outputDict["WordTagDict"] = self.WordTagDict
            text_file.write(str(outputDict))



learnObject = HMMlearn()
learnObject.readTrainFile(sys.argv[1])
#learnObject.readTrainFile("catalan_corpus_train_tagged.txt")
#learnObject.readTrainFile("test.txt")