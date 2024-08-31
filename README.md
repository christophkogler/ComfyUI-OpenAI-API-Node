# OpenAI API Node

## Description

A single simple node that provides LLM integration into ComfyUI workflows by calling an OpenAI API based server through a node. The server loads the requested LLM on demand and unloads it after use, freeing up any used VRAM. 

This repository is based on [ComfyUI-OpenAINode](https://github.com/Electrofried/ComfyUI-OpenAINode), rewritten to suit my preferences. Improvements include fine-grain prompt format control, and VRAM freeing after LLM inference is complete.

### Dependencies

requests  -  for post-ing to the API.

### Installation
Use [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager): Manager > Custom Nodes Manager > Install via Git URL. You may have to [drop your security_level to normal-](https://github.com/ltdrdata/ComfyUI-Manager?tab=readme-ov-file#security-policy) to install it.  
OR  
In your ComfyUI custom_nodes folder,  
```
git clone https://github.com/christophkogler/ComfyUI-OpenAINode
```
and then  
```
pip install requests
```

### Getting started
* Load your launcher of choice which has an OpenAI API (Ooba, LLM studio and many more support this).
* Insert the node into your workflow.
* Enter your chosen model's name as well as the system, user, and response headers, and the end turn token(s). The defaults are set up for the Llama 3.1 format.
* Alter the system and user prompts as you wish.
* The default api_url is set up for local hosting, `http://127.0.0.1:5000/v1`.
* If you are attempting to use a non-local server, you will almost certainly need to enter your API key, and the model loading/unloading may not work.
* Convert your CLIP encoder's text widget to an input by right clicking on the node.
* Feed the OpenAI API node output into the CLIP encoder.
* Enter your prompt.
* Start a run!

### Help

The seed input is there to allow a random seed to be input. It does not actually do anything to the image or text seed. Randomizing it each run will cause ComfyUI to re-prompt the LLM each time - for if you want to vary your prompt a bit. If you leave it fixed, then ComfyUI will cache the results and use the same prompt each time it runs, until you change the input.

If attempting to run both the ComfyUI image generation and the LLM locally: Executing this node at the start of the workflow should work well. However, ComfyUI caches loaded models until the end of the workflow, so if you try to naively execute this node in the middle of your workflow, you are likely to push the LLM into RAM and get very slow inference times or outright failure to load. A VRAM clearing node of some kind, like the 'VRAM debug' node in [KJNodes for ComfyUI](https://github.com/kijai/ComfyUI-KJNodes) can help resolve this. 

I will not provide help with running out of GPU memory (unless it is because THIS node isn't unloading models - then I might help).
