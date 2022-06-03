
from bson import ObjectId

from service import Service
import environement



import  Profiling

ServiceData = Service()


#get recommendation List of every Profile
def getProfileRecommendation(ListProfileId, CloseRecommendation):
    List = []

    ListRecommendationsId = [row['_id'] for index, row in CloseRecommendation.iterrows()]
    guestReviews = ServiceData.get_guestReviews({"_id.recommendationId":{"$in": ListRecommendationsId},"_id.guestId":{"$in": ListProfileId}})

    guestTags = ServiceData.get_guestTag({"_id.guestId":{"$in": ListProfileId}})
    guestCategorie= ServiceData.get_guestCategory({"_id.guestId":{"$in": ListProfileId}})

    #on boucle sur les Bonne Adreses
    for index, recommendation in CloseRecommendation.iterrows():
        DATA = {}
        for index, row in  guestReviews.iterrows():

           if  recommendation['_id']==row['recommendationId']:

                            DATA['Recommendation Id'] = recommendation['_id']
                            DATA['poi']=recommendation['poi']

                            #calcule du score
                            DATA['SCORE'] = getScore(row['nbClickRecoCard'],
                                                         row['nbClickRecoMarker'], \
                                                         row['nbClickRecoWebSite'],
                                                         row['nbClickRecoDirection'],
                                                         row['clickOnSliderPictures'])

                            List.append(DATA)






    RecommendationList=[]
    for element in List:

        RecommendationData = {}


        RecommendationData['Recommendation Id'] = element['Recommendation Id']

        RecommendationData['poi'] = element['poi']
        RecommendationData['score'] = element['SCORE']


        RecommendationList.append(RecommendationData)




    return   RecommendationList











def getScore(nbClickRecoCard,nbClickRecoMarker,nbClickRecoWebSite,nbClickRecoDirection , clickOnSliderPictures):
    NB_score = environement.SCORE_nbClickRecoCard + environement.SCORE_nbClickRecoMarker + environement.SCORE_nbClickRecoWebSite + \
               environement.SCORE_nbClickRecoDirection + \
               environement.SCORE_clickOnSliderPictures

    score = nbClickRecoMarker* environement.SCORE_nbClickRecoMarker + nbClickRecoCard*environement.SCORE_nbClickRecoCard+\
            nbClickRecoDirection* environement.SCORE_nbClickRecoDirection + nbClickRecoWebSite*environement.SCORE_nbClickRecoDirection

    return score /NB_score




def getScoreOnSliderPictures(clickOnSliderPictures):
    print(clickOnSliderPictures)

    if clickOnSliderPictures.bool()==True:
        return environement.SCORE_clickOnSliderPictures
    else:
        return 0









