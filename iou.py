from shapely.geometry import Polygon
import sys

def calculate_iou_yolo(box_1, box_2):
    bb1_half_w = box_1[2]/2
    bb1_half_h = box_1[3]/2
    bb1_x1 = box_1[0] - bb1_half_w
    bb1_y1 = box_1[1] - bb1_half_h
    bb1_x2 = box_1[0] + bb1_half_w
    bb1_y2 = box_1[1] + bb1_half_h


    bb2_half_w = box_2[2]/2
    bb2_half_h = box_2[3]/2
    bb2_x1 = box_2[0] - bb2_half_w
    bb2_y1 = box_2[1] - bb2_half_h
    bb2_x2 = box_2[0] + bb2_half_w
    bb2_y2 = box_2[1] + bb2_half_h

    b1 = [ [bb1_x1, bb1_y1], [bb1_x2, bb1_y1], [bb1_x2, bb1_y2], [bb1_x1, bb1_y2] ]
    b2 = [ [bb2_x1, bb2_y1], [bb2_x2, bb2_y1], [bb2_x2, bb2_y2], [bb2_x1, bb2_y2] ]

    poly_1 = Polygon(b1)
    poly_2 = Polygon(b2)
    iou = poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
    return iou

validations = []
predictions = []
with open(sys.argv[1], 'r') as val_file:
    while True:
        line = val_file.readline()
        entries = line.strip().split(' ')
        if not line:
            break
        #print(entries) #1,2,3,4
        box = [ float(entries[1]), float(entries[2]), float(entries[3]), float(entries[4]) ]
        validations.append(box)

with open(sys.argv[2], 'r') as pred_file:
    while True:
        line = pred_file.readline()
        entries = line.strip().split(' ')
        if not line:
            break
        #print(entries) #5,6,7,8
        box = [ float(entries[5]), float(entries[6]), float(entries[7]), float(entries[8]) ]
        predictions.append(box)

#print("validations: ", validations)
#print("predictions: ", predictions)

iou_scores = []
best_ious = []
indices_of_best_ious = []
for v in validations:
    iou_row = [] 
    index = 0
    index_of_best_iou = 0
    best_iou = -1
    for p in predictions:
        iou = calculate_iou_yolo(v, p)
        iou_row.append(iou)
        if iou > best_iou:
            best_iou = iou
            index_of_best_iou = index
        index = index + 1

    best_ious.append(best_iou)
    indices_of_best_ious.append(index_of_best_iou)
    iou_scores.append(iou_row)

#print("pair-wise iou: ", iou_scores)
#print("best ious: ", best_ious)
#print("indices of best ious: ", indices_of_best_ious)
unique_ious = 0
unique_ious = len(set(indices_of_best_ious)) == len(indices_of_best_ious)
if (unique_ious):
    print("best ious: ", best_ious)

