import json
from dataclasses import dataclass
from payos_lib_python.constants import ERROR_MESSAGE
from typing import List

class ItemData:
    def __init__(self, name: str, quantity: int, price: int):
        if not isinstance(name, str):
            raise ValueError(f"{ERROR_MESSAGE['INVALID_PARAMETER']} name item must be a str")
        if not isinstance(quantity, int):
            raise ValueError(f"{ERROR_MESSAGE['INVALID_PARAMETER']} quantity item must be a int")
        if not isinstance(price, int):
            raise ValueError(f"{ERROR_MESSAGE['INVALID_PARAMETER']} price item must be a int")
        self.name = name
        self.quantity = quantity
        self.price = price
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


    
class PaymentData:
    def __init__(self, orderCode: int, amount: int, description: str, cancelUrl: str, returnUrl: str, buyerName: str = None, items: List[ItemData] = None,\
                  buyerEmail: str = None, buyerPhone: str = None, buyerAddress: str = None, expiredAt: int= None, signature: str = None):
        if not isinstance(orderCode, int):
            raise ValueError(f"{ERROR_MESSAGE['INVALID_PARAMETER']} orderCode must be a int")
        if not isinstance(amount, int):
            raise ValueError(f"{ERROR_MESSAGE['INVALID_PARAMETER']} amount must be a int")
        if not isinstance(description, str):
            raise ValueError(f"{ERROR_MESSAGE['INVALID_PARAMETER']} description must be a str")
        if items is not None:
            if not isinstance(items, list):
                raise ValueError(f"{ERROR_MESSAGE['INVALID_PARAMETER']} items must be a list")
            for x in items:
                if not isinstance(x, ItemData):
                    raise ValueError(f"{ERROR_MESSAGE['INVALID_PARAMETER']} item must be a ItemData")
        if not isinstance(description, str):
            raise ValueError(f"{ERROR_MESSAGE['INVALID_PARAMETER']} description must be a str")
        if not isinstance(cancelUrl, str):
            raise ValueError(f"{ERROR_MESSAGE['INVALID_PARAMETER']} cancelUrl must be a str")
        if not isinstance(returnUrl, str):
            raise ValueError(f"{ERROR_MESSAGE['INVALID_PARAMETER']} returnUrl must be a str")
        #required
        self.orderCode = orderCode
        self.amount = amount
        self.description = description
        self.items = items
        self.cancelUrl = cancelUrl
        self.returnUrl = returnUrl
        self.signature = signature
        #notrequired
        self.buyerName = buyerName
        self.buyerEmail = buyerEmail
        self.buyerPhone = buyerPhone
        self.buyerAddress = buyerAddress
        self.expiredAt = expiredAt

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
    

@dataclass
class CreatePaymentResult:
    bin: str
    accountNumber: str
    accountName: str
    amount: int
    description: str
    orderCode: int
    paymentLinkId: str
    status: str
    checkoutUrl: str
    qrCode: str
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

@dataclass
class Transaction:
    reference: str
    amount: int
    accountNumber: str
    description: str
    transactionDateTime: str
    virtualAccountName: str or None
    virtualAccountNumber: str or None
    counterAccountBankId: str or None
    counterAccountBankName: str or None
    counterAccountName: str or None
    counterAccountNumber: str or None
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

@dataclass
class PaymentInformation:
    id: str
    orderCode: int
    amount: int
    amountPaid: int
    amountRemaining: int
    status: str
    createdAt: str
    transactions: List[Transaction]
    cancellationReason: str or None
    canceledAt: str or None
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

@dataclass
class WebhookData:
    orderCode: int
    amount: int
    description: str
    accountNumber: str
    reference: str
    transactionDateTime: str
    paymentLinkId: str
    code: str
    desc: str
    counterAccountBankId: str or None
    counterAccountBankName: str or None
    counterAccountName: str or None
    counterAccountNumber: str or None
    virtualAccountName: str or None
    virtualAccountNumber: str or None
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)