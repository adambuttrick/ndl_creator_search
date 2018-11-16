# NDL Creator/Book Search

Prototype of a creator search for the National Diet Library digital collections holdings. See here for the reference dataset:

http://www.ndl.go.jp/en/dlib/standards/opendataset/index.html

Script assumes your searching the data for books that are available online from any location (Available Online/Books file in the table). Input is a list of creators in a text file (see sample data for an example) and the NDL tsv file dataset. Output is a CSV file, where headings have been been translated and some data parsed into additional fields (see sample data again). 

The representation of creators in the underlying data mushes together authors, illustrators, editors, and translator into a single field, which the script attempts to sort out. Dates are also converted from the Japanese imperial format into something like ISO 8601. 

# Usage:

search.py (creator list).txt (ndl dataset).tsv
