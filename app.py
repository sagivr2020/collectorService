import json
import psycopg2
import os


def app(event, context):
    body = {
        "message": "Executed!",
        "input": event,
    }

    try:
        connection = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_TYPE_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'])
        cursor = connection.cursor()

        datastr = json.loads(event['body'])
        if os.environ['TOKEN'] != datastr['token']:
            print('Unauthorized')
            body = {
                "message": "Unauthorized access!",
                "input": event,
            }
            response = {"statusCode": 401, "body": json.dumps(body)}
            return response

        cursor.execute("INSERT INTO public.requests_table (data) VALUES (%s);", (json.dumps(event['body']),))
        connection.commit()
        cursor.close()
    except (Exception, psycopg2.Error) as error:
        print("log Error: ", error)
        body = {
            "message": "An error occurred!",
            "input": event,
        }
        response = {"statusCode": 500, "body": json.dumps(body)}
        return response
    finally:
        if connection is not None:
            connection.close()

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
