## File Format Description

Extracted from [Ozone Watch File Format Description](https://ozonewatch.gsfc.nasa.gov/data/file_format_description.txt)

Each data file begins with three header lines of text that identify the date, the satellite instrument, and certain information related to production.

The header lines are followed by a sequence of multi-line groups. Each group of lines is terminated by a latitude identifier (e.g., " lat = -89.5"). Each group contains the data around a single latitude circle. The number of longitude points around the latitude circle is given in the header; they are equally-spaced within the longitude range described in the header. To read the numbers in the group, concatenate its text lines together and divide the resulting string of characters into three-character subgroups. Each subgroup is an integer representing the number of Dobson Units. For example, a string that stsrts with "250248249249250245" would be parsed into an array of numbers that starts with [ 250, 248, 249, 249, 250, 245 ] Dobson Units. If there are 288 longitude bins specified in the header, there will be 288 numbers to be extracted from the group. A value of 0 indicates that no measurement was taken at the corresponding gridpoint; this usually indicates polar night or a gap between successive orbital swaths. 

The number of groups in the file will of course be the same as the number of latitude bins specified in the header.