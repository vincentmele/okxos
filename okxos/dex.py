from okxos.client import OKXClient

class DEXAPI:
    def __init__(self, client: OKXClient):
        self.client = client

    async def get_supported_chains(self, chain_id=1):
        # https://www.okx.com/web3/build/docs/waas/dex-get-aggregator-supported-chains
        endpoint = "/api/v5/dex/aggregator/supported/chain"
        params = {"chainId": chain_id} if chain_id else None
        return await self.client.request("GET", endpoint, params=params)

    async def get_all_tokens(self, chain_id=1):
        # https://www.okx.com/web3/build/docs/waas/dex-get-tokens
        endpoint = "/api/v5/dex/aggregator/all-tokens"
        params = {"chainId": chain_id}
        return await self.client.request("GET", endpoint, params=params)
    
    async def get_liquidity_sources(self, chain_id=1):
        # https://www.okx.com/web3/build/docs/waas/dex-get-tokens
        endpoint = "/api/v5/dex/aggregator/all-tokens"
        params = {"chainId": chain_id}
        return await self.client.request("GET", endpoint, params=params)
    
    async def approve_transactions(self, token_contract_address: str, approve_amt: float, chain_id=1):
        # https://www.okx.com/web3/build/docs/waas/dex-get-tokens
        endpoint = "/api/v5/dex/aggregator/all-tokens"
        params = {"chainId": chain_id,
                  "tokenContractAddress": token_contract_address,
                  "approveAmount": approve_amt}
        return await self.client.request("GET", endpoint, params=params)

    async def get_quote(self, amount_in: float, from_token_address, 
                        to_token_address, dex_ids=None, price_impact_protection_percentage=None, 
                        fee_percent=None, chain_id=1):
        # https://www.okx.com/web3/build/docs/waas/dex-get-quote
        endpoint = "/api/v5/dex/aggregator/quote"
        params = {
            "chainId": chain_id,
            "fromTokenAddress": from_token_address,
            "toTokenAddress": to_token_address,
            "amount": amount_in,
            "dexIds": dex_ids,
            "priceImpactProtectionPercentage": price_impact_protection_percentage,
            "feePercent": fee_percent
        }
        return await self.client.request("GET", endpoint, params=params)
    
    async def swap(self,):
        # https://www.okx.com/web3/build/docs/waas/dex-swap
        raise NotImplemented()
    
    # TODO: Implement error codes: https://www.okx.com/web3/build/docs/waas/dex-error-code