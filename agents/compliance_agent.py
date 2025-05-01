import os
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def read_10k_document():
    with open("data/10k_aapl.txt", "r", encoding="utf-8") as file:
        return file.read()

def get_compliance_insights(document_text):
    llm = Ollama(model="llama3")  # or "mistral" if you prefer
    prompt = PromptTemplate.from_template("""
You are a financial compliance analyst. Given this 10-K filing content, identify and summarize:

1. Key Risk Factors mentioned
2. Any legal proceedings or regulatory actions
3. SEC regulation references (e.g., Regulation S-K, Item 303)
4. ESG (Environmental, Social, Governance) disclosures if any

Output your findings in a well-structured report format.

10-K Content:
{document}
""")

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"document": document_text})

if __name__ == "__main__":
    document = read_10k_document()
    print("\n🔍 Compliance & Regulatory Insights:\n")
    print(get_compliance_insights(document))
