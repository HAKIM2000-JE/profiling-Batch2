# Data base params
DATA_BASE_NAME = 'yaago-prod-clone'

#URL_DATA_BASE = 'mongodb+srv://stage:password1234$@yaago-prod-cluster-pri.hq5rg.mongodb.net/yaago-prod?authSource=admin&replicaSet=atlas-i9ni26-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true'
URL_DATA_BASE='mongodb://root:T8GRF2_uB4%2F%3FqCvq@149.202.107.243:29517/?authSource=admin&readPreference=primary&directConnection=true&ssl=false'


BATCH_HOUR="02:28"
NBR_CLUSTER= 5

# Name of collection :

COLLECTION_TAGS = 'tags'
COLLECTION_RECOMMENDATION = 'recommendation'
COLLECTION_GUEST_TAG = 'guestTag'
COLLECTION_GUEST_CATEGORY = 'guestCategory'
COLLECTION_GUEST_REVIEWS = 'guestReviews'
COLLECTION_PROPRETYBOOKING='propertyBooking'
COLLECTION_PROPRETY = 'property'
COLLECTION_COUNTRY='country'
COLLECTION_PROFILE='profil'
COLLECTION_REGION='region'

#Data Scoring
SCORE_nbClickRecoCard = 1
SCORE_nbClickRecoMarker = 2
SCORE_nbClickRecoWebSite = 4
SCORE_nbClickRecoDirection = 10
SCORE_clickOnSliderPictures = 3





# Geust Gender :
GEUST_GENDER_MALE = 'homme'
GEUST_GENDER_FEMALE = 'femme'
GEUST_GENDER_AUTRE = 'A'

