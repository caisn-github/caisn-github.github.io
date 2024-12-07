#!bin/bash
function readFile() {
   cat 1.1 | while read line
      do
              len2=${#line}
              echo ${line: 0: len2-3}
              mkdir ${line: 0: len2-3}
              cp *.png ${line: 0: len2-3}
              # echo [${path}]
              ## mkdir ./path
      done
}

function mvImage() 
{
      rm 1.1
      find ./ -name "*.md" >> 1.1
      if [ ! -s 1.1 ];
      then echo "hello";
      else
          readFile
      fi

      rm *.png
      rm 1.1
}

function read_dir() {
	for subDir in  `ls $1`
	do 
		if [ -d $1"/"$subDir ]
		then 
	       	        echo ${subDir}
			read_dir $1"/"$subDir
                        cd $subDir
	       	        echo `pwd` 
			mvImage
		fi
	done
}

read_dir $1

