from simargs import *
import numpy as np
import math
def magnitude(array):
    arr_sq = array**2
    sum_arr_sq = np.sum(arr_sq)
    return sum_arr_sq**0.5

def angle(array1,array2):
    dot_prod = np.sum(array1 * array2)
    angle = math.acos(dot_prod)
    return angle

def out_norm(input):
    if input<0:
        return 0
    else:
        return input

def fuse_clusters(clusters):
        new_clusters = []
        changed = False
        for cl in clusters:
            found = False
            for cluster in new_clusters:
                found_vals =[]
                for val in cl:
                    if val in cluster:
                        found_vals.append(val)
                        found = True
                        changed = True
                if found:
                    cluster.extend([x for x in cl if x not in found_vals])
                    break
            if not found:
                new_clusters.append(cl)
        return new_clusters, changed

def cluster(data,max_diff):
    dataset=data.copy()
    n = len(dataset)
    core = []
    single = []
    for id,val in dataset:
        pts = 1
        nbs = [id]
        for i in range(0,n):
            diff = angle(val,dataset[i][1])
            if diff <= max_diff:
                pts +=1
                nbs.append(i)
        if pts == 1:
            single.append(nbs)
        else:
            core.append(nbs)

    while True:
        new_clusters, changed = fuse_clusters(core)
        if changed:
            core = new_clusters
        else:
            break
    return single, core

def clustereval(data,clusters):
    clusterdata = []
    avgs = []
    id = 0
    for cl in clusters:
        n = len(cl)
        avg = np.asarray([])
        for pt in cl:
            if avg.size == 0:
                avg = data[pt][1]/n
            else:
                avg += data[pt][1]/n
        gv = 0
        avg = avg/magnitude(avg)
        for pt in cl:
            gv += angle(avg,data[pt][1])
        gv /= n
        clusterdata.append([id,n,gv])
        avgs.append(avg)
        id +=1
    return clusterdata,avgs

def conc_avgs(avgs):
    filler = np.zeros((1,consts["num_in"]))
    res = np.copy(filler)
    for avg in avgs:
        res = np.concatenate((res,avg,filler),axis = 0)
    return res