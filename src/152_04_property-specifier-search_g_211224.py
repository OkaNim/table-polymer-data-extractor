# -*- coding: utf-8 -*-


def main():
    import sys, os
    import src_001_basic_210825 as src_1


    indir, outdir, propfile, propfile_ng = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]



    INPUT = src_1.input_data(propfile, tab=1, blanc_line=0)                                             # import
    BW = list(map(lambda x: x[0], INPUT))
    BW2 = list(map(lambda x: x[1], INPUT))

    BW3 = src_1.input_data(propfile_ng, tab=0, blanc_line=0)                                            # import

    INFNAME = src_1.file_list(indir, ext=".polymer.bioes")                                               # import

    DATA = []
    for i, infname in enumerate(INFNAME):
        # if i + 1 > 1: break
        print(i + 1, "\t", infname)

        infname_2 = indir + "/" + infname
        INPUT = src_1.input_data(infname_2, tab=1, blanc_line=0)                                         # import
        TOK = list(map(lambda x: x[0], INPUT))

        BTAG, BCATE = search_property_specifier(TOK, BW, BW2, BW3)                                       # def

        OUTPUT = edit_for_output(INPUT, BTAG, BCATE)                                                     # def
        outfname = "04_" + infname[3:]
        outfname = outfname.replace(".bioes", ".property.bioes")
        outfname_2 = outdir + "/" + outfname
        src_1.output(outfname_2, OUTPUT)                                                                 # import




# def
def search_property_specifier(TOK, BW, BW2, BW3):
    BTAG = ["O" for i in range(len(TOK))]
    BCATE = ["_" for i in range(len(TOK))]

    for i, tok in enumerate(TOK):
        for j, bw in enumerate(BW):
            if bw in tok: BTAG[i], BCATE[i] = "S", BW2[j]

        for bw3 in BW3:
            if bw3 in tok:
                BTAG[i], BCATE[i] = "O", "_"
                break

    return BTAG, BCATE



def edit_for_output(INPUT, BTAG, BCATE):
    OUTPUT = []
    for i, x in enumerate(INPUT):
        x.extend([BTAG[i], BCATE[i]])
        x = "\t".join(x)
        OUTPUT.append(x)

    return OUTPUT




main()

