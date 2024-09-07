# pip install -U FlagEmbedding

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from FlagEmbedding import BGEM3FlagModel

app = FastAPI()
model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True, device="cuda")

class TextInput(BaseModel):
    inputs: List[str]
    max_length: int

@app.post("/encode")
async def encode(input_data: TextInput):
    texts = input_data.inputs
    max = input_data.max_length
    
    if not texts:
        raise HTTPException(status_code=400, detail="No texts provided")
    if not max:
        max = 8192

    output = model.encode(texts, max_length=max, return_dense=False, return_sparse=True)
    sparse_weight_id = output['lexical_weights']
    # Sparse vector embedding of text
    sparse_indices = [[int(token_id) for token_id in text] for text in sparse_weight_id]
    sparse_values = [[float(text[token_id]) for token_id in text] for text in sparse_weight_id]
    for i in range(len(sparse_weight_id)):
        sparse_values[i] = [x for _, x in sorted(zip(sparse_indices[i], sparse_values[i]))]
        sparse_indices[i] = sorted(sparse_indices[i])

    return {
        "indices": sparse_indices[0],
        "values": sparse_values[0]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
