import psycopg2
import decimal
#Berkeley Conkling MIlestone 3
#This is the code to calculate my metrics

def executeQuery(sql_str):  # call this to run queries
    try:
        conn = psycopg2.connect("dbname='Yelp' user='postgres' host='localhost' password='Cyborg1137!'")
    except psycopg2.Error as e:
        print(f"Unable to connect to the database! Error: {e}")
        return None

    cur = conn.cursor()
    cur.execute(sql_str)
    conn.commit()
    result = cur.fetchall()
    conn.close()
    return result

def executeQueryNoRet(sql_str):  # call this to run queries
    try:
        conn = psycopg2.connect("dbname='Yelp' user='postgres' host='localhost' password='Cyborg1137!'")
    except psycopg2.Error as e:
        print(f"Unable to connect to the database! Error: {e}")
        return None

    cur = conn.cursor()
    cur.execute(sql_str)
    conn.commit()
    conn.close()


reviewThreshold = 3.75
nonZeroAvg = 13.11


# Function to calculate partial success based on review rating
def calculatePartialSuccess(rating):
    if rating < reviewThreshold:
        return rating - reviewThreshold
    else:
        return rating - reviewThreshold


# Function to calculate popularity score
def calculatePopularity(checkins):
    return float(checkins) / nonZeroAvg


sql_str = "SELECT business_id, num_checkins, review_rating FROM Business;"
businessData = executeQuery(sql_str)

if businessData:
   #with open('update_queries.sql', 'w') as file:
    count = 0
    for row in businessData:
        count = count + 1
        id = row[0]
        popularity = calculatePopularity(row[2])
        success = popularity * calculatePartialSuccess(row[1])
        update_sql = f"UPDATE Business SET popularity_score = '{popularity}', success_score = '{success}' WHERE business_id = '{id}';"
        #file.write(update_sql)
        print(count)
        executeQueryNoRet(update_sql)