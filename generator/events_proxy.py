from flask import Flask, request
import redis as Redis

proxy = Flask("proxy")
redis = Redis.Redis(host='redis', port=6379, db=0)

@proxy.route("/")
async def root():
    return "Hello"

@proxy.route("/users", methods=["GET"])
async def users():
    #offset = request.args.get("offset", "")
    return "<p>Hello, World!</p>" #redis.lrange("users", offset, -1)

if __name__ == '__main__':
    proxy.run(host='0.0.0.0', debug=True)