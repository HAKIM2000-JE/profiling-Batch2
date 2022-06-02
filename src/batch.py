

from service import Service
from datetime import date, datetime

from database import Database
import environement

Database.initialize()

import  Profiling


import psutil




import engine


def run():

    ServiceData = Service()

    Regions = ServiceData.get_Region_DataFrame({})

    # on boucle sur les regions
    for index, Region in Regions.iterrows():

        if Region['geometry'].get('type') == "Polygon":
            #list des propriétées on cas de region polygon
            Properties = ServiceData.get_Property_DataFrame({"poi": {"$geoWithin": {
                "$geometry": {"type": "Polygon", "coordinates": Region.get('geometry').get('coordinates')}}}})

        else:
            # list des propriétées on cas de region Multipolygon
            Properties = ServiceData.get_Property_DataFrame({"poi": {"$geoWithin": {
                "$geometry": {"type": "MultiPolygon", "coordinates": Region.get('geometry').get('coordinates')}}}})


        if not Properties.empty:


            ListPropertyId = [row['_id'] for index, row in Properties.iterrows()]

            Database.DATABASE[environement.COLLECTION_REGION].update_one({ "_id": Region['_id'] },{"$unset": {'propertiesIds' :1}})

            #Mettre a jour la list des propertiesIds par region
            Database.DATABASE[environement.COLLECTION_REGION].update_one({ "_id": Region['_id'] },{"$set":  {'propertiesIds' :ListPropertyId}})

            # Liste des réservations pris dans ces proprietés en passé
            Reservations = ServiceData.get_PropretBooking_DataFrame(
                {"propertyId": {"$in": ListPropertyId}, "startDate": {"$lt": datetime.now().strftime("%Y-%m-%d")},"removed":False})

            FinalProfilesList = []
            if not Reservations.empty:

                # Service de création des profiles
                Profiles = Profiling.getProfiles(Reservations)

                #On boucle sur les profiles
                for Profile in Profiles:
                    #creation de l'objet profile à stocker sur la base
                    Profile_Object = {}
                    Profile_Object['regionId'] = Region['_id']
                    Profile_Object['propertyBookingsIds'] = Profile.get('propertyBookingsIds')
                    Profile_Object['centroids'] = Profile.get('centroids')


                    if Region['geometry'].get('type') == "Polygon":

                        #les recommandations au niveau de la region en cas de region Polygon
                        Recommendations = ServiceData.get_Recommendation_DataFrame({"poi": {"$geoWithin": {
                            "$geometry": {"type": "Polygon",
                                          "coordinates": Region.get('geometry').get('coordinates')}}}})

                    else:
                        #les recommandations au niveau de la region en cas de multiPolygon
                        Recommendations = ServiceData.get_Recommendation_DataFrame({"poi": {"$geoWithin": {
                            "$geometry": {"type": "MultiPolygon",
                                          "coordinates": Region.get('geometry').get('coordinates')}}}})

                    if not Recommendations.empty:
                        #list des recommandations dans la région apres scoring pour chauqe profile
                        Recommendation_Output = engine.getProfileRecommendation(Profile.get('propertyBookingsIds'),
                                                                                Recommendations)
                        if len(Recommendation_Output) > 0:
                            listRecommendations = []
                            for recommendation in Recommendation_Output:

                                print("Scored Recommendation", recommendation)
                                # creartion de l'objet recommandation à sotcker sur la base
                                RecommendationScore = {}
                                RecommendationScore['recommendationId'] = recommendation.get('Recommendation Id')
                                RecommendationScore['poi'] = recommendation.get('poi')
                                RecommendationScore['score'] = recommendation.get('score')
                                listRecommendations.append(RecommendationScore)
                            #ajout des recommandations comme attributs d'objet profile
                            Profile_Object['recommendationScores'] = listRecommendations

                            #List des profiles à  stocker
                            FinalProfilesList.append(Profile_Object)

            if len(FinalProfilesList) > 0:
                #suppression des anciens profiles de la région
                Database.DATABASE[environement.COLLECTION_PROFILE].delete_many({"regionId": Region['_id']})
                # Ajout des nouveau profile de la région
                Database.DATABASE[environement.COLLECTION_PROFILE].insert_many(FinalProfilesList)
        #consommation cpu en pourcentage
        print('The CPU usage is: ', psutil.cpu_percent(5))