#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 11:57:02 2020
@author: lkurth
"""

import wx
#import wx.xrc
from file_reader import Txt_Reader
import os
from pubsub import pub

class ButtonPanel(wx.Panel):
   def __init__(self,parent):
      wx.Panel.__init__(self,parent,style=wx.BORDER_SUNKEN)
      self._bt_all = wx.Button(self,label="Select All",name=self.GetName()+".BT.ALL")
      self._bt_print = wx.Button(self,label="Print",name=self.GetName()+".BT.PRINT")
      #self._bt_del = wx.Button(self,label="Delete Selected",name=self.GetName()+".BT.DEL")
      self._bt_clear = wx.Button(self,label="Clear",name=self.GetName()+".BT.CLEAR")
      self._bt_apply = wx.Button(self,label="Apply",name=self.GetName()+".BT:APPLY")
      myButtonSizer=wx.BoxSizer(wx.HORIZONTAL)
      myButtonSizer.Add(self._bt_all,0,wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,5)
      myButtonSizer.Add(self._bt_print,0,wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,5)
      #myButtonSizer.Add(self._bt_del,0,wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,5)
      myButtonSizer.Add(self._bt_clear,0,wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,5)
      myButtonSizer.Add(self._bt_apply,0,wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,5)
      self.SetSizer(myButtonSizer)
      self.SetBackgroundColour("blue")
      
class LbBtPanel(wx.Panel):
   def __init__(self,parent,fname):
      wx.Panel.__init__(self,parent,style=wx.BORDER_SUNKEN)
      pub.subscribe(self.my_listener,"listBoxListener")
      self.reader=Txt_Reader()
      if os.path.exists(fname):
          choices = self.reader.read_file(fname)
      else:
          choices = list()
      self.mListBox=None
      self.Bind(wx.EVT_BUTTON,self.ClickOnButton)
      self.Bind(wx.EVT_LISTBOX,self.select)
      self.Bind(wx.EVT_MOTION,self.OnMouseMove)
      self.counter=0
      self.selectedItems=list()
      self.counter_text=wx.StaticText(self, wx.ID_ANY,(str)(self.counter)+"/0",wx.Point(-1,-1),wx.DefaultSize,0)
      self.counter_text.SetForegroundColour('red')
      if len(choices)>0:
          myListBoxSizer=wx.BoxSizer(wx.VERTICAL)
          myListBoxSizer.Add(self.counter_text,1,wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,5)
          self.mListBox = wx.ListBox(self,wx.ID_ANY,choices=choices,style=wx.LB_MULTIPLE) 
          self.mListBox.SetFont(wx.Font(12,75,90,90,False,wx.EmptyString))
          self.mListBox.SetToolTip("ListBox")
          myListBoxSizer.Add(self.mListBox,1,wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,5)
          self.btPanel=ButtonPanel(self)
          myListBoxSizer.Add(self.btPanel,0,wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.EXPAND,5)
          self.SetSizer(myListBoxSizer)
      else:
          fname=self.frame.OnOpen()
          choices=self.reader.read_file(fname)
          self.updateChoices(choices)
      self.update_counter_text()
   
   def my_listener(self,message,arg2=None):
       if message=="update":
            self.deleteAll()
            choices=self.reader.read_file(arg2)
            self.updateChoices(choices)
            #self.mListBox.InsertItems(items=self.reader.read_file(file),pos=0)
            self.update_counter_text()
            self.mListBox.Bind(wx.EVT_LISTBOX,self.select)
            self.mListBox.Bind(wx.EVT_MOTION,self.OnMouseMove)
   
   def ClickOnButton(self,event):
      obj=event.GetEventObject()
      if obj.GetLabel()=="Select All":
         self.selectAll()
      elif obj.GetLabel()=="Deselect All":
         self.deselectAll()
      elif obj.GetName().endswith(".BT.PRINT"):
         for i in self.selectedItems:
            print(self.reader._file_list[i])
      elif obj.GetName().endswith(".BT.DEL"):
         self.deleteSelectedItems()
      elif obj.GetName().endswith("BT.CLEAR"):
         self.deleteAll()
      elif obj.GetName().endswith("BT:APPLY"):
         pub.sendMessage("frame_listener", message="apply")
         
   def select(self,event):
        """Simulate CTRL-click on ListBox"""
        selection = self.mListBox.GetSelections()
        for i in selection:
            if i not in self.selectedItems:
                # add to list of selected items
                self.selectedItems.append(i)
                self.mListBox.Select(i)
                self.counter+=1
            elif len(selection) == 1:
                # remove from list of selected items
                self.selectedItems.remove(i)
                self.mListBox.Deselect(i)
                self.counter-=1
    
        for i in self.selectedItems:
            # actually select all the items in the list
            self.mListBox.Select(i)
            
        if len(self.selectedItems)==len(self.reader._file_list):
            self.btPanel._bt_all.SetLabel("Deselect All")
        else:
            self.btPanel._bt_all.SetLabel("Select All")
        self.update_counter_text()
        
        
   def selectAll(self):
      for i in range(len(self.reader._file_list)):
         self.mListBox.SetSelection(i)
         self.selectedItems.append(i)
      self.btPanel._bt_all.SetLabel("Deselect All")
      self.counter=len(self.reader._file_list)
      self.update_counter_text()
   
   def deselectAll(self):
      for i in self.mListBox.GetSelections():
         self.mListBox.Deselect(i)
      self.selectedItems.clear()
      self.btPanel._bt_all.SetLabel("Select All")
      self.counter=0
      self.update_counter_text()
      
   def deleteSelectedItems(self):
      if len(self.selectedItems)==0:
         pass
      else:
         selection=self.mListBox.GetSelections()
         selection.sort(reverse=True)
         for i in selection:
            self.mListBox.Delete(i)
            self.reader._file_list.pop(i)
         self.deselectAll()
         
   def deleteAll(self):
      self.mListBox.Clear()
      self.counter=0
      self.counter_text.SetLabel((str)(self.counter)+"/0")
      self.mListBox.SetToolTip("")
         
   def update_counter_text(self):
      self._maxFiles=len(self.reader._file_list)
      self.counter_text.SetLabel((str)(self.counter)+"/"+(str)(self._maxFiles))
   
   @property
   def frame(self):
      return self.GetParent().GetParent()
  
   def OnMouseMove(self, event):
        # Event handler for mouse move event. Updates current position of cursor in data coordinates.
        
        event.Skip()
        # get mouse position in window
        self.mousePos = self.ScreenToClient(wx.GetMousePosition())
        x, y = self.mousePos.Get()
        if self.mListBox.HitTest(x,y)!=wx.NOT_FOUND and len(self.reader._file_list)>1:
         self.mListBox.SetToolTip(self.reader._file_list[self.mListBox.HitTest(x,y)-1])
   
   def updateChoices(self,choices):
      if self.mListBox:
          self.mListBox.Clear()
          self.mListBox.AppendItems(choices)
      else:
          myListBoxSizer=wx.BoxSizer(wx.VERTICAL)
          myListBoxSizer.Add(self.counter_text,1,wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,5)
          self.mListBox = wx.ListBox(self,wx.ID_ANY,choices=choices,style=wx.LB_MULTIPLE) 
          self.mListBox.SetFont(wx.Font(12,75,90,90,False,wx.EmptyString))
          self.mListBox.SetToolTip("ListBox")
          myListBoxSizer.Add(self.mListBox,1,wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,5)
          self.btPanel=ButtonPanel(self)
          myListBoxSizer.Add(self.btPanel,0,wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.EXPAND,5)
          self.SetSizer(myListBoxSizer)
      self.selectAll()
      self.deselectAll()
      
class TreeCtrlPanel(wx.Panel):
    def __init__(self,parent):
      wx.Panel.__init__(self,parent)
      self.SetBackgroundColour("red")
      
      
class MyApp(wx.App):
   def OnInit(self):
      self.frame=MyFrame(None)
      self.SetTopWindow(self.frame)
      self.frame.Show()
      return True
   
class MyFrame(wx.Frame):
   def __init__(self,parent):
      wx.Frame.__init__(self,parent,id=wx.ID_ANY,title="JuMEG ListBox",pos=wx.DefaultPosition, size=wx.Size(500,400),style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
      pub.subscribe(self.my_listener,"frame_listener")
      
      fname="intext_meeg_filelist.txt"
      #fname=""
      
      self.Splitter=wx.SplitterWindow(self)
      
      """self.counter=0
      self.selectedItems=list()
      
      self.counter_text=wx.StaticText(self, wx.ID_ANY,(str)(self.counter)+"/0",wx.Point(-1,-1),wx.DefaultSize,0)
      self.counter_text.SetForegroundColour('red')"""
      
      """self.reader=Txt_Reader()
      if os.path.exists(fname):
          mListBoxChoices = self.reader.read_file(fname)
      else:
          mListBoxChoices = list()"""
      
      self._LbBtPanel=LbBtPanel(self.Splitter,fname)
      
      #self._LbBtPanel.Bind(wx.EVT_BUTTON,self.ClickOnButton)
      
      self._TreePanel=TreeCtrlPanel(self.Splitter)
      
      self.Splitter.SplitVertically(self._LbBtPanel,self._TreePanel)
      self.Splitter.SetSashGravity(0.5)
      
      self._menubar=wx.MenuBar()
      open_menu=wx.Menu()
      load_item=wx.MenuItem(open_menu,id=1,text="load",kind=wx.ITEM_NORMAL)
      open_menu.AppendItem(load_item)
      self._menubar.Append(open_menu, 'Menu')
      self.SetMenuBar(self._menubar)
      self.Bind(wx.EVT_MENU,self.menuhandler)
      
      #self._maxFiles=len(self.reader._file_list) 
      
      myBoxGridSizer=wx.BoxSizer(wx.VERTICAL)
      
      self.headerLabel = wx.StaticText(self, wx.ID_ANY,"JuMEG ListBox",wx.Point(-1,-1),wx.DefaultSize,0)
      self.headerLabel.Wrap(-1)
      self.headerLabel.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(),75,90,92,True,wx.EmptyString))
      
      myBoxGridSizer.Add(self.headerLabel,0,wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,5)
      myBoxGridSizer.Add(self.Splitter,1,wx.ALL | wx.EXPAND,5)
      self.SetSizer(myBoxGridSizer)
      self.Layout()
      
      self.Centre(wx.BOTH)
      
      """self.mListBox.Bind(wx.EVT_LISTBOX,self.select)
      self.mListBox.Bind(wx.EVT_MOTION,self.OnMouseMove)"""
      
      #self.update_counter_text()
    
   def my_listener(self,message,arg2=None):
       if message=="apply":
           self._TreePanel.SetBackgroundColour("green")
    
   @property
   def mListBox(self):
       return self._LbBtPanel.mListBox
   
   @property
   def bt_all(self):
       return self._LbBtPanel.btPanel._bt_all
    
   def menuhandler(self,event):
      id=event.GetId()
      if id==1:
         file=self.OnOpen()
         if file:
            pub.sendMessage("listBoxListener",message="update",arg2=file)
      
   """def OnMouseMove(self, event):
        # Event handler for mouse move event. Updates current position of cursor in data coordinates.
        
        event.Skip()
        # get mouse position in window
        self.mousePos = self.ScreenToClient(wx.GetMousePosition())
        x, y = self.mousePos.Get()
        if self.mListBox.HitTest(x,y)!=wx.NOT_FOUND and len(self.reader._file_list)>1:
         self.mListBox.SetToolTip(self.reader._file_list[self.mListBox.HitTest(x,y)-1])
        
   ef update_counter_text(self):
      self._maxFiles=len(self.reader._file_list)
      self.counter_text.SetLabel((str)(self.counter)+"/"+(str)(self._maxFiles))"""
   
   """def select(self,event):
    selection = self.mListBox.GetSelections()
    for i in selection:
        if i not in self.selectedItems:
            # add to list of selected items
            self.selectedItems.append(i)
            self.mListBox.Select(i)
            self.counter+=1
        elif len(selection) == 1:
            # remove from list of selected items
            self.selectedItems.remove(i)
            self.mListBox.Deselect(i)
            self.counter-=1

    for i in self.selectedItems:
        # actually select all the items in the list
        self.mListBox.Select(i)
        
    if len(self.selectedItems)==self._maxFiles:
        self.bt_all.SetLabel("Deselect All")
    else:
        self.bt_all.SetLabel("Select All")
    self.update_counter_text()
        
        
   def selectAll(self):
      for i in range(self._maxFiles):
         self.mListBox.SetSelection(i)
         self.selectedItems.append(i)
      self.bt_all.SetLabel("Deselect All")
      self.counter=self._maxFiles
      self.update_counter_text()
   
   def deselectAll(self):
      for i in self.mListBox.GetSelections():
         self.mListBox.Deselect(i)
      self.selectedItems.clear()
      self.bt_all.SetLabel("Select All")
      self.counter=0
      self.update_counter_text()
      
   def deleteSelectedItems(self):
      if len(self.selectedItems)==0:
         pass
      else:
         selection=self.mListBox.GetSelections()
         selection.sort(reverse=True)
         for i in selection:
            self.mListBox.Delete(i)
            self.reader._file_list.pop(i)
         self.deselectAll()
         
   def deleteAll(self):
      self.mListBox.Clear()
      self.counter=0
      self.counter_text.SetLabel((str)(self.counter)+"/0")
      self.mListBox.SetToolTip("")
      
   def ClickOnButton(self,event):
      obj=event.GetEventObject()
      if obj.GetLabel()=="Select All":
         self.selectAll()
      elif obj.GetLabel()=="Deselect All":
         self.deselectAll()
      elif obj.GetName().endswith(".BT.PRINT"):
         for i in self.selectedItems:
            print(self.reader._file_list[i])
      elif obj.GetName().endswith(".BT.DEL"):
         self.deleteSelectedItems()
      elif obj.GetName().endswith("BT.CLEAR"):
         self.deleteAll()
      elif obj.GetName().endswith("BT:APPLY"):
         pub.sendMessage("frame_listener", message="apply") """
         
   def OnOpen(self, event=None):
       '''
       opens a dialogue to load a .txt file and build a ListBox out of it
       '''
       # otherwise ask the user what new file to open
       with wx.FileDialog(self, "Open txt file", wildcard="txt file (*.txt)|*.txt",
                          style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
           
           #fileDialog.SetDirectory(os.path.dirname(self.cfg.filename))
           if fileDialog.ShowModal() == wx.ID_CANCEL:
               return     # the user changed their mind
   
           # Proceed loading the file chosen by the user
           pathname = fileDialog.GetPath()
           try:
              if os.path.isfile(pathname):
                  return pathname
           except IOError:
               wx.LogError("Cannot open file '%s'." % pathname)
           return None
      
      
if __name__ == "__main__":
   app=MyApp(False)
   app.MainLoop()