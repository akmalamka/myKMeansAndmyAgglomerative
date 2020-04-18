from itertools import permutations
import math

def calculateAccuracy(data,konfig):
#I.S. data memiliki label dan prediksi klaster
#F.S. mengembalikan nilai akurasi dari data
#Proses: mencari nilai true-positif dibandingkan dengan jumlah datum
#Asumsi: #Asumsi: Kolom terakhir data : cluster, Kolom 1 sebelum terakhir data : label
    tp = 0      #inisialisasi nilai awal true positif
    temp = data
    for i in range(len(data)):
        if((konfig.index(temp[i][-2])) == (int(temp[i][-1]))):
            tp += 1
    return(tp/len(data))

def convertCluster(data):
#I.S. data memiliki label dan prediksi klaster, prediksi label memiliki syntax berbeda
#F.S. mengembalikan data dengan klaster yang sudah di convert sehingga syntax dan semantik sama dengan label
#Proses: menyamakan dengan kombinasi sehingga masing-masing klaster memiliki akurasi terbaik
#Asumsi: Kolom terakhir data : cluster, Kolom 1 sebelum terakhir data : label
    #mengidentifikasi nilai unik label
    label = getUniqueCluster(data)

    #Semua kemungkinan permutasi label
    labelPerm = list(permutations(label))
    konfigurasi = labelPerm[0]
    akurasi = 0

    #Mencari konfigurasi permutasi dengan nilai akurasi maksimum
    for perm in labelPerm:
        #mengganti setiap label dengan konfigurasi bersesuaian
        acc = calculateAccuracy(data,perm)
        if(acc > akurasi):
            akurasi = acc
            konfigurasi = perm

    for datum in data:
        datum[-1] = konfigurasi[int(datum[-1])]
    return(data,akurasi)

def getUniqueCluster(data):
#I.S. data memiliki label dan klaster
#F.S. mengembalikan nilai unik dari label yang ada
#Asumsi: Kolom terakhir data : cluster, Kolom 1 sebelum terakhir data : label
    label = []
    for datum in data:
        if((datum[-2]) not in label):
            label.append(datum[-2])
    return(label)

def calculateFMI(data):
#I.S. data memiliki label dan klaster
#F.S. mengembalikan nilai FMI untuk setiap klaster yang ada
#Asumsi: Kolom terakhir data : cluster, Kolom 1 sebelum terakhir data : label
    label = getUniqueCluster(data)
    result = []
    for cluster in label:
        tp = 0
        fp = 0
        fn = 0
        for datum in data:
            if((datum[-2] == cluster) and (datum[-1] == cluster)):
                tp += 1
            elif((datum[-1] == cluster) and (datum[-2] != cluster)):
                fp += 1
            elif((datum[-1] != cluster) and (datum[-2] == cluster)):
                fn += 1
        fmi = (tp)/(math.sqrt((tp+fp)*(tp+fn)))
        result.append([cluster,fmi])
    return result

def avgIntraDistance(datum, cluster):
#I.S. datum adalah objek yang diamati terhadap data di cluster
#F.S. mengembalikan nilai rata-rata jarak dari datum terhadap semua objek di intra-cluster
#Asumsi: kolom pada cluster berisikan properti objek
    distance = 0.0
    for obj in cluster:
        dist = 0.0
        for i in range(len(datum)-2):
            dist += pow(((float(datum[i]))-(float(obj[i]))),2)
        distance += math.sqrt(dist)

    return(distance/(len(cluster)-1))  #dikurangi satu karena pada kenyataan jarak datum ke dirinya dihitung

def avgInterDistance(datum, cluster):
#I.S. datum adalah objek yang diamati terhadap data di cluster
#F.S. mengembalikan nilai rata-rata jarak dari datum terhadap semua objek di cluster
#Asumsi: kolom pada cluster berisikan properti objek
    distance = 0.0
    for obj in cluster:
        dist = 0.0
        for i in range(len(datum)-2):
            dist += pow(((float(datum[i]))-(float(obj[i]))),2)
        distance += math.sqrt(dist)

    return(distance/(len(cluster)))

def splitCluster(data):
#I.S. data memiliki cluster
#F.S. mengembalikan data baru yang sudah terbagi atas clusternya
#Asumsi: kolom terakhir data adalah klaster
    label = []
    result = []
    for x in data:
        if(x[-1] not in label):
            label.append(x[-1])
    for x in label:
        clust = []
        for datum in data:
            if(datum[-1] == x):
                obj = []
                for i in range(len(datum)-1):
                    obj.append(datum[i])
                clust.append(obj)
        result.append([clust,x])
    return(result)

def calculateSilhoutte(data):
#I.S. data memiliki sejumlah properti, label, dan prediksi klaster
#F.S. akan dikembalikan sebuah data baru dengan tambahan kolom koefisien silhoutte masing-masing datum
#Asumsi: Kolom terakhir data : cluster, Kolom 1 sebelum terakhir data : label
    silhoutte = []
    splitedData = splitCluster(data)
    for datum in data:
        a = 0
        b = []
        for cluster in splitedData:
            if(cluster[-1] == datum[-1]):
                a = avgIntraDistance(datum,cluster[0])
            else:
                b.append(avgInterDistance(datum,cluster[0]))
        b = min(b)
        silhoutte.append((b-a)/(max([a,b])))
        
    return silhoutte

