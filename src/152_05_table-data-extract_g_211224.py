# -*- coding: utf-8 -*-


def main():
    import sys, os
    import src_001_basic_210825 as src_1


    indir, outdir = sys.argv[1], sys.argv[2]


    INFNAME = src_1.file_list(indir, ext="_all.dat")                                                             # import

    EXTRACT_ALL, no_dat = [], 0
    for i, infname in enumerate(INFNAME):
        print(i + 1, "\t", infname)

        INPUT = src_1.input_data(os.path.join(indir, infname), tab=1, blanc_line=1)                              # import

        infname_2 = "04_" + infname[3:].replace("_all.dat", ".polymer.property.bioes")
        INPUT_2 = src_1.input_data(os.path.join(indir, infname_2), tab=1, blanc_line=0)                          # import

        DATA, PTAG = edit_input(INPUT, INPUT_2)                                                                  # def

        PTAG2 = modify_tag(DATA, PTAG)                                                                           # def

        # PTAG2 = PTAG        # before tag modfication
        EXTRACT, no_dat = extract_data(DATA, PTAG2, no_dat)                                                      # def
        EXTRACT_ALL.extend(EXTRACT)


        # Output of tag-modified data
        DATA = merge_data(DATA, PTAG2)                                                                           # def

        OUTPUT = edit_for_output(DATA)                                                                           # def
        outfname = "05_" + infname[3:].replace("_all.dat", ".final.bioes")
        src_1.output(os.path.join(outdir, outfname), OUTPUT)                                                     # import



    # Output
    HEADER = [["no_paper = " + str(len(EXTRACT_ALL)) + ",  " + "no_dat = " + str(no_dat)],
              ["file-name", "tlabel", "polymer-name", "prop-specifier", "value", "property", "cell-address", "no-thead", "related-tcd", "caption", "footnote"]]
    OUTPUT = edit_for_output_2(HEADER, EXTRACT_ALL)                                                              # def
    outfname = "05_extract.dat"
    src_1.output(os.path.join(outdir, outfname), OUTPUT)                                                         # import



    # Print screen
    print("\n" + HEADER[0][0])




# def
def edit_input(INPUT, INPUT_2):
    INPUT_MERGE = []
    a = -1
    for i, x in enumerate(INPUT):
        if x[-1].startswith("((supple))"): X = ["_", "_", "_"]
        else:
            a += 1
            X = INPUT_2[a][1:]
        INPUT[i].extend(X)

    DATA, PTAG, DATA_TABLE, PTAG_TABLE, X, A = [], [], [], [], [], []
    fname2, tlabel2 = "", ""
    for x in INPUT:
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


    return DATA, PTAG



def modify_tag(DATA, PTAG):
    import re, copy

    PTAG2 = copy.deepcopy(PTAG)

    for i, paper in enumerate(PTAG2):
        for j, table in enumerate(paper):
            PNAME = []
            for k, ptag in enumerate(table):
                if ptag == "_": continue
                btag = DATA[i][j][k][5]
                if ptag == "S" and btag == "S": PTAG2[i][j][k] = "O"                       # Tag modify 1

            row_max, thead, cnts1, cnts2, CNTS1_CHECK, CNTS2_CHECK = -1, 0, 0, 0, [], []
            cnt_k = -1
            for k, ptag in enumerate(table):
                if ptag == "_": continue
                cnt_k += 1
                if cnt_k % 3 == 0:
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
            cnt_k = -1
            for k, ptag in enumerate(table):
                if ptag == "_": continue
                cnt_k += 1
                if cnt_k % 3 == 0:
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

    return PTAG2



def extract_data(DATA, PTAG2, no_dat):
    import re

    EXTRACT = []
    for i, paper in enumerate(PTAG2):
        EXTRACT_PAPER = []
        for j, table in enumerate(paper):
            fname, tlabel, thead, tcaption, tfoot = DATA[i][j][0][0], DATA[i][j][0][1], int(DATA[i][j][0][3][16:]), DATA[i][j][1][3][10:], DATA[i][j][2][3][10:]
            EXTRACT_TABLE, ADDRESS_3, SUPPLE_TABLE = [], [], []
            cnt_k = -1
            for k, ptag in enumerate(table):
                if ptag == "_": continue
                cnt_k += 1
                if cnt_k % 3 == 0:
                    address1, tok1, ptag1, btag1, bcate1 = DATA[i][j][k][2], DATA[i][j][k][3], PTAG2[i][j][k], DATA[i][j][k][5], DATA[i][j][k][-1]
                    address2, tok2, ptag2, btag2, bcate2 = DATA[i][j][k + 1][2], DATA[i][j][k + 1][3], PTAG2[i][j][k + 1], DATA[i][j][k + 1][5], DATA[i][j][k + 1][-1]
                    address3, tok3, ptag3, btag3 = DATA[i][j][k + 2][2], DATA[i][j][k + 2][3], PTAG2[i][j][k + 2], DATA[i][j][k + 2][5]
                    if re.search(r"[0-9]", tok3) and ptag3 == "O" and btag3 == "O":
                        if tok1 == "non" or tok2 == "non": continue
                        if ptag1 == "S" and btag1 == "O" and ptag2 == "O" and btag2 == "S":
                            X = [fname, tlabel, tok1, tok2, tok3, bcate2]
                            if not address3 in ADDRESS_3 and not X in EXTRACT_TABLE:
                                ADDRESS_3.append(address3)
                                EXTRACT_TABLE.append(X)
                                no_dat += 1
                                ADDRESS = [address1, address2, address3]
                                supple = supplemental_data(ADDRESS, DATA, i, j, k, thead)                        # def
                                Y = [" / ".join(ADDRESS), "thead=" + str(thead), supple, tcaption, tfoot]
                                SUPPLE_TABLE.append(Y)
                        elif ptag1 == "O" and btag1 == "S" and ptag2 == "S" and btag2 == "O":
                            X = [fname, tlabel, tok2, tok1, tok3, bcate1]
                            if not address3 in ADDRESS_3 and not X in EXTRACT_TABLE:
                                ADDRESS_3.append(address3)
                                EXTRACT_TABLE.append(X)
                                no_dat += 1
                                ADDRESS = [address1, address2, address3]
                                supple = supplemental_data(ADDRESS, DATA, i, j, k, thead)                        # def
                                ADDRESS[0], ADDRESS[1] = ADDRESS[1], ADDRESS[0]
                                Y = [" / ".join(ADDRESS), "thead=" + str(thead), supple, tcaption, tfoot]
                                SUPPLE_TABLE.append(Y)
            if EXTRACT_TABLE != []:
                for k, x in enumerate(EXTRACT_TABLE): x.extend(SUPPLE_TABLE[k])
                EXTRACT_PAPER.append(EXTRACT_TABLE)
        if EXTRACT_PAPER != []: EXTRACT.append(EXTRACT_PAPER)

    return EXTRACT, no_dat



def supplemental_data(ADDRESS, DATA, i, j, k, thead):
    supple = "_"
    X = []
    for a in range(2):
        address = ADDRESS[0 + a].split(", ")
        row_2, col_2 = int(address[0]), int(address[1])
        for b, data in enumerate(DATA[i][j]):
            if data[2] == "_": continue
            address = data[2].split(", ")
            row, col = int(address[0]), int(address[1])
            if col == col_2 and row <= thead:
                if not data[2] in ADDRESS:
                    x = "(" + data[2] + ")" + DATA[i][j][b][3].replace("((supple))", "")
                    if not x in X: X.append(x)
            if a != 0 or col_2 < 2: continue
            if col < col_2:
                if row == row_2 or row <= thead:
                    if not data[2] in ADDRESS:
                        x = "(" + data[2] + ")" + DATA[i][j][b][3].replace("((supple))", "")
                        if not x in X: X.append(x)
    if X != []:
        X = sorted(X)
        supple = " / ".join(X)

    return supple



def merge_data(DATA, PTAG2):
    for i, paper in enumerate(PTAG2):
        for j, table in enumerate(paper):
            for k, ptag in enumerate(table): DATA[i][j][k].insert(-2, ptag)        # Add PTAG2

    return DATA



def edit_for_output(OUTPUT):
    OUTPUT_2 = []
    for i, paper in enumerate(OUTPUT):
        for j, table in enumerate(paper):
            for k, x in enumerate(table):
                x = "\t".join(x)
                OUTPUT_2.append(x)
            OUTPUT_2.append("")

    return OUTPUT_2



def edit_for_output_2(HEADER, OUTPUT):
    OUTPUT_2 = []
    for x in HEADER: OUTPUT_2.append("\t".join(x))
    for i, paper in enumerate(OUTPUT):
        for j, table in enumerate(paper):
            for k, x in enumerate(table):
                x = "\t".join(x)
                OUTPUT_2.append(x)
        OUTPUT_2.append("")
    del OUTPUT_2[-1]

    return OUTPUT_2




# Main
if __name__ == "__main__": main()


