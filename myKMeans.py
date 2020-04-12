import numpy as np
import copy
import pandas as pd
import math
import random

class KMeans:
    def __init__(self, data, n_cluster):
        self.data = copy.deepcopy(data)
        self.n_cluster = n_cluster
        self.centroid = random.choices(self.data, k=self.n_cluster) #memilih titik cluster awal secara acak
        self.centroid_equal = False
        self.coordinate_count = len(self.data[0])
        i = 0
        while(not self.centroid_equal):
            self.distance = []
            self.group = []
            self.calculateDistance() #menghitung jarak masing masing titik dengan titik cluster
            self.grouping() # mengelompokkan berdasarkan kedekatan dengan suatu titik cluster
            self.updateCentroid() # mengubah nilai centroid
            i = i + 1
    def calculateDistance(self):
        for i in range(len(self.data)):
            arr = []
            for j in range(len(self.centroid)):
                arr.append(self.euclideanDistance(self.data[i], self.centroid[j]))
            self.distance.append(arr)

    def euclideanDistance(self, point, centroid):
        sum = 0
        for i in range(len(point)):
            sum = sum + (point[i] - centroid[i])*(point[i] - centroid[i])
        sum = math.sqrt(sum)
        return sum

    def grouping(self):
        for i in range(len(self.distance)):
            self.group.append(self.distance[i].index(min(self.distance[i])))

    def updateCentroid(self):
        new_centroid = []
        for i in range(self.n_cluster):
            cluster_index = [j for j in range(len(self.group)) if self.group[j] == i]
            # if (len(cluster_index) == 0): pastiin ga mungkin ada kasus ini
            avg = self.average(cluster_index)
            new_centroid.append(avg)
        self.centroid_equal = True
        for i in range(self.n_cluster):
            for j in range(self.coordinate_count):
                if (self.centroid[i][j] != new_centroid[i][j]):
                    self.centroid_equal = False
                    break
        if (not self.centroid_equal):
            self.centroid = new_centroid

    def average(self, cluster_index):
        avg_all = []
        for i in range(self.coordinate_count):
            sum = 0
            for j in range(len(cluster_index)):
                sum = sum + self.data[cluster_index[j]][i]
            average_coordinate = sum / len(cluster_index)
            avg_all.append(average_coordinate)
        return avg_all