from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import anthropic
from dotenv import load_dotenv
import os
import base64

from pydantic import BaseModel

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")  # You need to create a .env file with your key.
client = anthropic.Anthropic(
    api_key=api_key,
)

app = FastAPI()

# Add CORS middleware to allow everything # TODO: Change this.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


class ShaderData(BaseModel):
    fragment_shader: str
    instruction: str

@app.post("/fragment-shader-change/")
async def describe_image(shader_data: ShaderData):
    instruction = shader_data.instruction
    current_frag_shader_encoded = shader_data.fragment_shader
    current_frag_shader = base64.b64decode(current_frag_shader_encoded).decode('utf-8')
    message_response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4096,
        system="Respond only with GLSL with no introduction or explanation and in plain text",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Given the following fragment shader for three.js GLSL, {current_frag_shader}, "
                                f"can you {instruction}. "
                                f"use u_time uniform and vUv for varying, "
                                f"remember to include all necessary functions and "  
                                f"Respond only with the shader code and nothing else, and don't include the uniforms "
                                f"at the beginning of the code ."
                    }
                ],
            }
        ],
    )
    result_encoded = base64.b64encode(message_response.content[0].text.encode('utf-8')).decode('utf-8')
    return {"result": result_encoded}
