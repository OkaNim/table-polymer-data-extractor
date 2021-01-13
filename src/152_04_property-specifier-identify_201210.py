# -*- coding: utf-8 -*-


def main():

    import os, sys

    bash = 0
    if bash == 1:
        args = sys.argv
        indir = args[1]
        print(indir)
    else:
        indir, outdir = sys.argv[1], sys.argv[1]
        filedir_0 = os.getcwd() + "/152_04_file"


    TERM = ["Tg", "Tm", "Td"]
    for term in TERM:
        print("")
        print(term)

        # Dir
        outdir = indir + "/" + term
        os.makedirs(outdir, exist_ok = True)
        filedir = filedir_0 + "/" + term


        # Main
        searching(indir, outdir, filedir, term)        # Function



def searching(indir, outdir, filedir, term):

    import os, re


    # Input index terms, category-name, and stop words
    os.chdir(filedir)
    infname_term = term + ".txt"
    with open(infname_term, "r", encoding = "utf-8") as inf:
        BW, BW2 = [], []
        for x in inf:
            x = x.rstrip()
            x = x.split("\t")
            BW.append(x[0])
            BW2.append(x[1])

    infname_stop = infname_term.replace(".txt", "_NG.txt")
    with open(infname_stop, "r", encoding = "utf-8") as inf:
        BW3 = []
        for x in inf:
            x = x.rstrip()
            BW3.append(x)



    # Main
    INFNAME0 = os.listdir(indir)
    INFNAME = []
    for x in INFNAME0:
        if x.endswith(".polymer.bioes"): INFNAME.append(x)
    cntinput = 0
    DATA = []
    for infname in INFNAME:
        cntinput += 1
        # if cntinput > 1: break
        print(cntinput, infname)

        THEAD, LINE_ID = [], []

        os.chdir(indir)
        with open(infname, "r", encoding = "utf-8") as inf:
            TOK, PTAG, PROB_S, PROB_O = [], [], [], []
            for x in inf:
                x = x.rstrip()
                if x != "":
                    x = x.split("\t")
                    if x[0] != "00000":
                        TOK.append(x[0])
                        PTAG.append(x[1])
                    # PROB_S.append(x[2])
                    # PROB_O.append(x[3])
                else:
                    TOK.append("")
                    PTAG.append("")
                    # PROB_S.append("")
                    # PROB_O.append("")


        BTAG = ["O" for i in range(len(TOK))]
        BCATE = ["_" for i in range(len(TOK))]


        for i, tok in enumerate(TOK):
            for j, bw in enumerate(BW):
                if bw in tok:
                     BTAG[i], BCATE[i] = "S", BW2[j]


        for i, tok in enumerate(TOK):
            for bw3 in BW3:
                if bw3 in tok:
                    BTAG[i], BCATE[i] = "O", "_"
                    break



        # Output
        os.chdir(outdir)
        outfname = "04_" + infname[3:]
        outfname = outfname.replace(".bioes", ".property.bioes")
        with open(outfname, "w", encoding = "utf-8") as outf:
            for i in range(len(TOK)):
                if TOK[i] != "":
                    # X = [TOK[i], PTAG[i], PROB_S[i], PROB_O[i], BTAG[i], BCATE[i]]
                    X = [TOK[i], PTAG[i], BTAG[i], BCATE[i]]
                    x = "\t".join(X)
                else: x = ""
                print(x, file = outf)



main()

