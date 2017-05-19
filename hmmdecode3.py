from copy import deepcopy
import sys

class HMMDecode:

    TransProbDict = {}
    EmissionProbDict = {}
    WordTagDict = {}
    ProbabilityList = []

    def readHMMModelFile(self):
        with open("hmmmodel.txt", "r") as file:
            lineCount = 1
            for line in file:
                tempDict = {}
                if lineCount == 1:
                    tempDict = eval(line)
                    self.TransProbDict = tempDict["TransitionProb"]
                if lineCount == 2:
                    tempDict = eval(line)
                    self.EmissionProbDict = tempDict["EmissionProb"]
                if lineCount == 3:
                    tempDict = eval(line)
                    self.WordTagDict = tempDict["WordTagDict"]
                lineCount = lineCount + 1
            #print(str(self.WordTagDict))


    def readDevFile(self, devFile):
        with open("hmmoutput.txt", "w", encoding="utf8") as outputFile:
            with open(devFile, "r", encoding="utf8") as file:
                count = 1
                for line in file:
                    #print ("Line Count = " + str(count))
                    count = count + 1
                    line = line.rstrip()
                    words = line.split(' ')

                    self.ProbabilityList.clear()

                    backTrackList = self.decodeHMM(["q0"], words, 1)
                    #print(backTrackList)
                    #finalTagList = self.backtrackHMM()
                    finalTaggedSent = self.createTaggedCorpus(words, backTrackList)

                    outputFile.write(finalTaggedSent)
                    outputFile.write("\n")


    def decodeHMM(self, backtrackList, words, prevProb):
        for word in words:
            isInDictionary = 1
            if word in self.WordTagDict.keys():
                listOfTags = self.WordTagDict[word]
                if len(listOfTags) == 1:
                    backtrackList.append(listOfTags[0])
                    #self.ProbabilityList.append([backtrackListCopy, prevProb])

                else:
                    maxHMMProb = -1
                    selectedHMMTag = ""
                    for tag in listOfTags:
                        prevTag = backtrackList[-1]
                        transProb = self.TransProbDict[prevTag][tag]
                        if isInDictionary == 1:
                            emmisProb = self.EmissionProbDict[tag][word]
                        else:
                            emmisProb = 1

                        currProb = prevProb * transProb * emmisProb
                        if currProb > maxHMMProb:
                            maxHMMProb = currProb
                            selectedHMMTag = tag

                    prevProb = maxHMMProb
                    backtrackList.append(selectedHMMTag)

            else:
                isInDictionary = 0
                prevTag = backtrackList[-1]
                prevTagDict = self.TransProbDict[prevTag]
                maxProb = -1
                selectedTag = ""
                for nextTag in prevTagDict:
                    prob = prevTagDict[nextTag]
                    if prob > maxProb:
                        maxProb = prob
                        selectedTag = nextTag
                listOfTags = [selectedTag]
                backtrackList.append(selectedTag)

        return backtrackList







    def backtrackHMM(self):
        maxProb = -1
        selectedTagList = []
        for eachList in self.ProbabilityList:
            currProb = eachList[1]
            if currProb > maxProb:
                maxProb = currProb
                selectedTagList = eachList[0]
        return selectedTagList


    def createTaggedCorpus(self, words, tags):
        newSent = ""
        #print(str(len(words))+ "   " +str(len(tags)))
        for i in range(0,len(words)):
            newWord = words[i]+"/"+tags[i+1]
            if(newSent == ""):
                newSent = newWord
            else:
                newSent = newSent + " " + newWord
        return newSent


decodeObj = HMMDecode()
decodeObj.readHMMModelFile()
#decodeObj.readDevFile(sys.argv[1])
decodeObj.readDevFile("catalan_corpus_dev_raw.txt")
#decodeObj.readDevFile("test.txt")