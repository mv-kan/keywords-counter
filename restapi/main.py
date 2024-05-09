from fastapi import FastAPI
import redis
from pydantic import BaseModel
from enum import Enum
from uuid import uuid4
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
# assuming that redis is in docker compose 
redis_url = "redis://redis:6379"
app = FastAPI()
r = redis.from_url(redis_url, decode_responses=True)

text_count_q = "text_count_q"

class Health(BaseModel):
    ok: bool

class Keyword(BaseModel):
    keyword: str

class KeywordCount(BaseModel):
    keyword: str
    count: int

class KeywordCountRequest(BaseModel):
    text: str
    keyword: str

class RequestId(BaseModel):
    rid: str

class CountRequest(BaseModel):
    rid: str
    keyword: str
    text: str

class StatusEnum(str, Enum):
    error = "error"
    ok = "ok"

class RequestStatus(BaseModel):
    status: RequestStatusEnum = RequestStatusEnum.error

@app.get("/health")
async def health() -> Health:
    return Health(ok=True)

@app.post("/request-status")
async def request_status(req: RequestId) -> RequestStatus:
    value = r.get(f"request:{req.rid}")
    result = RequestStatus(status=RequestStatusEnum.error)
    # magic numbers i know 
    if value == RequestStatusEnum.started:
        result.status = RequestStatusEnum.started
    elif value == RequestStatusEnum.finished:
        result.status = RequestStatusEnum.finished
    return result    

@app.post("/keyword")
async def keyword(keyword: Keyword) -> KeywordCount: 
    value = r.get(f"keyword:{keyword.keyword}")
    result = KeywordCount(keyword=keyword.keyword, count=0)
    if value != None:
        result.count = value
    return result

@app.post("/count-keywords")
async def count_keywords(req: KeywordCountRequest) -> RequestId:
    rid = uuid4()
    count_request = CountRequest(rid=rid.hex, keyword=req.keyword, text=req.text)
    r.rpush(text_count_q, count_request.model_dump_json())
    return RequestId(rid=rid.hex)