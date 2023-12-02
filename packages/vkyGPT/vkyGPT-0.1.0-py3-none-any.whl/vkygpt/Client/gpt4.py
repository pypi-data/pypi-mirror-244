from uuid import uuid4
from re import findall
from curl_cffi.requests import get, RequestsError


class Completion:
    def create(self, prompt):
        resp = get(
            "https://you.com/api/streamingSearch",
            headers={
                "cache-control": "no-cache",
                "referer": "https://you.com/search?q=gpt4&tbm=youchat",
                "cookie": f"safesearch_guest=Off; uuid_guest={str(uuid4())}",
            },
            params={
                "q": prompt,
                "page": 1,
                "count": 10,
                "safeSearch": "Off",
                "onShoppingPage": False,
                "mkt": "",
                "responseFilter": "WebPages,Translations,TimeZone,Computation,RelatedSearches",
                "domain": "youchat",
                "queryTraceId": str(uuid4()),
                "chat": [],
            },
            impersonate="chrome107",
        )
        if "youChatToken" not in resp.text:
            raise RequestsError("Unable to fetch the response.")
        return (
            "".join(
                findall(
                    r"{\"youChatToken\": \"(.*?)\"}",
                    resp.content.decode("unicode-escape"),
                )
            )
            .replace("\\n", "\n")
            .replace("\\\\", "\\")
            .replace('\\"', '"')
        )
