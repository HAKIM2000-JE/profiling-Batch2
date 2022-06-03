
from bson import ObjectId

from service import Service
import environement


import Profiling

ServiceData = Service()


# get recommendation List of every Profile
def getProfileRecommendation(ListProfileId, CloseRecommendation):
    List = []

    # Create list of recommendation
    ListRecommendationsId = [row['_id']
                             for index, row in CloseRecommendation.iterrows()]

    List_tags_util = []
    List_category_util = []
    for index, row in CloseRecommendation.iterrows():
        # get tags util
        if ('tagIds' in row.keys()):
            tagIds = row['tagIds']
            for tag_id in tagIds:
                if tag_id not in List_tags_util:
                    List_tags_util.append(tag_id)

        if ('category' in row.keys()):
            category = row['category']
            if (category not in List_category_util and category != None):
                List_category_util.append(category)



    DataFrame_GuestReviewsScore = ServiceData.get_guestReviews({"recommendationId": {
        "$in": ListRecommendationsId}, "guestId": {"$in": ListProfileId}})

    DataFrame_GuestTags = ServiceData.get_guestTag(
        {"guestId": {"$in": ListProfileId}, "_id": {"$in": List_tags_util}})

    print(DataFrame_GuestTags.columns)

    DataFrame_GuestCategorie = ServiceData.get_guestCategory(
        {"guestId": {"$in": ListProfileId}, "category": {"$in": List_category_util}})

    print(DataFrame_GuestCategorie.columns)

    for index, recommendation in CloseRecommendation.iterrows():
        DATA = {}
        scoreLike=0
        scoreTag=0
        scoreCategory=0
        for index, row in DataFrame_GuestReviewsScore.iterrows():
            if recommendation['_id'] == row['recommendationId']:
                DATA['Recommendation Id'] = recommendation['_id']
                DATA['poi'] = recommendation['poi']
                scoreBehavior = getScore(row['nbClickRecoCard'],
                                         row['nbClickRecoMarker'], \
                                         row['nbClickRecoWebSite'],
                                         row['nbClickRecoDirection'],
                                         row['clickOnSliderPictures'])

                if 'bookingWhichLikes' in recommendation.keys():
                    for _id in recommendation['bookingWhichLikes']:
                        if _id in ListProfileId :
                            scoreLike= scoreLike + environement.SCORE_LIKE

                for index , row in DataFrame_GuestCategorie.iterrows():
                    scoreCategory =scoreCategory+  row['nbClickCategory']

                for index , row in  DataFrame_GuestTags.iterrows():
                    scoreCategory = scoreCategory + row['nbClickTag']


                DATA['SCORE']= (scoreTag+ scoreCategory + scoreBehavior + scoreLike)/4
                List.append(DATA)
    RecommendationList=[]
    for element in List:

        RecommendationData = {}


        RecommendationData['Recommendation Id'] = element['Recommendation Id']

        RecommendationData['poi'] = element['poi']
        RecommendationData['score'] = element['SCORE']


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

