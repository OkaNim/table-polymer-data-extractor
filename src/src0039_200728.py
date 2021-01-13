def pnameBIES(curdir, TOK):


  import os, glob, sys, re



  # 補助ファイルの入力
  os.chdir(curdir + "/151_01_file")
  in_f = open("NGOKWpy_190521.txt", "r", encoding = "utf-8").readlines()
  NGOKW = [[], [], [], [], [], []]
  for x in in_f:
    x = x.rstrip()
    if not "0_NG_PVA_etc" in x:
      x = x.split("\t")
      for i in range(len(x)):
        if x[i] != "":
          if i == 3:
            x[i] = x[i].split()
          elif i == 5:
            x[i] = x[i].replace("-", " ")
            x[i] = x[i].split()
          NGOKW[i].append(x[i])




  # TAGの準備
  TAG = []
  for i in range(len(TOK)):
    TAG.append("O")



  # 正解タグ付け
  LKAKKO = ["(", "[", "{"]
  RKAKKO = [")", "]", "}"]
  for i in range(len(TOK)):
    # 1-4. 登録しているOKなポリマー名へタグ付け(Nafion、polyacrylic acidなど)
    for x in NGOKW[3]:
      if TOK[i] == x[0] and TAG[i] == "O":
        cntmatch = 1
        for k in range(1, len(x)):
          if i + k > len(TOK) -1: break
          if TOK[i + k] == x[k]:
            cntmatch += 1
        if len(x) == cntmatch:
          if len(x) == 1:
            TAG[i] = "S"
          elif len(x) > 1:
            TAG[i] = "B"
            for k in range(1, len(x)):
              if k == len(x) - 1:
                TAG[i + k] = "E"
              else:
                TAG[i + k] = "I"
              break



    # 1-1. ポリマー名　poly(～)、P(～)、p(～)など
    if re.fullmatch(r".*poly", TOK[i].lower()) or TOK[i].lower() == "p":
      cntkakko = 0
      for k in range(len(LKAKKO)):
        if i < len(TOK) - 1 and TOK[i + 1] == LKAKKO[k]:
          Lkakko = LKAKKO[k]
          Rkakko = RKAKKO[k]
          cntkakko = 1
          break

      if cntkakko == 1:
        cnt = 0
        for k in range(1, 31):
          if TOK[i + k] != Rkakko:
            cnt += 1
          else:
            break
          if i + k + 1 == len(TOK):
            break

        # ) までの ( の数を数える
        cnt_Lkakko = 0
        for k in range(1, cnt + 1):
          if TOK[i + k] == Lkakko:
            cnt_Lkakko += 1

        # ) までのkを調べる
        cnt_Rkakko = 0
        k2 = 0
        for k in range(1, 21):
          if i + k + 1 == len(TOK):
            break
          if TOK[i + k] == Rkakko:
            cnt_Rkakko += 1
            if cnt_Rkakko == cnt_Lkakko:
              k2 = k
              break

        # BIOESタグ付け
        if k2 > 0:
          for k in range(0, k2 + 1):
            if k == 0:
              TAG[i + k] = "B"
            elif k == k2:
              TAG[i + k] = "E"
            else:
              TAG[i + k] = "I"



    # 1-2. ポリマー名 省略型(3 character 以上)  PVAなど
    if TOK[i] != TOK[i].lower() and TAG[i] == "O" and not "." in TOK[i]:
      if len(TOK[i]) == 2:
        for x in NGOKW[4]:
          pat = re.compile(r"%s"% x)
          if re.fullmatch(pat, TOK[i]):
            TAG[i] = "S"
            break
      elif len(TOK[i]) > 2:
        # OKWのチェック (NGOKW[4])
        cntNGW = 0
        for x in NGOKW[4]:
          pat = re.compile(r"%s"% x)
          if re.fullmatch(pat, TOK[i]):
            TAG[i] = "S"
            cntNGW = 1
            break

        # NGWのチェック(cntNGW, NGOKW[0])
        if cntNGW == 0:
          for x in NGOKW[0]:
            pat = re.compile(r"%s"% x)
            if re.fullmatch(pat, TOK[i]):
              cntNGW = 1
              break

        # OKWおよびNGWに該当しなかった場合
        if cntNGW == 0:
          cntU = len(re.findall("[A-Z]", TOK[i]))      # 大文字の数を数える (cntU)
          round = lambda x: (x*2+1)//2
          cntU2 = int(round(len(TOK[i]) * 0.6))        # 大文字のcharacterの条件(cntU2)
          cntP = len(re.findall("p", TOK[i].lower()))  # "p"または"P"の数を数える (cntU)
          cntN = len(re.findall("[0-9]", TOK[i]))      # 数字の数を数える (cntN)

          # "p"または"P"を含み、6割以上大文字なら、正解タグ付けする
          #  （最初、"p"または"P"でなく、6割以上数字なら、正解タグ付けしない）
          if cntP > 0 and cntU >= cntU2:
            if TOK[i][0].lower() == "p":
              TAG[i] = "S"
            elif cntU2 > cntN:
              TAG[i] = "S"



    # 1-3. ポリマー名　polystyrene など
    if re.search(r".*poly.+", TOK[i].lower()) and TAG[i] == "O":
      # NGWのチェック(cntNGW, NGOKW[1])
      cntNGW = 0
      for x in NGOKW[1]:
        pat = re.compile(r"%s"% x)
        if re.fullmatch(pat, TOK[i].lower()):
          cntNGW = 1
          break
      if cntNGW == 0 and not TOK[i].endswith("ed"):
        TAG[i] = "S"



    # 1-3-2. polyamide 66 など、polyamide後の数字に正解タグ付け
    for x in ["polyamide.*", "Polyamide.*", "nylon.*", "Nylon.*", "PA.*"]:
      pat = re.compile(r"%s"% x)
      if len(TOK) >= i + 4 and re.fullmatch(pat, TOK[i]) and TAG[i] != "O":
        if TOK[i + 1].isnumeric():
          if not "," in TOK[i + 2]:
            TAG[i], TAG[i + 1] = "B", "E"
          elif TOK[i + 2] == "," and TOK[i + 3].isnumeric():
            TAG[i], TAG[i + 1], TAG[i + 2], TAG[i + 3] = "B", "I", "I", "E"



    # 1-5. copolymer
    if TOK[i].lower() == "copolymer":
      k2 = 0

      # 1-5-1. A/B/C copolymer （/ でトークン分割されていない場合）
      if "/" in TOK[i - 1]:
        k2 = 1
        TAG[i - 1] = "B"
        TAG[i] = "E"

      # 1-5-2. A/B/C copolymer, A－B－C copolymers
      if k2 == 0:
        for k in range(1, 8):
          if i - k < 0: break
          if TOK[i - k] in ["-", "/"]:
            k2 = k
        if k2 > 1:
          for k in range(k2 + 2):
            if k == k2 + 1:
              TAG[i - k] = "B"
            elif k == 0:
              TAG[i - k] = "E"
            else:
              TAG[i - k] = "I"

      # 1-5-3. copolymer of A, B and C
      if i + 1 < len(TOK) - 1 and TOK[i + 1] == "of" and k2 == 0:
        for k in range(2, 8):
          if i + k > len(TOK) - 1: break
          if TOK[i + k] in ["and", "-", "/"]:
            k2 = k
            break
          if i + k + 1 == len(TOK):
            break
        if k2 > 2:
          for k in range(k2 + 2):
            if k == 0:
              TAG[i + k] = "B"
            elif k == k2 + 1:
              TAG[i + k] = "E"
            else:
              TAG[i + k] = "I"



    # 1-6. NGOKW[5]に登録しているcopolymer, plastic, resin, ABS resin　etc.
    if TOK[i].lower() in ["copolymer", "copolymers", "plastic", "plastics", "resin", "resins"] and TAG[i] == "O":
      cntTOK = 0
      k2 = 0
      for x in NGOKW[5]:
        if TOK[i - 1] == x[-1]:
          for k in range(1, len(x) * 2):
            if TOK[i - k] in x:
              cntTOK += 1
              if TOK[i - k] == x[0]:
                k2 = k
          if cntTOK == len(x):
            for k in range(k2 + 1):
              if k == k2:
                TAG[i - k] = "B"
              elif k == 0:
                TAG[i - k] = "E"
              else:
                TAG[i - k] = "I"

      if cntTOK == 0:
        for x in NGOKW[5]:
          if TOK[i - 1] == x:
            TAG[i - 1] = "B"
            TAG[i] = "E"
            break



  # 正解タグ付けの細かな修正
  # 2-1. 形容詞 (NGOKW[2])
  cntKeiyo = 1
  if cntKeiyo == 1:
    for i in range(len(TOK)):
      if TAG[i] in ["B", "S"]:
        for x in NGOKW[2]:
          pat = re.compile(r"%s"% x)
          if re.fullmatch(pat, TOK[i - 1].lower()):
            TAG[i - 1] = "B"
            if TAG[i] == "B":
              TAG[i] = "I"
            elif TAG[i] == "S":
              TAG[i] = "E"



  # 2-2. ポリマー名間を繋ぐ　"-"や"/"
  for i in range(len(TOK)):
    if TOK[i] in ["-", "/"]:
      if TAG[i - 1] == "E" and TAG[i + 1] == "B":
        TAG[i - 1], TAG[i], TAG[i + 1] = "I", "I", "I"
      elif TAG[i - 1] == "E" and TAG[i + 1] == "S":
        TAG[i - 1], TAG[i], TAG[i + 1] = "I", "I", "E"
      elif TAG[i - 1] == "S" and TAG[i + 1] == "S":
        TAG[i - 1], TAG[i], TAG[i + 1] = "B", "I", "E"
      elif TAG[i - 1] == "S" and TAG[i + 1] == "B":
        TAG[i - 1], TAG[i], TAG[i + 1] = "B", "I", "I"



  # 2-3. 30/70 blend など
  for i in range(len(TOK)):
    if re.fullmatch(r"blend.?", TOK[i - 1]):
      k2, cntblendnum = 0, 0
      for k in range(1, 8):
        if TAG[i - k] != "O":
          k2 = k
          break
        if k2 > 0:
          for k in range(1, k2):
            for x in [".+s", ".+.ed", "are", "were", "in", "the", "a", "an", "or", "\."]:
              pat = re.compile(r"%s"% x)
              if re.fullmatch(pat, TOK[i - k].lower()):
                k2 = 0
                break
          for k in range(1, k2):
            if TOK[i - k].isnumeric():
              cntblendnum = 1
              break
          if k2 > 0 and cntblendnum == 1:
            if TAG[i - k2] == "E":
              TAG[i - k2] = "I"
            else:
              TAG[i - k2] = "B"
            for k in range(1, k2):
              TAG[i - k] = "I"
            TAG[i] = "E"



  # 2-4. polymer 1a, colymer A などのサンプルIDで表記のもの
  ABB = []
  for i in range(len(TOK)):
    cntABB = 0
    if TOK[i].lower() in ["polymer", "copolymer"] and TAG[i] == "O":
      cntABB = 1
    elif TOK[i].lower() in ["polymers", "copolymers"] and TAG[i] == "O":
      for k in range(1, 8):
        if i + k > len(TOK) - 1: break
        if TOK[i + k] == "and":
          cntABB = k + 1
          break
    elif re.fullmatch(r".*poly.*", TOK[i].lower()) and TAG[i] == "S":
      cntABB = 1
    elif re.fullmatch(r".*poly", TOK[i].lower()) and TAG[i] == "B":
      for k in range(1, 11):
        if TAG[i + k] == "E":
          cntABB = k
          break
        if i + k + 1 == len(TOK):
          break
    elif TOK[i] == "denoted" and TAG[i + 1] == "O":
      for k in range(1, 8):
        if TAG[i - k] != "O":
          cntABB = 1
          break
        if i - k == 0 and cntABB == 0:
          break
        if cntABB > 0:
          if TOK[i - 1] == "is":
            cntABB = 1
          if TOK[i - 1] == "are":
            for k in range(1, 8):
              if TOK[i + k] == "and":
                cntABB = k + 1
                break
              if i + k + 1 == len(TOK):
                break
    if cntABB > 0:
      for k in range(1, cntABB + 1):
        if i + k > len(TOK) - 1: continue
        for x in ["[0-9]+[a-z]", "[A-Z]", "[A-Z]+[0-9]+"]:
          pat = re.compile(r"%s"% x)
          m = re.fullmatch(pat, TOK[i + k])
          if m and TAG[i + k] == "O":
            TAG[i + k] = "S"
            if not m.group() in ABB:
              ABB.append(m.group())
            break
        if i + k + 1 == len(TOK):
          break



  #ABBに登録されたポリマー名をTOK[0]からチェック
  checkABB = 1
  if checkABB == 1:
    for i in range(len(TOK)):
      if TOK[i] in ABB and TAG[i] == "O":
        TAG[i] = "S"



  # 2-5. A doped polymer など
  for i in range(len(TOK)):
    # 2-5-1. copolymer
    if TOK[i] == "doped" and TAG[i] != "O":
      cntU = len(re.findall("[A-Z]", TOK[i - 1]))    # 大文字の数を数える(cntU)
      round = lambda x: (x*2+1)//2                   # 大文字のcharacterの条件(cntU2)
      cntU2 = int(round(len(TOK[i - 1]) * 0.6))
      if cntU >= cntU2:
        TAG[i - 1] = "B"
        TAG[i] = "I"
        TAG[i + 1] = "E"



  return TAG


