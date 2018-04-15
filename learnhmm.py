import sys
import numpy as np

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

    #print words

    l = 0
    for line in tagfile.readlines():
        tags[line.rstrip()] = l
        l = l + 1

    #print tags

    for line in trainfile.readlines():
        a = line.split(" ")
        l = 0
        for b in a:
            c = b.rstrip().split("_")
            train.append([l + 1, words[c[0]], tags[c[1]]])
            l = l + 1
        train.append([-1, -1, -1])

    #print train

    trainfile.close()
    tagfile.close()
    wordfile.close()


def write(priorfilename, emitfilename, transfilename):

    priorfile = open(priorfilename, "w")
    emitfile = open(emitfilename, "w")
    transfile = open(transfilename, "w")

    prior = [np.float64(1.0)] * len(tags.keys())

    width_e = len(words.keys())
    height_e = len(tags.keys())
    emit = [np.float64(1.0)] * (height_e * width_e)

    width_t = len(tags.keys())
    height_t = len(tags.keys())
    trans = [np.float64(1.0)] * (height_t * width_t)

    l = len(train)
    for k in range(0, l):
        tr = train[k]

        if tr[0] == -1:
            continue
        if tr[0] == 1:
            prior[tr[2]] = prior[tr[2]] + np.float64(1.0)
        emit[(tr[2] * width_e) + tr[1]] = emit[(tr[2] * width_e) + tr[1]] + np.float64(1.0)

        if k == l - 1:
            break
        tr_next = train[k + 1]

        if tr_next[2] == -1:
            continue

        trans[(tr[2] * width_t) + tr_next[2]] = trans[(tr[2] * width_t) + tr_next[2]] + np.float64(1.0)

    c = np.float64(sum(prior))
    prior[:] = [np.float64(x) / c for x in prior]

    #write prior file

    for i in range(0, height_e):
        priorfile.write(format(prior[i], '.16e'))
        priorfile.write("\n")

    #write emit file

    for i in range(0, height_e):
        start = i*width_e
        end = start + width_e
        c = np.float64(sum(emit[start:end]))
        emit[start:end] = [np.float64(x) / c for x in emit[start:end]]

    for i in range(0, height_e):
        for j in range(0, width_e):
            emitfile.write(format(emit[i * width_e + j], '.16e'))
            emitfile.write(" ")
        emitfile.write("\n")

    #write trans file

    for i in range(0, height_t):
        start = i*width_t
        end = start + width_t
        c = np.float64(sum(trans[start:end]))
        trans[start:end] = [np.float64(x) / c for x in trans[start:end]]

    for i in range(0, height_t):
        for j in range(0, width_t):
            transfile.write(format(trans[i * width_t + j], '.16e'))
            transfile.write(" ")
        transfile.write("\n")

    #print trans
    #print prior
    #print emit

    emitfile.close()
    priorfile.close()
    transfile.close()


read(sys.argv[1], sys.argv[2], sys.argv[3])
write(sys.argv[4], sys.argv[5], sys.argv[6])