from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import anthropic
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

from pydantic import BaseModel

load_dotenv()

anthropic_client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_KEY")
)

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_KEY")
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
    ai_model: str


@app.post("/fragment-shader-change/")
async def describe_image(shader_data: ShaderData):
    instruction = shader_data.instruction
    ai_model = shader_data.ai_model
    current_frag_shader_encoded = shader_data.fragment_shader
    current_frag_shader = base64.b64decode(current_frag_shader_encoded).decode('utf-8')
    
    if ai_model == "claude-opus":
        message_response = anthropic_client.messages.create(
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
                                    f"don't include the uniforms "
                                    f"at the beginning of the code ."
                        }
                    ],
                }
            ],
        )
        result_text = message_response.content[0].text

    elif ai_model == "gpt4":
        prompt = f"Given the following fragment shader for three.js GLSL, {current_frag_shader}, " \
                 f"can you {instruction}. " \
                 f"use u_time uniform and vUv for varying, " \
                 f"remember to include all necessary functions and " \
                 f"don't include the uniforms at the beginning of the code ."
        message_response = (openai_client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "Respond only with GLSL with no "
                                              "introduction or explanation."
                                              " Response in plain text with no triple quotes"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        ))
        result_text = message_response.choices[0].message.content
    else:
        return {"error": "Invalid AI model specified. options are 'claude-opus' and 'gpt4'"}
    
    result_encoded = base64.b64encode(result_text.encode('utf-8')).decode('utf-8')
    return {"result": result_encoded}

