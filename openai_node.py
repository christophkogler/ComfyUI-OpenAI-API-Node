import requests
import json

class OpenAINode:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_name": ("STRING", {
                    "multiline": False,
                    "default": "BadPanda"
                }),
                "system_header": ("STRING", {
                    "multiline": True,
                    "default": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
                }),
                "system_prompt": ("STRING", {
                    "multiline": True,
                    "default": "You are a prompt generation AI. Your task is to take a user input for a stable diffusion prompt and expand the supplied prompt in a stable diffusion format (comma seperated tags) to provide high quality images. Do not output anything other than a stable diffusion prompt."
                }),
                "user_header": ("STRING", {
                    "multiline": True,
                    "default": "<|start_header_id|>user<|end_header_id|>\n\n"
                }),
                "user_prompt": ("STRING", {
                    "multiline": True,
                    "default": "A world without prompts"
                }),
                "response_header": ("STRING", {
                    "multiline": True,
                    "default": "<|start_header_id|>assistant<|end_header_id|>\n\n"
                }),
                "end_turn_token": ("STRING", {
                    "multiline": False,
                    "default": "<|eot_id|>"
                }),
                "api_url": ("STRING", {
                    "multiline": False,
                    "default": "http://127.0.0.1:5000/v1"
                }),
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": "BadPanda"
                }),
                "temperature": ("FLOAT", {
                    "default": .1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.01,
                    "display": "number"
                }),
                "max_tokens": ("INT", {
                        "default": 250,
                        "min": -1, 
                        "max": 2048,
                        "display": "number"
                }),
                "seed": ("INT", {
                        "default": 0,
                        "min": 0, 
                        "max": 0xffffffffffffffff
                })
            }
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "get_completion"

    CATEGORY = "OpenAIapi"

    def get_completion(self, system_header, system_prompt, user_header, user_prompt, response_header, api_url, api_key, temperature, end_turn_token, max_tokens, seed, model_name):
        # compose prompt.
        full_system_prompt = system_header + system_prompt + end_turn_token
        full_user_prompt = user_header + user_prompt + end_turn_token
        final_prompt = full_system_prompt + full_user_prompt + response_header

        # If forgot to change API key OR removed it, assume no authorization required.
        if api_key == "BadPanda" or api_key == "" or api_key == None:
            headers = { "Content-Type": "application/json" }
        else: # If they added an API key, try to send it as authorization.
            headers = { 
                "Content-Type": "application/json",
                "authorization": api_key
            }

        load_args = json.dumps({
            "model_name": model_name,
            "args": {
                "n_ctx":2000
            },
            "settings": {}
        })

        generation_data = json.dumps({
            "model":model_name,
            "prompt":final_prompt,
            "temperature":temperature,
            "max_tokens":max_tokens,
            "stop":end_turn_token,
        })

        # attempt to run VRAM-light: load the LLM, perform inference, and then unload the model.
        # want to be able to run it at the start of a workflow without screwing up vram limits afterwards.
        try:
            response = requests.post(api_url + "/internal/model/load", headers = headers, data = load_args)
            response.raise_for_status()
        except Exception as e:
            print(f"Error: {str(e)}")
            return ("Sad Panda",)

        try:
            response = requests.post(api_url+"/completions", data = generation_data, headers = headers) 	
            response.raise_for_status()
            response = response.json()
            response = response["choices"][0]["text"]
        except Exception as e:
            print(f"Error: {str(e)}")
            return ("Sad Panda",)

        try:
            response = requests.post(api_url + "/internal/model/unload", headers = headers, data = {})
            response.raise_for_status()
        except Exception as e:
            print(f"Error: {str(e)}")
            return ("Sad Panda",)

        print(response)
        return response


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "OpenAINode": OpenAINode
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenAINode": "OpenAI API Node"
}
