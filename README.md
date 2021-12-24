# table-polymer-data-extractor


## Requirements
[Merlin](https://github.com/hshindo/Merlin.jl)


## How to use (command lines)
#### Polymer data extraction from tables
python 152_01_xml_g_211224.py [input-dir (including .xml)] [output-dir]<br>
python 152_02_format-table-triple_g_211224.py [input dir (including .tsv)] [output-dir]<br>
julia 152_03_Merlin-predict.jl [input filename] [output filename]<br>
  (152_03_Merlin-predict.jl is located in the master branch.)<br>
python 152_04_property-specifier-search_g_211224.py [input dir (including .polymer.bioes] [output-dir] [index-term-file(e.g. Tg.txt)] [stop-word-file(e.g. Tg_NG.txt))] <br> 
python 152_05_table-data-extract_g_211224.py [input dir (including all.dat & .polymer.property.bioes)]  [output-dir]<br>
<br>


