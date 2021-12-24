# -*- coding: utf-8 -*-

def main():
    import sys, os
    import src_001_basic_210825 as src_1


    indir, outdir = sys.argv[1], sys.argv[2]



    # Input HTML-XML char data.
    infname = "HTMLXMLchar_190718.txt"
    INPUT = src_1.input_data(infname, tab=1, blanc_line=0)                                                # def
    CODE = list(map(lambda x: x[0], INPUT))
    SIGN = list(map(lambda x: x[2], INPUT))



    # Input XML tags.
    infname = "XMLTAG_211224_github.dat"
    INPUT = src_1.input_data(infname, tab=1, blanc_line=0)                                                # def
    del INPUT[0]

    XMLTAGS = edit_input(INPUT)                                                                           # def



    # Main
    INFNAME = file_list(indir, EXT=[".xml", ".XML"])                                                      # def

    for i, infname in enumerate(INFNAME):
        # if i + 1 > 1: break
        # if not "acs.macromol.6b02504" in infname: continue
        print(i + 1, "\t", infname)

        publisher = judge_publisher(infname)                                                              # def
        if publisher == -1: continue

        INPUT = src_1.input_data(os.path.join(indir, infname), tab=0, blanc_line=0)                       # def



        # Edit XML
        XML = edit_XML(INPUT, XMLTAGS, publisher)                                                         # def
        XML = convert_HTMLXMLchar(XML ,CODE, SIGN)                                                        # def
        # outfname = infname[:-4] + ".xml2"
        # src_1.output(os.path.join(outdir, outfname), XML)                                               # def



        # Extract text
        HEAD, BODY, FLOATS = head_body(XML, publisher)                                                    # def

        TXT, TABLE_PART = extract_text(XML, HEAD, BODY, FLOATS, publisher)                                # def

        OUTPUT = edit_text(TXT)                                                                           # def

        # if TXT != []:
        #     outfname = infname[:-4] + ".txt"
        #     src_1.output(os.path.join(outdir, outfname), OUTPUT)                                          # def



        # Extract tables
        TABLE_PAPER = []
        for part in TABLE_PART:
            THEAD, TBODY = thead_tbody(XML, start=part[0], end=part[1])                                   # def
            if THEAD == []: continue
            elif len(THEAD) == 1: cnt_merged = 0
            elif len(THEAD) > 1: cnt_merged = 1

            tlabel, tcaption, tfoot, colnum = tlabel_tcaption_tfootnote(XML, publisher, start=part[0], end=part[1])    # def

            for j in range(len(THEAD)):
                ROW = []
                cnt_thead = 0
                if THEAD[j] != []:
                    ROW = count_row(ROW, XML, start=THEAD[j][0], end=THEAD[j][1])                         # def
                    for k in range(len(ROW)): ROW[k].append("thead")
                    cnt_thead = len(ROW)

                ROW = count_row(ROW, XML, start=TBODY[j][0], end=TBODY[j][1])                             # def
                for k in range(cnt_thead, len(ROW)): ROW[k].append("tbody")
                if len(ROW) < 2: continue

                TABLE, cnt_multi_col, cnt_multi_row = embed_table_cell_datum(colnum, ROW, XML, publisher) # def

                TABLE = edit_table(TABLE, tlabel, tcaption, tfoot, cnt_thead, cnt_multi_col, cnt_multi_row, cnt_merged)    # def

                TABLE_PAPER.append(TABLE)



        if TABLE_PAPER != []:
            OUTPUT = edit_for_output_2(TABLE_PAPER)                                                       # def
            outfname = infname[:-4] + ".tsv"
            src_1.output(os.path.join(outdir, outfname), OUTPUT)                                          # def




# def
def edit_input(INPUT):
    INPUT_2 = []
    for i in range(len(INPUT[0])):
        X = list(map(lambda x: x[i], INPUT))
        Y = []
        for x in X:
            Y.append(x)
            if "/" in x:
                x2 = x[:-1].replace("/", "")
                Y.append(x2)
                x3 = x2 + "/>"
                Y.append(x3)
        INPUT_2.append(Y)

    return INPUT_2



def file_list(indir, EXT):
    import os

    INFNAME0 = os.listdir(indir)
    INFNAME = []
    for x in INFNAME0:
        if x[-4:] in EXT: INFNAME.append(x)

    return INFNAME



def judge_publisher(infname):
    publisher = -1
    if "acs" in infname: publisher = 1
    elif "DOI" in infname or "10.1016_" in infname: publisher = 2
    elif ".XML" in infname: publisher = 3
    elif "doi_10.1007" in infname: publisher = 4
    else: publisher = 5

    return publisher



def edit_XML(INPUT, XMLTAGS, publisher):
    import re

    XMLTAG_STA = XMLTAGS[0]
    XMLTAG = XMLTAGS[publisher]

    INPUT_2 = []
    for x in INPUT:
        for j, y in enumerate(XMLTAG):
            z = XMLTAG_STA[j]
            if ">" in y:
                if y in x: x = x.replace(y, "zzzzz" + z)
            else:
                for a in [">", " "]:
                    y2 = y + a
                    if y2 in x:
                        z2 = z + a
                        x = x.replace(y2, "zzzzz" + z2)
        x = x.split("zzzzz")
        INPUT_2.extend(x)

    INPUT_3 = []
    for x in INPUT_2:
        for y in XMLTAG_STA:
            if ">" in y:
                if y in x: x = x.replace(y, "zzzzz" + y + "zzzzz")
            else:
                y2 = y + ">"
                if y2 in x: x = x.replace(y2, "zzzzz" + y2 + "zzzzz")
                y2 = y + " [^>]+>"
                pat = re.compile(r"%s" % y2)
                m = pat.search(x)
                if m: x = x.replace(m.group(), "zzzzz" + m.group() + "zzzzz")
        x = x.split("zzzzz")
        for y in x:
            if re.search(r'colname="[0-9]+', y): y = y.replace('colname="', 'colname="col')
            if re.search(r'namest="[0-9]+', y): y = y.replace('namest="', 'namest="col')
            if re.search(r'nameend="[0-9]+', y): y = y.replace('nameend="', 'nameend="col')
            if re.search(r'colname="c[0-9]+', y): y = y.replace('colname="c', 'colname="col')
            if re.search(r'namest="c[0-9]+', y): y = y.replace('namest="c', 'namest="col')
            if re.search(r'nameend="c[0-9]+', y): y = y.replace('nameend="c', 'nameend="col')
            y = y.lstrip()
            if y != "": INPUT_3.append(y)

    INPUT_4 = []
    for x in INPUT_3:
        if re.fullmatch("<equation [^>]+>", x) or x == "<equation>":
            INPUT_4.append("</p>")
            INPUT_4.append(x)
        elif x == "</equation>":
            INPUT_4.append(x)
            INPUT_4.append("<p>")
        else: INPUT_4.append(x)


    return INPUT_4



def convert_HTMLXMLchar(XML ,CODE, SIGN):
    for i in range(len(XML)):
        for (code, sign) in zip(CODE, SIGN):
            if code in XML[i]: XML[i] = XML[i].replace(code, sign)

    return XML



def head_body(XML, publisher):
    HEAD, BODY, FLOATS = [], [], []
    for i, x in enumerate(XML):
        if publisher == 4:
            if "<ArticleInfo " in x: HEAD.append(i)
        else:
            if "<head" in x: HEAD.append(i)
        if x == "</head>": HEAD.append(i)

        if "<body" in x:
            if publisher == 4:
                if x == "<body>": BODY.append(i)
            else: BODY.append(i)
        if publisher == 5:
            if "<bibliography " in x: BODY.append(i)
        else:
            if x == "</body>": BODY.append(i)

        if "<floats" in x: FLOATS.append(i)
        if x == "</floats>": FLOATS.append(i)

    return HEAD, BODY, FLOATS



def extract_text(XML, HEAD, BODY, FLOATS, publisher):
    ART_TITLE, ABSTRACT, FIG, TABLE, TXT_BODY, TABLE_PART = [], [], [], [], [], []

    CHECK_J = []
    PART = [[HEAD], [BODY, FLOATS], [BODY]]
    END_TAG = [["</article-title>", "</abstract>"], ["</fig>", "</table-wrap>"], ["</p>", "</label>", "</title>", "</equation>"]]
    for i in range(len(PART)):
        for part in PART[i]:
            if part == []: continue
            for j in range(part[0], part[1] + 1):
                x = XML[j]
                for end_tag in END_TAG[i]:
                    start_tag = end_tag.replace("/", "")
                    if start_tag[:-1] in x:
                        if end_tag == "</article-title>":
                            if publisher == 5:
                                if not XML[j + 1].startswith('<title type="main">'): continue
                                else: end_tag, j = "</title>", j + 1
                        elif end_tag == "</abstract>":
                            if publisher == 2:
                                if not "<abstract " in x or not 'class="author"' in x: continue
                            elif publisher == 4:
                                if not "<abstract " in x: continue
                        j_end = iter_end(XML, CHECK_J, j, end_tag)                           # def
                        if j_end == -1: continue
                        text = extract_part_text(XML, CHECK_J, j, j_end, publisher)          # def
                        if end_tag in ["</fig>", "</table-wrap>"]:
                            for k in range(j, j_end): CHECK_J.append(k)
                        if end_tag == "</table-wrap>": TABLE_PART.append([j, j_end])
                        if text == "": continue
                        if publisher == 5:
                            if start_tag == "<article-title>": end_tag = "</article-title>"
                        X = [start_tag, text, end_tag]
                        if end_tag == "</article-title>": ART_TITLE = X
                        elif end_tag == "</abstract>": ABSTRACT = X
                        elif end_tag == "</fig>": FIG.extend(X)
                        elif end_tag == "</table-wrap>": TABLE.extend(X)
                        else: TXT_BODY.extend(X)

                if part == HEAD:
                    if ART_TITLE != [] and ABSTRACT != []: break

    ART_TITLE.extend(ABSTRACT)
    ART_TITLE.extend(TXT_BODY)
    ART_TITLE.extend(FIG)
    ART_TITLE.extend(TABLE)


    return ART_TITLE, TABLE_PART



def iter_end(DATA, CHECK_J, i, end):
    i_end = -1
    start = end.replace("/", "")
    for j in range(i + 1, len(DATA)):
        if j in CHECK_J: continue
        if DATA[j] == end:
            i_end = j
            break
        elif DATA[j].startswith(start) or DATA[j].startswith(start[:-1] + " "): break

    return i_end



def extract_part_text(XML, CHECK_J, i, i_end, publisher=None):
    import re

    text = ""
    for j in range(i, i_end + 1):
        if j in CHECK_J: continue
        x = XML[j]
        if publisher == 3: x = re.sub(r"Electronic supplementary information .+", "", x)
        elif publisher == 4:
            m = re.search(r"<Supesrscript>[a-z]</Superscript>", x)
            if m: x = x.replace(m.group(), m.group()[13:14] + " ")
            if '"TEX"' in x: continue
        if x in ["<p>", "</p>", "<label>", "</label>"]: text += " "
        else:
            if re.search(r"^<[^>]+>[^>]+</[^>]+>", x): inter_char = ""
            else: inter_char = " "
            x = delete_XML_tags(x)                                                     # def
            if x != "": text += inter_char + x

    text = re.sub(r"\s{2,}", " ", text)    # More than two spaces.
    text = text.lstrip()
    text = text.rstrip()


    return text



def delete_XML_tags(x):
    import re

    x = re.sub(r'<[^>]*hsp sp="[^>]+>', " ", x)            # Replace a space. Elsevier.
    x = x.replace("<br/>", " ")                            # Replace a space. Elsevier.

    s1 = re.search(r"<\s?-?[0-9]+", x)                     # sign of inequality, "<-1" or "< -1"
    s2 = re.search(r"<<", x)                               # "<<"
    if s1: x = x.replace(s1.group(), "s1abcdefgh")
    if s2: x = x.replace(s2.group(), "s2abcdefgh<")

    x = re.sub(r"<[^>]+>", "", x)

    if s1: x = x.replace("s1abcdefgh", s1.group())
    if s2: x = x.replace("s2abcdefgh", "<")


    return x



def edit_text(TXT):
    for i in range(len(TXT)):
        TXT[i] = TXT[i].replace(" ", " ").replace(" ", " ").replace("–", "-").replace("−", "-").replace("‐", "-").replace("∕", "/").replace("μ", "µ")    # Unify characters.

    return TXT



def thead_tbody(XML, start, end):
    THEAD, TBODY = [], []
    for i in range(start, end + 1):
        x = XML[i]
        if "<thead" in x:
            THEAD.append([])
            THEAD[-1].append(i)
        elif x == "</thead>": THEAD[-1].append(i)
        elif "<tbody" in x:
            TBODY.append([])
            TBODY[-1].append(i)
        elif x == "</tbody>":
            TBODY[-1].append(i)
        if len(THEAD) == len(TBODY) - 1: THEAD.insert(0, [])

    return THEAD, TBODY



def tlabel_tcaption_tfootnote(XML, publisher, start, end):
    import re

    CHECK_J = []
    T_ID = ['id="tbl[1-9][0-9]*[^"]*', "", 'id="tab[1-9][0-9]*[^"]*', 'ID="Tab[1-9][0-9]*[^"]*', 'tbl-0+[1-9][0-9]*[^"]*']

    tlabel, tcaption, tfoot, colnum = "Table noNo", "non", "non", 0
    TFOOT, TGROUP = [], []
    for i in range(start, end + 1):
        x = XML[i]

        if "<table-wrap" in x:
            if publisher != 2:    # Other than Elsevier
                pat = re.compile(r"%s" % T_ID[publisher - 1])
                m = pat.search(x)
                if m: tlabel = "Table " + m.group()[(len(T_ID[publisher - 1]) - 16):]
        if tlabel == "Table noNo":
            m = re.search(r"Table.[0-9]+.?", x)
            if m: tlabel = m.group()

        if "<title" in x:
            i_end = iter_end(XML, CHECK_J, i, end="</title>")                                 # def
            if i_end != -1:
                text = extract_part_text(XML, CHECK_J, i, i_end, publisher)                   # def
                if text != "": tcaption = text

        if "<tfoot" in x:
            i_end = iter_end(XML, CHECK_J, i, end="</tfoot>")                                 # def
            if i_end != -1:
                text = extract_part_text(XML, CHECK_J, i, i_end, publisher)                   # def
                if text != "": TFOOT.append(text)

        if "<tgroup" in x:
            n = re.search(r'cols="[0-9]+"', x)
            if n: tgroup = int(n.group()[6:-1])
            TGROUP.append(tgroup)
        if "<colspec" in x:
            n = re.search(r'colname="col[0-9]+', x)
            if n:
                if colnum < int(n.group()[12:]): colnum = int(n.group()[12:])

    if colnum < max(TGROUP): colnum = max(TGROUP)

    m = re.search(r"0+[1-9][0-9]*", tlabel)
    if m: tlabel = tlabel.replace(m.group(), str(int(m.group())))

    if TFOOT != []: tfoot = " ".join(TFOOT)

    return tlabel, tcaption, tfoot, colnum



def count_row(ROW, XML, start, end):
    for i in range(start, end + 1):
        x = XML[i]
        if "<row" in x:
            ROW.append([])
            ROW[-1].append(i)
        elif "</row>" in x:
            ROW[-1].append(i)

    return ROW



def embed_table_cell_datum(colnum, ROW, XML, publisher):
    import re

    CHECK_J = []

    TABLE = [["" for b in range(colnum)] for a in range(len(ROW))]

    cnt_multi_col, cnt_multi_row = 0, 0
    for i, row_id in enumerate(ROW):
        end_col = 0
        headbody = row_id[2]
        for j in range(row_id[0], row_id[1] + 1):
            if XML[j].startswith("<entry"):
                if re.search(r"<entry[^>]*?/>", XML[j]): tcd = "non"
                else:
                    j_end = iter_end(XML, CHECK_J, j, end="</entry>")                      # def
                    tcd = extract_part_text(XML, CHECK_J, j, j_end, publisher)             # def

                # Embed table cell data (tcd).
                n = re.search(r'colname="col[0-9]+', XML[j])
                o = re.search(r'namest="col[0-9]+', XML[j])
                p = re.search(r'nameend="col[0-9]+', XML[j])
                r = re.search(r'morerows="[0-9]+', XML[j])

                start_col, align = 0, ""
                if n:
                    end_col = int(n.group()[12:])
                    TABLE[i][end_col - 1] = tcd
                elif o and p:
                    cnt_multi_col = 1
                    start_col = int(o.group()[11:])
                    end_col = int(p.group()[12:])
                    if headbody == "thead":
                        for k in range(start_col - 1, end_col): TABLE[i][k] = tcd
                    else: TABLE[i][start_col - 1] = tcd
                else:
                    end_col += 1
                    for k in range(end_col - 1, len(TABLE[i])):
                        if TABLE[i][k] != "": end_col += 1
                        else: break
                    TABLE[i][end_col - 1] = tcd

                if r:
                    cnt_multi_row = 1
                    end_row = int(r.group()[10:])
                    if headbody == "thead": tcd = "non2"
                    for a in range(end_row):
                        if o and p:
                            for b in range(start_col - 1, end_col): TABLE[i + a + 1][b] = tcd
                        else: TABLE[i + a + 1][end_col - 1] = tcd


    return TABLE, cnt_multi_col, cnt_multi_row



def edit_table(TABLE, tlabel, tcaption, tfoot, cntthead, cnt_multi_col, cnt_multi_row, cnt_merged):
    for i in range(len(TABLE)):
        for j in range(len(TABLE[i])):
            if TABLE[i][j] in ["", "non2"]: TABLE[i][j] = "non"
        TABLE[i] = "\t".join(TABLE[i])

    TABLE.insert(0, tcaption)
    TABLE.insert(0, tlabel)
    x = "thead={}, multi_col={}, multi_row={}, merged={}".format(str(cntthead), str(cnt_multi_col), str(cnt_multi_row), str(cnt_merged))
    TABLE.insert(0, x)
    tfoot = "(Footnote) " + tfoot
    TABLE.append(tfoot)

    for i in range(len(TABLE)):
        TABLE[i] = TABLE[i].replace(" ", " ").replace(" ", " ").replace("–", "-").replace("−", "-").replace("‐", "-").replace("∕", "/").replace("μ", "µ")    # Unify characters.


    return TABLE



def edit_for_output_2(OUTPUT):
    OUTPUT_2 = []
    for x in OUTPUT:
        OUTPUT_2.extend(x)
        OUTPUT_2.append("")
    del OUTPUT_2[-1]

    return OUTPUT_2




# Main
if __name__ == "__main__": main()


