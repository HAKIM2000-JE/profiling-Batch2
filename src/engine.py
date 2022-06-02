
from bson import ObjectId

from service import Service
import environement



import  Profiling

ServiceData = Service()


#get recommendation List of every Profile
def getProfileRecommendation(ListProfileId, CloseRecommendation):
    List = []

    #on boucle sur les Bonne Adreses
    for index, row in CloseRecommendation.iterrows():
        DATA = {}
        if not ServiceData.get_guestReviews({"_id.recommendationId": row['_id']}).empty:
                        Recommandation_guestReviews = ServiceData.get_guestReviews({"_id.recommendationId": row['_id']})

                        #on recupere l id du voyageur
                        guetId= ObjectId(Recommandation_guestReviews['_id'].tolist()[0]['guestId'])

                        #verification que le voyageur appartinet au profile
                        if (guetId in ListProfileId):
                            DATA['Recommendation Id'] = row['_id']
                            DATA['poi']=row['poi']

                            #calcule du score
                            DATA['SCORE'] = getScore(Recommandation_guestReviews['nbClickRecoCard'],
                                                         Recommandation_guestReviews['nbClickRecoMarker'], \
                                                         Recommandation_guestReviews['nbClickRecoWebSite'],
                                                         Recommandation_guestReviews['nbClickRecoDirection'],
                                                         Recommandation_guestReviews['clickOnSliderPictures'])

                            List.append(DATA)
                        else :
                         print("no score from profile guest ")

    print("outside the boucle :", List)


    RecommendationList=[]
    for element in List:

        RecommendationData = {}


        RecommendationData['Recommendation Id'] = element['Recommendation Id']

        RecommendationData['poi'] = element['poi']
        RecommendationData['score'] = element['SCORE'].tolist()[0]


        RecommendationList.append(RecommendationData)

    #afiichage par score decroissant


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









