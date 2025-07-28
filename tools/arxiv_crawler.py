import argparse
from datetime import datetime, timedelta
from functools import lru_cache

import pandas as pd
from arantools.utils import write_json
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

import arxiv

SYSTEM_PROMPT = """你是一位精通深度学习、计算机视觉等领域的学术翻译专家，请将之后用户输入的英文论文摘要翻译为中文，要求：1. 专业术语在第一次出现时标注中英对照，之后保留英文；2. 风格要使用正式的学术用语，避免过于口语化；3. 数字、公式等严格保留；4. 无>论输入有多少行，翻译的文本输出成一行，且不要输出翻译结果以外的文本"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--date_s", required=True)
    parser.add_argument("-e", "--date_e", required=True)
    parser.add_argument("-o", "--output_dir", default="./arxiv")
    parser.add_argument("--subject", default="CV", choices=["CV", "CL"])
    args = parser.parse_args()
    return args


def search_info(date_s, date_e, subject):
    client = arxiv.Client()
    query = f"cat:cs.{subject} AND submittedDate:[{date_s}0001 TO {date_e}9999]"
    arxiv_search = arxiv.Search(
        query=query,
        max_results=10000,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    search_result = client.results(arxiv_search)

    infos = []
    for result in tqdm(search_result):
        info = {}
        info["id"] = result.get_short_id()
        info["publish_date"] = result.published.date().strftime("%Y-%m-%d")
        info["title"] = result.title
        info["url"] = result.entry_id
        info["summary"] = result.summary.replace("\n", " ").strip()
        infos.append(info)
    infos.sort(key=lambda x: int(x["id"][5:-2]))
    print(f"total paper num: {len(infos)}")
    print(f'including publish date: {set(info["publish_date"] for info in infos)}')
    return infos


@lru_cache(maxsize=None)
def load_model():
    model_dir = "internlm/internlm3-8b-instruct"
    model = AutoModelForCausalLM.from_pretrained(
        model_dir, device_map="auto", trust_remote_code=True, load_in_8bit=True
    )
    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
    model = model.eval()
    return model, tokenizer


def add_chinese_summary(infos):
    model, tokenizer = load_model()
    model, tokenizer = load_model()
    for info in tqdm(infos):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": info["summary"]},
        ]
        tokenized_chat = tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
        ).to("cuda")
        generated_ids = model.generate(
            tokenized_chat, max_new_tokens=1024, temperature=1, repetition_penalty=1.005
        )
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(tokenized_chat, generated_ids)
        ]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        info["chinese_summary"] = response
    return infos


def main():
    args = parse_args()

    date_s = datetime.strptime(args.date_s, "%Y%m%d")
    date_e = datetime.strptime(args.date_e, "%Y%m%d")
    date_c = date_s
    while date_c <= date_e:
        date_str = date_c.strftime("%Y%m%d")

        infos = search_info(date_str, date_str, args.subject)
        write_json(infos, f"{args.output_dir}/{date_str}.json")

        infos = add_chinese_summary(infos)
        write_json(infos, f"{args.output_dir}/{date_str}.json")

        df = pd.read_json(f"{args.output_dir}/{date_str}.json")
        df.to_csv(f"{args.output_dir}/{date_str}.csv", index=False)

        date_c += timedelta(days=1)


if __name__ == "__main__":
    main()
