# -*- coding: utf-8 -*-

def main():

    import os, sys, re


    indir, outdir = sys.argv[1], sys.argv[1]


    # Main
    INFNAME0 = os.listdir(indir)
    INFNAME = []
    for x in INFNAME0:
        if x.endswith(".tsv"): INFNAME.append(x)

    DATA, NO_CHANGE = [], []
    cntinput, cnt_data, cntoutput = 0, 0, 0
    for infname in INFNAME:
        DATA_PAPER = []

        cntinput += 1
        print(cntinput, infname)

        os.chdir(indir)
        with open(infname, "r", encoding = "utf-8") as inf:
            LINE = []
            for x in inf:
                x = x[:-1]
                LINE.append(x)


        TABLE_i, TABLE_j = [], []
        for i in range(len(LINE)):
            if LINE[i].startswith("thead="): TABLE_i.append(i)
            elif LINE[i].startswith("(Footnote)"): TABLE_j.append(i)


        infname = infname[:-4]
        for i in range(len(TABLE_i)):
            DATA_TABLE = []

            thead, tlabel, tcaption, tfoot = 0, "", "", ""
            n = re.search(r"thead=[0-9]+", LINE[TABLE_i[i]])
            if n: thead = int(n.group()[6:])
            tlabel = LINE[TABLE_i[i] + 1]
            tcaption, tfoot = LINE[TABLE_i[i] + 2], LINE[TABLE_j[i]]


            TABLE = []
            for j in range(TABLE_i[i] + 3, TABLE_j[i]):
                x = LINE[j].split("\t")
                TABLE.append(x)
            no_row, no_col = len(TABLE), len(TABLE[0])


            # Creation of triples
            if no_row > 1:    # Check if there are two more rows.

                # Check if the triple data are created.
                if no_col == 1:                                        # (1) no_col=1
                    x = infname + "\t" + tlabel + "\t" + "no_col=1"
                    NO_CHANGE.append(x)
                    continue

                if thead == 0:                                         # (2) thead=0
                    x = infname + "\t" + tlabel + "\t" + "thead=0"
                    NO_CHANGE.append(x)
                    continue

                no_col_check = 0                                       # (3) Check the number of table cells in each row
                for j in range(1, no_row):
                    if len(TABLE[j]) != no_col:
                        no_col_check = 1
                        break
                if no_col_check == 1:
                    x = infname + "\t" + tlabel + "\t" + "no_col error"
                    NO_CHANGE.append(x)
                    continue


                # Creation of the triple data.
                for a in range(thead):
                    for b in range(2):
                        for c in range(thead, no_row):
                            for d in range(b + 1, no_col):
                                x1, x2, x3 = [str(c + 1), str(b + 1)], [str(a + 1), str(d + 1)], [str(c + 1), str(d + 1)]
                                x1, x2, x3 = ", ".join(x1), ", ".join(x2), ", ".join(x3)
                                y1, y2, y3 = TABLE[c][b], TABLE[a][d], TABLE[c][d]
                                X1, X2, X3 = [infname, tlabel, x1, y1], [infname, tlabel, x2, y2], [infname, tlabel, x3, y3]
                                DATA_TABLE.append(X1)
                                DATA_TABLE.append(X2)
                                DATA_TABLE.append(X3)


                if DATA_TABLE != []:
                    DATA_PAPER.append(DATA_TABLE)
                    cnt_data += len(DATA_TABLE)

        """
        # Output
        if DATA == []: continue
        outfname = infname + ".dat"
        os.chdir(outdir)
        with open(outfname, "w", encoding = "utf-8") as outf:
            for i, table in enumerate(DATA):
                for x in table:
                    x = "\t".join(x)
                    print(x, file = outf)
                if i < len(DATA): print("", file = outf)
        """

        # print(infname, len(DATA_PAPER))
        if DATA_PAPER != []: DATA.append(DATA_PAPER)


        if cntinput % 10000 == 0:
            cntoutput += 1
            output(DATA, cntoutput, outdir)
            DATA = []



    if DATA != []:
        cntoutput += 1
        output(DATA, cntoutput, outdir)




    print("")
    print("len(NO_CHANGE) =", len(NO_CHANGE))



    # Output of NO_CHANGE
    out_no_change = 1
    if out_no_change == 1 and NO_CHANGE != []:
        outfname = "02_no-triple-change.dat"
        os.chdir(outdir)
        with open(outfname, "w", encoding = "utf-8") as outf:
            for x in NO_CHANGE: print(x, file = outf)



# Function
def output(DATA, cntoutput, outdir):

    import os


    id = str(cntoutput)
    if cntoutput < 10: id = "0" + str(cntoutput)

    os.chdir(outdir)

    outfname = "02_table-triple_all_" + id + ".dat"
    with open(outfname, "w", encoding = "utf-8") as outf:
        for i, paper in enumerate(DATA):
            for j, table in enumerate(paper):
                for x in table:
                    x = "\t".join(x)
                    print(x, file = outf)
                if i == len(DATA) - 1 and j == len(paper) - 1: break
                print("", file = outf)

    outfname = "02_table-triple_" + id + ".dat"
    with open(outfname, "w", encoding = "utf-8") as outf:
        for i, paper in enumerate(DATA):
            for j, table in enumerate(paper):
                for x in table:
                    x = x[-1]
                    print(x, file = outf)
                if i == len(DATA) - 1 and j == len(paper) - 1: break
                print("", file = outf)




main()


