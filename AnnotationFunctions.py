#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 13:14:06 2019

@author: dwulf
"""

import subprocess
import argparse


def Annotate (Sequences, Annotationscsv,ID,desc,name,Output):
    #Open the anotationfile (CSV seperated by ,)
    with open(Annotationscsv,"r") as file:
        Anotation=file.readlines()
    
    #Create an empty dictionary    
    dic={}
    
    #Put each sequence header in the dictionary as value and key and strip them
    for i in Sequences:
        if i.startswith(">"):
            dic[i.rstrip("\n").lstrip(">")]=i.rstrip("\n")
            
            
    #If the key form the anotationfile is in the dictrionary add the description and the name to its value sperated by |
    for i in Anotation:
        i=i.rstrip("\n")
        i=i.split(",")#Split the line by ,
        if i[ID] in dic:
            function="|"+i[desc]+"|"+i[name]
            dic[i[0]]+=function
     
    #Create an output file. For each line in the sequence file: If it starts with > write the value from the dictionary, else write the same line.
    #This replaces only the sequence header while keeping the original protein sequence       
    file=open(Output,"w")
    for i in Sequences:
        if i.startswith(">"):
            i=i.lstrip(">").rstrip("\n")
            file.writelines(dic[i]+"\n")
        else:
            file.write(i)
            
        
        
    file.close()
    return Output

#Initilising all Arguments
parser = argparse.ArgumentParser(description="Python skript for anotating genes and generating decoys using decoy.pl. Decoy.pl must be in the same folder")
parser.add_argument("-faa", action="store", required=True,help="Sequence file")
parser.add_argument("-csv", action="store",default="None!",help="Annotation file")
parser.add_argument("-desc_col",action="store",default=2 , type=int, help="Column in the CSV with the protein description (0-n)")
parser.add_argument("-name_col", action="store",default=1 , type=int, help="Column in the CSV with the protein name (0-n)")
parser.add_argument("-ID", action="store",default=0 , type=int, help="Column in the CSV with the protein ID (0-n)")
parser.add_argument("-out", action="store", default="None!",help="Name of the output file")
parser.add_argument("--random", action="store_const", const="--random",default="",help="If --random is specified, the output entries will be random sequences")
parser.add_argument("--append", action="store_const", const="--append",default="",help="If --append is specified, the new entries will be appended to the input database. Otherwise, a separate decoy database file will be created.")
parser.add_argument("--keep_accessions", action="store_const", const="--keep_accessions",default="",help="If --keep_accessions is specified, the original accession strings will be retained. This is necessary if you want to use taxonomy and the taxonomy is derived from the accessions, (e.g. NCBI gi2taxid). Otherwise, the string ###REV### or ###RND### is prepended to the original accession strings.")
parser.add_argument("--decoy_method",action="store",default="decoy.pl",help="File name of the decoy Perl skript.")


parser.parse_args()
args = parser.parse_args()


#Opens the input seqences
with open(args.faa,"r") as file:
    Sequences=file.readlines()

#If no output file is specified take the inputfile+_decoy as name
if args.out=="None!":
    Outputfile=(args.faa+"_decoy")
else:
    Outputfile=(args.out)


#If -csv is specified anotate the input sequences. Else just copy the sequence for decoy.pl
if args.csv != "None!":
    Annotate(Sequences=Sequences,Annotationscsv=args.csv,ID=int(args.ID),desc=int(args.desc_col),name=int(args.name_col),Output=Outputfile)
else:
    file=open(Outputfile,"w")
    file.writelines(Sequences)
    file.close()

#Prepare the Perl subprocess with the specified Perl skript
Perl=["perl",args.decoy_method]

#Append the arguments for the Perl skript
if args.append == "--append":
    Perl.append(args.append)


if args.random == "--random":
    Perl.append(args.random)
    
if args.keep_accessions=="--keep_accessions":
    Perl.append(args.keep_accessions)
    
#If --append was not specified the Anotated file is the Inputfile 
Perl.append(Outputfile)

if args.append !="--append":
    Perl.append(Outputfile+"_Out.faa")

print("running with following arguments: ",Perl )    

#Execute the Perl skript with the given specified parameters
subprocess.call(Perl)
