# -*- coding: utf-8 -*-


def main():

    import os, sys
    import src0039_200728

    indir, outdir = sys.argv[1], sys.argv[1]
    curdir = os.getcwd()


    print(indir)
    INFNAME0 = os.listdir(indir)
    INFNAME = []
    for x in INFNAME0:
        if x.endswith(".tok"): INFNAME.append(x)

    cntinput = 0
    for infname in INFNAME:
        cntinput += 1
        print(cntinput, infname)

        TOK = []
        os.chdir(indir)
        with open(infname, "r", encoding = "utf-8") as inf:
            for x in inf:
                x = x.rstrip()
                if x != "": TOK.append(x)

        TAG = src0039_200728.pnameBIES(curdir, TOK)


        # Output
        os.chdir(outdir)
        outfname = infname[:-4] + ".bioes"
        with open(outfname, "w", encoding = "utf-8") as outf:
            for i in range(len(TOK)):
                x = TOK[i] + "\t" + TAG[i]
                print(x, file = outf)
                if TOK[i] == ".": print("", file = outf)




main()



