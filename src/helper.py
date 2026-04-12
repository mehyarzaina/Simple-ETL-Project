from datetime import datetime
#transformation phase

#Convert list fields to comma-separated string.
def list_to_string(value):
    if not value:
        return None
    return ", ".join(value)


#Convert API pubDate string to datetime object.
def parse_pub_date(date_str):
    
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None