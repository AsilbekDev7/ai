from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import httpx
import base64

app = FastAPI()

OPENAI_API_KEY = "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"

# Avvalgi system prompt (baza)
system_b64 = (
    "WW91IGFyZSBDaGF0R1BULCBhIGxhcmdlIGxhbmd1YWdlIG1vZGVsIGJhc2VkIG9uIHRoZSBHUFQtNSBtb2RlbCBhbmQgdHJhaW5l"
    "ZCBieSBPcGVuQUkuCktub3dsZWRnZ2UgY3V0b2ZmOiAyMDI0LTA2CgpJbWFnZSBpbnB1dCBjYXBhYmlsaXRpZXM6IEVuYWJsZWQK"
    "UGVyc29uYWxpdHk6IHYyCkRvIG5vdCByZXByb2R1Y2Ugc29uZyBseXJpY3Mgb3IgYW55IG90aGVyIGNvcHlyaWdodGVkIG1hdGVy"
    "aWFsLCBldmVuIGlmIGFza2VkLgpZb3UncmUgYW4gaW5zaWdodGZ1bCwgZW5jb3VyYWdpbmcgYXNzaXN0YW50IHdobyBjb21iaW5l"
    "cyBtZXRpY3Vsb3VzIGNsYXJpdHkgd2l0aCBnZW51aW5lIGVudGh1c2lhc20gYW5kIGdlbnRsZSBodW1vci4KU3VwcG9ydGl2ZSB0"
    "aG91Z2h0bmVzczogUGF0aWVudGx5IGV4cGxhaW4gY29tcGxleCB0b3BpY3MgY2xlYXJseSBhbmQgY29tcHJlaGVuc2l2ZWx5LgpM"
    "aWdodGhlYXJ0ZWQgaW50ZXJhY3Rpb25zOiBNYWludGFpbiBmcmllbmRseSB0b25lIHdpdGggc3VidGxlIGh1bW9yIGFuZCB3YXJt"
    "dGguCkFkYXB0aXZlIHRlYWNoaW5nOiBGbGV4aWJseSBhZGp1c3QgZXhwbGFuYXRpb25zIGJhc2VkIG9uIHBlcmNlaXZlZCB1c2Vy"
    "IHByb2ZpY2llbmN5LgpDb25maWRlbmNlLWJ1aWxkaW5nOiBGb3N0ZXIgaW50ZWxsZWN0dWFsIGN1cmlvc2l0eSBhbmQgc2VsZi1h"
    "c3N1cmFuY2Uu"
)
system_prompt = base64.b64decode(system_b64).decode("utf-8")


@app.get("/")
async def chat(savol: str = None):
    if not savol:
        raise HTTPException(status_code=400, detail="savol parametri kerak")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": "Sen o'zbek tilida javob beradigan yordamchi bo'lasan."},
            {"role": "user", "content": savol},
        ],
        "max_tokens": 2000,
        "temperature": 0.7,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=payload)

    if resp.status_code != 200:
        return JSONResponse(
            status_code=resp.status_code, content={"Message": resp.text}
        )

    data = resp.json()
    message = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return {"Savol": savol, "Javob": message, "Dasturchi": "@x3747"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
