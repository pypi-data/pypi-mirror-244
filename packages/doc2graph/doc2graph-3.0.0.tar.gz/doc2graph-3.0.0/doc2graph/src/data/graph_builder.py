
import os
import json
import random
import numpy as np
from tqdm import tqdm
import cv2
#import math
import xml.etree.ElementTree as ET

import torch
#import easyocr
import dgl
from PIL import Image, ImageDraw


from doc2graph.src.data.preprocessing import unnormalize_box
from doc2graph.src.data.utils import polar
from doc2graph.src.utils import get_config
from doc2graph.src.data.utils import intersectoin_by_axis, find_dates, find_amounts, find_numbers, find_codes, find_word, find_words, file_to_images
from typing import List, Tuple
from sklearn.metrics import pairwise_distances
from functools import cmp_to_key

def compare_items(a, b):
    if intersectoin_by_axis('x',a[1],b[1])>0.4: #if boxes on same level, compare by x
        return a[1][0]-b[1][0]
    return a[1][1]-b[1][1] 

center = lambda rect: ((rect[2]+rect[0])/2, (rect[3]+rect[1])/2)


def box_distance(box_left: Tuple[int,int,int,int], 
                 box_right: Tuple[int,int,int,int],
                 verbose=False)->float:
    """Distance between centers of two boxes."""
    x_dist = (box_right[2] - box_left[2]) 
    if x_dist<0:
        x_dist = 0
   
    y_dist = (box_right[3] - box_left[3]) 
    if y_dist<0:
        y_dist = 0
    
    if verbose:
        print(x_dist,y_dist)
        
    distance = x_dist + 3*y_dist
    
    return distance


def box_distance_far(box_left: Tuple[int,int,int,int], 
                 box_right: Tuple[int,int,int,int],
                 verbose=False)->float:
    """Distance between centers of two boxes."""
    x_dist = max(box_right[2] - box_left[0],box_left[2] - box_right[0]) 
    if x_dist<0:
        x_dist = 0
   
    y_dist = max(box_right[3] - box_left[1],box_left[3] - box_right[1]) 
    if y_dist<0:
        y_dist = 0
    
    if verbose:
        print(x_dist,y_dist)
        
    distance = x_dist + 3*y_dist
    
    return distance


def get_word_boxes(image_path, host):
    import io
    import requests
    import base64
    import json

    pil_image = file_to_images(image_path)[0]
    with io.BytesIO() as buffer:
        pil_image.save(buffer, format='jpeg')
        image_bytes = buffer.getvalue()
        
    data = {
        "image_bytes":base64.b64encode(image_bytes).decode("utf8")
    }

    response = requests.post(f"{host}",
                    data=json.dumps(data),
                    headers={'content-type':'application/json',
                            'x-amzn-RequestId': '84cad557-a68f-45db-9c01-79449f0aeecb'},
                    timeout=29
                    )
    
    ict_str = response.content.decode("UTF-8")
    res = json.loads(ict_str)
    return res
    

def has_xy_intersection(box, neighbor_boxes, min_share = 0.8):
    for neighbor_box in neighbor_boxes:
        if intersectoin_by_axis('x',box, neighbor_box)>=min_share:
            return True
        elif intersectoin_by_axis('y',box, neighbor_box)>=min_share:
            return True
    return False


def has_x_intersection(box, neighbor_boxes, min_share = 0.8):
    for neighbor_box in neighbor_boxes:
        if intersectoin_by_axis('x',box, neighbor_box)>=min_share:
            return True
    return False


def neighbors_idx(i, u, v):
    return [v for u,v in zip(u,v) if u==i]


def get_box_to_side(boxes, i, u, v, side='right', min_share=0.8):
    neighbors = neighbors_idx(i, u, v)
    for ix in neighbors:
        neighbor_box = boxes[ix]
        box = boxes[i]
        if side=='right':
            if neighbor_box[0]+neighbor_box[2]>box[0]+box[2]:
                if intersectoin_by_axis('x',box, neighbor_box)>=min_share:
                    return ix
        if side=='left':        
            if neighbor_box[0]+neighbor_box[2]<box[0]+box[2]:
                if intersectoin_by_axis('x',box, neighbor_box)>=min_share:
                    return ix
        
    return None


def get_line_to_side(boxes, i, u, v, side='right', min_share=0.8):
    boxes_to_right_ix = []
    box_to_right_ix = get_box_to_side(boxes, i, u, v, side, min_share)
    orig_box = boxes[i]
    while box_to_right_ix:
        boxes_to_right_ix.append(box_to_right_ix)
        box_to_right_ix = get_box_to_side(boxes, box_to_right_ix, u, v, side, min_share)
        
        if box_to_right_ix:
            box_to_right = boxes[box_to_right_ix]
            if intersectoin_by_axis('x',orig_box, box_to_right)<min_share:
                break
        
    return boxes_to_right_ix


def get_line(boxes, i, u, v, min_share=0.8):
    res=[i]
    res.extend(get_line_to_side(boxes, i, u, v, 'right', min_share))
    res.extend(get_line_to_side(boxes, i, u, v, 'left', min_share))
    return res


def get_lines(boxes, u, v, min_share=0.8):
    used=[]
    lines=[]
    for i in u:
        if i not in used:
            line =  get_line(boxes, i, u, v, min_share)
            if len(line)>1:
                lines.append(line)
            used.extend(line)    
    return lines            


def merge_boxes(boxes):
    return [
        min([box[0] for box in boxes]),
        min([box[1] for box in boxes]),
        max([box[2] for box in boxes]),
        max([box[3] for box in boxes])
    ]


def ccw(A, B, C):
    """Check if points are listed in counter-clockwise order."""
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def intersect(A, B, C, D):
    """Check if line segments AB and CD intersect."""
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def remove_diag_edges(boxes, u, v):
    min_share = 0.8
    links = {'src':[],'dst':[]}
    for i, box in enumerate(boxes):
        neighbors = neighbors_idx(i, u, v)
        
        if has_xy_intersection(box, [boxes[ix] for ix in neighbors], min_share):
            neighbors = [ix for ix in neighbors if max(intersectoin_by_axis('x',box, boxes[ix]), intersectoin_by_axis('y',box, boxes[ix]))>=min_share]

        links['src'].extend([i]*len(neighbors))
        links['dst'].extend(neighbors)
        
    slinks = set((u,v) for u,v in zip(links['src'],links['dst']))
    slinks = [x for x in slinks if (x[1],x[0]) in slinks]
    links = {'src': [x[0] for x in slinks], 
    'dst': [x[1] for x in slinks] }
    
    return links['src'], links['dst']


def remove_diag_edges2(boxes, u, v, words, min_share):
    min_share = 0.8
    links = {'src':[],'dst':[]}
    for i, box in enumerate(boxes):
        # if not '11/2023' in words[i]:
        #     continue
        # print(words[i])
        
        neighbors = neighbors_idx(i, u, v)
        
        # boxes_to_left = [ix for ix in neighbors if 
        #                  boxes[ix][0]<=box[2]
        #                 ]
        # neighbors = [ix for ix in boxes_to_left if 
        #                  boxes[ix][1]<=box[3]
        #                 ]
        
        boxes_to_left = [ix for ix in neighbors if 
                             (
                                (
                                   (0.5*(boxes[ix][0]+boxes[ix][2])<=box[2]) or #center of boxes left to right edge
                                   (intersectoin_by_axis('y',boxes[ix], box)>min_share) #intesects on y
                                )
                                and (ix!=i)
                             )]
            
        boxes_to_up =   [ix for ix in boxes_to_left if 
                            (
                            (
                                (0.5*(boxes[ix][1]+boxes[ix][3])<=box[3]) or #center of boxes left to right edge
                                (intersectoin_by_axis('x',boxes[ix], box)>min_share) #intesects on x
                            )
                            and (ix!=i)
                            )]
            
        neighbors = boxes_to_up
        
        if len(neighbors)<=2:
            if neighbors:
                links['src'].extend([i]*len(neighbors))
                links['dst'].extend(neighbors)
                links['dst'].extend([i]*len(neighbors))
                links['src'].extend(neighbors)
        else:           
            min_share = 0.5
            top_neighbors = [ix for ix in neighbors if intersectoin_by_axis('y',box, boxes[ix])>=min_share]
            if top_neighbors:
                top_neighbor = sorted(top_neighbors,key=lambda ix: box_distance(boxes[ix],box), reverse=False)[0]
            else:
                top_neighbor = None
            
            left_neighbors = [ix for ix in neighbors if intersectoin_by_axis('x',box, boxes[ix])>=min_share]
            if left_neighbors:
                left_neighbor = sorted(left_neighbors,key=lambda ix: box_distance(boxes[ix],box), reverse=False)[0]
            else:
                left_neighbor = None
                
            if left_neighbor and top_neighbor:
                links['src'].extend([i,i,left_neighbor,top_neighbor])
                links['dst'].extend([left_neighbor,top_neighbor,i,i])
            else:
                neighbors = sorted(neighbors,key=lambda ix: box_distance(boxes[ix],box), reverse=False)
                
                neighbors = neighbors[:2]
                
                if neighbors:
                    links['src'].extend([i]*len(neighbors))
                    links['dst'].extend(neighbors)
                    links['dst'].extend([i]*len(neighbors))
                    links['src'].extend(neighbors)
        
    slinks = set((u,v) for u,v in zip(links['src'],links['dst']))
    slinks = [x for x in slinks if (x[1],x[0]) in slinks]
    links = {'src': [x[0] for x in slinks], 
    'dst': [x[1] for x in slinks] }
    
    return links['src'], links['dst']


def sin(x1,y1,x2,y2):
    if x2-x1==0:
        return 1
    return abs(y2-y1)/abs(x2-x1)


def remove_intersected_edges(boxes, u, v):
    links = {'src':[],'dst':[]}
    n = len(u)
    for i in range(n):
        intersected = False
        line1 = [center(boxes[u[i]]), center(boxes[v[i]])]
        
        s1 = sin(line1[0][0],line1[0][1],line1[1][0],line1[1][1])
        if s1:
            for j in range(i,n):
                line2 = [center(boxes[u[j]]), center(boxes[v[j]])]
                s2 = sin(line2[0][0],line2[0][1],line2[1][0],line2[1][1])
                
                if intersect(line1[0], line1[1], line2[0], line2[1]):
                    if (s2 is None) or (s1<s2):
                        intersected = True
                        break
            
        if not intersected:
            links['src'].extend([u[i],v[i]])
            links['dst'].extend([v[i],u[i]])
        
    slinks = set((u,v) for u,v in zip(links['src'],links['dst']))
    slinks = [x for x in slinks if (x[1],x[0]) in slinks]
    links = {'src': [x[0] for x in slinks], 
    'dst': [x[1] for x in slinks] }
    
    return links['src'], links['dst']


def remove_vertical_edges(boxes, u, v):
    links = {'src':[],'dst':[]}
    n = len(u)
    for i in range(n):
        box1 = boxes[u[i]]
        box2 = boxes[v[i]]
        height_box1 = abs(box1[1]-box1[3])
        height_box2 = abs(box2[1]-box2[3])
        height = max(height_box1,height_box2)
        c1 = center(box1)
        c2 = center(box2)
        
        if abs(c2[1]-c1[1])<3*height:
            links['src'].extend([u[i],v[i]])
            links['dst'].extend([v[i],u[i]])
        
    slinks = set((u,v) for u,v in zip(links['src'],links['dst']))
    slinks = [x for x in slinks if (x[1],x[0]) in slinks]
    links = {'src': [x[0] for x in slinks], 
    'dst': [x[1] for x in slinks] }
    
    return links['src'], links['dst']


def remove_notline_edges(boxes, u, v):
    min_share = 0.8
    links = {'src':[],'dst':[]}
    for i, box in enumerate(boxes):
        neighbors = neighbors_idx(i, u, v)
        neighbors_boxes =  [boxes[ix] for ix in neighbors]
        
        if has_x_intersection(box, neighbors_boxes, min_share):
            new_neighbors = []
            for j in neighbors:
                j_neighbors = neighbors_idx(j, u, v)
                j_neighbors_boxes =  [boxes[ix] for ix in j_neighbors]
                if has_x_intersection(boxes[j], j_neighbors_boxes, min_share):
                    new_neighbors.append(j)
            neighbors = new_neighbors
            
        if neighbors:
            links['src'].extend([i]*len(neighbors))
            links['dst'].extend(neighbors)
        
    slinks = set((u,v) for u,v in zip(links['src'],links['dst']))
    slinks = [x for x in slinks if (x[1],x[0]) in slinks]
    links = {'src': [x[0] for x in slinks], 
    'dst': [x[1] for x in slinks] }
    
    return links['src'], links['dst']


def remove_long_edges(boxes, u, v, d_mult = 3):
    links = {'src':[],'dst':[]}
    p_dist = pairwise_distances(boxes,metric = box_distance)
    for i in range(len(boxes)):
        neighbors = [v for u,v in zip(u,v) if u==i]
        
        dist = p_dist[i,neighbors]
        dist = sorted(dist)
        dist = [x for x in dist if x>0]
        
        # if words[i] in ['Type','Date']:
        #     print(i,[words[j] for j in neighbors],dist)
            
        if len(dist)>1:
            prev_dist = dist[0]
            for ix,val in enumerate(dist[1:]):
                if val>d_mult*prev_dist:
                    dist = dist[:ix+1]
                    break
                prev_dist = val
            neighbors = [v for v in neighbors if p_dist[i,v]<=max(dist)]
        
        links['src'].extend([i]*len(neighbors))
        links['dst'].extend(neighbors)
        
        #if words[i] in ['Type','Date']:
        #    print(i,[words[j] for j in neighbors],neighbors)
            #print(links)
            
    slinks = set((u,v) for u,v in zip(links['src'],links['dst']))
    slinks = [x for x in slinks if (x[1],x[0]) in slinks]
    links = {'src': [x[0] for x in slinks], 
    'dst': [x[1] for x in slinks] }
    
    return links['src'], links['dst']


def filter_boxes_up(box, box_main, boxes_to_up, boxes_x_intersected, boxes_y_intersected,texts):
    #print(texts[box[0]])
    #print('before',[texts[x[0]] for x in boxes_to_up])
    if box in boxes_x_intersected:
        boxes_to_up = [x for x in boxes_to_up if 
                        ((x[1][2]+x[1][0]>2*box[1][2]) or 
                        (intersectoin_by_axis('y',x[1], box[1])>0.8)) and
                        (intersectoin_by_axis('x',x[1], box_main)<0.5)  #avoid 2 connections on x
                        ]
        #print('x',[texts[x[0]] for x in boxes_to_up])
    elif box in boxes_y_intersected:
        boxes_to_up = [x for x in boxes_to_up if 
                        ((x[1][3]+x[1][1]>2*box[1][3]) or 
                        (intersectoin_by_axis('x',x[1], box[1])>0.8)) and 
                        (intersectoin_by_axis('y',x[1], box_main)<0.5) #avoid 2 connections on y
                        ]
        #print('y',[texts[x[0]] for x in boxes_to_up])
    else:
        boxes_to_up =    [x for x in boxes_to_up if 
                             max(intersectoin_by_axis('x',x[1], box_main), intersectoin_by_axis('y',x[1], box_main))>0.8  #intersected with main
                             or 
                             (
                                 max(intersectoin_by_axis('x',x[1], box[1]), intersectoin_by_axis('y',x[1], box[1]))<0.1 and #not intersected with diag
                                 not ((x[1][0]<box[1][2]) and (x[1][1]<box[1][3])) # not in 4th quater
                             )
                             ]
        #print('z',[texts[x[0]] for x in boxes_to_up])
        
        
    return boxes_to_up      
     
        
class GraphBuilder():
    def __init__(self, data_type='img', edge_type='fully', node_granularity='gt', word_to_word = 'word_to_word'):
        # self.cfg_preprocessing = get_config('preprocessing')
        self.edge_type = edge_type# self.cfg_preprocessing.GRAPHS.edge_type
        self.data_type = data_type# self.cfg_preprocessing.GRAPHS.data_type
        self.node_granularity = node_granularity# self.cfg_preprocessing.GRAPHS.node_granularity
        self.word_to_word=word_to_word
        random.seed = 42
        return
    
    
    def get_graph(self, 
                  src_path: List[str],
                  src_data : str,
                  word_boxes_list: list = None,
                  max_depth = 1
                  ):
        """ Given the source, it returns a graph

        Args:
            src_path (str) : path to source data
            src_data (str) : either FUNSD, PAU or CUSTOM
        
        Returns:
            tuple (lists) : graphs, nodes and edge labels, features
        """
        
        if src_data == 'FUNSD':
            return self.__fromFUNSD(src_path)
        if src_data == 'REMITTANCE':
            return self.__fromREMITTANCE(src_path)
        elif src_data == 'PAU':
            return self.__fromPAU(src_path)
        elif src_data == 'CUSTOM':
            if self.data_type == 'img':
                return self.__fromIMG(src_path)
            elif self.data_type == 'pdf':
                return self.__fromPDF(src_path)
            elif self.data_type == 'word_boxes':
                return self.__fromWB(src_path, word_boxes_list, max_depth)
            else:
                raise Exception('GraphBuilder exception: data type invalid. Choose from ["img", "pdf"]')
        else:
            raise Exception('GraphBuilder exception: source data invalid. Choose from ["FUNSD", "PAU", "CUSTOM"]')
    
    
    def balance_edges(self, g : dgl.DGLGraph, cls=None ):
        """ if cls (class) is not None, but an integer instead, balance that class to be equal to the sum of the other classes

        Args:
            g (DGLGraph) : a DGL graph
            cls (int) : class number, if any
        
        Returns:
            g (DGLGraph) : the new balanced graph
        """
        
        edge_targets = g.edata['label']
        u, v = g.all_edges(form='uv')
        edges_list = list()
        for e in zip(u.tolist(), v.tolist()):
            edges_list.append([e[0], e[1]])

        if type(cls) is int:
            to_remove = (edge_targets == cls)
            indices_to_remove = to_remove.nonzero().flatten().tolist()

            for _ in range(int((edge_targets != cls).sum()/2)):
                indeces_to_save = [random.choice(indices_to_remove)]
                edge = edges_list[indeces_to_save[0]]

                for index in sorted(indeces_to_save, reverse=True):
                    del indices_to_remove[indices_to_remove.index(index)]

            indices_to_remove = torch.flatten(torch.tensor(indices_to_remove, dtype=torch.int32))
            g = dgl.remove_edges(g, indices_to_remove)
            return g
            
        else:
            raise Exception("Select a class to balance (an integer ranging from 0 to num_edge_classes).")
    
    
    def get_info(self):
        """ Returns graph information.
        """
        print(f"-> edge type: {self.edge_type}")


    def fully_connected(self, ids : list):
        """ Creates fully connected graph.

        Args:
            ids (list) : list of node indices
        
        Returns:
            u, v (lists) : lists of indices
        """
        u, v = list(), list()
        for id_ in ids:
            u.extend([id for i in range(len(ids)) if i != id_])
            v.extend([i for i in range(len(ids)) if i != id_])
        return u, v
    
                
    def half_fully_connected(self, 
                              bboxs : List[Tuple[int,int,int,int]], 
                              texts:  List[str], 
                              kind='word_to_notword'):
        """ Creates connected graph with connection allowed only to left and to up.

        Args:
        
        Returns:
            u, v (lists) : lists of indices
        """
        
        bboxs_with_id = [(ix, box) for ix, box in enumerate(bboxs)]
        
        u, v = list(), list()
        
        for ix, box_main in enumerate(bboxs):
            #source_number = find_dates(texts[ix]) or find_amounts(texts[ix]) or find_numbers(texts[ix]) or find_codes(texts[ix])
            source_word = find_word(texts[ix]) or find_words(texts[ix])
            
            # if ix>34:
            #    continue
            
            # if '78.40' not in texts[ix]:
            #     continue
            #print(ix,texts[ix])
            
            if kind.split('_to_')[0]=='word':
                if not source_word:
                    continue
            if kind.split('_to_')[0]=='notword':
                if source_word:
                    continue
            # if not source_number:
            #     continue
            
            prev_dist = None
                        
            #===========================================================================
            min_share = 0.4
            
            boxes_to_left = [x for x in bboxs_with_id if 
                             (
                                (
                                   (x[1][0]<=box_main[2])# or #(0.5*(x[1][0]+x[1][2])<=box_main[2]) or #center of boxes left to right edge
                                   #(intersectoin_by_axis('y',x[1], box_main)>min_share) #intesects on y
                                )
                                and (x[0]!=ix)
                             )]
            
            boxes_to_up =   [x for x in boxes_to_left if 
                             (
                                (
                                    (0.5*(x[1][1]+x[1][3])<=box_main[3]) or #center over bottom
                                    (intersectoin_by_axis('x',x[1], box_main)>min_share) #intesects on x
                                )
                                and (x[0]!=ix)
                             )]
            boxes_to_up =   [x for x in boxes_to_up if not 
                             ((intersectoin_by_axis('x',x[1], box_main)>min_share) and
                              (x[1][0]>box_main[0]))]
            
            
            boxes_to_up = sorted(boxes_to_up,key=lambda x: box_distance(x[1],box_main), reverse=False)
            # if 'Our Voucher Number' in texts[ix]:
            #     print('all',[texts[x[0]] for x in boxes_to_up])
            #     print('all',[box_distance(x[1],box_main,verbose=True) for x in boxes_to_up])
                
            boxes_x_intersected = [x for x in boxes_to_up if intersectoin_by_axis('x',x[1], box_main)>max(min_share,intersectoin_by_axis('y',x[1], box_main))]
            boxes_y_intersected = [x for x in boxes_to_up if intersectoin_by_axis('y',x[1], box_main)>max(min_share,intersectoin_by_axis('x',x[1], box_main))]
            #boxes_not_xy_intersected = [x for x in boxes_to_up if max(intersectoin_by_axis('x',x[1], box_main),intersectoin_by_axis('y',x[1], box_main))<min_share]
            
            #===============================================================================
            neighbors=[]
            #get three neighbors
            if True:
                while True:
                    if not boxes_to_up:
                        break
                    
                    box = boxes_to_up[0]
                    #print(texts[box[0]])
                    boxes_to_up = boxes_to_up[1:]
                    boxes_to_up = filter_boxes_up(box, box_main, boxes_to_up, boxes_x_intersected, boxes_y_intersected,texts)
                    
                    target_word = find_word(texts[box[0]]) or find_words(texts[box[0]])
                    if kind.split('_to_')[1]=='notword':    
                        if target_word:
                            continue
                    elif kind.split('_to_')[1]=='word':    
                        if not target_word:
                            continue
                    
                    neighbors.append(box[0])     
                    # u.extend([ix,box[0]])
                    # v.extend([box[0],ix])
                    break
                
                #up
                while True:
                    if not boxes_to_up:
                        break
                    box = boxes_to_up[0]
                    #print(texts[box[0]])
                    boxes_to_up = boxes_to_up[1:]
                    boxes_to_up = filter_boxes_up(box, box_main, boxes_to_up, boxes_x_intersected, boxes_y_intersected,texts)
                    
                    target_word = find_word(texts[box[0]]) or find_words(texts[box[0]])
                    if kind.split('_to_')[1]=='notword':    
                        if target_word:
                            continue
                    elif kind.split('_to_')[1]=='word':    
                        if not target_word:
                            continue
                    
                    neighbors.append(box[0])     
                    # u.extend([ix,box[0]])
                    # v.extend([box[0],ix])
                    break
                
                
                #diag
                while True:
                    if not boxes_to_up:
                        break
                    box = boxes_to_up[0]
                    #print(texts[box[0]])
                    boxes_to_up = boxes_to_up[1:]
                    
                    target_word = find_word(texts[box[0]]) or find_words(texts[box[0]])
                    if kind.split('_to_')[1]=='notword':    
                        if target_word:
                            continue
                    elif kind.split('_to_')[1]=='word':    
                        if not target_word:
                            continue
                    
                    neighbors.append(box[0])     
                    # u.extend([ix,box[0]])
                    # v.extend([box[0],ix])
                    break
            
            #===============================================================================    
            #detect left_neighbor
            left_neighbors = [i for i in neighbors if intersectoin_by_axis('x',bboxs[ix], bboxs[i])>=min_share]
            if left_neighbors:
                left_neighbor = sorted(left_neighbors,key=lambda i: box_distance(bboxs[i],bboxs[ix]), reverse=False)[0]
            else:
                left_neighbor = None
                
            top_neighbors = [i for i in neighbors if intersectoin_by_axis('y',bboxs[ix], bboxs[i])>=min_share]
            if top_neighbors:
                top_neighbor = sorted(top_neighbors,key=lambda i: box_distance(bboxs[i],bboxs[ix]), reverse=False)[0]
            else:
                top_neighbor = None
                
            # remove far neighbors
            if left_neighbor:
                if left_neighbor in neighbors[:2]:
                    max_dist = box_distance_far(bboxs[left_neighbor],bboxs[ix])
                    neighbors = [i for i in neighbors if box_distance(bboxs[i],bboxs[ix])<=max_dist]
            elif len(neighbors)>1 and neighbors[0]!=top_neighbor:
                max_dist = box_distance_far(bboxs[neighbors[0]],bboxs[ix])
                neighbors = [i for i in neighbors if box_distance(bboxs[i],bboxs[ix])<=max_dist]
                
                top_neighbors = [i for i in neighbors if intersectoin_by_axis('y',bboxs[ix], bboxs[i])>=min_share]
                if top_neighbors:
                    top_neighbor = sorted(top_neighbors,key=lambda i: box_distance(bboxs[i],bboxs[ix]), reverse=False)[0]
                else:
                    top_neighbor = None
            #===============================================================================
            
            #keeping only left and top
            if len(neighbors)>2:
                if left_neighbor and top_neighbor:
                    neighbors = [left_neighbor,top_neighbor]
                elif left_neighbor:
                    neighbors.remove(left_neighbor)
                    closest_non_left = sorted(neighbors,key=lambda i: box_distance(bboxs[i],bboxs[ix]), reverse=False)[0]
                    neighbors = [closest_non_left,left_neighbor]
                elif top_neighbor:
                    neighbors.remove(top_neighbor)
                    closest_non_top = sorted(neighbors,key=lambda i: box_distance(bboxs[i],bboxs[ix]), reverse=False)[0]
                    neighbors = [closest_non_top,top_neighbor]
                else:
                    neighbors = sorted(neighbors,key=lambda i: box_distance(bboxs[i],bboxs[ix]), reverse=False)
                    neighbors = neighbors[:2]
            #===============================================================================
            
            #avoid duplicate top neighbor
            non_left_neighbors = [i for i in neighbors if i!=left_neighbor]
            for neighbor in non_left_neighbors:
                sub_neighbors = neighbors_idx(neighbor, u, v)
                
                bottom_neighbors = [i for i in sub_neighbors if 
                                    intersectoin_by_axis('y',bboxs[neighbor], bboxs[i])>=min_share and
                                    (0.5*(bboxs[i][1]+bboxs[i][3])>=bboxs[neighbor][3]) ]
                
                if bottom_neighbors:
                    bottom_neighbor = sorted(bottom_neighbors,key=lambda i: box_distance(bboxs[neighbor],bboxs[i]), reverse=False)[0]
                else:
                    bottom_neighbor = None
                
                if bottom_neighbor:
                    neighbors.remove(neighbor)
            #===============================================================================
                    
            # avoid duplicate top neighbor 2
            non_left_neighbors = list(reversed([i for i in neighbors if i!=left_neighbor]))
            for neighbor in non_left_neighbors:
                sub_neighbors = neighbors_idx(neighbor, u, v)
                left_sub_neighbors = [i for i in sub_neighbors if intersectoin_by_axis('x',bboxs[neighbor], bboxs[i])>=min_share]
                if left_neighbor in left_sub_neighbors:
                    neighbors.remove(left_neighbor)
                elif set(sub_neighbors) & set(neighbors):
                    neighbors.remove(neighbor)
                    
            # #===============================================================================
            # # remove to far
            non_left_neighbors = list(reversed([i for i in neighbors if i!=left_neighbor]))
            for neighbor in non_left_neighbors:
                sub_neighbors = neighbors_idx(neighbor, u, v)
                if not sub_neighbors:
                    continue
                
                max_dist = max([box_distance_far(bboxs[neighbor],bboxs[i]) for i in sub_neighbors])
                
                if box_distance(bboxs[neighbor],bboxs[ix])>max_dist:
                    neighbors.remove(neighbor)
            
            #===============================================================================
            for n in neighbors:
                u.extend([ix,n])
                v.extend([n,ix])
            
        return v, u
    
    
    def half_share_connected(self, bboxs : list, texts: list, min_share=0.1):
        """ create connected graph with connection allowed only to right and to bottom

        Args:
            bboxs (list) : list of bounding box coordinates
        
        Returns:
            u, v (lists) : lists of indices
        """
        
        bboxs_with_id = [(ix, box) for ix, box in enumerate(bboxs)]
        
        u, v = list(), list()
        
        for ix, box in enumerate(bboxs):
            boxes_to_right = [x for x in bboxs_with_id if x[1][0]+x[1][2]>=box[0]+box[2] and x[0]!=ix]
            boxes_to_right = [x for x in boxes_to_right if 0.5*(x[1][1]+x[1][3])>=box[1]]
            
            boxes_to_right = [x for x in boxes_to_right if intersectoin_by_axis('x',x[1], box)>min_share]
            
            #source_word = find_word(texts[ix]) or find_words(texts[ix])
            
            #print(texts[ix], source_word)
           
            if len(boxes_to_right):
                boxes_to_right = sorted(boxes_to_right,key=lambda x: x[1][0], reverse=False)
                boxes_to_right = boxes_to_right[:1]
                #print(boxes_to_right)
                if boxes_to_right:
                    box_to_right = boxes_to_right[0]
                    
                    #if source_word:
                    target_word = find_word(texts[box_to_right[0]]) or find_words(texts[box_to_right[0]])
                    # else:
                    #     target_word = False
                        
                    if not target_word:
                        u.append(ix)
                        v.append(box_to_right[0])
            
            boxes_to_bottom = [x for x in bboxs_with_id if x[1][1]+x[1][3]>=box[1]+box[3] and x[0]!=ix]
            boxes_to_bottom = [x for x in boxes_to_bottom if 0.5*(x[1][0]+x[1][2])>=box[0]]
            
            boxes_to_bottom = [x for x in boxes_to_bottom if intersectoin_by_axis('y',x[1], box)>min_share]
            if len(boxes_to_bottom):
                boxes_to_bottom = sorted(boxes_to_bottom,key=lambda x: x[1][1], reverse=False)
                boxes_to_bottom = boxes_to_bottom[:1]
                if boxes_to_bottom:
                    box_to_bottom = boxes_to_bottom[0]
                
                #if source_word:
                target_word = find_word(texts[box_to_bottom[0]]) or find_words(texts[box_to_bottom[0]])
                # else:
                #     target_word = False    
                    
                if not target_word:
                    u.append(ix)
                    v.append(box_to_bottom[0])    
            #break
        
        return u, v
    
    
    def knn_connection(self, size : tuple, bboxs : list, k = 10):
        """ Given a list of bounding boxes, find for each of them their k nearest ones.

        Args:
            size (tuple) : width and height of the image
            bboxs (list) : list of bounding box coordinates
            k (int) : k of the knn algorithm
        
        Returns:
            u, v (lists) : lists of indices
        """

        edges = []
        width, height = size[0], size[1]
        
        # creating projections
        vertical_projections = [[] for i in range(width)]
        horizontal_projections = [[] for i in range(height)]
        for node_index, bbox in enumerate(bboxs):
            for hp in range(bbox[0], bbox[2]):
                if hp >= width: hp = width - 1
                vertical_projections[hp].append(node_index)
            for vp in range(bbox[1], bbox[3]):
                if vp >= height: vp = height - 1
                horizontal_projections[vp].append(node_index)
        
        def bound(a, ori=''):
            if a < 0 : return 0
            elif ori == 'h' and a > height: return height
            elif ori == 'w' and a > width: return width
            else: return a

        for node_index, node_bbox in enumerate(bboxs):
            neighbors = [] # collect list of neighbors
            window_multiplier = 2 # how much to look around bbox
            wider = (node_bbox[2] - node_bbox[0]) > (node_bbox[3] - node_bbox[1]) # if bbox wider than taller
            
            ### finding neighbors ###
            while(len(neighbors) < k and window_multiplier < 100): # keep enlarging the window until at least k bboxs are found or window too big
                vertical_bboxs = []
                horizontal_bboxs = []
                neighbors = []
                
                if wider:
                    h_offset = int((node_bbox[2] - node_bbox[0]) * window_multiplier/4)
                    v_offset = int((node_bbox[3] - node_bbox[1]) * window_multiplier)
                else:
                    h_offset = int((node_bbox[2] - node_bbox[0]) * window_multiplier)
                    v_offset = int((node_bbox[3] - node_bbox[1]) * window_multiplier/4)
                
                window = [bound(node_bbox[0] - h_offset),
                        bound(node_bbox[1] - v_offset),
                        bound(node_bbox[2] + h_offset, 'w'),
                        bound(node_bbox[3] + v_offset, 'h')] 
                
                [vertical_bboxs.extend(d) for d in vertical_projections[window[0]:window[2]]]
                [horizontal_bboxs.extend(d) for d in horizontal_projections[window[1]:window[3]]]
                
                for v in set(vertical_bboxs):
                    for h in set(horizontal_bboxs):
                        if v == h: neighbors.append(v)
                
                window_multiplier += 1 # enlarge the window
            
            ### finding k nearest neighbors ###
            neighbors = list(set(neighbors))
            if node_index in neighbors:
                neighbors.remove(node_index)
            neighbors_distances = [polar(node_bbox, bboxs[n])[0] for n in neighbors]
            for sd_num, sd_idx in enumerate(np.argsort(neighbors_distances)):
                if sd_num < k:
                    if [node_index, neighbors[sd_idx]] not in edges and [neighbors[sd_idx], node_index] not in edges:
                        edges.append([neighbors[sd_idx], node_index])
                        edges.append([node_index, neighbors[sd_idx]])
                else: break

        return [e[0] for e in edges], [e[1] for e in edges]
    
    
    def __fromIMG(self, paths : list):
        
        graphs, node_labels, edge_labels = list(), list(), list()
        features = {
            'paths': paths, 
            'texts': [], 
            'boxs': []
            }

        for path in paths:
            # reader = easyocr.Reader(['en']) #! TODO: in the future, handle multilanguage!
            # result = reader.readtext(path, 
            #                  min_size=10, 
            #                 slope_ths=0.2, 
            #                 ycenter_ths=0.5, 
            #                 height_ths=0.5, 
            #                 width_ths=0.5,
            #                 decoder='wordbeamsearch', 
            #                 beamWidth=10, )
            
            img = file_to_images(path)[0] #Image.open(path).convert('RGB')
            size = img.size
            #draw = ImageDraw.Draw(img)
            # boxs, texts = list(), list()

            # for r in result:
            #     box = [int(r[0][0][0]), int(r[0][0][1]), int(r[0][2][0]), int(r[0][2][1])]
            #     draw.rectangle(box, outline='red', width=3)
            #     boxs.append(box)
            #     texts.append(r[1])
            
            word_boxes = get_word_boxes(path)
            boxs = word_boxes['boxes']
            boxs = [unnormalize_box(box, size[0], size[1]) for box in boxs]
            texts = word_boxes['words']
            #=======================================================

            features['boxs'].append(boxs)
            features['texts'].append(texts)
            #img.save('prova.png')

            # if self.edge_type == 'fully':
            #     u, v = self.fully_connected(range(len(boxs)))
            # elif self.edge_type == 'knn': 
            #     u,v = self.knn_connection(Image.open(path).size, boxs)
            # else:
            #     raise Exception('Other edge types still under development.')
            
            u, v = self.half_fully_connected(boxs, texts, self.word_to_word)

            g = dgl.graph((torch.tensor(u), torch.tensor(v)), num_nodes=len(boxs), idtype=torch.int32)
            graphs.append(g)

        return graphs, node_labels, edge_labels, features
    
    
    def __fromWB(self, paths : list, word_boxes_list : list, max_depth = 1):
        
        graphs, node_labels, edge_labels = list(), list(), list()
        features = {
            'paths': paths, 
            'texts': [], 
            'boxs': []
            }

        for word_boxes in word_boxes_list:
            boxes = word_boxes['boxes']
            words = word_boxes['words']

            features['boxs'].append(boxes)
            features['texts'].append(words)
            
            u, v = self.half_fully_connected(boxes, words, self.word_to_word)
            
            #Filtering================
            #u,v = remove_diag_edges2(boxes,u,v,words,0.4)
            #u,v = remove_vertical_edges(boxes,u,v)
            
            #u,v = remove_notline_edges(boxes,u,v)
            
            
            g = dgl.graph((torch.tensor(u), torch.tensor(v)), num_nodes=len(boxes), idtype=torch.int32)
            graphs.append(g)

        return graphs, node_labels, edge_labels, features
        

    def __fromPDF(self, src: str):
        #TODO: dev from PDF import of graphs
        return


    def __fromPAU(self, src: str):
        """ build graphs from Pau Riba's dataset

        Args:
            src (str) : path to where data is stored
        
        Returns:
            tuple (lists) : graphs, nodes and edge labels, features
        """

        graphs, node_labels, edge_labels = list(), list(), list()
        features = {'paths': [], 'texts': [], 'boxs': []}

        for image in tqdm(os.listdir(src), desc='Creating graphs'):
            if not image.endswith('tif'): continue
            
            img_name = image.split('.')[0]
            file_gt = img_name + '_gt.xml'
            file_ocr = img_name + '_ocr.xml'
            
            if not os.path.isfile(os.path.join(src, file_gt)) or not os.path.isfile(os.path.join(src, file_ocr)): continue
            features['paths'].append(os.path.join(src, image))

            # DOCUMENT REGIONS
            root = ET.parse(os.path.join(src, file_gt)).getroot()
            regions = []
            for parent in root:
                if parent.tag.split("}")[1] == 'Page':
                    for child in parent:
                        region_label = child[0].attrib['value']
                        region_bbox = [int(child[1].attrib['points'].split(" ")[0].split(",")[0].split(".")[0]),
                                    int(child[1].attrib['points'].split(" ")[1].split(",")[1].split(".")[0]),
                                    int(child[1].attrib['points'].split(" ")[2].split(",")[0].split(".")[0]),
                                    int(child[1].attrib['points'].split(" ")[3].split(",")[1].split(".")[0])]
                        regions.append([region_label, region_bbox])

            # DOCUMENT TOKENS
            root = ET.parse(os.path.join(src, file_ocr)).getroot()
            tokens_bbox = []
            tokens_text = []
            nl = []
            
            for parent in root:
                if parent.tag.split("}")[1] == 'Page':
                    for child in parent:
                        if child.tag.split("}")[1] == 'TextRegion':
                            for elem in child:
                                if elem.tag.split("}")[1] == 'TextLine':
                                    for word in elem:
                                        if word.tag.split("}")[1] == 'Word':
                                            word_bbox = [int(word[0].attrib['points'].split(" ")[0].split(",")[0].split(".")[0]),
                                                        int(word[0].attrib['points'].split(" ")[1].split(",")[1].split(".")[0]),
                                                        int(word[0].attrib['points'].split(" ")[2].split(",")[0].split(".")[0]),
                                                        int(word[0].attrib['points'].split(" ")[3].split(",")[1].split(".")[0])]
                                            word_text = word[1][0].text
                                            c = center(word_bbox)
                                            for reg in regions:
                                                r = reg[1]
                                                if r[0] < c[0] < r[2] and r[1] < c[1] < r[3]:
                                                    word_label = reg[0]
                                                    break
                                            tokens_bbox.append(word_bbox)
                                            tokens_text.append(word_text)
                                            nl.append(word_label)
            
            features['boxs'].append(tokens_bbox)
            features['texts'].append(tokens_text)
            node_labels.append(nl)

            # getting edges
            if self.edge_type == 'fully':
                u, v = self.fully_connected(range(len(tokens_bbox)))
            elif self.edge_type == 'knn': 
                u,v = self.knn_connection(Image.open(os.path.join(src, image)).size, tokens_bbox)
            else:
                raise Exception('Other edge types still under development.')
            
            el = list()
            for e in zip(u, v):
                if (nl[e[0]] == nl[e[1]]) and (nl[e[0]] == 'positions' or nl[e[0]] == 'total'):
                    el.append('table')
                else: el.append('none')
            edge_labels.append(el)

            g = dgl.graph((torch.tensor(u), torch.tensor(v)), num_nodes=len(tokens_bbox), idtype=torch.int32)
            graphs.append(g)
        
        return graphs, node_labels, edge_labels, features


    def __fromFUNSD(self, src : str):
        """Parsing FUNSD annotation files

        Args:
            src (str) : path to where data is stored
        
        Returns:
            tuple (lists) : graphs, nodes and edge labels, features
        """

        graphs, node_labels, edge_labels = list(), list(), list()
        features = {'paths': [], 'texts': [], 'boxs': []}
        # justOne = random.choice(os.listdir(os.path.join(src, 'adjusted_annotations'))).split(".")[0]
        
        if self.node_granularity == 'gt':
            for file in tqdm(os.listdir(os.path.join(src, 'adjusted_annotations')), desc='Creating graphs - GT'):
            
                img_name = f'{file.split(".")[0]}.png'
                img_path = os.path.join(src, 'images', img_name)
                features['paths'].append(img_path)

                with open(os.path.join(src, 'adjusted_annotations', file), 'r') as f:
                    form = json.load(f)['form']

                # getting infos
                boxs, texts, ids, nl = list(), list(), list(), list()
                pair_labels = list()

                for elem in form:
                    boxs.append(elem['box'])
                    texts.append(elem['text'])
                    nl.append(elem['label'])
                    ids.append(elem['id'])
                    [pair_labels.append(pair) for pair in elem['linking']]
                
                for p, pair in enumerate(pair_labels):
                    pair_labels[p] = [ids.index(pair[0]), ids.index(pair[1])]
                
                node_labels.append(nl)
                features['texts'].append(texts)
                features['boxs'].append(boxs)
                
                # getting edges
                if self.edge_type == 'fully':
                    u, v = self.fully_connected(range(len(boxs)))
                elif self.edge_type == 'knn': 
                    u,v = self.knn_connection(Image.open(img_path).size, boxs)
                else:
                    raise Exception('GraphBuilder exception: Other edge types still under development.')
                
                el = list()
                for e in zip(u, v):
                    edge = [e[0], e[1]]
                    if edge in pair_labels: el.append('pair')
                    else: el.append('none')
                edge_labels.append(el)

                # creating graph
                g = dgl.graph((torch.tensor(u), torch.tensor(v)), num_nodes=len(boxs), idtype=torch.int32)
                graphs.append(g)

            #! DEBUG PURPOSES TO VISUALIZE RANDOM GRAPH IMAGE FROM DATASET
            if False:
                if justOne == file.split(".")[0]:
                    print("\n\n### EXAMPLE ###")
                    print("Savin example:", img_name)

                    edge_unique_labels = np.unique(el)
                    g.edata['label'] = torch.tensor([np.where(target == edge_unique_labels)[0][0] for target in el])

                    g = self.balance_edges(g, 3, int(np.where('none' == edge_unique_labels)[0][0]))

                    img_removed = Image.open(img_path).convert('RGB')
                    draw_removed = ImageDraw.Draw(img_removed)

                    for b, box in enumerate(boxs):
                        if nl[b] == 'header':
                            color = 'yellow'
                        elif nl[b] == 'question':
                            color = 'blue'
                        elif nl[b] == 'answer':
                            color = 'green'
                        else:
                            color = 'gray'
                        draw_removed.rectangle(box, outline=color, width=3)

                    u, v = g.all_edges()
                    labels = g.edata['label'].tolist()
                    u, v = u.tolist(), v.tolist()

                    num_pair = 0
                    num_none = 0

                    for p, pair in enumerate(zip(u,v)):
                        sc = center(boxs[pair[0]])
                        ec = center(boxs[pair[1]])
                        if labels[p] == int(np.where('pair' == edge_unique_labels)[0][0]): 
                            num_pair += 1
                            color = 'violet'
                            draw_removed.ellipse([(sc[0]-4,sc[1]-4), (sc[0]+4,sc[1]+4)], fill = 'green', outline='black')
                            draw_removed.ellipse([(ec[0]-4,ec[1]-4), (ec[0]+4,ec[1]+4)], fill = 'red', outline='black')
                        else: 
                            num_none += 1
                            color='gray'
                        draw_removed.line((sc,ec), fill=color, width=3)
                    
                    print("Balanced Links: None {} | Key-Value {}".format(num_none, num_pair))
                    img_removed.save(f'esempi/FUNSD/{img_name}_removed_graph.png')

        # elif self.node_granularity == 'yolo':
        #     path_preds = os.path.join(src, 'yolo_bbox')
        #     path_images = os.path.join(src, 'images')
        #     path_gts = os.path.join(src, 'adjusted_annotations')
        #     all_paths, all_preds, all_links, all_labels, all_texts = load_predictions(path_preds, path_gts, path_images)
        #     for f, img_path in enumerate(tqdm(all_paths, desc='Creating graphs - YOLO')):
            
        #         features['paths'].append(img_path)
        #         features['boxs'].append(all_preds[f])
        #         features['texts'].append(all_texts[f])
        #         node_labels.append(all_labels[f])
        #         pair_labels = all_links[f]

        #         # getting edges
        #         if self.edge_type == 'fully':
        #             u, v = self.fully_connected(range(len(features['boxs'][f])))
        #         elif self.edge_type == 'knn': 
        #             u,v = self.knn_connection(Image.open(img_path).size, features['boxs'][f])
        #         else:
        #             raise Exception('GraphBuilder exception: Other edge types still under development.')
                
        #         el = list()
        #         for e in zip(u, v):
        #             edge = [e[0], e[1]]
        #             if edge in pair_labels: el.append('pair')
        #             else: el.append('none')
        #         edge_labels.append(el)

        #         # creating graph
        #         g = dgl.graph((torch.tensor(u), torch.tensor(v)), num_nodes=len(features['boxs'][f]), idtype=torch.int32)
        #         graphs.append(g)
        else:
            #TODO develop OCR too
            raise Exception('GraphBuilder Exception: only \'gt\' or \'yolo\' available for FUNSD.')


        return graphs, node_labels, edge_labels, features
    
    
    def __fromREMITTANCE(self, src : str):
        """Parsing FUNSD annotation files

        Args:
            src (str) : path to where data is stored
        
        Returns:
            tuple (lists) : graphs, nodes and edge labels, features
        """

        graphs, node_labels, edge_labels = list(), list(), list()
        features = {'paths': [], 'texts': [], 'boxs': []}
        # justOne = random.choice(os.listdir(os.path.join(src, 'adjusted_annotations'))).split(".")[0]
        
        if self.node_granularity == 'gt':
            files = os.listdir(os.path.join(src, 'layoutlm_annotations'))[:10]
            for file in tqdm(files, desc='Creating graphs - GT'):
            
                img_name = f'{file.split(".")[0]}.jpg'
                img_path = os.path.join(src, 'images', img_name)
                features['paths'].append(img_path)
                
                #size = Image.open(img_path).size
                img = cv2.imread(img_path)
                size = (img.shape[1],img.shape[0])

                with open(os.path.join(src, 'layoutlm_annotations', file), 'r') as f:
                    form = json.load(f)

                # getting infos
                boxs, texts, ids, nl = list(), list(), list(), list()
                pair_labels = list()

                for id, elem in enumerate(form):
                    boxs.append(unnormalize_box(elem['box'], size[0], size[1]))
                    texts.append(elem['text'])
                    
                    #debug
                    # if elem['text'].lower() in ['amount']:
                    #     elem['label'] = 'invoice_amount'
                    # else:
                    #     elem['label'] = 'O'
                    
                    if elem['label'] not in ['invoice_amount', 'invoice_date','invoice_number', 'payment_amount', 'payment_date','payment_number']:
                        nl.append('O')
                    else:
                        nl.append(elem['label'])
                    ids.append(id)
                    #[pair_labels.append(pair) for pair in elem['linking']]
                
                # for p, pair in enumerate(pair_labels):
                #     pair_labels[p] = [ids.index(pair[0]), ids.index(pair[1])]
                
                node_labels.append(nl)
                features['texts'].append(texts)
                features['boxs'].append(boxs)
                
                # getting edges
                if self.edge_type == 'fully':
                    u, v = self.half_fully_connected(boxs, texts, self.word_to_word)
                    #u, v = self.half_share_connected(boxs,texts)
                elif self.edge_type == 'knn': 
                    u,v = self.knn_connection(Image.open(img_path).size, boxs)
                else:
                    raise Exception('GraphBuilder exception: Other edge types still under development.')
                
                el = list()
                for e in zip(u, v):
                    edge = [e[0], e[1]]
                    if False: el.append('pair') #edge in pair_labels:
                    else: el.append('none')
                edge_labels.append(el)

                # creating graph
                g = dgl.graph((torch.tensor(u), torch.tensor(v)), num_nodes=len(boxs), idtype=torch.int32)
                graphs.append(g)

        # elif self.node_granularity == 'yolo':
        #     path_preds = os.path.join(src, 'yolo_bbox')
        #     path_images = os.path.join(src, 'images')
        #     path_gts = os.path.join(src, 'adjusted_annotations')
        #     all_paths, all_preds, all_links, all_labels, all_texts = load_predictions(path_preds, path_gts, path_images)
        #     for f, img_path in enumerate(tqdm(all_paths, desc='Creating graphs - YOLO')):
            
        #         features['paths'].append(img_path)
        #         features['boxs'].append(all_preds[f])
        #         features['texts'].append(all_texts[f])
        #         node_labels.append(all_labels[f])
        #         pair_labels = all_links[f]

        #         # getting edges
        #         if self.edge_type == 'fully':
        #             u, v = self.fully_connected(range(len(features['boxs'][f])))
        #         elif self.edge_type == 'knn': 
        #             u,v = self.knn_connection(Image.open(img_path).size, features['boxs'][f])
        #         else:
        #             raise Exception('GraphBuilder exception: Other edge types still under development.')
                
        #         el = list()
        #         for e in zip(u, v):
        #             edge = [e[0], e[1]]
        #             if edge in pair_labels: el.append('pair')
        #             else: el.append('none')
        #         edge_labels.append(el)

        #         # creating graph
        #         g = dgl.graph((torch.tensor(u), torch.tensor(v)), num_nodes=len(features['boxs'][f]), idtype=torch.int32)
        #         graphs.append(g)
        else:
            #TODO develop OCR too
            raise Exception('GraphBuilder Exception: only \'gt\' or \'yolo\' available for FUNSD.')


        return graphs, node_labels, edge_labels, features