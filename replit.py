import flask
from replit import db, web

# -- Create & configure Flask application.
app = flask.Flask(__name__)
app.static_url_path = "/static"

users = web.UserStore()

@app.route("/")
def index():
    return "Hello"


web.run(app)
def is_mod(username):
    # Check whether a user has moderator priveleges
    return web.auth.name in ("Scoder12", "Your_username_here")

# Landing page, only for signed out users
@app.route("/")
def index():
    if web.auth.is_authenticated:
        return web.local_redirect("/home")
    return flask.render_template("index.html")


# Home page, only for signed in users
@app.route("/home")
def home():
    if not web.auth.is_authenticated:
        return web.local_redirect("/")
    return flask.render_template("home.html", name=web.auth.name, MOD=is_mod(web.auth.name))
    users["example"] = {
  "tweets": [tweet]
}
tweet = {
  "ts": time.time() * 1000, # UTC in ms, will be used as a unique ID
  "body": "Hello repltweet!", # the body of the tweet
  "likes": ["Scoder12"] # a list of the usernames of the users who liked this tweet
}
# add to imports:
import time

@app.route("/api/tweet", methods=["POST"])
@web.params("body")
def api_tweet(body):
    if len(body) == 0:
        return {"error": "Cannot submit a blank tweet"}, 400

    newtweet = dict(body=body, ts=int(time.time() * 1000), likes=[])
    # Use .get() to handle missing keys
    users.current.get("tweets", []).append(newtweet)

    print(f"{web.auth.name} tweeted: {body!r}")

    return {"success": True}
    @app.route("/api/feed")
def feed():
  # The username is only stored as the key name, but the client
  # doesn't know the key name so add an author field to each tweet
  tweets = []
  for name in users.keys():
      for tweet in users[name].get("tweets", []):
          tweets.append({**tweet, "author": "name"})

  # Sort by time, newest first
  tweets = sorted(tweets, key=(lambda t: t.get("ts", 0)), reverse=True)

  return {"tweets": tweets}
  def find_matching_tweet(author, ts):
    matches = [t for t in users[author].get("tweets", []) if t.get("ts") == ts]
    if len(matches) == 1:
        return matches[0]
    else:
        return None
       @app.route("/api/like", methods=["POST"])
@web.params("author", "ts", "action")
def like(author, ts, action):
    # validate arguments
    if not ts.isdigit():
        return {"error": "Bad ts"}, 400
    ts = int(ts)
    if action not in ["like", "unlike"]:
        return {"error": "Invalid action"}, 400

    tweet = find_matching_tweet(author, ts)
    if tweet is None:
        return {"error": "Tweet not found"}, 404

    me = web.auth.name
    # Convert to a unique set so we can add and remove and prevent double liking
    likes = set(tweet.get("likes", []))
    if action == "like":
        likes.add(me)
    else:
        likes.discard(me)
    tweet["likes"] = list(likes)

    verb = "liked" if action == "like" else "unliked"
    print(f"{me} {verb} {author}'s tweet, it now has {len(likes)} likes")

    return {"success": True}
    import json

ratelimit = web.per_user_ratelimit(
  max_requests=60,
  period=60,
  login_res=json.dumps({"error": "Not signed in"}),
  get_ratelimited_res=(
      lambda time_left: json.dumps(
          {"error": f"Wait {time_left:.2f} sec before trying again."}
      )
  ),
)

# --snip--

@app.route("/api/tweet", methods=["POST"])
@ratelimit
@web.params("body")
def api_tweet(body):