#!/bin/bash
echo ${1}
if [ ! -d /root/blog/snBlog/content/post/${1} ]; then
    mkdir /root/blog/snBlog/content/post/${1}
fi
cp -r ./${1}/* /root/blog/snBlog/content/post/${1}
cd /root/blog/snBlog
ls -a
git status
git fetch --all
git rebase 
git add content/*
git commit -m "add new article"
git push snDay main 
