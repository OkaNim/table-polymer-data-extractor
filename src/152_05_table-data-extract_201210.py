# -*- coding: utf-8 -*-


def main():

    import os, sys

    bash = 0
    if bash == 1:
        args = sys.argv
        indir_all, indir = args[1], args[2]
        print(indir)
    else:
        indir_all, indir = sys.argv[1], sys.argv[1]



    TERM = ["Tg", "Tm", "Td"]
    for term in TERM:
        # if term in ["Tg", "Td"]: continue
        print(term)
        print("")

        indir2 = indir + "/" + term
        outdir = indir2

        # Main
        main2(indir_all, indir2, outdir, term)        # Function




def main2(indir_all, indir, outdir, term):

    import os


    INFNAME0 = os.listdir(indir_all)
    INFNAME = []
    for x in INFNAME0:
        if "_all" in x: INFNAME.append(x)

    EXTRACT, no_dat = [], 0
    cntinput = 0
    for infname in INFNAME:
        ALL = []
        cntinput += 1
        print(cntinput, infname)
        os.chdir(indir_all)
        with open(infname, "r", encoding = "utf-8") as inf:
            for x in inf:
                x = x[:-1]
                if x != "":
                    x = x.split("\t")
                    ALL.append(x)

        DATA = []
        infname = "04_" + infname[3:]
        infname = infname.replace("_all", "").replace(".dat", ".polymer.property.bioes")
        print(cntinput, infname)
        os.chdir(indir)
        with open(infname, "r", encoding = "utf-8") as inf:
            for x in inf:
                x = x[:-1]
                if x != "":
                    x = x.split("\t")
                    DATA.append(x)

        for i in range(len(ALL)): ALL[i].extend(DATA[i][1:])


        EXTRACT, no_dat, DATA = extract_data(ALL, EXTRACT, no_dat)    # Function



        # Output of the final bioes
        outfname = "05_" + infname[3:].replace(".polymer.property.bioes", ".final.bioes")
        os.chdir(outdir)
        with open(outfname, "w", encoding = "utf-8") as outf:
            for i, paper in enumerate(DATA):
                for j, table in enumerate(paper):
                    for k, x in enumerate(table):
                        x = "\t".join(x)
                        print(x, file = outf)
                    print("", file = outf)    # if i != len(DATA) - 1 or j != len(paper) - 1: 



    # Print screen
    print("")
    print("no_file = " + str(len(EXTRACT)) + ",  " + "no_dat = " + str(no_dat))
    print("")
    print("")


    # Output
    outfname = "05_extract.dat"
    os.chdir(outdir)
    with open(outfname, "w", encoding = "utf-8") as outf:
        print("no_file = " + str(len(EXTRACT)) + ",  " + "no_dat = " + str(no_dat), file = outf)
        print("", file = outf)
        for i, paper in enumerate(EXTRACT):
            for j, table in enumerate(paper):
                for k, x in enumerate(table):
                    x = "\t".join(x)
                    print(x, file = outf)
            if i < len(EXTRACT) - 1: print("", file = outf)




def extract_data(ALL, EXTRACT, no_dat):

    import re, copy

    DATA, PTAG, DATA_TABLE, PTAG_TABLE, X, A = [], [], [], [], [], []
    fname2, tlabel2 = "", ""
    for x in ALL:
        fname = x[0]
        tlabel = x[0] + "_" + x[1]
        if tlabel2 != tlabel:
            if X != []:
                DATA_TABLE.append(X)
                PTAG_TABLE.append(A)
            X, A, tlabel2 = [], [], tlabel
        if fname2 != fname:
            if DATA_TABLE != []:
                DATA.append(DATA_TABLE)
                PTAG.append(PTAG_TABLE)
            DATA_TABLE, PTAG_TABLE, fname2 = [], [], fname
        X.append(x)
        A.append(x[4])

    if X != []:
        DATA_TABLE.append(X)
        PTAG_TABLE.append(A)
    if DATA_TABLE != []:
        DATA.append(DATA_TABLE)
        PTAG.append(PTAG_TABLE)


    """
    cntp1, cntp2 = 0, 0
    for i, paper in enumerate(DATA):
        for j, table in enumerate(paper):
            for k, ptag in enumerate(table):
                if "j.polymer.2015.01.027" in ptag[0]:
                    print(paper)
                    break
                    
                    if cntp1 == 0: print(paper)
                    
                    cntp1 = 1
                if "j.polymer.2015.01.028" in ptag[0]:
                    if cntp2 == 0: print(table)
                    cntp2 = 1
    """



    PTAG2 = copy.deepcopy(PTAG)



    # Tag modification of polymer name recognition
    for i, paper in enumerate(PTAG2):
        for j, table in enumerate(paper):
            PNAME = []
            for k, ptag in enumerate(table):
                btag = DATA[i][j][k][5]
                if ptag == "S" and btag == "S": PTAG2[i][j][k] = "O"                       # Tag modify 1

            row_max, thead, cnts1, cnts2, CNTS1_CHECK, CNTS2_CHECK = -1, 0, 0, 0, [], []
            for k, ptag in enumerate(table):
                if k % 3 == 0:
                    address = DATA[i][j][k][2]
                    address = address.split(", ")
                    row, col = int(address[0]), int(address[1])
                    if row_max == -1: thead = row - 1
                    if row_max < row: row_max = row
                    X = [row, col]
                    if ptag == "S":
                        if col == 1:
                            if not X in CNTS1_CHECK:
                                cnts1 += 1
                                CNTS1_CHECK.append(X)
                        elif col == 2:
                            if not X in CNTS2_CHECK:
                                cnts2 += 1
                                CNTS2_CHECK.append(X)
            for k, ptag in enumerate(table):
                if k % 3 == 0:
                    address = DATA[i][j][k][2]
                    address = address.split(", ")
                    row, col = int(address[0]), int(address[1])
                    X = [row, col]
                    if cnts1 > 0 or cnts2 > 0:
                        if cnts1 >= cnts2:
                            # print("cnts1, row_max - thead, row_max, thead", cnts1, row_max - thead, row_max, thead)
                            if col == 1:
                                if cnts1 >= (row_max - thead) * 0.3: PTAG2[i][j][k] = "S"    # Tag modify 2 (Over 30 % in a column)
                            elif col == 2: PTAG2[i][j][k] = "O"                              # Tag modify 3 (Select column 1 or 2)
                        else:
                            if col == 2:
                                if cnts2 >= (row_max - thead) * 0.3: PTAG2[i][j][k] = "S"    # Tag modify 2 (Over 30 % in acolumn)
                            elif col == 1: PTAG2[i][j][k] = "O"                              # Tag modify 3 (Select column 1 or 2)

            """
            for k, ptag in enumerate(table):
                tok = DATA[i][j][k][3]
                if PTAG2[i][j][k] == "S":
                    if not tok in PNAME: PNAME.append(tok)
                else:
                    if tok in PNAME: PTAG2[i][j][k] = "S"                                    # Tag modify 4
            """


    # Data extraction
    # PTAG2 = PTAG    # before tag modfication
    for i, paper in enumerate(PTAG2):
        EXTRACT_PAPER = []
        for j, table in enumerate(paper):
            fname, tlabel = DATA[i][j][0][0], DATA[i][j][0][1]
            EXTRACT_TABLE = []
            for k, ptag in enumerate(table):
                if k % 3 == 0:
                    tok1, ptag1, btag1, bcate1 = DATA[i][j][k][3], PTAG2[i][j][k], DATA[i][j][k][5], DATA[i][j][k][-1]
                    tok2, ptag2, btag2, bcate2 = DATA[i][j][k + 1][3], PTAG2[i][j][k + 1], DATA[i][j][k + 1][5], DATA[i][j][k + 1][-1]
                    tok3, ptag3, btag3 = DATA[i][j][k + 2][3], PTAG2[i][j][k + 2], DATA[i][j][k + 2][5]
                    if re.search(r"[0-9]", tok3) and ptag3 == "O" and btag3 == "O":
                        if tok1 == "non" or tok2 == "non": continue
                        if ptag1 == "S" and btag1 == "O" and ptag2 == "O" and btag2 == "S":
                            X = [fname, tlabel, tok1, tok2, tok3, bcate2]
                            if not X in EXTRACT_TABLE:
                                EXTRACT_TABLE.append(X)
                                no_dat += 1
                        elif ptag1 == "O" and btag1 == "S" and ptag2 == "S" and btag2 == "O":
                            X = [fname, tlabel, tok2, tok1, tok3, bcate1]
                            if not X in EXTRACT_TABLE:
                                EXTRACT_TABLE.append(X)
                                no_dat += 1
            if EXTRACT_TABLE != []: EXTRACT_PAPER.append(EXTRACT_TABLE)
        if EXTRACT_PAPER != []: EXTRACT.append(EXTRACT_PAPER)


        for j, table in enumerate(paper):
            for k, ptag in enumerate(table): DATA[i][j][k].insert(-2, ptag)        # Add PTAG2



    return EXTRACT, no_dat, DATA




main()

