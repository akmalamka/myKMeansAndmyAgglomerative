import itertools
import copy
import numpy as np

class Aglomerative:
    # A, B = satu cluster
    def single(self, A, B):
        i = 0
        for a, b in itertools.product(A, B):
            if (i == 0):
                temp = self.dist(a, b)
            else:
                temp = min(self.dist(a, b), temp)
            i += 1

        return temp

    def complete(self, A, B):
        i = 0
        for a, b in itertools.product(A, B):
            if (i == 0):
                temp = self.dist(a, b)
            else:
                temp = max(self.dist(a, b), temp)
            i += 1

        return temp

    def average(self, A, B):
        i = 0
        temp_sum = 0
        for a, b in itertools.product(A, B):
            temp_sum += self.dist(a, b)
            i += 1

        return temp_sum/i

    def average_group(self, A, B):
        i = 0
        for index in A:
            if i == 0:
                cluster_A = [self.data[index]]
            else:
                cluster_A.append(self.data[index])
            i += 1
        cluster_A = np.array(cluster_A)
        mean_A = np.mean(cluster_A, axis=0)

        i = 0
        for index in B:
            if i == 0:
                cluster_B = [self.data[index]]
            else:
                cluster_B.append(self.data[index])
            i += 1
        cluster_B = np.array(cluster_B)
        mean_B = np.mean(cluster_B, axis=0)

        temp = 0
        for x, y in zip(mean_A, mean_B):
            temp += abs(x - y)

        return temp

    # a, b = satu data dalam sebuah cluster
    def dist(self, a, b):
        temp = 0
        for x, y in zip(self.data[a], self.data[b]):
            temp += abs(x - y)

        return temp

    # distance_function = [single, complete, average, average_group]
    def __init__(self, data, distance_function_name):
        self.data = data.to_numpy()
        self.cluster = []
        self.cluster_history = []
        
        for i in range(len(self.data)):
            self.cluster.append([i])

        self.distance = self.__getattribute__(distance_function_name)
        self.train()

    def train(self):
        while (len(self.cluster) != 1):            
            sum_of_distance = 0
            for i in range(len(self.cluster)):
                for j in range(i + 1, len(self.cluster)):                        
                    temp = self.distance(self.cluster[i], self.cluster[j])
                    if (i == 0 and j == 1):
                        min_distance = temp
                        min_index = [i, j]
                    else:
                        if (temp < min_distance):
                            min_distance = temp
                            min_index = [i, j]
                        
                    sum_of_distance += temp

            self.cluster_history.append((sum_of_distance, copy.deepcopy(self.cluster)))

            # Gabungin 2 cluster dengan jarak minimum
            a = self.cluster[min_index[0]]
            b = self.cluster[min_index[1]]
            self.cluster.append(a + b)
            self.cluster.remove(a)
            self.cluster.remove(b)
        self.cluster_history.append((0, copy.deepcopy(self.cluster)))

    def get_result_by_treshold(self, treshold):
        for distance_sum, clusters in self.cluster_history:
            if (distance_sum < treshold):
                result = ['' for i in range(len(self.data))]
                for cluster in clusters:
                    for obj in cluster:
                        result[obj] = clusters.index(cluster)
                return result

    def get_result_by_number_of_cluster(self, number_of_cluster):
        for distance_sum, clusters in self.cluster_history:
            if (len(clusters) <= number_of_cluster):
                result = ['' for i in range(len(self.data))]
                for cluster in clusters:
                    for obj in cluster:
                        result[obj] = clusters.index(cluster)
                return result
