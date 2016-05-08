#!/usr/bin/env python

"""
    Utilities for epitopepredict
    Created March 2013
    Copyright (C) Damien Farrell
"""

from __future__ import absolute_import, print_function
import os, math, csv, string
import shutil
#import Image, ImageFont, ImageDraw
from configparser import ConfigParser
import numpy as np
import pandas as pd
import matplotlib
import pylab as plt
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio import PDB

home = os.path.expanduser("~")

def venndiagram(names,labels,ax=None):
    """Plot a venn diagram"""

    from matplotlib_venn import venn2,venn3
    import pylab as plt
    f=None
    if ax==None:
        f=plt.figure(figsize=(4,4))
        ax=f.add_subplot(111)
    if len(names)==2:
        n1,n2=names
        v = venn2([set(n1), set(n2)], set_labels=labels)
    elif len(names)==3:
        n1,n2,n3=names
        v = venn3([set(n1), set(n2), set(n3)], set_labels=labels)
    ax.axis('off')
    #f.patch.set_visible(False)
    ax.set_axis_off()
    return f

def compress(filename, remove=False):
    """Compress a file with gzip"""
    import gzip
    fin = open(filename, 'rb')
    fout = gzip.open(filename+'.gz', 'wb')
    fout.writelines(fin)
    fout.close()
    fin.close()
    if remove == True:
        os.remove(filename)
    return

def rmse(ar1, ar2):
    """Mean squared error"""
    ar1 = np.asarray(ar1)
    ar2 = np.asarray(ar2)
    dif = ar1 - ar2
    dif *= dif
    return np.sqrt(dif.sum()/len(ar1))

def addDicts(a, b):
    return dict((n, a.get(n, 0)+b.get(n, 0)) for n in set(a)|set(b))

def copyfile(source, dest, newname=None):
    """Helper method to copy files"""

    if not os.path.exists(source):
        #print 'no such file %s' %source
        return False
    shutil.copy(source, newname)
    dest = os.path.join(dest, newname)
    if os.path.exists(dest):
        os.remove(dest)
    shutil.move(newname, dest)
    return True

def copyfiles(path, files):
    for f in files:
        src = os.path.join(path, f)
        print (src)
        if not os.path.exists(src):
            return False
        shutil.copy(src, f)
    return True

def symmetrize(m, lower=True):
    """Return symmetric array"""
    m=m.fillna(0)
    if lower==True:
        return np.tril(m) + np.triu(m.T) - np.diag(np.diag(m))
    else:
        return np.triu(m) + np.tril(m.T) - np.diag(np.diag(m))

def getSymmetricDataFrame(m):
    x = symmetrize(m)
    return pd.DataFrame(x, columns=m.columns,index=m.index)

'''def getcsvdata(f, delimiter=','):
    cr = csv.reader(open(f,'r'),delimiter=delimiter)
    a = [i for i in cr]
    return a'''

def parseConfig(conffile=None):
    """Parse the config file"""

    f = open(conffile,'r')
    cp = ConfigParser.ConfigParser()
    try:
        cp.read(conffile)
    except Exception as e:
        print ('failed to read config file! check format')
        print ('Error returned:', e)
        return
    obj = setAttributesfromConfigParser(cp)
    return obj

def writeDefaultConfig(conffile='default.conf', defaults={}):
    """Write a default conf file"""
    if not os.path.exists(conffile):
        cp = createConfigParserfromDict(defaults, ['base'])
        cp.write(open(conffile,'w'))
    return conffile

def createConfigParserfromDict(data, sections, **kwargs):
    """Helper method to create a ConfigParser from a dict and/or keywords"""
    cp = ConfigParser.ConfigParser()
    for s in sections:
        cp.add_section(s)
        if not data.has_key(s):
            continue
        for i in data[s]:
            name,val = i
            cp.set(s, name, val)
    #use kwargs to create specific settings in the appropriate section
    for s in cp.sections():
        opts = cp.options(s)
        for k in kwargs:
            if k in opts:
                cp.set(s, k, kwargs[k])
    return cp

def setAttributesfromConfigParser(cp, obj=None):
    """A helper method that makes the options in a ConfigParser object
       attributes of an arbitrary object, obj """

    if obj == None:
        class Object(object):
            pass
        obj = Object()
    for s in cp.sections():
        obj.__dict__[s] = cp.items(s)
        for f in cp.items(s):
            try: val=int(f[1])
            except: val=f[1]
            obj.__dict__[f[0]] = val
    return obj

def getSequencefromFasta(filename):
    rec = SeqIO.parse(open(filename,'r'),'fasta').next()
    seq = str(rec.seq)
    return seq

def getListfromConfig(string, types='int'):
    """Extract a list from a comma separated config entry"""
    if types == 'int':
        vals = [int(i) for i in string.split(',')]
    return vals

def findFilefromString(files, string):
    for f in files:
        if string in os.path.splitext(f)[0]:
            return f
    return ''

def findFiles(path, ext='txt'):
    """List files in a dir of a specific type"""
    if not os.path.exists(path):
        print ('no such directory: %s' %path)
        return []
    files=[]
    for dirname, dirnames, filenames in os.walk(path):
        for f in filenames:
            name = os.path.join(dirname, f)
            if f.endswith(ext):
                files.append(name)
    return files

def findFolders(path):
    if not os.path.exists(path):
        print ('no such directory: %s' %path)
        return []
    dirs = []
    for dirname, dirnames, filenames in os.walk(path):
        dirs.append(dirname)
    return dirs

def reorderFilenames(files, order):
    """reorder filenames by another list order(seqs)"""
    new = []
    for i in order:
        found=False
        for f in files:
            if i in f:
                new.append(f)
                found=True
        if found==False:
            new.append('')
    return new

def readIEDB(filename, key='Epitope ID'):
    """Load iedb peptidic csv file and return dataframe"""
    #cr = csv.reader(open(filename,'r'))
    cr = csv.DictReader(open(filename,'r'),quotechar='"')
    cr.fieldnames = [field.strip() for field in cr.fieldnames]
    D={}
    for r in cr:
        k = r[key]
        D[k] = r
    return D

def getSequencefromPDB(pdbfile, chain='C', index=0):
    """Get AA sequence from PDB"""
    parser = PDB.PDBParser(QUIET=True)
    struct = parser.get_structure(pdbfile,pdbfile)
    ppb = PDB.PPBuilder()
    model = struct[0]
    peptides = ppb.build_peptides(model[chain])
    seq=''
    for i,pep in enumerate(peptides):
        seq+=str(pep.get_sequence())
    return seq

def filterIEDBFile(filename, field, search):
    """Return filtered iedb data"""
    X = pd.read_csv(filename)
    cols = ['PubMed ID','Author','Journal','Year','T Cell ID','MHC Allele Name',
                'Epitope Linear Sequence','Epitope Source Organism Name']
    y = X[X[field].str.contains(search)]
    print (y[cols])
    y.to_csv('filtered.csv',cols=cols)
    return y

def test():
    sourcefasta = os.path.join(home,'dockingdata/fastafiles/1KLU.fasta')
    findClosestStructures(sourcefasta)
    #fetchPDBList('MHCII_homologs.csv')

if __name__ == '__main__':
    test()
