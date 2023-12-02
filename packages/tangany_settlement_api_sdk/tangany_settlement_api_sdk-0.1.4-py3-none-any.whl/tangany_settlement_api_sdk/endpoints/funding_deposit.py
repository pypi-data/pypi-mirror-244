from typing import List
import requests, json

from attr import define
from .response_handler import return_or_raise
from ..auth import Authenticator

@define
class FundingDepositsPostEntry:
    _id: str
    _to_account_id: str
    _value: str
    _value_date: str
    _asset_id: str
    _fiat_currency: str
    _fiat_value: str
    _reference: str
    _tx_hash: str
    
    def __init__(self, id: str, to_account_id: str, value: str, asset_id: str, fiat_currency: str, fiat_value: str, tx_hash: str, reference: str = None, value_date: str = None):
        self._id = id
        self._to_account_id = to_account_id
        self._value = value
        self._asset_id = asset_id
        self._fiat_currency = fiat_currency
        self._fiat_value = fiat_value
        self._tx_hash = tx_hash
        self._reference = reference
        self._value_date = value_date   

    def to_json_body(self) -> str:        
        payload = {}
        payload['id'] = self._id
        payload['toAccountId'] = self._to_account_id
        payload['value'] = self._value
        payload['assetId'] = self._asset_id
        payload['fiatCurrency'] = self._fiat_currency
        payload['fiatValue'] = self._fiat_value
        payload['txHash'] = self._tx_hash   

        if self._value_date is not None:
            payload['valueDate'] = self._value_date

        if self._reference is not None:
            payload['reference'] = self._reference

        return payload
    
@define
class FundingDeposits:
    _authenticator: Authenticator
    _base_url: str

    def __init__(self, authenticator: Authenticator):
        self._authenticator = authenticator  
        self._base_url = f"{authenticator.credentials.base_url}/ledgers"

    def list(self, ledger_id: str, next_page_token: str = None, limit: str = "100", status: str = None, reference: str = None,
             value_date_before: str = None, value_date_after: str = None, 
             booking_date_before: str = None, booking_date_after: str = None) -> str:
        url = f"{self._base_url}/{ledger_id}/funding/deposits"
        params = {}
        params['limit'] = limit

        if next_page_token is not None:
            params['pageToken'] = next_page_token

        if value_date_before is not None:
            params['valueDateBefore'] = value_date_before   

        if value_date_after is not None:
            params['valueDateAfter'] = value_date_after 

        if booking_date_before is not None:
            params['bookingDateBefore'] = booking_date_before 

        if booking_date_after is not None:
            params['bookingDateAfter'] = booking_date_after   

        if reference is not None:
            params['reference'] = reference  

        if status is not None:
            params['status'] = status              

        response = requests.get(url=url, headers=self._authenticator.get_base_header(), params=params)
        responseJson = return_or_raise(response)
        return responseJson         
    
    def create(self, ledger_id: str, transaction_id: str, to_account_id: str, value: str, asset_id: str, fiat_currency: str, fiat_value: str,  tx_hash: str,
               value_date: str = None, reference: str = None) -> str: 
        url = f"{self._base_url}/{ledger_id}/funding/deposits"
        deposit = FundingDepositsPostEntry(id=transaction_id, to_account_id=to_account_id, value=value, asset_id=asset_id, fiat_currency=fiat_currency, fiat_value=fiat_value, 
                                           txHash= tx_hash, reference=reference,value_date=value_date)        
        
        response = requests.post(url=url, json=[deposit.to_json_body()], headers=self._authenticator.get_base_header())
        return return_or_raise(response)    
    
    def create_batch(self, ledger_id: str, transactions: List[FundingDepositsPostEntry]) -> str: 
        url = f"{self._base_url}/{ledger_id}/funding/deposits"
        
        payload = []        
        for transaction in transactions:
            payload.append(transaction.to_json_body())        
        
        response = requests.post(url=url, json=payload, headers=self._authenticator.get_base_header())
        return return_or_raise(response)