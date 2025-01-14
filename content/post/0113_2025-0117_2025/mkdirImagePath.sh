#!bin/bash
rm 1.1
function readFile() {
   cat 1.1 | while read line
      do 
	      echo ${line}
	      len2=${#line}
	      echo ${len2}
	      echo ${line: 0: len2-3}
	      mkdir ${line: 0: len2-3}
              cp *.png ${line: 0: len2-3}
	      # echo [${path}] 
	      ## mkdir ./path
      done
}
find ./ -name "*.md" >> 1.1
if [ ! -s 1.1 ];
then echo "hello"; 
else 
	readFile
fi

rm *.png
rm 1.1
	
