```
                                ██████╗ ██╗     ██╗███╗   ██╗███╗   ██╗
                                ██╔══██╗██║     ██║████╗  ██║████╗  ██║
                                ██████╔╝██║     ██║██╔██╗ ██║██╔██╗ ██║
                                ██╔══██╗██║     ██║██║╚██╗██║██║╚██╗██║
                                ██████╔╝███████╗██║██║ ╚████║██║ ╚████║
                                ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝
```

# Blinn API for AI assisted Fragment Shaders

Welcome to the Blinn API project! This API is designed to communicate with the Anthropic Claude API to provide modifications for fragment shaders. It's part of an experiment of a tool to play around with three.js and GLSL shaders.

This API is intended to be used with a web app, which can be accessed at the following link: [Blinn](https://github.com/LessThan12Parsecs/blinn).

## Features

- **Fragment Shader Modification**: Send your current fragment shader and get back a modified version based on your instructions.
- **Anthropic Claude Integration**: Utilizes the powerful Claude model from Anthropic for generating shader code changes.
- **Easy to Use**: Simple API endpoints make it straightforward to send your shaders and receive modifications.

## Getting Started

To use the Blinn API, you'll need to set up a few things first:

1. **Clone the Repository**: Get the code on your local machine.
2. **Environment Variables**: Ensure you have a `.env` file with your `ANTHROPIC_API_KEY` set up. Refer to the provided `.env` example.
3. **Install Dependencies**: Run `pip install -r requirements.txt` to install the necessary Python packages.
4. **Run the API**: Use `uvicorn main:app --reload` to start the FastAPI server.

## Usage

To modify a fragment shader, make a POST request to `/fragment-shader-change/` with the following JSON body:

```json
{
  "fragment_shader": "base64_encoded_shader",
  "instruction": "make the colors more vibrant"
}
```
## License

This project is licensed under the MIT License - see  [LICENSE.md](LICENSE.md) file for details.

## Author

- **Emanuel Ramirez** - *Initial author* - [LessThan12Parsecs](https://github.com/LessThan12Parsecs)
