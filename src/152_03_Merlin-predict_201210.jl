using LightNLP
using LightNLP.NER
using JLD2, FileIO


training = false

if training
    embedsfile = ".data/acstdm+elsevier.txt.clean.100d.h5"
    trainfile = ".data/predict.bioes"
    testfile = ".data/predict.bioes"
    nepochs = 20
    learnrate = 0.0005
    batchsize = 5
    ner = NER.Decoder(embedsfile, trainfile, testfile, nepochs, learnrate, batchsize)
    save("predict.jld2", "ner", ner)
else
    ner = load("152_03_file/polymername_588_06_06_acs720162017_201027.jld2", "ner")
    testfile = ARGS[1]
    decode(ner, testfile)
end
