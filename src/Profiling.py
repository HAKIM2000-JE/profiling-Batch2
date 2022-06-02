
from bson import ObjectId

from sklearn.preprocessing import LabelEncoder

import environement

from sklearn.cluster import KMeans





import numpy as np
import pandas as pd



def getProfiles(df):

    cols = ['_id',"adults","children","babies","doubleBeds","singleBeds","sofaBeds","babyBeds","startDate"]
    df = df[cols]

    df['_id'] = df['_id'].apply(
        lambda x: str(x))

    encode = LabelEncoder()
    encoded = encode.fit_transform(df.iloc[:, 0])
    df['_id'] = encoded

    #extraire le mois depuis la date
    df['startDate'] = df['startDate'].apply(
        lambda x: pd.datetime.strptime(str(x), '%Y-%m-%d').month if type(x) == str else 1)








    kmeans = KMeans(n_clusters=environement.NBR_CLUSTER).fit(df)

    # Generated Profiles
    labels = kmeans.labels_


    #Means value of profiles
    centroids = kmeans.cluster_centers_

    print(pd.Series(labels).value_counts())
    ProfilingResult = []
    for i in np.unique(labels):
        profile_object={}
        centroids_objects= {}
        print("#########################################################")
        print( df[labels == i])
        encoded_reverse = encode.inverse_transform(df.iloc[:, 0])


        centroids_objects['adultsMean']=centroids[i].tolist()[1]
        centroids_objects['childrensMean'] = centroids[i].tolist()[2]
        centroids_objects['babiesMean'] = centroids[i].tolist()[3]
        centroids_objects['doubleBedsMean'] = centroids[i].tolist()[4]
        centroids_objects['singleBedsMean'] = centroids[i].tolist()[5]
        centroids_objects['sofaBedsMean'] = centroids[i].tolist()[6]
        centroids_objects['BabyBedsMean'] = centroids[i].tolist()[7]
        centroids_objects['startDateMean'] = centroids[i].tolist()[8]
        profile_object['centroids']= centroids_objects      #centroids[i]

        profile_object['propertyBookingsIds']=[ObjectId(x) for x in encoded_reverse.tolist() ]

        print("this is your profile object:", profile_object)

        ProfilingResult.append(profile_object)

        print(encoded_reverse.tolist())


    print("Centroide",centroids)



    return ProfilingResult



