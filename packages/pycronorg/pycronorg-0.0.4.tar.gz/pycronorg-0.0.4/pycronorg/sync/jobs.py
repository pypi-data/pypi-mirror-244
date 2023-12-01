from typing import Optional
from pycronorg.schemas import (
    HistoryItemRetrieve,
    JobCreationResponse,
    JobDetailUpdate,
    JobHistory,
    JobsDetails, 
    JobDetailCreate,
    Scheldule,
)
from .base import BaseApi


class JobsApi(BaseApi):
    _DEFAULT_BASE_PATH = "jobs"
    Schema = JobDetailCreate 
    SchemaUpdate = JobDetailUpdate
    SchelduleSchema = Scheldule

    def __init__(self, token, *, base_path=None, headers=None) -> None:
        super().__init__(token, base_path=base_path, headers=headers)
        self._base_path = f"{base_path}/jobs"

    def all(self) -> JobsDetails:
        res = self._safe_response(self._proxy_request.get(self._url, headers=self._headers))
        return JobsDetails(**res.json())
    
    def get(self, jobId: int):
        url = f"{self._url}/{jobId}"
        res = self._safe_response(self._proxy_request.get(url, headers=self._headers))
        return JobsDetails(**res.json())

    def delete(self, jobId: int):
        url = f"{self._url}/{jobId}"
        self._safe_response(self._proxy_request.delete(url, headers=self._headers))

    def create(self, jobDetail: JobDetailCreate):
        jobData = jobDetail.dict(exclude_unset=True)

        if not 'enabled' in jobData:
            jobData['enabled'] = True

        res = self._safe_response(
            self._proxy_request.put(
                self._url, 
                headers=self._headers, 
                json={
                    'job': jobData,
                }
            )
        )
        return JobCreationResponse(**res.json())

    def update(self, jobDetail: JobDetailUpdate):
        url = f"{self._url}/{jobDetail.jobId}"
        self._safe_response(
            self._proxy_request.patch(
                url, 
                headers=self._headers, 
                json={
                    'job': jobDetail.dict(exclude_unset=True),
                }
            )
        )

    def retrive_history(self, jobId):
        url = f"{self._url}/{jobId}/history"
        res = self._safe_response(self._proxy_request.get(url, headers=self._headers))
        return JobHistory(**res.json())

    def retrive_history_item(self, jobId, identifier):
        url = f"{self._url}/{jobId}/history/{identifier}"
        res = self._safe_response(self._proxy_request.get(url, headers=self._headers))
        return HistoryItemRetrieve(**res.json())

