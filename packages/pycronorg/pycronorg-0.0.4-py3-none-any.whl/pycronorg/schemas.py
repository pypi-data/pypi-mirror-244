from typing import Optional
from pydantic import BaseModel, Field


class Auth(BaseModel):
    enable: bool = False
    user: str = ""
    password = ""


class Notification(BaseModel):
    onFailure: bool = False
    onSuccess: bool = False
    onDisable: bool = False


class ExtendedData(BaseModel):
    headers: Optional[dict] = None
    body: Optional[str] = None


class Scheldule(BaseModel):
    timezone = "Europe/Berlin"
    expiresAt: int = 0  
    hours: list[int] = Field(default_factory=lambda: [-1])
    mdays: list[int] = Field(default_factory=lambda: [-1])
    minutes: list[int] = Field(default_factory=lambda: [0, 15, 30, 45])
    months: list[int] = Field(default_factory=lambda: [-1])
    wdays: list[int] = Field(default_factory=lambda: [-1])


class JobDetail(BaseModel):
    jobId: int
    enabled: bool = True
    title: str = "Example Job"
    url: str = "https://example.com/"
    saveResponses: bool = False
    lastStatus: Optional[int] = 0
    lastDuration: Optional[int] = 0
    lastExecution: Optional[int] = 0
    nextExecution: Optional[int] = 0
    type: int = 0
    requestTimeout: int = 300
    redirectSuccess: bool = False
    folderId: int = 0
    scheldule: Optional[Scheldule] = None
    auth: Optional[Auth] = None
    notification: Optional[Notification] = None
    extendedData: Optional[ExtendedData] = None
    requestMethod: int = 0


class JobsDetails(BaseModel):
    jobs: list[JobDetail]
    someFailed: bool = False


class JobDetailCreate(JobDetail):
    jobId: Optional[int] = None
    enabled: bool = True


class JobDetailUpdate(JobDetail):
    jobId: int
    enabled: Optional[bool] = None
    title: Optional[str] = None
    url: Optional[str] = None
    saveResponses: Optional[bool] = None
    lastStatus: Optional[int] = None
    lastDuration: Optional[int] = None
    lastExecution: Optional[int] = None
    nextExecution: Optional[int] = None
    type: Optional[int] = None
    requestTimeout: Optional[int] = None
    redirectSuccess: Optional[bool] = None
    folderId: Optional[int] = None
    scheldule: Optional[Scheldule] = None
    auth: Optional[Auth] = None
    notification: Optional[Notification] = None
    extendedData: Optional[ExtendedData] = None
    requestMethod: Optional[int] = None


class ItemStats(BaseModel):
    nameLookup: int
    connect: int
    appConnect: int
    preTransfer: int
    startTransfer: int
    total: int


class JobHistoryItem(BaseModel):
    jobLogId: int
    jobId: int
    identifier: str
    date: int
    datePlanned: int
    jitter: int
    url: str
    duration: int
    status: int
    statusText: str
    httpStatus: int
    headers: Optional[dict] = None
    body: Optional[str] = None
    stats: ItemStats


class JobHistory(BaseModel):
    history: list[JobHistoryItem]
    predictions: list[int]


class HistoryItemRetrieve(BaseModel):
    jobHistoryDetails: JobHistoryItem


class JobCreationResponse(BaseModel):
    jobId: int

