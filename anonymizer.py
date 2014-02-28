#!/usr/bin/env python
#coding=utf-8

from generalization import *
from datetime import datetime
import random
import pdb
import math
import sys
import heapq
from ftp_upload import ftpupload
import socket
from pylab import *

__DEBUG = False
gl_useratt = ['DUID','PID','DUPERSID','DOBMM','DOBYY','SEX','RACEX','RACEAX','RACEBX','RACEWX','RACETHNX','HISPANX','HISPCAT','EDUCYEAR','Year','marry','income','poverty']
gl_conditionatt = ['DUID','DUPERSID','ICD9CODX','year']
gl_att_name = []
gl_att_QI = 7
gl_attlist = [3,4,5,6,13,15,16]
# att_tree store root node for each att
gl_att_tree = []
# leaf_to_path store leaf node and treepath relations for each att
gl_leaf_to_path = []
# databack store all reacord for dataset
gl_databack = []
# store data for python plot
gl_plotdata = [[],[],[]]
gl_treecover = []
# store coverage of each att according to  dataset
gl_att_cover = [[],[],[],[],[],[],[],[]]
# reduce 
gl_LCA = []


def distance(record, cluster):
    "return distance between record and cluster" 
    mid = middle(record, cluster.middle)
    distance = NCP(record, mid) + len(cluster.member) * NCP(cluster.middle, mid)
    return distance

def NCP(record, middle):
    "compute NCP (Normalized Certainty Penalty)"
    ncp = 0.0
    # exclude SA values(last one type [])
    for i in range(len(record) - 1):
        # if support of numerator is 1, then NCP is 0
        if gl_att_tree[i][record[i]].support == 1:
            continue
        ncp += gl_att_tree[i][record[i]].support * 1.0  / gl_att_tree[i][middle[i]].support
    return ncp

def get_LCA(index, item1, item2):
    "get lowest commmon ancestor(including themselves)"
    # get parent list from 
    if item1 == item2:
        return item1
    parent1 = gl_att_tree[index][item1].parent[:]
    parent2 = gl_att_tree[index][item2].parent[:]
    parent1.insert(0,item1)
    parent2.insert(0,item2)
    minlen = min(len(parent1), len(parent2))
    for i in range(minlen):
        if parent1[-i] == parent2[-i]:
            last_LCA = parent1[-i]
        else:
            break 
    return last_LCA

def middle(record1, record2):
    "compute generalization result of record1 and record2"
    middle = []
    for i in range(gl_att_QI):
        middle.append(get_LCA(i, record1[i], record2[i]))
    return middle

def middle(records):
    "calculat middle of records(list) recursively"
    len_r = len(records)
    if len_r == 1:
        return records[0]
    elif len_r == 2:
        return middle(records[0], records[1])
    else:
        mid = len_r / 2
        return middle(records[:mid], records[mid:])



def insert_to_knn(knn, k, temp):
    "insert element(index,distance) pair to knn(list)"
    # insert sort
    for i in range(len(knn)):
        if knn[i][1] > temp[1]:
            knn.insert(i, temp)
            break
    # if knn > k, del last element
    if knn > k:
        del knn[-1]
    # return largest
    return knn[-1][1]

def find_best_KNN(record, k, data):
    "key fuction of KNN. Find k nearest neighbors of record, remove them from data"
    # elements = heapq.nsmallest(k,)
    knn = []
    element = []
    max_distance = 1000000000000
    for i, t in enumerate(clusters):
        distance  = distance(record, t.middle)
        id distance < max_distance:
            temp = [i, distance]
            max_distance = insert_to_knn(knn, k, temp)
    c = Cluster(elements)
    # delete multiple elements from data according to knn index list
    data[:] = [t for i, t in enumerate(data) if i not in knn[:][1]]
    return c

def find_best_cluster(record, clusters):
    "residual assignment. Find best cluster for record."
    min_distance = 1000000000000
    min_index = 0
    best_cluster = clusters[0]
    for i, t in enumerate(clusters):
        distance = distance(record, t.middle)
        if distance < min_distance:
            min_distance = distance
            min_index = i
            best_cluster = t
    # add record to best cluster
    return min_index

def CLUSTER(data, k):
    "Group record according to QID distance. KNN"
    global gl_att_tree
    global gl_treecover
    global gl_leaf_to_path
    clusters = []
    # randomly choose seed and find k-1 nearest records to form cluster with size k
    while len(data) >= k:
        index = random.randrange(len(data))
        c =  find_best_KNN(data[index], k, data)
        clusters.append(c)
    # residual assignment
    while len(data) > 0:
        t = data.pop()
        cluster_index = find_best_cluster(t, clusters)
        clusters[cluster_index].append(t)
    return clusters

def Rum():
    return

def Tum():
    return


def RMERGE_R():
    return

def RMERGE_T():
    return

def RMERGE_RT():
    return


def TMERGE_R():
    return

def TMERGE_T():
    return

def TMERGE_RT():
    return

def num_analysis(attlist):
    "plot distribution of attlist"
    import operator
    temp = {}
    for t in attlist:
        t = int(t)
        if not t in temp.keys():
            temp[t] = 1
        else:
            temp[t] += 1
    # sort the dict
    items = temp.items()
    items.sort()
    value = []
    count = []
    for k, v  in items:
        value.append(k)
        count.append(v)
    pdb.set_trace()
    xlabel('value')
    ylabel('count')
    plt.hist(count, bins=value, normed=1, histtype='step', rwidth=0.8)
    # legend(loc='upper left')
    # grid on
    grid(True)
    show()
    
def read_tree_file(treename):
    "read tree data from treefile,store them in treenode and treelist"
    global gl_treecover
    global gl_att_tree
    global gl_leaf_to_path

    treecover = 0
    leaf_to_path = {}
    nodelist = {}
    prefix = 'data/treefile_'
    postfix = ".txt"
    treefile = open(prefix + treename + postfix,'rU')
    nodelist['*'] = GenTree('*')
    if __DEBUG:
        print "Reading Tree" + treename
    for line in treefile:
        #delete \n
        if len(line) <= 1:
            break
        line = line.strip()
        temp = line.split(';')
        # copy temp
        leaf_to_path[temp[0]] = temp[:]
        temp.reverse()
        for i, t in enumerate(temp):
            if not t in nodelist:
                # always satisfy 
                nodelist[t] = GenTree(t, nodelist[temp[i - 1]])
    treecover = nodelist['*'].getsupport()
    if __DEBUG:
        print "Nodes No. = %d" % treecover
    gl_treecover.append(treecover)
    gl_leaf_to_path.append(leaf_to_path)
    gl_att_tree.append(nodelist)

    treefile.close()

def readtree():
    global gl_att_name
    print "Reading Tree"
    for t in gl_attlist:
        gl_att_name.append(gl_useratt[t])
    gl_att_name.append(gl_conditionatt[2])
    "read tree data from treefiles, store them in treenode and leaf_to_treepath"    
    for t in gl_att_name:
        read_tree_file(t)
    

def readdata():
    "read microda for *.txt and store them in {}[]"
    global gl_databack
    global gl_att_cover
    global gl_useratt
    global gl_conditionatt
    userfile = open('data/demographics05test.csv', 'rU')
    conditionfile = open('data/conditions05.csv', 'rU')
    userdata = {}
    # We selet 3,4,5,6,13,15,15 att from demographics05, and 2 from condition05
    print "Reading Data..."
    for i, line in enumerate(userfile):
        line = line.strip()
        # ignore first line of csv
        if i == 0:
            continue
        row = line.split(',')
        row[2] = row[2][1:-1]
        if row[2] in userdata:
            userdata[row[2]].append(row)
        else:
            userdata[row[2]] = row
    conditiondata = {}
    for i, line in enumerate(conditionfile):
        line = line[:-2]
        # ignore first line of csv
        if i == 0:
            continue
        row = line.split(',')
        row[1] = row[1][1:-1]
        row[2] = row[2][1:-1]
        if row[1] in conditiondata:
            conditiondata[row[1]].append(row)
        else:
            conditiondata[row[1]] = [row]
    hashdata = {}
    for k, v in userdata.iteritems():
        if k in conditiondata:
            temp = []
            for t in conditiondata[k]:
                temp.append(t[2])
                if not t[2] in gl_att_cover[7]:
                    gl_att_cover[7].append(t[2])
            hashdata[k] = []
            for i in range(len(gl_attlist)):
                index = gl_attlist[i]
                hashdata[k].append(v[index])
                if not v[index] in gl_att_cover[i]:
                    gl_att_cover[i].append(v[index])
            hashdata[k].append(temp)
    for k, v in hashdata.iteritems():
        gl_databack.append(v)
    # pdb.set_trace()
    # num_analysis([t[6] for t in gl_databack[:]])
    userfile.close()
    conditionfile.close()


if __name__ == '__main__':
    #read gentree tax
    readtree()
    #read record
    readdata()
    # pdb.set_trace()
    CLUSTER()
    
    
    '''
    hostname = socket.gethostname()
    filetail = datetime.now().strftime('%Y-%m-%d-%H') + '.txt'
    filepath = 'output/'
    rediroutname = hostname + '-output' + filetail
    redirout = open(filepath + rediroutname, 'w')
    sys.stdout = redirout
    
    print "Anonymizing Data..."
    print "Size of dataset %d" % len(databack) 
    for i in range(2, 51):
        data = databack[:]
        
        print "are = %f" % are

    plotfilename = hostname + '-plot' + filetail
    plotfile = open(filepath + plotfilename,'w')
    
    for line in plotdata:
        ltemp = [str(s) for s in line]
        temp = ','.join(ltemp) + '\n'
        plotfile.write(temp)
    print 'OK...'
    redirout.close()
    plotfile.close()    
    # upload result file to ftp server
    ftpupload(plotfilename, filepath)
    ftpupload(rediroutname, filepath)
    '''
