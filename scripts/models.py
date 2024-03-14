from openai import OpenAI
import os
import google.generativeai as genai
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
import tqdm
import anthropic


MAX_TOKENS = 4096

class Model:

  def __init__(self, system_prompt, model_name):
    pass

  def sample(self, input_prompt, n):
    pass

  def fix(self, messages, fix_prompt):
    pass

class OpenAIModel(Model):
  def __init__(self, system_prompt, model_name):
    self.client = OpenAI()
    self.system_prompt = system_prompt
    self.model_name = model_name

  def sample(self, input_prompt, n=1):
    samples = []
    response = self.client.chat.completions.create(
      model=self.model_name,
      messages=[
        {
          "role": "system",
          "content": self.system_prompt
        },
        {
          "role": "user",
          "content": input_prompt
        }
      ],
      max_tokens=MAX_TOKENS,
      n=n
    )
    samples = [r.message.content for r in response.choices]
    return samples

  def fix(self, messages, fix_prompt):
    response = self.client.chat.completions.create(
      model=self.model_name,
      messages=messages +
        [{
          "role": "user",
          "content": fix_prompt
        }],
      max_tokens=MAX_TOKENS,
      n=1
    )
    output = response.message.content
    return self.output_parser.parse(output)

class GeminiModel(Model):
  def __init__(self, system_prompt, model_name):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    # Set up the model
    generation_config = {
      "temperature": 0.9,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": MAX_TOKENS,
    }
    self.system_prompt = system_prompt
    self.model = genai.GenerativeModel(model_name=model_name,
                          generation_config=generation_config)

  def sample(self, input_prompt, n=1):
    message = self.system_prompt + "\n" + input_prompt
    samples = []
    for i in range(n):
      response = self.model.generate_content(message)
      samples.append(response.text)
    return samples

class VertexModel(Model):
  def __init__(self, system_prompt, model_name):
    vertexai.init(project="gemini-415719", location="us-central1")
    self.model = GenerativeModel(model_name)
    self.system_prompt = system_prompt

  def sample(self, input_prompt, n=1):
    message = self.system_prompt + "\n" + input_prompt
    samples = []
    for i in range(n):
      response = self.model.generate_content(message)
      print(response.text)
      samples.append(response.text)
    return samples

class AnthropicModel(Model):
  def __init__(self, system_prompt, model_name):
    self.client = anthropic.Anthropic()
    self.system_prompt = system_prompt
    self.model_name = model_name

  def sample(self, input_prompt, n=1):
    samples = []
    for i in range(n):
      response = self.client.messages.create(
        model=self.model_name,
        max_tokens=MAX_TOKENS,
        system=self.system_prompt,
        messages=[
            {"role": "user", "content": input_prompt}
        ]
      ) 
      samples.append(response.content[0].text)
    return samples
