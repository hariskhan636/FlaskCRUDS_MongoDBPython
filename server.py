from flask import Flask, Response, request
from bson.objectid import ObjectId
import pymongo
import json

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host='localhost',
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo.company
    mongo.server_info()
except:
    print("Error - Cant connect to the db")

if __name__ == "__main__":
    app.run(port=80, debug=True)


#########################################################################################


@app.route("/users", methods=["POST"])
def create_user():
    try:

        user = {"name": request.form["name"],
                "lastName": request.form["lastName"]}
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)

        return Response(
            response=json.dumps(
                {"message": "user created", "id": f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print(ex)

#########################################################################################


@app.route("/users", methods=["GET"])
def get_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])

        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps(
                {"message": "cannot read user"}),
            status=500,
            mimetype="application/json"
        )

#########################################################################################


@app.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name": request.form["name"]}}
        )
        if dbResponse.modified_count == 1:
            return Response(
                response=json.dumps(
                    {"message": "updated user"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps(
                    {"message": "nothing to update"}),
                status=200,
                mimetype="application/json"
            )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps(
                {"message": "cannot update user"}),
            status=500,
            mimetype="application/json"
        )

#########################################################################################


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(
                response=json.dumps(
                    {"message": "deleted user", "id": "f{id}"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps(
                {"message": "nothing to delete"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps(
                {"message": "cannot delete user"}),
            status=500,
            mimetype="application/json"
        )
