from okxos.client import OKXClient

class DEXAPI:
    def __init__(self, client: OKXClient):
        self.client = client
    #@classmethod
    #async def create(cls, client: OKXClient):
    #    self = cls()
    #    self.client = client
    #    self.chain_id = chain_id
    #    self.pool = await self._get_tokens(self.chain_id)
    #    return self
    
    #async def _get_tokens(self, chain_id):
    #    endpoint = "/api/v5/dex/aggregator/all-tokens"
    #    params = {"chainId": chain_id}
    #    raw = await self.client.request("GET", endpoint, params=params)
    #    if raw:
    #        tokens = {}
    #        for t in raw['data']:
    #            tokens[t['tokenSymbol']] = t
    #        self.tokens = tokens

    async def get_supported_chains(self, chain_id=None):
        endpoint = "/api/v5/dex/aggregator/supported/chain"
        params = {"chainId": chain_id} if chain_id else None
        return await self.client.request("GET", endpoint, params=params)

    # 获取币种列表
    async def get_all_tokens(self, chain_id):
        endpoint = "/api/v5/dex/aggregator/all-tokens"
        params = {"chainId": chain_id}
        return await self.client.request("GET", endpoint, params=params)
    
    async def get_quote(self, chain_id, token_in, token_out, amount_in):
        endpoint = "/api/v5/dex/aggregator/quote"
        params = {
            "chainId": chain_id,
            "fromTokenAddress": token_in,
            "toTokenAddress": token_out,
            "amount": amount_in,
        }
        return await self.client.request("GET", endpoint, params=params)
    