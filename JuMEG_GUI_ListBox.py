#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 11:57:02 2020

@author: lkurth
"""

import wx
import wx.xrc
from file_reader import Txt_Reader

class MyApp(wx.App):
   def OnInit(self):
      self.frame=MyFrame(None)
      self.SetTopWindow(self.frame)
      self.frame.Show()
      return True
   
class MyFrame(wx.Frame):
   def __init__(self,parent):
      wx.Frame.__init__(self,parent,id=wx.ID_ANY,title="JuMEG ListBox",pos=wx.DefaultPosition, size=wx.Size(500,400),style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
      
      self.selectedItems=list()
      
      self._bt_all = wx.Button(self,label="Select All",name=self.GetName()+".BT.ALL")
      self._bt_print = wx.Button(self,label="Print",name=self.GetName()+".BT.PRINT")
      
      self.Bind(wx.EVT_BUTTON,self.ClickOnButton)
      
      self.SetSizeHints(wx.DefaultSize,wx.DefaultSize)
      self.SetBackgroundColour(wx.Colour(0,128,128))
      
      myFlexGridSizer = wx.FlexGridSizer(1,1,0,0)
      myFlexGridSizer.SetFlexibleDirection(wx.BOTH)
      myFlexGridSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
      
      myBoxGridSizer = wx.BoxSizer(wx.VERTICAL)
      
      self.headerLabel = wx.StaticText(self, wx.ID_ANY,"JuMEG ListBox",wx.Point(-1,-1),wx.DefaultSize,0)
      
      self.headerLabel.Wrap(-1)
      self.headerLabel.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(),75,90,92,True,wx.EmptyString))
      myBoxGridSizer.Add(self.headerLabel,0,wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,5)
      
      reader=Txt_Reader()
      mListBoxChoices = reader.read_file("intext_meeg_filelist.txt")    
      
      self.mListBox = wx.ListBox(self,wx.ID_ANY,wx.Point(-1,-1),wx.Size(300,300),mListBoxChoices,wx.LB_MULTIPLE) 
      self.mListBox.SetFont(wx.Font(12,75,90,90,False,wx.EmptyString))
      
      """self.mListBox.SetSelection(n=3)
      self.mListBox.SetSelection(n=5)"""
      self.mListBox.Bind(wx.EVT_LISTBOX,self.select)
      
      myBoxGridSizer.Add(self.mListBox,0,wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,5)
      myBoxGridSizer.Add(self._bt_all,0,wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,5)
      myBoxGridSizer.Add(self._bt_print,0,wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,5)
      
      myFlexGridSizer.Add(myBoxGridSizer,1,wx.EXPAND,5)
      
      self.SetSizer(myFlexGridSizer)
      self.Layout()
      
      self.Centre(wx.BOTH)
      
      self._maxFiles=self.mListBox.GetCount()
      
      
   
   def select(self,event):
    """Simulate CTRL-click"""
    selection = self.mListBox.GetSelections()
    for i in selection:
        if i not in self.selectedItems:
            # add to list of selected items
            self.selectedItems.append(i)
            self.mListBox.Select(i)
        elif len(selection) == 1:
            # remove from list of selected items
            self.selectedItems.remove(i)
            self.mListBox.Deselect(i)

    for i in self.selectedItems:
        # actually select all the items in the list
        self.mListBox.Select(i)
        
    if len(self.selectedItems)==self._maxFiles:
        self._bt_all.SetLabel("Deselect All")
    else:
        self._bt_all.SetLabel("Select All")
        
        
   def selectAll(self,event):
      for i in range(self.mListBox.GetCount()):
         self.mListBox.SetSelection(i)
         self.selectedItems.append(i)
      self._bt_all.SetLabel("Deselect All")
   
   def deselectAll(self,event):
      for i in self.selectedItems:
         self.mListBox.Deselect(i)
      self.selectedItems.clear()
      self._bt_all.SetLabel("Select All")
      
   def ClickOnButton(self,event):
      obj=event.GetEventObject()
      if obj.GetLabel()=="Select All":
         self.selectAll(event)
      elif obj.GetLabel()=="Deselect All":
         self.deselectAll(event)
      elif obj.GetName().endswith(".BT.PRINT"):
         for i in self.selectedItems:
            print(self.mListBox.GetString(i))
      
      
if __name__ == "__main__":
   app=MyApp(False)
   app.MainLoop()      