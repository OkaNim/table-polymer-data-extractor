# table-polymer-data-extractor


# Requirements
[Merlin](https://github.com/hshindo/Merlin.jl) ver 0.0.0


# How to use (command lines)
#### Polymer name annotation
python 151_01_pnameBIES.py <input dir><br>
<br>
<br>
#### Extraction of polymer data from table
python 152_01_xml.py [input dir (including .xml)]<br>
python 152_02_format-table-triple.py [input dir (including .tsv)]<br>
julia 152_03_Merlin-predict.jl [input filename] [output filename]<br>
python 152_04_property-specifier-identify.py [input dir (including .polymer.bioes)] ("Tg", "Tm", and "Td" directories are automatically created.)<br>
python 152_05_table-data-extract.py [input dir (including _all.dat)]<br>


# References

