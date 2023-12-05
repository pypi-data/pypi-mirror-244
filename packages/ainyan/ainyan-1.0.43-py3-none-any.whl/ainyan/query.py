import argparse
import configparser

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


def post_query(model, tokenizer, config):
    config_queries = config["queries"]
    string_list_str = config_queries.get('texts')
    string_list = string_list_str.split(', ')
    # https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
    temperature = config_queries.getfloat("temperature", fallback=1.0)
    repetition_penalty = config_queries.getfloat("repetition_penalty", fallback=1.0)
    top_k = config_queries.getint("top_k", fallback=50)
    max_length = config_queries.getint("max_length", fallback=50)

    prompt = pipeline(task="text-generation",
                      model=model,
                      tokenizer=tokenizer,
                      temperature=temperature,
                      repetition_penalty=repetition_penalty,
                      top_k=top_k,
                      max_length=max_length)

    for query in string_list:
        print("----\n" + query + "----\n")
        print(prompt(query)[0]['generated_text']+ "\n")
        print("----\n")


def main():
    parser = argparse.ArgumentParser(description='Training facilitator')
    parser.add_argument('--config', metavar='config', required=True,
                        help='the path to the ini file used for query')
    parser.add_argument('--model', metavar='model', required=False,
                        help='override the name defined in the ini file')
    args = parser.parse_args()

    training_file = args.config

    config = configparser.ConfigParser()
    config.read(training_file)

    # override model if needed
    if args.model is not None:
        config.set("training", "finalname", args.model)

    training = config["training"]
    newmodel_finalname = training["finalname"]

    print("Using training file:" + training_file + " ; loading model:" + newmodel_finalname+"\n")

    model = AutoModelForCausalLM.from_pretrained(newmodel_finalname, trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(newmodel_finalname, trust_remote_code=True)
    post_query(model, tokenizer, config)


if __name__ == '__main__':
    main()