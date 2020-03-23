#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 09:24:01 2020
@author: lkurth
"""

class Txt_Reader():
   
   def __init__(self):
      self._file_list=list()
      self._edited_list=list()
   
   def split_lines_by_comma(self, f):
      for zeile in f:
         zeile=f.readline()
         self._file_list.append(zeile)
         zeile=str.split(zeile,",",1)[0]
         zeile=str.split(zeile,"/",5)[5]
         self._edited_list.append(zeile)
      return self._edited_list
         
         
   
   def read_file(self, fname):
      self._file_list=list()
      self.edited_list=list()
      with open(fname,"r") as f:
         f=self.split_lines_by_comma(f)
         return f
      

if __name__=="__main__":        
   reader=Txt_Reader()
   f=reader.read_file("intext_meeg_filelist.txt")    
   print(f)