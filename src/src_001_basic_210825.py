# -*- coding: utf-8 -*-

def file_list(indir, ext):
    import os

    INFNAME0 = os.listdir(indir)
    INFNAME = []
    for x in INFNAME0:
        if x.endswith(ext): INFNAME.append(x)

    return INFNAME



def input_data(infname, tab, blanc_line):
    with open(infname, "r", encoding = "utf-8") as inf:
        INPUT = []
        for x in inf:
            x = x[:-1]    # rstrip()
            if blanc_line == 1 and x == "": continue
            if tab == 1: x = x.split("\t")
            INPUT.append(x)

    return INPUT



def edit_for_output(HEADER, OUTPUT):
    OUTPUT_2 = []
    for x in HEADER: OUTPUT_2.append("\t".join(x))
    for i, x in enumerate(OUTPUT): OUTPUT_2.append("\t".join(x))

    return OUTPUT_2



def output(outfname, OUTPUT):
    with open(outfname, "w", encoding = "utf-8") as outf:
        for x in OUTPUT: print(x, file = outf)



def make_tmpdir():
    import os, shutil

    curdir = os.getcwd()
    tmpdir = curdir + "/tmpdir"
    if "tmpdir" in os.listdir(curdir): shutil.rmtree(tmpdir)
    os.makedirs(tmpdir, exist_ok = True)

    return tmpdir



def delete_directory(deldir):
    import shutil

    shutil.rmtree(deldir)



def iter_end(DATA, start, end_word, stop_word=None, CHECK_J=None):
    j2 = -1
    for j in range(start, len(DATA)):
        if CHECK_J != None:
            if j in CHECK_J: continue
        if end_word in DATA[j]:
            j2 = j
            break
        if stop_word != None:
            if stop_word in DATA[j]: break

    return j2



def extract_BIES_tagged_entity(TOK, TAG, del_tok_whitespace):
    ENTITY, TOKID = [], []
    for i, tok in enumerate(TOK):
        tag = TAG[i]
        if tag[0] in ["S", "B"]:
            j2 = -1
            if tag[0] == "S": j2 = i
            elif tag[0] == "B":
                for j in range(i + 1, len(TOK)):
                    if TAG[j][0] in ["S", "O"]: break
                    elif TAG[j][0] == "E":
                        j2 = j
                        break
            if j2 != -1:
                entity = " ".join(TOK[i : j2 + 1])
                if del_tok_whitespace == 1:
                    entity = entity.replace(" ( ", "(").replace(" ) ", ")").replace(" )", ")").replace(" { ", "{").replace(" } ", "}").replace(" }", "}").replace(" [ ", "[").replace(" [", "[").replace(" ] ", "]").replace(" ]", "]").replace(" / ", "/").replace(" /", "/").replace("/ ", "/").replace(" , ", ",").replace(", ", ",").replace(" ,", ",").replace(" - ", "-").replace("- ", "-").replace(" -", "-")
                ENTITY.append(entity)
                TOKID.append([i + 1, j2 + 1])

    LONG_ABB = []
    for i in range(len(TOKID) - 1):
        if TOKID[i + 1][0] - TOKID[i][1] == 2:
            a = TOKID[i][1]    # TOKID is not started from zero, but one.
            if TOK[a] in ["(", "[", ","]:
                long, abb = ENTITY[i], ENTITY[i + 1]
                # if len(re.findall(r"[A-Z]", abb)) / len(abb) >= 0.5:
                X = [long, abb]
                if not X in LONG_ABB: LONG_ABB.append(X)


    for x in TOKID: x[0], x[1] = str(x[0]), str(x[1])


    return ENTITY, TOKID, LONG_ABB


