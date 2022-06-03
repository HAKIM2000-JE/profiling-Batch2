
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

    # get data
    DataFrame_Recommendation = CloseRecommendation
    DataFrame_GuestReviewsScore = ServiceData.get_guestReviews({"_id.recommendationId": {
        "$in": ListRecommendationsId}, "_id.guestId": {"$in": ListProfileId}})

    DataFrame_GuestTags = ServiceData.get_guestTag(
        {"_id.guestId": {"$in": ListProfileId}})
    DataFrame_GuestCategorie = ServiceData.get_guestCategory(
        {"_id.guestId": {"$in": ListProfileId}})

    # get score of behvior :

    # get score of like :
    # get  score of tags :
    # get score of categorie :

    # get moyenne of score : is the big score

    # on boucle sur les Bonne Adreses
    RecommendationList = []
    for index, recommendation in CloseRecommendation.iterrows():
        recommendation_id = recommendation['_id']
        DATA = {}
        DATA['Recommendation Id'] = recommendation['_id']
        DATA['poi'] = recommendation['poi']

        # calcule du score
        DATA['SCORE'] = get_big_score(ListProfileId, recommendation_id, DataFrame_GuestReviewsScore,
                                      DataFrame_Recommendation, DataFrame_GuestTags, DataFrame_GuestCategorie)
        RecommendationList.append(DATA)

    return RecommendationList


def get_big_score(LIST_IDs_OF_GUEST_IN_PROFILE_ON_REGION, recommendation_id, DataFrame_GuestReviewsScore, DataFrame_Recommendation, DataFrame_GuestTags, DataFrame_GuestCategorie):
    LIST_OF_SCORE = []
    for guest_id in LIST_IDs_OF_GUEST_IN_PROFILE_ON_REGION:

        # get score of behavior
        BEHAVIOR_SCORE = getScore_BEHAVIOR_byID(
            guest_id, recommendation_id, DataFrame_GuestReviewsScore)
        # get score of like
        LIKE_SCORE = getScore_LIKE_byID(
            guest_id, recommendation_id, DataFrame_Recommendation)
        # get score of tag
        TAG_SCORE = getScore_TAG_byID(
            guest_id, recommendation_id, DataFrame_GuestTags, DataFrame_Recommendation)
        # get score of categorie :
        CATEGORIE_SCORE = getScore_CATEGORIE_byID(
            guest_id, recommendation_id, DataFrame_GuestCategorie, DataFrame_Recommendation)

        MOY_SCORE = (BEHAVIOR_SCORE+LIKE_SCORE+TAG_SCORE+CATEGORIE_SCORE)/4
        LIST_OF_SCORE.append(MOY_SCORE)
    return max(LIST_OF_SCORE)


def getScore_BEHAVIOR_byID(guest_id, recommendation_id, DataFrame_GuestReviewsScore):
    # No bugs
    # Score Data
    NB_score = environement.SCORE_nbClickRecoCard + environement.SCORE_nbClickRecoMarker+environement.SCORE_nbClickRecoWebSite + \
        environement.SCORE_nbClickRecoDirection + \
        environement.SCORE_clickOnSliderPictures
    for index, row in DataFrame_GuestReviewsScore.iterrows():
        if(str(guest_id) == str(row['guestId']) and str(recommendation_id) == str(row['recommendationId'])):
            # initialise sum to zero:
            SUM_MOY = 0

            SCORE_nbClickRecoCard = row['nbClickRecoCard'] * \
                environement.SCORE_nbClickRecoCard

            SCORE_nbClickRecoMarker = row['nbClickRecoMarker'] * \
                environement.SCORE_nbClickRecoMarker

            SCORE_nbClickRecoWebSite = row['nbClickRecoWebSite'] * \
                environement.SCORE_nbClickRecoWebSite

            SCORE_nbClickRecoDirection = row['nbClickRecoDirection'] * \
                environement.SCORE_nbClickRecoDirection

            SCORE_clickOnSliderPictures = row['clickOnSliderPicturesScore'] * \
                environement.SCORE_clickOnSliderPictures

            # Summ all scores :
            SUM_MOY = SCORE_nbClickRecoCard + SCORE_nbClickRecoMarker+SCORE_nbClickRecoWebSite + \
                SCORE_nbClickRecoDirection+SCORE_clickOnSliderPictures

            # create Score Beheiver :
            SCORE_BEHAVIOR = (SUM_MOY/NB_score)*100
            return int(SCORE_BEHAVIOR)
    return 0


def getScore_LIKE_byID(guest_id, recommendation_id, DataFrame_Recommendation):
    for index, row in DataFrame_Recommendation.iterrows():
        recommendationId = row['_id']
        if (str(recommendationId) == str(recommendation_id)):
            bookingWhichLikes = row['bookingWhichLikes']
            if(isinstance(bookingWhichLikes, list) and bookingWhichLikes != None):
                for _id in bookingWhichLikes:
                    if(str(_id) == str(guest_id)):
                        return 1
    return 0


def getScore_TAG_byID(guest_id, recommendation_id, DataFrame_GuestTags, DataFrame_Recommendation):
    print('Get data is DONE !')
    for index, row_recommendation in DataFrame_Recommendation.iterrows():
        if(str(row_recommendation) == str(recommendation_id)):
            if 'tagIds' in row_recommendation.keys():
                tagIds = row_recommendation['tagIds']
                SCORE_TAG = 0
                TAGS_LEN = 0
                for index, row_guest_tag in DataFrame_GuestTags.iterrows():
                    if ((str(guest_id) == str(row_guest_tag['guestId'])) and (row_guest_tag['tagId'] in tagIds)):
                        SCORE_TAG = SCORE_TAG + row_guest_tag['nbClickTag']

                return SCORE_TAG/TAGS_LEN
            else:
                return 0
    return 0


def getScore_CATEGORIE_byID(guest_id, recommendation_id, DataFrame_GuestCategorie, DataFrame_Recommendation):
    for index, row_recommendation in DataFrame_Recommendation.iterrows():
        if(str(row_recommendation) == str(recommendation_id)):
            if 'category' in row_recommendation.keys():
                category = row_recommendation['category']
                SCORE_CATEGORIE = 0
                for index, row_guest_categorie in DataFrame_GuestCategorie.iterrows():
                    if (str(guest_id) == str(row_guest_categorie['guestId'])) and (category == row_guest_categorie['category']):
                        print('CALCULE DES CATEGORY')
                        SCORE_CATEGORIE = row_guest_categorie['nbClickCategory']
                        return SCORE_CATEGORIE
                return SCORE_CATEGORIE
            else:
                return 0
    return 0


# def getScore(nbClickRecoCard, nbClickRecoMarker, nbClickRecoWebSite, nbClickRecoDirection, clickOnSliderPictures):
#     NB_score = environement.SCORE_nbClickRecoCard + environement.SCORE_nbClickRecoMarker + environement.SCORE_nbClickRecoWebSite + \
#         environement.SCORE_nbClickRecoDirection + \
#         environement.SCORE_clickOnSliderPictures

#     score = nbClickRecoMarker * environement.SCORE_nbClickRecoMarker + nbClickRecoCard*environement.SCORE_nbClickRecoCard +\
#         nbClickRecoDirection * environement.SCORE_nbClickRecoDirection + \
#         nbClickRecoWebSite*environement.SCORE_nbClickRecoDirection

#     return score / NB_score


# def getScoreOnSliderPictures(clickOnSliderPictures):
#     print(clickOnSliderPictures)

#     if clickOnSliderPictures.bool() == True:
#         return environement.SCORE_clickOnSliderPictures
#     else:
#         return 0
