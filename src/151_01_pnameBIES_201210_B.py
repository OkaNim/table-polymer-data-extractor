# -*- coding: utf-8 -*-


def main():

    import os, shutil


    indir = "/mnt/c/Oka/Sagyou/151_polymer-name-ML/out/01_PDF/05_copoly149"    #out/01_PDF/01_AIP277"  C:\Oka\Sagyou\151_polymer-name-ML\
    outdir = "/mnt/c/Oka/Sagyou/151_polymer-name-ML/out/02_pnameBIES/06_201022/copoly149"
    indir2 = "/mnt/c/Oka/Sagyou/151_polymer-name-ML/data/CA/CA_bioes"
    INFNAME02 = os.listdir(indir2)

    curdir = os.getcwd()
    newdir = curdir + "/tmpdir"
    if "tmpdir" in os.listdir(curdir): shutil.rmtree(newdir)
    os.makedirs(newdir, exist_ok = True)


    INFNAME0 = os.listdir(indir)
    INFNAME = []
    for x in INFNAME0:
        if x[-4:] in [".pdf", ".PDF", ".tok"]:
            # y = x[:-4] + ".te.bioes"
            # if y in INFNAME02: continue    # AIP277から103は省く
            INFNAME.append(x)

    cntinput = 0
    for infname in INFNAME:
        cntinput += 1
        print(cntinput, infname)
        # if cntinput < 308: continue

        pdfbox(indir, newdir, infname)               # Function

        SCoreNLP(indir, newdir, infname)             # Function

        # newdir = indir
        TOK, TAG = pnameBIES(newdir, infname)        # Function


        # Output
        os.chdir(outdir)
        outfname = infname[:-4] + ".bioes"
        with open(outfname, "w", encoding = "utf-8") as outf:
            for i in range(len(TOK)):
                x = TOK[i] + "\t" + TAG[i]
                print(x, file = outf)
                if TOK[i] == ".": print("", file = outf)




# Function
def pdfbox(indir, newdir, infname):

    import os, subprocess
    from subprocess import PIPE

    outfname = infname.replace(".pdf", ".txt")
    srcdir = "/mnt/c/Oka_b/pdfbox"
    CMD = ["java -jar ", srcdir, "/pdfbox-app-2.0.20.jar ExtractText ", indir, "/", infname, " ", newdir, "/", outfname]
    subprocess.run("".join(CMD), shell = True, stdout = PIPE, stderr = PIPE)



def SCoreNLP(indir, newdir, infname):

    import os, subprocess
    from subprocess import PIPE

    infname = infname.replace(".pdf", ".txt")
    srcdir = "/mnt/c/Oka_b/stanford-corenlp-4.1.0"
    CMD = ["java -cp ", srcdir, '/"*" edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit -file ', newdir, "/", infname, " -outputFormat conll -output.columns word -outputDirectory ", newdir]
    subprocess.run("".join(CMD), shell = True, stdout = PIPE, stderr = PIPE)



def pnameBIES(newdir, infname):

    import os, sys

    infname = infname.replace(".pdf", ".txt.conll")    # ".tok"
    TOK = []
    os.chdir(newdir)
    with open(infname, "r", encoding = "utf-8") as inf:
        for x in inf:
            x = x.rstrip()
            if x != "": TOK.append(x)

    srcdir = "/mnt/c/Oka_b/mysrc"
    sys.path.append(srcdir)
    from pkg0039_pnameBIES import src0039_200728    # Package
    TAG = src0039_200728.pnameBIES(srcdir, TOK)


    return TOK, TAG




# Main
main()




