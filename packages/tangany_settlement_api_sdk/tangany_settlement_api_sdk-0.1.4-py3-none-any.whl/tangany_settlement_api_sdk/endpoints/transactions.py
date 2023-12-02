import json, requests
from typing import List

from attr import define
from .response_handler import return_or_raise
from ..auth import Authenticator

@define
class TransactionPostEntry:
    _id: str
    _from_account_id: str
    _to_account_id: str
    _value: str
    _value_date: str
    _asset_id: str
    _fiat_currency: str
    _fiat_value: str
    _reference: str
    _trade_info_fill_date: str
    _trade_info_market_maker_tx_id: str
    
    def __init__(self, id: str, from_account_id: str, to_account_id: str, value: str, value_date: str, asset_id: str, 
                 fiat_currency: str, fiat_value: str, reference: str = None, trade_info_fill_date: str = None, trade_info_market_maker_tx_id: str = None):
        self._id = id
        self._from_account_id = from_account_id
        self._to_account_id = to_account_id
        self._value = value
        self._value_date = value_date
        self._asset_id = asset_id
        self._fiat_currency = fiat_currency
        self._fiat_value = fiat_value
        self._reference = reference
        self._trade_info_fill_date = trade_info_fill_date
        self._trade_info_market_maker_tx_id = trade_info_market_maker_tx_id       

    def to_json_body(self) -> str:        
        payload = {}
        payload['id'] = self._id
        payload['fromAccountId'] = self._from_account_id
        payload['toAccountId'] = self._to_account_id
        payload['value'] = self._value
        payload['valueDate'] = self._value_date
        payload['assetId'] = self._asset_id
        payload['fiatCurrency'] = self._fiat_currency
        payload['fiatValue'] = self._fiat_value
        
        if self._reference is not None:
            payload['reference'] = self._reference

        if self._trade_info_fill_date is not None or self._trade_info_market_maker_tx_id is not None:
            tradeInfo = {}
            if self._trade_info_fill_date is not None:
                tradeInfo['fillDate'] = self._trade_info_fill_date                
            if self._trade_info_market_maker_tx_id is not None:
                tradeInfo['marketMakerTxId'] = self._trade_info_market_maker_tx_id
            payload['tradeInfo'] = tradeInfo

        return payload

@define
class Transactions:
    _authenticator: Authenticator
    _base_url: str

    def __init__(self, authenticator: Authenticator):
        self._authenticator = authenticator
        self._base_url = f"{authenticator.credentials.base_url}/ledgers"

    def list(self, ledger_id: str, next_page_token: str = None, limit: str = "100", status: str = None, reference: str = None,  involving_account_id: str = None,
             value_date_before: str = None, value_date_after: str = None, 
             booking_date_before: str = None, booking_date_after: str = None) -> str:
        url = f"{self._base_url}/{ledger_id}/transactions"
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

        if involving_account_id is not None:
            params['involvingAccountId'] = involving_account_id  

        if reference is not None:
            params['reference'] = reference  

        if status is not None:
            params['status'] = status  

        response = requests.get(url=url, headers=self._authenticator.get_base_header(), params=params)
        responseJson = return_or_raise(response)
        return responseJson        

    def get(self, ledger_id: str, transaction_id: str) -> str: 
        url = f"{self._base_url}/{ledger_id}/transactions/{transaction_id}"
        response = requests.get(url=url, headers=self._authenticator.get_base_header())
        return return_or_raise(response)    
    
    def create(self, ledger_id: str, transaction_id: str, from_account_id: str, to_account_id: str, value: str, value_date: str, asset_id: str, fiat_currency: str, fiat_value: str, 
               reference: str = None, trade_info_fill_date: str = None, trade_info_market_maker_tx_id: str = None) -> str: 
        url = f"{self._base_url}/{ledger_id}/transactions"
        transaction = TransactionPostEntry(id=transaction_id, from_account_id=from_account_id, to_account_id=to_account_id, value=value, value_date=value_date, asset_id=asset_id, fiat_currency=fiat_currency, 
                                       fiat_value=fiat_value, reference=reference, trade_info_fill_date=trade_info_fill_date, trade_info_market_maker_tx_id=trade_info_market_maker_tx_id)
        
        response = requests.post(url=url, json=[transaction.to_json_body()], headers=self._authenticator.get_base_header())
        return return_or_raise(response)

    def create_batch(self, ledger_id: str, transactions: List[TransactionPostEntry]) -> str: 
        url = f"{self._base_url}/{ledger_id}/transactions"
        
        payload = []        
        for transaction in transactions:
            payload.append(transaction.to_json_body())        
        
        response = requests.post(url=url, json=payload, headers=self._authenticator.get_base_header())
        return return_or_raise(response)
    
    def delete(self, ledger_id: str, transaction_id: str) -> str: 
        url = f"{self._base_url}/{ledger_id}/transactions/{transaction_id}"
        response = requests.delete(url=url, headers=self._authenticator.get_base_header())
        return return_or_raise(response)