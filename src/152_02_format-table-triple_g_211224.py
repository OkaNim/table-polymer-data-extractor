# -*- coding: utf-8 -*-

def main():
    import sys, os
    import src_001_basic_210825 as src_1


    indir, outdir = sys.argv[1], sys.argv[2]


    INFNAME = src_1.file_list(indir, ext=".tsv")                                                       # import

    TRIPLE_ALL, NON_FORMAT = [], []
    cnt_data, cntoutput = 0, 0
    for i, infname in enumerate(INFNAME):
        # if i + 1 > 100: break
        print(i + 1, "\t", infname)

        INPUT = src_1.input_data(os.path.join(indir, infname), tab=0, blanc_line=0)                    # import

        TABLE_PART = each_table(INPUT)                                                                 # def

        TRIPLE_PAPER = []
        infname = infname[:-4]
        for part in TABLE_PART:
            TABLE, thead, tlabel, tcaption, tfoot = extract_table(INPUT, part)                         # def

            error, NON_FORMAT = check_table(TABLE, infname, thead, tlabel, NON_FORMAT)                 # def
            if error != "": continue

            TRIPLE = create_triple(TABLE, infname, thead, tlabel, tcaption, tfoot)                     # def

            if TRIPLE != []:
                TRIPLE_PAPER.append(TRIPLE)
                # cnt_data += len(TRIPLE)


        if TRIPLE_PAPER != []: TRIPLE_ALL.append(TRIPLE_PAPER)


        if (i + 1) % 10000 == 0:
            cntoutput += 1
            edit_and_output(TRIPLE_ALL, cntoutput, outdir, src_1)                                     # def
            TRIPLE_ALL = []


    if TRIPLE_ALL != []:
        cntoutput += 1
        edit_and_output(TRIPLE_ALL, cntoutput, outdir, src_1)                                         # def



    # Output of NON_FORMAT
    out_no_change = 1
    if out_no_change == 1 and NON_FORMAT != []:
        outfname = "02_not-formatting.dat"
        src_1.output(os.path.join(outdir, outfname), NON_FORMAT)                                       # import



    # Print screen
    print("")
    print("len(NON_FORMAT) =", len(NON_FORMAT))




# def
def each_table(INPUT):
    TABLE_PART = []
    for i, x in enumerate(INPUT):
        if x.startswith("thead="): TABLE_PART.append([i])
        elif x.startswith("(Footnote)"): TABLE_PART[-1].append(i)

    return TABLE_PART



def extract_table(INPUT, part):
    import re

    start, end = part[0], part[1]

    thead, tlabel, tcaption, tfoot = 0, "", "", ""
    n = re.search(r"thead=[0-9]+", INPUT[start])
    if n: thead = int(n.group()[6:])
    tlabel = INPUT[start + 1]
    tcaption, tfoot = INPUT[start + 2], INPUT[end]

    TABLE = []
    for i in range(start + 3, end):
        x = INPUT[i].split("\t")
        TABLE.append(x)

    return TABLE, thead, tlabel, tcaption, tfoot



def check_table(TABLE, infname, thead, tlabel, NON_FORMAT):
    error = ""
    no_row, no_col = len(TABLE), len(TABLE[0])
    if no_row < 2:                                                          # Check if there are two more rows.
        error = infname + "\t" + tlabel + "\t" + "no_row < 2"               # (1) no_row < 2
        NON_FORMAT.append(error)
    else:
        if no_col == 1:
            error = infname + "\t" + tlabel + "\t" + "no_col=1"             # (2) no_col=1
            NON_FORMAT.append(error)
        if thead == 0:
            error = infname + "\t" + tlabel + "\t" + "thead=0"              # (3) thead=0
            NON_FORMAT.append(error)
        no_col_check = 0                                                    # (4) Check the number of table cells in each row
        for i in range(1, no_row):
            if len(TABLE[i]) != no_col:
                error = infname + "\t" + tlabel + "\t" + "no_col error"
                NON_FORMAT.append(error)
                break

    return error, NON_FORMAT



def create_triple(TABLE, infname, thead, tlabel, tcaption, tfoot):
    no_row, no_col = len(TABLE), len(TABLE[0])

    TRIPLE = [[infname, tlabel, "_", "((supple))thead=" + str(thead)],
              [infname, tlabel, "_", "((supple))(Caption) " + tcaption],
              [infname, tlabel, "_", "((supple))" + tfoot]]
    for a in range(thead):
        X = [infname, tlabel, str(a + 1) + ", 1", "((supple))" + TABLE[a][0]]
        TRIPLE.append(X)

    for a in range(thead):
        for b in range(2):
            for c in range(thead, no_row):
                for d in range(b + 1, no_col):
                    x1, x2, x3 = [str(c + 1), str(b + 1)], [str(a + 1), str(d + 1)], [str(c + 1), str(d + 1)]
                    x1, x2, x3 = ", ".join(x1), ", ".join(x2), ", ".join(x3)
                    y1, y2, y3 = TABLE[c][b], TABLE[a][d], TABLE[c][d]
                    X1, X2, X3 = [infname, tlabel, x1, y1], [infname, tlabel, x2, y2], [infname, tlabel, x3, y3]
                    TRIPLE.append(X1)
                    TRIPLE.append(X2)
                    TRIPLE.append(X3)

    return TRIPLE



def edit_and_output(TRIPLE, cntoutput, outdir, src_1):
    OUTPUT_1, OUTPUT_2 = edit_for_output(TRIPLE)                                                       # def

    id = str(cntoutput)
    if cntoutput < 10: id = "0" + str(cntoutput)

    outfname = "02_table-triple_" + id + "_all.dat"
    src_1.output(outdir + "/" + outfname, OUTPUT_1)                                                    # import

    outfname = "02_table-triple_" + id + ".bioes"
    src_1.output(outdir + "/" + outfname, OUTPUT_2)                                                    # import




def edit_for_output(OUTPUT):
    OUTPUT_1, OUTPUT_2 = [], []
    for i, paper in enumerate(OUTPUT):
        for j, table in enumerate(paper):
            for k, x in enumerate(table):
                OUTPUT_1.append("\t".join(x))
                if not x[-1].startswith("((supple))"): OUTPUT_2.append(x[-1])
            OUTPUT_1.append("")
            OUTPUT_2.append("")

    del OUTPUT_1[-1]
    del OUTPUT_2[-1]

    return OUTPUT_1, OUTPUT_2




if __name__ == "__main__":
    main()


