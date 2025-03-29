from typing import Dict, Any, List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import Tron

from .schemas import AddressRequestResponse
from .models import WalletInfo
from tronpy.exceptions import BadAddress
import logging

client = Tron()

DEFAULT_INFO = {
    'bandwidth': 0,
    'energy': 0,
    'balance': 0,
}


async def get_wallet_info(address: str) -> Dict[str, Any]:
    try:
        account = await client.get_account(address)
    except BadAddress:
        logging.exception(f'BadAddress {address}')
        account = DEFAULT_INFO
    except Exception:
        logging.exception(f'Exception for {address}')
        account = DEFAULT_INFO

    account["address"] = address
    return {
        "address": account['address'],
        "bandwidth": account['bandwidth'],
        "energy": account['energy'],
        "trx_balance": account['balance'],
    }


async def save_wallet_info(db: AsyncSession, address: str, info: Dict[str, Any]) -> AddressRequestResponse:
    wallet_info = WalletInfo(
        address=address,
        bandwidth=info['bandwidth'],
        energy=info['energy'],
        trx_balance=info['trx_balance']
    )
    db.add(wallet_info)
    await db.commit()
    await db.refresh(wallet_info)

    return AddressRequestResponse(
        id=wallet_info.id,
        address=wallet_info.address,
        bandwidth=wallet_info.bandwidth,
        energy=wallet_info.energy,
        trx_balance=wallet_info.trx_balance,
        time_created=wallet_info.time_created
    )


async def get_recent_wallets(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[AddressRequestResponse]:
    query = select(WalletInfo).offset(skip).limit(limit)
    result = await db.execute(query)
    wallets = result.scalars().all()

    return [
        AddressRequestResponse(
            id=wallet.id,
            address=wallet.address,
            bandwidth=wallet.bandwidth,
            energy=wallet.energy,
            trx_balance=wallet.trx_balance,
            time_created=wallet.time_created
        ) for wallet in wallets
    ]
