import time


from flask import  Flask

from service import Service

import schedule
import batch
from database import Database
import environement


Database.initialize()



app = Flask(__name__)


# Service data
ServiceData = Service()








if __name__ == "__main__":

    schedule.every().day.at(environement.BATCH_HOUR).do(batch.run)

    while True:
        schedule.run_pending()
        time.sleep(1)

    app.run(debug=False)



