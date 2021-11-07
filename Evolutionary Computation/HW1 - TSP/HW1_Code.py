import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm.notebook import tqdm
import math

pi = math.pi
data = np.genfromtxt('tsp.txt', delimiter=',')

circle_points = [(math.cos(2*pi/36*x)*0.5,math.sin(2*pi/36*x)*0.5) for x in range(0,36+1)] #generate a set of 36 points on the circumference of circle with radius 0.5
circle_points = list(circle_points); random.shuffle(circle_points)

test_data = circle_points #while using the generated circle data
test_data = data #while using the actual data

##Random Search
%%time
shortest_iteration_series = []
longest_iteration_series = []
shortest_dist_best = np.infty
longest_dist_best = 0

for epoch in tqdm(range(50000)):
    iter_data = list(test_data); random.shuffle(iter_data)
    iter_data = np.vstack([iter_data,iter_data[0]])
    total_dist = 0
    for i in range(len(iter_data)-1):
        node_dist = np.sqrt((iter_data[i+1][1]-iter_data[i][1])**2+(iter_data[i+1][0]-iter_data[i][0])**2)
        total_dist += node_dist
    #total_dist +=  np.sqrt((iter_data[0][1]-iter_data[len(iter_data)-1][1])**2+(iter_data[len(iter_data)-1][0]-iter_data[0][0])**2)
    if total_dist<shortest_dist_best:
        shortest_dist_best=total_dist
        shortest_path = iter_data
        shortest_iteration_series.append((epoch,total_dist))
    if total_dist>longest_dist_best:
        longest_dist_best=total_dist
        longest_path = iter_data
        longest_iteration_series.append((epoch,total_dist))
shortest_iteration_series = np.asarray(shortest_iteration_series)
shortest_path= np.asarray(shortest_path)
longest_iteration_series = np.asarray(longest_iteration_series)
longest_path= np.asarray(longest_path)
        
#Hill Climber
##For shortest path
current_data = data
output = []
shortest_dist = np.infty
shortest_iteration_series = []
#before swapping
for i in range(len(current_data)-1):
    node_dist = np.sqrt((current_data[i+1][1]-current_data[i][1])**2+(current_data[i+1][0]-current_data[i][0])**2)
    current_dist += node_dist
current_dist += np.sqrt((current_data[len(current_data)-1][1]-current_data[0][1])**2+(current_data[len(current_data)-1][0]-current_data[0][0])**2)
for epoch in tqdm(range(50000)):
    swap_index = random.randint(0,len(current_data)-2)
    new_data = current_data.copy() #for swapping
    new_data[swap_index], new_data[swap_index+1] = current_data[swap_index+1], current_data[swap_index]
    new_dist = 0
    for i in range(len(new_data)-1):
        node_dist = np.sqrt((new_data[i+1][1]-new_data[i][1])**2+(new_data[i+1][0]-new_data[i][0])**2)
        new_dist += node_dist
    new_dist += np.sqrt((new_data[len(new_data)-1][1]-new_data[0][1])**2+(new_data[len(new_data)-1][0]-new_data[0][0])**2)
    if new_dist<shortest_dist:
        shortest_dist = new_dist
        shortest_path = new_data
        current_data = new_data
        shortest_iteration_series.append((epoch,new_dist))
shortest_iteration_series = np.asarray(shortest_iteration_series)
shortest_path= np.asarray(shortest_path)

#Hill Climber
##For longest path
current_data = data
current_dist = 0
longest_dist = 0
longest_iteration_series = []
#before swapping
for i in range(len(current_data)-1):
    node_dist = np.sqrt((current_data[i+1][1]-current_data[i][1])**2+(current_data[i+1][0]-current_data[i][0])**2)
    current_dist += node_dist
current_dist += np.sqrt((current_data[len(current_data)-1][1]-current_data[0][1])**2+(current_data[len(current_data)-1][0]-current_data[0][0])**2)
for epoch in tqdm(range(50000)):
    swap_index = random.randint(0,len(current_data)-2)
    new_data = current_data.copy() #for swapping
    new_data[swap_index], new_data[swap_index+1] = current_data[swap_index+1], current_data[swap_index]
    new_dist = 0
    for i in range(len(new_data)-1):
        node_dist = np.sqrt((new_data[i+1][1]-new_data[i][1])**2+(new_data[i+1][0]-new_data[i][0])**2)
        new_dist += node_dist
    new_dist += np.sqrt((new_data[len(new_data)-1][1]-new_data[0][1])**2+(new_data[len(new_data)-1][0]-new_data[0][0])**2)
    if new_dist>longest_dist:
        longest_dist = new_dist
        longest_path = new_data
        current_data = new_data
        longest_iteration_series.append((epoch,new_dist))
longest_iteration_series = np.asarray(longest_iteration_series)
longest_path= np.asarray(longest_path)