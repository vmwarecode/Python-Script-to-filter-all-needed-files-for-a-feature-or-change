#!/usr/bin/python
'''
Used to extrac the source files which Developer has updated/created/modified

The branch and the related grep command determined what you are looking for

@Baoyin Qiao

Note: this script verified using python2.7.

'''

import  re, subprocess

#define which branch you want to see the changelist
cmdMainstage=r'''p4 changes //depot/bora/main-stage/...|grep -i vmcrypt'''
cmdVmcoremain=r'''p4 changes //depot/bora/vmcore-main/...|grep -i vmcrypt'''
cmds=[cmdMainstage,cmdVmcoremain]

#Iterate very branch and get the change numers
cls=[]
for cmd in cmds:
   exe=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
   clslist=exe.communicate()[0].split('\n')
   for cl in clslist:
      clsres=re.findall(r'Change\s+(\d+)\s+',cl)
      cls.extend(clsres)

#Only for c and c++ files are needed
f=open('filelistnew.txt','w+')

filelist=[]

for cl in cls:
   cmdfile=r'''p4 files @='''+cl+r'''|grep -v vcqe|grep -v vsphere-client-*|grep -v vpx|grep -v vmodl'''
   exe=subprocess.Popen(cmdfile,stdout=subprocess.PIPE,shell=True)
   filelist=exe.communicate()[0].split('\n')
   filelist=[x.split('#')[0] for x in filelist]
   for file in filelist:
      print ".....Process the file %s....." % file
      if file.endswith(('.c','.cpp')):
         print "###### Save the file into list %s #####" % file
         f.write(file+'\n')
f.close()

#remove the duplicated files
line_seen=set()

outfile=open('outputfiles.txt','w+')

for line in open('filelistnew.txt','r'):
   if line not in line_seen:
      outfile.write(line)
      line_seen.add(line)
outfile.close()