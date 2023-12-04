import argparse
import configparser

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


def post_query(model, tokenizer, config):
    config_queries = config["queries"]
    string_list_str = config_queries.get('texts')
    string_list = string_list_str.split(', ')
    # https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
    top_k = config_queries.get("top_k", fallback=50)
    repetition_penalty = config_queries.get("repetition_penalty", fallback=1.0)
    temperature = config_queries.get("repetition_penalty", fallback=1.0)
    max_length = config_queries.get("max_length", fallback=50)

    prompt = pipeline(task="text-generation",
                      model=model,
                      tokenizer=tokenizer,
                      temperature=temperature,
                      repetition_penalty=repetition_penalty,
                      top_k=top_k,
                      max_length=max_length)

    for query in string_list:
        print("Post Query:" + query + "\n")
        print(prompt(query)[0]['generated_text'])


def main():
    parser = argparse.ArgumentParser(description='Training facilitator')
    parser.add_argument('--config', metavar='config', required=True,
                        help='the path to the ini file used for query')
    args = parser.parse_args()

    training_file = args.config
    print("Using training file:" + training_file + " and starting from phase:" + args.phase)

    config = configparser.ConfigParser()
    config.read(training_file)

    training = config["training"]
    newmodel_finalname = training["finalname"]

    print("Loading model:"+newmodel_finalname+"\n")
    model = AutoModelForCausalLM.from_pretrained(newmodel_finalname, trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(newmodel_finalname, trust_remote_code=True)
    post_query(model, tokenizer, config)


if __name__ == '__main__':
    main()