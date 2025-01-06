import hmac
import base64
import json
import httpx
from datetime import datetime, timezone

from urllib.parse import (
    urlencode, unquote, urlparse, parse_qsl, ParseResult
)

class OKXClient:
    def __init__(self, api_key, secret_key, passphrase, project_id=None, base_url="https://www.okx.com"):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.project_id = project_id
        self.base_url = base_url

    def _add_url_params(self, url, params):
        """ Add GET params to provided URL being aware of existing.

        :param url: string of target URL
        :param params: dict containing requested params to be added
        :return: string with updated URL

        >> url = 'https://stackoverflow.com/test?answers=true'
        >> new_params = {'answers': False, 'data': ['some','values']}
        >> add_url_params(url, new_params)
        'https://stackoverflow.com/test?data=some&data=values&answers=false'
        """
        # Unquoting URL first so we don't lose existing args
        url = unquote(url)
        # Extracting url info
        parsed_url = urlparse(url)
        # Extracting URL arguments from parsed URL
        get_args = parsed_url.query
        # Converting URL arguments to dict
        parsed_get_args = dict(parse_qsl(get_args))
        # Merging URL arguments dict with new params
        parsed_get_args.update(params)

        # Bool and Dict values should be converted to json-friendly values
        # you may throw this part away if you don't like it :)
        parsed_get_args.update(
            {k: json.dumps(v) for k, v in parsed_get_args.items()
             if isinstance(v, (bool, dict))}
        )

        # Converting URL argument to proper query string
        encoded_get_args = urlencode(parsed_get_args, doseq=True)
        # Creating new parsed result object based on provided with new
        # URL arguments. Same thing happens inside urlparse.
        new_url = ParseResult(
            parsed_url.scheme, parsed_url.netloc, parsed_url.path,
            parsed_url.params, encoded_get_args, parsed_url.fragment
        ).geturl()

        return new_url

    def _generate_signature(self, timestamp, method, request_path, body="", params=None):
        request_path = self._add_url_params(request_path, params) if params else request_path
        pre_hash = f"{timestamp}{method}{request_path}{body}"
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            pre_hash.encode("utf-8"),
            digestmod="sha256"
        ).digest()
        return base64.b64encode(signature).decode("utf-8")

    async def request(self, method, endpoint, params=None, body=None):
        url = f"{self.base_url}{endpoint}"
        timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        body_str = "" if not body else json.dumps(body)
        signature = self._generate_signature(timestamp, method.upper(), endpoint, body_str, params)

        headers = {
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": signature,
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json",
        }
        if self.project_id:
            headers["OK-ACCESS-PROJECT"] = self.project_id

        async with httpx.AsyncClient() as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, headers=headers, params=params)
                elif method.upper() == "POST":
                    response = await client.post(url, headers=headers, json=body)
                else:
                    raise ValueError("Unsupported HTTP method")

                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise RuntimeError(f"HTTP request failed: {e}")
            except httpx.HTTPStatusError as e:
                raise RuntimeError(f"HTTP error: {e.response.text}")
