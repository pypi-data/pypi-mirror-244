from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import httpx
from pydantic import BaseModel

from typing import Any
import inspect
import importlib

from sarya import UI
from .request_typings import NewMessage, Response
from .signature import HMAS


class AIRequest:
    def __init__(self) -> None:
        pass

    async def __call__(self, request: Request):
        self.request = request
        self.j = await request.json()
        return self

    @property
    def messages(self):
        print(self.j)
        return self.j["messages"]


class Sarya:
    def __init__(self, key: str | None = None):
        self.key = key
        self._set_app()

    def run(self, main: str | None = "main", host: str = "0.0.0.0", port: int = 8000):
        caller_frame = inspect.currentframe().f_back
        caller_module_info = inspect.getmodule(caller_frame)
        if caller_module_info is not None:
            caller_module_name = caller_module_info.__name__
            module = importlib.import_module(caller_module_name)

            main_func = getattr(module, main)
            self.main_function = main_func
            self.app.post("/main")(self.main)
            uvicorn.run(self.app, host=host, port=port)
        else:
            raise Exception("Could not find main function")

    def _set_app(self):
        self.app = FastAPI()
        self.app.get("/subscribe")(self._subscribe)
        self.app.get("//subscribe")(self._subscribe)
        self.app.middleware("http")(self._hmas)

    def main(self, payload: NewMessage):
        # add func to be post route
        if (params := len(inspect.signature(self.main_function).parameters)) == 2:
            output = self.main_function(payload.messages, payload.meta)
        elif params == 1:
            output = self.main_function(payload.messages)
        else:
            output = self.main_function()
        if isinstance(output, Response):
            return output
        elif isinstance(output, UI.Text) or isinstance(output, UI.Image):
            return Response(messages=[output])
        elif isinstance(output, list):
            return Response(messages=output)
        return Response(**output)

    async def _subscribe(self):
        return {"data": {"secret": self.key}}

    async def _hmas(self, request: Request, call_next):
        sign = await HMAS.verify(self.key, request)
        if sign:
            return await call_next(request)
        else:
            return JSONResponse(
                {"error": "request was not sign correctly"}, status_code=401
            )
