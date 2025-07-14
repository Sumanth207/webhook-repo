def format_event(data):
    event_type = data.get("event_type")
    author = data.get("author")
    from_branch = data.get("from_branch")
    to_branch = data.get("to_branch")
    timestamp = data.get("timestamp")

    if event_type == "push":
        return f'"{author}" pushed to "{to_branch}" on {timestamp}'
    elif event_type == "pull_request":
        return f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
    elif event_type == "merge":
        return f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
    else:
        return "Unknown event"