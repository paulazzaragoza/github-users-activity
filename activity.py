from datetime import datetime
import urllib.request as request
import urllib.error as error
import json
import os

#dict that saves the relevant info for each event
event_dict = {
    "CommitCommentEvent": {
        "count": 0,
        "emoji": "💬",
        "description": "A comment was made on a commit:"},
    "CreateEvent": {
        "count": 0,
        "emoji": "🆕",
        "description": "A branch, tag, or repository was created:"},
    "DeleteEvent": {
        "count": 0,
        "emoji": "❌",
        "description": "A branch or tag was deleted:"},
    "ForkEvent": {
        "count": 0,
        "emoji": "🍴",
        "description": "The repository was forked:"},
    "GollumEvent": {
        "count": 0,
        "emoji": "📄",
        "description": "A Wiki page was created or edited:"},
    "IssueCommentEvent": {
        "count": 0,
        "emoji": "🗨️ ",
        "description": "A comment was made on an Issue or Pull Request:"},
    "IssuesEvent": {
        "count": 0,
        "emoji": "🐞",
        "description": "An Issue was opened, closed, or edited:"},
    "MemberEvent": {
        "count": 0,
        "emoji": "👤",
        "description": "A collaborator was added to or removed from the repository:"},
    "PublicEvent": {
        "count": 0,
        "emoji": "🔓",
        "description": "The repository was made public:"},
    "PullRequestEvent": {
        "count": 0,
        "emoji": "📦",
        "description": "A Pull Request was opened, closed, or updated:"},
    "PullRequestReviewEvent": {
        "count": 0,
        "emoji": "✅",
        "description": "A Pull Request was reviewed (approved or requested changes):"},
    "PullRequestReviewCommentEvent": {
        "count": 0,
        "emoji": "📝",
        "description": "A comment was made on the code in a Pull Request:"},
    "PullRequestReviewThreadEvent": {
        "count": 0,
        "emoji": "🧵",
        "description": "A review thread in a Pull Request was resolved or reopened:"},
    "PushEvent": {
        "count": 0,
        "emoji": "🚀",
        "description": "One or more commits were pushed to a branch:"},
    "ReleaseEvent": {
        "count": 0,
        "emoji": "📦✨",
        "description": "A release was created or updated:"},
    "SponsorshipEvent": {
        "count": 0,
        "emoji": "💰",
        "description": "A sponsorship was created or updated:"},
    "WatchEvent": {
        "count": 0,
        "emoji": "⭐",
        "description": "A repository was starred:"}
}

#saves the json info of the request
data_json = None

#headers for the request
headers = {
    "User-Agent": "Python urllib",
    "Accept": "application/vnd.github.v3+json"
}


#checks if more than 2 hours have passed since the last modification of the JSON file for the specific user
def time_diff(file):
    passed_hours = False

    file_exists = os.path.exists(file)

    if file_exists == True:
        file_timestamp = os.path.getmtime(file)
        file_datetime = datetime.fromtimestamp(file_timestamp)

        now_datetime = datetime.now()

        diff = now_datetime - file_datetime

        if diff.seconds >= 3600 * 2:
            passed_hours = True

    return passed_hours

#function that loads all json data into the variable
def get_json_data(file):
    global data_json
    try:
        with open (file, "r") as file:
            data_json = json.load(file)

    except json.JSONDecodeError:
        data_json = []


#function that request the data from the GitHub API
def request_data(url, file):
    global data_json

    req = request.Request(url, headers=headers)
    try:
        with request.urlopen(req) as response:
            data = response.read()
            data_json = json.loads(data)
            with open (file, "w") as file:
                json.dump(data_json, file, indent=4)

    except error.HTTPError as exception:
        raise Exception(exception)

#gets the info for each event type
def get_events_info():
    keys = event_dict.keys()

    for key in keys:
        for event in data_json:
                if event["type"] == key:
                    event_dict[key]["count"] += 1

#prints the info for each event
def print_events_info():
    keys = event_dict.keys()

    for key in keys:
        if event_dict[key]["count"] > 0:
            print(f'-{event_dict[key]["emoji"]} {event_dict[key]["description"]} {event_dict[key]["count"]} times.')


if __name__ == "__main__":
    username = input(">>> github-activity enter the username: ")

    try:
        url = f"https://api.github.com/users/{username}/events"
        json_file_path = f".{username}-data.json"

        if not time_diff(json_file_path):
            request_data(url, json_file_path)
        else:
            get_json_data(json_file_path)

        get_events_info()
        print_events_info()

    except Exception as exception:
        print(exception)