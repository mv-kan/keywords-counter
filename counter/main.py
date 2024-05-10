import redis
####
from pydantic import BaseModel
from enum import Enum

class RequestStatusEnum(str, Enum):
    error = "error"
    started = "started"
    finished = "finished"

class CountRequest(BaseModel):
    rid: str
    keyword: str
    text: str
####
redis_url = "redis://redis:6379"
r = redis.from_url(redis_url, decode_responses=True)

text_count_q = "text_count_q"

def safe_int(value, default=0):
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (ValueError, TypeError):
        return default

def handle_text_count_q(req_json):
    req = CountRequest.model_validate_json(req_json)
    r.set(f"request:{req.rid}", RequestStatusEnum.started)

    n = req.text.count(req.keyword)
    value = r.get(f"keyword:{req.keyword}")
    value = safe_int(value)
    r.set(f"keyword:{req.keyword}", n + value)
    print(f"keyword:{req.keyword} = count:{n + value}")
    r.set(f"request:{req.rid}", RequestStatusEnum.finished)


print("counter: init successful, queue listening...")

while True:
    v = r.blpop([text_count_q])
    if v[0] == text_count_q:
        handle_text_count_q(v[1])