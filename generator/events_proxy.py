from flask import Flask, request
import redis as Redis

proxy = Flask(__name__)
proxy.env = "development"

redis = Redis.Redis(host='redis', port=6379, db=0)

@proxy.route("/")
async def home():
    return {"text":"Welcome to pyrogi!"}

@proxy.route("/users", methods=["GET"])
async def users():
    offset = request.args.get("offset", "")
    if offset:
        return f"{redis.lrange('users', int(offset), -1)}"
    else:
        return f"{redis.lrange('users', 0, -1)}"
    

@proxy.route("/events", methods=["GET"])
async def events():
    offset = request.args.get("offset", "")
    if offset:
        return f"{redis.lrange('events', int(offset), -1)}"
    else:
        return f"{redis.lrange('events', 0, -1)}"
        

if __name__ == '__main__':
    proxy.run(host='0.0.0.0', debug=True)