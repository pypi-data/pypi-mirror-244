import os
from transformers import pipeline, AutoTokenizer
import torch
from langchain import HuggingFacePipeline, PromptTemplate, LLMChain
from langchain.llms import OpenAI
from langchain import PromptTemplate


class LLM_KeywordExtractor:
    def __init__(self, model_name, openai_api_key=None):
        if 'llama' in model_name.lower():
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.pipeline = pipeline(
                "text-generation",
                model=model_name,
                tokenizer=self.tokenizer,
                torch_dtype=torch.bfloat16,
                device_map="auto",
                max_length=512,
                do_sample=True,
                top_k=10,
                num_return_sequences=1,
                eos_token_id=self.tokenizer.eos_token_id
            )
            self.llm = HuggingFacePipeline(pipeline=self.pipeline, model_kwargs={'temperature':0.3})
        elif 'davinci' in model_name.lower():
            self.openai = OpenAI(
                model_name=model_name,
                openai_api_key=openai_api_key
            )
        else:
            raise ValueError("Unsupported model name")

    def extract_keywords(self, input_text):
        if hasattr(self, 'llm'):
            template = """
            You are an intelligent AI Assistant. Extract relevant keywords that represent the main ideas, concepts, entities, or themes mentioned in the provided text.
            Input: {input_text}
            Answer:"""
            prompt = PromptTemplate(template=template, input_variables=["input_text"])
            llm_chain = LLMChain(prompt=prompt, llm=self.llm)
            return llm_chain.run(input_text)
        elif hasattr(self, 'openai'):
            template = """You are an expert in keyword extraction. You are provided with various contexts. Your task is to generate a set of relevant keywords for the context provided. The keywords should ideally represent the main ideas, concepts, entities, or themes mentioned in the context.

            Context: {input_text}
            Question: Extract relevant keywords from the context provided.

            Answer: """
            prompt_template = PromptTemplate(
                input_variables=["input_text"],
                template=template
            )
            return self.openai(
                prompt_template.format(query=input_text)
            )
        else:
            raise RuntimeError("Model not initialized properly")








