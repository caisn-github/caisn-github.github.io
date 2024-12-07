#!bin/bash
find ./ -name "*.md" >> 1.1
if [! -s 1.1];
then echo "hello"; 
fi

	
