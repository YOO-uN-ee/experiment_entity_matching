import os
import argparse
import logging
import pickle

import polars as pl
from serialization.text_based import *
from LLM_based.prompt_generation import design_prompt
from LLM_based.llama3_based import *
# from LLM_based.gpt_based import *

def main():
    print(test_llama3("POINT (441000.0000000000000000 5725750.0000000000000000) is located in Quebec Canada. Guess the EPSG system."))

if __name__ == "__main__":
    main()