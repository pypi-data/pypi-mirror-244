from requests import get
from requests.exceptions import RequestException
from random import randint


class Generation:
    def create(self, prompt):
        try:
            return get(
                url=f"https://image.pollinations.ai/prompt/{prompt}{randint(1, 10000)}",
                timeout=30,
            ).content
        except RequestException as exc:
            raise RequestException("Unable to fetch the response.") from exc
