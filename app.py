from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

CHATBOT_API_URL = "https://stablediffusion.fr/gpt4/predict2"


@app.get("/")
async def chatbot(savol: str = None):
    if not savol:
        raise HTTPException(
            status_code=400,
            detail={"error": True, "message": "Missing 'savol' parameter"},
        )

    payload = {
        "prompt": f"Sen o'zbek tilida javob beradigan yordamchi bo'lasan.\nFoydalanuvchi: {savol}"
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Powered-by-@bizft-Telegram-Channel",
        "Referer": "https://stablediffusion.fr/",
        "Origin": "https://stablediffusion.fr",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(CHATBOT_API_URL, json=payload, headers=headers)

        data = response.json()

        # API dan kelgan javobni toza olish
        if isinstance(data, dict) and "message" in data:
            javob = data["message"]
        else:
            javob = str(data)

        result = {
            "Savol": savol,
            "Javob": javob,
            "Dasturchi": "@x3747"
        }

        return JSONResponse(
            content=result,
            status_code=200,
            headers={"Access-Control-Allow-Origin": "*"},
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": True, "message": "Internal Error", "details": str(e)},
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
