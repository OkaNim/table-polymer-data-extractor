# -*- coding: utf-8 -*-


import os, sys, re


INDIR, OUTDIR = sys.argv[1], sys.argv[1]
FDIR = os.getcwd() + "/152_01_file"


# 入力および出力ファイルの拡張子指定
inext1 = ".xml"
outext1, outext2, outext3 = ".txt", ".tsv", ".xml2"



# 補助ファイルの入力
CODE, SIGN = [], []
os.chdir(FDIR)
"""
in_f = open("HTMLXMLchar_190718.txt", "r", encoding = "utf-8").readlines()    # HTMLXMLchar
for x in in_f:
  x = x.rstrip()
  x = x.split("\t")
  CODE.append(x[0])
  SIGN.append(x[2])
"""

in_f = open("XMLTAG_201210.dat", "r", encoding = "utf-8").readlines()    # XMLTAG
XMLTAG = []
for x in in_f:
  x = x.rstrip()
  x = x.split("\t")
  if x[0] == "STANDARD":
    for i in range(len(x)):
      XMLTAG.append([])
  else:
    for i in range(len(x)):
      if x[i] != "" and x[i] != "_":
        y2 = x[i]
        if "/" in y2:
          y1 = y2[:-1].replace("/", "")
          XMLTAG[i].append(y1)
        XMLTAG[i].append(y2)



# 関数
def bra(x):
  s1 = re.search(r"<\s?-?[0-9]+", x)        # "<-1"または"< -1"のときの対策 （"<"をブラと判断し、削除してしまう）
  s2 = re.search(r"<.>", x)               # "<1 character>"の対策 ("<p>"は除く)
  s3 = re.search(r"<<", x)                # "<<"の対策
  if s1:
    x = x.replace(s1.group(), "s1abcdefgh")
  if s2:
    if s2.group() == "<p>":
      x = x.replace(s2.group(), "s2abcdefgh")
  if s3:
    x = x.replace(s3.group(), "s3abcdefgh<")
  x = re.sub(r"<[^>]*?>", "", x)
  if s1:
    x = x.replace("s1abcdefgh", s1.group())
  if s2:
    if s2.group() == "<p>":
      x = x.replace("s2abcdefgh", s2.group())
  if s3:
    x = x.replace("s3abcdefgh", "<")
  return x



# 本処理
fnames = os.listdir(INDIR)
f1names = []
for x in fnames:
  if x.endswith(inext1) or x.endswith(inext1.upper()):
    if x.endswith(inext1.upper()):
      inext1 = inext1.upper()
    f1names.append(x)



TABLE_TYPE = []
all_multi_col, all_multi_row, all_merged = 0, 0, 0
cntinput = 0
for f1name in f1names:
  cntinput += 1
  # if not "macromol" in f1name:    # 途中から開始する用
    # continue
  print(cntinput, f1name)


  # ファイル名でどの出版社かを決める
  if "acs" in f1name:
    publisher = 1
  elif "DOI" in f1name or "test" in f1name:
    publisher = 2
  elif ".XML" in f1name:
    publisher = 3
  elif "999" in f1name:
    publisher = 4
  elif "989" in f1name:
    publisher = 5



  os.chdir(INDIR)
  in_f = open(f1name, "r", encoding = "utf-8").readlines()
  SENT0 = []
  for x in in_f:
    x = x.rstrip()

    # タグの整理 1
    for i in range(len(XMLTAG[1])):
      y = XMLTAG[publisher][i]
      z = XMLTAG[0][i]
      if y in x:
        x = x.replace(y, "\n" + z)
    x = x.split("\n")
    for y in x:
      SENT0.append(y)

  # タグの整理 2
  SENT = []
  for x in SENT0:
    for y in XMLTAG[0]:
      if not ">" in y:
        y += "[^>]*?>"
      pat = re.compile(r"%s"% y)
      m = re.search(pat, x)
      if m:
        x = x.replace(m.group(), "\n" + m.group() + "\n")
        break
    x = x.split("\n")
    for y in x:
      if re.search(r'colname="[0-9]+', y):
        y = y.replace('colname="', 'colname="col')
      if re.search(r'namest="[0-9]+', y):
        y = y.replace('namest="', 'namest="col')
      if re.search(r'nameend="[0-9]+', y):
        y = y.replace('nameend="', 'nameend="col')
      if  re.search(r'colname="c[0-9]+', y):
        y = y.replace('colname="c', 'colname="col')
      if re.search(r'namest="c[0-9]+', y):
        y = y.replace('namest="c', 'namest="col')
      if re.search(r'nameend="c[0-9]+', y):
        y = y.replace('nameend="c', 'nameend="col')
      y = y.lstrip()
      if y != "":
        SENT.append(y)



  # HTMLXMLcharの変換
  for i in range(len(SENT)):
    for k in range(len(CODE)):
      if CODE[k] in SENT[i]:
        SENT[i] = SENT[i].replace(CODE[k], SIGN[k])



  # xml2ファイルの保存
  outxml2 = 0
  if outxml2 == 1:
    os.chdir(OUTDIR)
    f2name = f1name.replace(inext1, outext3)
    with open(f2name, "w", encoding = "utf-8") as out_f:
      for x in SENT:
        print(x, file = out_f)



  # txt抽出
  arttitle_i, arttitle_k, floats_i, floats_k, abstract_i, abstract_k, body_i, body_k = 0, 0, 0, 0, 0, 0, 0, 0
  cntabst = 0
  for i in range(len(SENT)):
    if "<article-title" in SENT[i]:
      arttitle_i = i
    elif "</article-title>" in SENT[i]:
      arttitle_k = i
    elif "<floats" in SENT[i]:
      floats_i = i
    elif "</floats>" in SENT[i]:
      floats_k = i
    elif "<abstract" in SENT[i]:
      if publisher == 1:
        if abstract_i == 0:
          abstract_i = i
      elif publisher == 2:
        if 'class="author"' in SENT[i]:
          abstract_i = i
    elif "</abstract>" in SENT[i]:
      if publisher == 1:
        if abstract_k == 0:
          abstract_k = i
      elif publisher == 2:
        if abstract_i != 0 and abstract_k == 0:
          abstract_k = i
    elif "<body" in SENT[i]:
      body_i = i
    elif "</body>" in SENT[i]:
      body_k = i
      break



  TXT = []
  # <article-title>のところ
  y = ""
  for i in range(arttitle_i, arttitle_k + 1):
    x = SENT[i]
    x = bra(x)
    if x != "":
      y += " " + x
  y = y.lstrip()
  y = y.rstrip()
  TXT.append("<article-title>")
  TXT.append(y)
  TXT.append("</article-title>")

  # <abstract>のところ
  y = ""
  for i in range(abstract_i, abstract_k + 1):
    x = SENT[i]
    x = bra(x)
    x = x.replace("<p>", "")    # abstractでは<p>、</p>は入れない。
    if x != "":
      y += " " + x
  y = y.lstrip()
  y = y.rstrip()
  TXT.append("<abstract>")
  TXT.append(y)
  TXT.append("</abstract>")

  # <body>のところ
  for i in range(body_i, body_k + 1):
    x = SENT[i]
    cnty = 0
    for y2 in ["</body>", "</p>", "</title>", "</equation>", "</fig>", "</table-wrap>"]:
      y1 = y2.replace("/", "")
      if y1[:-1] in x:
        cnty = 1
        for z in XMLTAG[-1]:
          if z in x:
            cnty = 0
            break
        break
      elif y2 in x:
        cnty = 2
        break
    if cnty == 0:
      x = bra(x)
    elif cnty == 1:
      x = re.sub(r"<[^>]*?>", y1, x)
    TXT.append(x)

  # <floats>のところ
  if floats_i != 0:
    for i in range(floats_i, floats_k + 1):
      x = SENT[i]
      cnty = 0
      for y2 in ["</floats>", "</fig>", "</table-wrap>"]:
        y1 = y2.replace("/", "")
        if y1[:-1] in x:
          cnty = 1
          break
        elif y2 in x:
          cnty = 2
          break
      if cnty == 0:
        x = bra(x)
      elif cnty == 1:
        x = re.sub(r"<[^>]*?>", y1, x)
      if x != "<p>" and x != "</p>":    # figキャプションでは<p>、</p>は入れない。
        TXT.append(x)

  TXT2 = []
  for x in TXT:
    x = x.lstrip()
    if x != "":
      TXT2.append(x)



  # <floats>がないとき、figとtableを<floats>へ集める
  if floats_i == 0:
    FIG, TABLEWRAP, TXT3 = [], [], []
    cntfig, cnttablewrap = 0, 0
    for x in TXT2:
      if x == "<fig>":
        cntfig = 1
      elif x == "</fig>":
        FIG.append(x)
        cntfig = 0
      elif x == "<table-wrap>":
        cnttablewrap = 1
      elif x == "</table-wrap>":
        TABLEWRAP.append(x)
        cnttablewrap = 0

      if cntfig == 1 and cnttablewrap == 0:
        if x != "<p>" and x != "</p>":    # figキャプションでは<p>、</p>は入れない。
          FIG.append(x)
      elif cntfig == 0 and cnttablewrap == 1:
        if x != "<p>" and x != "</p>":    # tableの脚注キャプションでは<p>、</p>は入れない。
          TABLEWRAP.append(x)
      elif cntfig == 0 and cnttablewrap == 0:
        if x != "</fig>" and x != "</table-wrap>":
          TXT3.append(x)

    TXT4 = []
    for x in TXT3:
      TXT4.append(x)
    TXT4.append("<floats>")
    for x in FIG:
      TXT4.append(x)
    for x in TABLEWRAP:
      TXT4.append(x)
    TXT4.append("</floats>")
    TXT2 = TXT4

  TXT = TXT2


  """
  # txtファイルの保存
  os.chdir(OUTDIR)
  f2bname = f1name.replace(inext1, outext1)
  with open(f2bname, "w", encoding = "utf-8") as out_f:
    for x in TXT:
      print(x, file = out_f)
  """


  # Table抽出
  TABLEINFO = []
  for i in range(len(SENT)):
    if "<table-wrap" in SENT[i]:
      TABLEINFO.append([])
      TABLEINFO[-1].append(i)
    elif "</table-wrap>" in SENT[i]:
      TABLEINFO[-1].append(i)

  if len(TABLEINFO) > 0:
    TABLE_PAPER = []
    for i in range(len(TABLEINFO)):
      colnum, tlabel, tcaption, tfoot, cntm, cnttfoot = 0, "Table noNo", "", "", 0, 0
      TGROUP, THEAD, TBODY, HEADBODY = [], [], [], []
      for k in range(TABLEINFO[i][0], TABLEINFO[i][1] + 1):
        cnt_multi_col, cnt_multi_row, cnt_merged = 0, 0, 0
        
        x = SENT[k]

        # Tableラベルの取得
        if "<table-wrap" in x:
          tlabel = re.findall("[0-9]+", x)
          tlabel = "".join(tlabel)
          tlabel = "Table " + tlabel
        m = re.search(r"Table.[0-9]+.?", x)
        if cntm == 0 and m:
          tlabel = m.group()
          tlabel = tlabel.replace(" ", " ")
          cntm = 1

        # キャプションの取得
        if "<caption" in x:
          for j in range(0, 10):
            if "</caption>" in SENT[k + j]:
              j2 = j
              break
          for j in range(0, j2 + 1):
            y = SENT[k + j]
            y = bra(y)
            y = y.replace("<p>", "")
            if y != "":
              tcaption += " " + y
          tcaption = tcaption.lstrip()

        # 列数の取得１
        if "<tgroup" in x:
          n = re.search(r'cols="[0-9]+"', x)
          if n: tgroup = int(n.group()[6:-1])
          TGROUP.append(tgroup)
        # 列数の取得２
        if "<colspec" in x:
          n = re.search(r'colname="col[0-9]+', x)
          if n:
            if colnum < int(n.group()[12:]):
              colnum = int(n.group()[12:])


        # thead、tbodyの取得
        if "<thead" in x:
          THEAD.append([])
          THEAD[-1].append(k)
        elif x == "</thead>":
          THEAD[-1].append(k)
        elif "<tbody" in x:
          TBODY.append([])
          TBODY[-1].append(k)
        elif x == "</tbody>":
          TBODY[-1].append(k)
        if len(THEAD) == len(TBODY) - 1:
          THEAD.insert(0, [])

        # 脚注の取得
        if "<tfoot" in x:
          for j in range(0, TABLEINFO[i][1] + 1):
            if "</tfoot>" in SENT[k + j]:
              j2 = j
              break
          for j in range(0, j2 + 1):
            y = SENT[k + j]
            y = bra(y)
            y = y.replace("<p>", "")
            if y != "":
              tfoot += " " + y
          tfoot = tfoot.lstrip()


      # Table内容の取得
      if len(THEAD) == 0: continue


      # 列数の決定
      if colnum < max(TGROUP): colnum = max(TGROUP)


      if len(THEAD) > 1: cnt_merged = 1
      for t in range(len(THEAD)):
        # row数を数える
        ROW = []
        cntthead = 0
        if len(THEAD[t]) > 0:
          for k in range(THEAD[t][0], THEAD[t][1] + 1):
            x = SENT[k]
            if "<row" in x:
              ROW.append([])
              ROW[-1].append(k)
            elif "</row>" in x:
              ROW[-1].append(k)
              HEADBODY.append("thead")
            cntthead = len(ROW)
        for k in range(TBODY[t][0], TBODY[t][1] + 1):
          x = SENT[k]
          if "<row" in x:
            ROW.append([])
            ROW[-1].append(k)
          elif "</row>" in x:
            ROW[-1].append(k)
            HEADBODY.append("tbody")



        # Tableの枠を作る
        TABLE = []
        for k in range(len(ROW)):
          exec("ROW_%d = []" % (k))
          for j in range(colnum):
            exec("ROW_%d.append('')" % (k))
          exec("TABLE.append(ROW_%d)" % (k))


        # Table情報の取得
        for k in range(len(ROW)):
          num2 = 0
          for j in range(ROW[k][0], ROW[k][1] + 1):
            if SENT[j].startswith("<entry"):

              # セル中の文字列を取得する
              x = ""
              if re.search(r"<entry[^>]*?/>", SENT[j]):
                x = "non"
              else:
                for m in range(0, 50):
                  if "</entry>" in SENT[j + m]:
                    m2 = m
                    break
                for m in range(0, m2 + 1):
                  y = SENT[j + m]
                  if not '="TEX"' in y:
                    y = bra(y)
                    y = y.replace("<p>", "")
                    if y != "":
                      x += " " + y
                x = x.lstrip()


              # タグ内の情報をチェックする
              n = re.search(r'colname="col[0-9]+', SENT[j])
              o = re.search(r'namest="col[0-9]+', SENT[j])
              p = re.search(r'nameend="col[0-9]+', SENT[j])
              num, align = 0, ""
              if n:
                num2 = int(n.group()[12:])
                TABLE[k][num2 - 1] = x
              elif o and p:
                cnt_multi_col = 1
                num = int(o.group()[11:])
                num2 = int(p.group()[12:])
                if HEADBODY[k] == "thead":                      # <thead>の場合
                  for a in range(num - 1, num2):
                    TABLE[k][a] = x
                elif HEADBODY[k] == "tbody":                    # <tbody>の場合
                  TABLE[k][num - 1] = x
              else:
                num2 += 1
                for a in range(num2 - 1, ROW[k][1] + 1):
                  if TABLE[k][a] != "":
                    num2 += 1
                  else:
                    break
                TABLE[k][num2 - 1] = x


              # morerows(rowspan)のチェック
              r = re.search(r'morerows="[0-9]+', SENT[j])
              if r:
                cnt_multi_row = 1
                rnum = int(r.group()[10:])
                if HEADBODY[k] == "thead":    # <thead>の場合は繰り返して文字列を記載しない。
                  x = "non2"
                if o and p:
                  for a in range(rnum):
                    for b in range(num - 1, num2):
                      TABLE[k + a + 1][b] = x
                else:
                  for a in range(rnum):
                    TABLE[k + a + 1][num2 - 1] = x


        if len(TABLE) > 1:
          for k in range(len(TABLE)):   # TABLE内で""をチェックし、あれば"non"とする
            for j in range(len(TABLE[k])):
              if TABLE[k][j] == "" or TABLE[k][j] == "non2":
                TABLE[k][j] = "non"
          for i in range(len(TABLE)): TABLE[i] = "\t".join(TABLE[i])
          if tcaption == "":  tcaption = "non"
          TABLE.insert(0, tcaption)
          TABLE.insert(0, tlabel)
          TABLE.insert(0, "thead=" + str(cntthead) + ", multi_col=" + str(cnt_multi_col) + ", multi_row=" + str(cnt_multi_row) + ", merged=" + str(cnt_merged))
          if cnttfoot == 0:
            if tfoot == "": tfoot = "(Footnote) non"
            else: tfoot = "(Footnote) " + tfoot
            cnttfoot = 1
          TABLE.append(tfoot)

          TABLE_PAPER.append(TABLE)

          X = [f1name, tlabel, str(cnt_multi_col), str(cnt_multi_row), str(cnt_merged)]
          if not X in TABLE_TYPE:
              TABLE_TYPE.append(X)
              all_multi_col += cnt_multi_col
              all_multi_row += cnt_multi_row
              all_merged += cnt_merged



    # tsvファイルの出力
    if TABLE_PAPER != []:
      os.chdir(OUTDIR)
      f2cname = "01_" + f1name.replace(inext1, outext2)
      with open(f2cname, "w", encoding = "utf-8") as out_f:
        for i, table in enumerate(TABLE_PAPER):
          for x in table: print(x, file = out_f)
          if i < len(TABLE_PAPER) - 1: print("", file = out_f)



print("")
print("all_multi_col =", all_multi_col, "\t", "all_multi_row=", all_multi_row, "\t", "all_merged =", all_merged)
print("")


# TABLE_TYPEの出力
outfname = "01_table-type.dat"
os.chdir(OUTDIR)
with open(outfname, "w", encoding = "utf-8") as outf:
  X = ["file-name", "tlabel", "multi_col", "multi_row", "merged"]
  x = "\t".join(X)
  print(x, file = outf)
  for x in TABLE_TYPE:
    x = "\t".join(x)
    print(x, file = outf)
  X = ["sum", "sum", str(all_multi_col), str(all_multi_row), str(all_merged)]
  x = "\t".join(X)
  print(x, file = outf)



