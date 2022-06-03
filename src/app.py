import time


from service import Service
import schedule
import batch
from database import Database
import environement
Database.initialize()
print('RUUUUUUUUUUUUUUUn')

# Service data
ServiceData = Service()


if __name__ == "__main__":

    schedule.every().day.at(environement.BATCH_HOUR).do(batch.run)

    while True:
        print('STAAART')
        schedule.run_pending()
        time.sleep(1000)
