from flask import request, abort
from flask_restx import Namespace, Resource, fields
import json
import db
import logging
from bson.objectid import ObjectId

logger = logging.getLogger(__name__)
mongo = db.mongo

api = Namespace("profiles", description="Profile related routes", path="/api/profiles")

profile = api.model(
    "Profile",
    {
        "_id": fields.String(required=True, description="Profile ID"),
        "user": fields.String(required=True, description="Belong to user"),
        "firstname": fields.String(),
        "lastname": fields.String(),
        "age": fields.Integer(),
        "discipline": fields.String(),
    },
)

PROFILES = [
    {
        "user": ObjectId("5f7968905510ad91c3510870"),
        "firstname": "John",
        "lastname": "Lee",
        "age": "22",
        "discipline": "Computer Science",
    }
]


@api.route("/profile/user/<userid>")
class Profile(Resource):
    @api.doc("Get profile by userid")
    @api.marshal_with(profile)
    def get(self, userid):
        if not userid:
            abort(400, "Bad request.")

        profile_col = mongo.db.profiles
        target_profile = profile_col.find_one({"user": ObjectId(userid)})
        logger.debug(target_profile)
        if not target_profile:
            abort(404, "Profile not found.")
        else:
            return target_profile, 200

    @api.doc("Create profile for userid")
    @api.marshal_with(profile)
    def post(self, userid):
        if not userid:
            abort(400, "Bad request.")
        user_col = mongo.db.users
        profile_col = mongo.db.profiles

        target_user = user_col.find_one({"_id": ObjectId(userid)})
        if not target_user:
            abort(404, "User not found.")

        target_profile = profile_col.find_one({"user": ObjectId(userid)})
        if target_profile:
            abort(400, "Profile already exists.")

        profile_new = {}
        profile_new["user"] = ObjectId(userid)
        profile_new["firstname"] = request.form.get("firstname")
        profile_new["lastname"] = request.form.get("lastname")
        profile_new["age"] = request.form.get("age")
        profile_new["discipline"] = request.form.get("discipline")

        profile_col = mongo.db.users
        profile_added = profile_col.insert_one(profile_new)
        profile_new["_id"] = profile_added.inserted_id

        if profile_added:
            return profile_new, 200
        else:
            abort(500, "Failed to create profile.")