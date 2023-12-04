from requests import post
from requests.exceptions import RequestException


class Completion:
    def create(self, prompt):
        try:
            resp = post(
                "https://us-central1-arched-keyword-306918.cloudfunctions.net/run-inference-1",
                json={"prompt": prompt},
            )
            resp_json = resp.json()
        except RequestException as exc:
            raise RequestException("Unable to fetch the response.") from exc
        return resp_json["completion"]
