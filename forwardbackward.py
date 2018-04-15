import sys
import numpy as np

prior = []
emit = []
trans = []
words = {}
tags = {}
test = []
widths = []


def readtestfile(testfilename, wordfilename, tagfilename):

    wordfile = open(wordfilename, "r")
    tagfile = open(tagfilename, "r")
    testfile = open(testfilename, "r")

    l = 0
    for line in wordfile.readlines():
        words[line.rstrip()] = l
        l = l + 1

    #print words

    l = 0
    for line in tagfile.readlines():
        tags[line.rstrip()] = l
        l = l + 1

    print tags

    for line in testfile.readlines():
        a = line.split(" ")
        l = 0
        widths.append(len(a))
        for b in a:
            c = b.rstrip().split("_")
            test.append([l + 1, words[c[0]], tags[c[1]]])
            l = l + 1
        test.append([-1, -1, -1])

    #print "test", test

    testfile.close()
    tagfile.close()
    wordfile.close()


def readmatrices(priorfilename, emitfilename, transfilename):

    priorfile = open(priorfilename, "r")
    emitfile = open(emitfilename, "r")
    transfile = open(transfilename, "r")

    priorlength= 0
    for line in priorfile.readlines():
        prior.append(np.float64(line.rstrip()))
        priorlength = priorlength + 1

    #print "prior", prior

    width_e = 0
    height_e = 0
    for line in emitfile.readlines():
        elements = line.rstrip().split(" ")
        if width_e == 0:
            width_e = len(elements)
        for e in elements:
            emit.append(np.float64(e))
        height_e = height_e + 1

    #print "emit", emit

    width_t = 0
    height_t = 0
    for line in transfile.readlines():
        elements = line.rstrip().split(" ")
        if width_t == 0:
            width_t = len(elements)
        for e in elements:
            trans.append(np.float64(e))
        height_t = height_t + 1

    #print "trans", trans

    priorfile.close()
    emitfile.close()
    transfile.close()
    return [priorlength, height_e, width_e, height_t, width_t]

def makepredictions(dim, predictionfilename):
    priorlength = dim[0]
    height_e = dim[1]
    width_e = dim[2]
    height_t = dim[3]
    width_t = dim[4]

    predictfile = open(predictionfilename,"w")

    start = 0
    for w in range(0, len(widths)):
        width_s = widths[w]

        alpha = [np.float64(0.0)] * (height_t * width_s)

        x1 = test[start][1]
        for j in range(0, height_t):
            alpha[j*width_s] = prior[j] * emit[j * width_e + x1]

        for t in range(1, width_s):
            xt = test[start+t][1]
            for j in range(0, height_t):
                p = 0
                for k in range(0, height_t):
                    p = p + (trans[k * width_t + j] * alpha[(k*width_s) + t-1])
                alpha[j*width_s + t] = emit[j * width_e + xt] * p
        #print "alpha", alpha

        beta = [np.float64(0.0)] * (height_t * width_s)

        for j in range(0, height_t):
            beta[j*width_s + (width_s-1)] = np.float64(1.0)

        t = width_s - 2
        while t >= 0:
            x_t_1 = test[start + t + 1][1]
            for j in range(0, height_t):
                p = 0
                for k in range(0, height_t):
                    p = p + (trans[j * width_t + k] * beta[(k*width_s) + t+1] * emit[k * width_e + x_t_1])
                beta[j*width_s + t] = p
            t = t - 1

        #print "beta", beta

        maxtags = [0] * width_s

        for i in range(0, width_s):
            maxp = 0
            for j in range(0, height_t):
                p = alpha[j*width_s+i] * beta[j*width_s+i]
                if p > maxp:
                    maxp = p
                    maxtags[i] = j
            predictfile.write(words.keys()[words.values().index(test[start+i][1])] + "_" + tags.keys()[tags.values().index(maxtags[i])] + " ")
        predictfile.write("\n")
        #print maxtags
        start = start + widths[w] + 1



readtestfile(sys.argv[1], sys.argv[2], sys.argv[3])
dim = readmatrices(sys.argv[4], sys.argv[5], sys.argv[6])
makepredictions(dim, sys.argv[7])