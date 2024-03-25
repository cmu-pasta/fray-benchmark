import argparse
import os
from models import OpenAIModel, GeminiModel, VertexModel, AnthropicModel
from prompts import SYSTEM_PROMPT_TEMPLATE, TRANSPILE_PROMPT_TEMPLATE
from parsers import JavaOutputParser

def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)

def main():
    if "OPENAI_API_KEY" not in os.environ:
        print("Environment variable OPENAI_API_KEY not set.")
        return

    parser = argparse.ArgumentParser(description="Generate samples using OpenAI API.")
    parser.add_argument("--model_name", type=str, required=True, help="Model to be used for generation.")
    parser.add_argument("--program_path", type=str, required=True, help="Path to the input program.")
    parser.add_argument("--output_dir", type=str, required=True, help="Path to the output dir.")
    parser.add_argument("--samples", type=int, default=1, help="Number of samples.")
    args = parser.parse_args()

    file_name = os.path.basename(args.program_path)
    class_name = snake_to_camel(file_name)[:-2]
    output_path = os.path.join(args.output_dir, f"{class_name}.java")
    if os.path.exists(output_path):
      return
    try:
        with open(args.program_path, 'r') as f:
            program = f.read()
    except Exception as e:
        print(f"Failed to read program: {e}")
        return

    system_prompt = SYSTEM_PROMPT_TEMPLATE
    generate_prompt = TRANSPILE_PROMPT_TEMPLATE.format(file_name=file_name, class_name=class_name, program=program)
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    with open(os.path.join(args.output_dir, "prompt.txt"), 'w') as f:
        f.write(system_prompt + "\n" + generate_prompt)
    if "gpt" in args.model_name:
        ai_model = OpenAIModel(system_prompt, args.model_name)
    elif "gemini" in args.model_name:
        ai_model = VertexModel(system_prompt, args.model_name)
    else:
        ai_model = AnthropicModel(system_prompt, args.model_name)

    samples = ai_model.sample(generate_prompt, n=args.samples)
    parser = JavaOutputParser()

    for i in range(len(samples)):
        sample = samples[i]
        output_path = os.path.join(args.output_dir, f"{class_name}.java")
        with open(output_path, "w") as f:
            f.write(parser.parse(sample))

if __name__ == "__main__":
    main()
