from fastapi import FastAPI, Query, HTTPException
from typing import Optional
import pandas as pd

DATA_FILE = "LE.txt"
PAGE_SIZE = 50

df = None

async def lifespan(app: FastAPI):
    global df
    df = pd.read_csv(DATA_FILE, sep="\t", encoding="utf-8")
    df["name"] = df["name"].astype(str)
    df["sn"] = df["sn"].astype(str)
    
    yield

app = FastAPI(lifespan=lifespan)

def filter_data(name: Optional[str], sn: Optional[str], search: Optional[str], sort: Optional[str]):
    global df
    filtered = df

    if search:
        filtered = filtered[
            filtered["name"].str.contains(search, case=False, na=False) |
            filtered["sn"].str.contains(search, case=False, na=False)
        ]
    else:
        if name:
            filtered = filtered[filtered["name"].str.contains(name, case=False, na=False)]
        if sn:
            filtered = filtered[filtered["sn"].str.contains(sn, case=False, na=False)]

    if sort:
        ascending = True
        sort_col = sort
        if sort.startswith("-"):
            ascending = False
            sort_col = sort[1:]
        if sort_col not in filtered.columns:
            raise HTTPException(status_code=400, detail=f"Invalid sort column: {sort_col}")
        filtered = filtered.sort_values(by=sort_col, ascending=ascending)

    return filtered

@app.get("/spare-parts")
def spare_parts(
    name: Optional[str] = Query(None),
    sn: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
):
    filtered = filter_data(name, sn, search, sort)

    total = len(filtered)
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE

    data_page = filtered.iloc[start:end]
    results = data_page.to_dict(orient="records")

    return {
        "total": total,
        "page": page,
        "page_size": PAGE_SIZE,
        "results": results,
    }
