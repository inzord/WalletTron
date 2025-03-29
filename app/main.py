import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from .database import get_session, init_db
from .schemas import AddressRequestResponse, AddressRequestCreate, AddressRequestList
from .services import get_wallet_info, save_wallet_info, get_recent_wallets

logging.basicConfig(filename='tron_app.log', level=logging.INFO)
logging.info('start app')

app = FastAPI()


@app.post("/wallets-create/", response_model=AddressRequestResponse)
async def create_wallet(request: AddressRequestCreate, db: AsyncSession = Depends(get_session)):
    try:
        wallet_info = await get_wallet_info(request.address)
        saved_wallet_info = await save_wallet_info(db, request.address, wallet_info)
        return saved_wallet_info
    except Exception as e:
        logging.exception(f"Error creating wallet for address {request.address}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/wallets-info/", response_model=AddressRequestList)
async def read_wallets(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    try:
        wallets = await get_recent_wallets(db, skip=skip, limit=limit)
        total = len(wallets)
        return AddressRequestList(total=total, items=wallets)
    except Exception as e:
        logging.exception(f"Error retrieving wallets: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.on_event("startup")
async def startup_event():
    await init_db()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
