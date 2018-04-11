import sys

words = {}
tags = {}
train = []


def read(trainfilename, wordfilename, tagfilename):

    wordfile = open(wordfilename, "r")
    tagfile = open(tagfilename, "r")
    trainfile = open(trainfilename, "r")

    l = 0
    for line in wordfile.readlines():
        words[line.rstrip()] = l
        l = l + 1

    l = 0
    for line in tagfile.readlines():
        tags[line.rstrip()] = l
        l = l + 1

    for line in trainfile.readlines():
        a = line.split(" ")
        l = 0
        for b in a:
            c = b.rstrip().split("_")
            train.append([l + 1, words[c[0]], tags[c[1]]])
            l = l + 1
        train.append([-1, -1, -1])

    trainfile.close()
    tagfile.close()
    wordfile.close()


def write(priorfilename, emitfilename):

    priorfile = open(priorfilename, "w")
    emitfile = open(emitfilename, "w")

    prior = [0] * len(tags.keys())

    for tr in train:
        if tr[0] == 1:
            prior[tr[2]] = prior[tr[2]] + 1
    prior[:] = [(x + 1) for x in prior]
    c = sum(prior)
    prior[:] = [(x * 1.0) / c for x in prior]

    print prior

    width = len(words.keys())
    emit = [0] * (len(tags.keys()) * width)

    for t in tags.keys():
        for w in words.keys():
            count = 0
            for tr in train:
                if tr[0] == -1:
                    continue
                if tr[1] == words[w] and tr[2] == tags[t]:
                    count = count + 1
            emit[tags[t] * width + words[w]] = count

    emit[:] = [(x + 1) for x in emit]
    for i in range(0, len(tags.keys())):
        start = i*width
        end = start + width
        c = sum(emit[start:end])
        emit[start:end] = [(x * 1.0) / c for x in emit[start:end]]

    print emit

    trans = [0] * (len(tags.keys())*len(tags.keys()))
    width = len(tags.keys())

    for i in range(0, width):
        t0 = tags.values()[i]
        for j in range(0, width):
            t1 = tags.values()[j]
            count = 0
            for k in range(0, len(train) - 1):
                if train[k][0] == -1:
                    continue
                if train[k][2] == t0 and train[k+1][2] == t1:
                    count = count + 1
            trans[i*width+j] = count

    trans[:] = [(x + 1) for x in trans]
    width = len(tags.keys())
    for i in range(0, len(tags.keys())):
        start = i*width
        end = start + width
        c = sum(trans[start:end])
        trans[start:end] = [(x * 1.0) / c for x in trans[start:end]]

    print trans






read(sys.argv[1], sys.argv[2], sys.argv[3])
write(sys.argv[4], sys.argv[5])