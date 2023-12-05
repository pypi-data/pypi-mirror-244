import pandas as pd
import os
from datasets import load_dataset
import pyarrow
import json
from tqdm import tqdm
import math
import yaml
import configparser
import colorama
from colorama import Fore, Style
import psutil
from typing import Dict, Optional 
import gc

# Define dataset names and their configurations
class DatasetConcatConfig:
    """
    Configuration for concatenating multiple datasets into a single dataset.

    Args:
        directory (str): Directory to save the concatenated datasets
        datasets (dict): Dictionary mapping dataset name to dataset configuration
            The dataset configuration can be:
                - None for default config
                - A string representing the dataset split (e.g. "train") 
                - A dictionary with dataset specific options
        columns (dict): Dictionary mapping dataset name to list of column name and type tuples
            The column types can be "Input" or "Output"
            The column name can be:
                - A string representing a single column 
                - A concat expression like "Concat(col1 and col2)" to join multiple columns
    """

    def __init__(self, directory, datasets=None, columns=None, **kwargs):
        self.rows_per_gb = kwargs.pop("rows_per_gb", 25000)
            
        self.datasets = datasets
        self.columns = columns
        self.directory = directory
    @property
    def datasets(self):
        return self._datasets

    @datasets.setter
    def datasets(self, datasets):
        self._datasets = datasets

    @property
    def columns(self):
        return self._columns    

    @columns.setter
    def columns(self, columns):
        self._columns = columns
    @property
    def directory(self):
        return self._directory
    @directory.setter
    def directory(self, directory):
        self._directory = directory
    def load_from_json(self, datasets_file, columns_file):
        with open(datasets_file) as f:
            self.datasets = json.load(f)

        with open(columns_file) as f:   
            self.columns = json.load(f)

    def load_from_yaml(self, datasets_file, columns_file):  
        with open(datasets_file) as f:
            self.datasets = yaml.safe_load(f)

        with open(columns_file) as f:
            self.columns = yaml.safe_load(f)

    def load_from_ini(self, config_file):
        parser = configparser.ConfigParser()
        parser.read(config_file)

        self.datasets = dict(parser['Datasets'])
        self.columns = dict(parser['Columns'])

class ChatDatasetConcatenator:
    def __init__(self, config: DatasetConcatConfig):
        if isinstance(config, DatasetConcatConfig):
            self.config = config
        else:
            raise RuntimeError(f"Config must be an instance of DatasetConcatConfig but got " + type(self.config).__name__)
    @staticmethod
    def _concatenate(
            directory,
            datasets: dict[str, str],
            columns_to_include: dict[str, tuple[str, str]],
            rows_per_gb: Optional[int]=25000,
            cache_dir: Optional[str] = None,
        ) -> None:
        colorama.init(autoreset=True)
        dataframes = []

        def print_success(args):
            print(Fore.GREEN + args + Style.RESET_ALL)

        def print_error(args):
            print(Fore.RED + args + Style.RESET_ALL)

        def print_warning(args):
            print(Fore.YELLOW + args + Style.RESET_ALL)
        for dataset_name, dataset_config in datasets.items():
            try:
                dataset = load_dataset(dataset_name, dataset_config, split="train", cache_dir=cache_dir)
                dataframe = dataset.data.to_pandas()
            except Exception as e:
                print_warning(f"Failed to load {dataset_name} from Hugging Face Datasets. Trying to load from local storage...")
                # Adjust the path to the datasets on your PC
                try:
                    dataframe = pd.read_parquet(dataset_name)
                except FileNotFoundError:
                    print_error(f"Failed to load {dataset_name} from local storage. Skipping... Reason {e}")
                    continue
                except pyarrow.lib.ArrowInvalid:
                    print_warning(f"{dataset_name} is not a parquet dataset, trying json...")
                    with open(dataset_name, "r", encoding="utf-8") as file:
                        try:
                            data = json.load(file)["train"]
                        except KeyError:
                            data = json.load(file)
                        except Exception as e:
                            try:
                                print_warning(f"Failed to load {dataset_name} with json, trying csv... Reason {e}")
                                data = pd.read_csv(dataset_name).to_dict()
                            except Exception as e:
                                print_warning(f"Failed to load {dataset_name} with csv, trying configparser... Reason {e}")
                                try:
                                    parser = configparser.ConfigParser()
                                    parser.read(dataset_name)
                                    data = pd.DataFrame(parser).to_dict()
                                except Exception:
                                    print_error(f"Dataset {dataset_name} is an unknown file format. Skipping...")
                        dataframe = pd.DataFrame(data)
                        del data
                        gc.collect()
                except Exception:
                    print_error("{}".format("=" * 40))
                    print_error("Failed to append dataset" + dataset_name + "for reason: " + e)
                    print_error("{}".format("=" * 40))
            for col, col_type in columns_to_include[dataset_name]:
                if "Input" in col_type:
                    if col.startswith("Concat(") and col.endswith(")"):
                        concat_cols = col[len("Concat("):-1].split(" and ")
                        # Check that all the columns in 'concat_cols' exist in the dataframe
                        if not all(col_name in dataframe.columns for col_name in concat_cols):
                            print_error("One or more columns specified in Concat() do not exist in the dataframe.")
                            dataframe["Input"] = ""
                            continue
                        dataframe["Input"] = dataframe[concat_cols].astype(str).agg(" ".join, axis=1)
                    else:
                        dataframe["Input"] = dataframe[col]
                elif "Output" in col_type:
                    if col.startswith("Concat(") and col.endswith(")"):
                        concat_cols = col[len("Concat("):-1].split(" and ")
                        # Check that all the columns in 'concat_cols' exist in the dataframe
                        if not all(col_name in dataframe.columns for col_name in concat_cols):
                            print_error("One or more columns specified in Concat() do not exist in the dataframe.")
                            dataframe["Output"] = ""
                            continue
                        dataframe["Output"] = dataframe[concat_cols].astype(str).agg(" ".join, axis=1)
                    else:
                        dataframe["Output"] = dataframe[col]
            try:
                dataframes.append(dataframe[["Input", "Output"]])
                print_success(f"Successfully appended the dataset {dataset_name}")
            except KeyError:
                print_error("The following index does not exist:" + e + "Make sure you included the correct column/index in the Tuple")
            except Exception:
                print_error("{}".format("=" * 40))
                print_error("Failed to append dataset" + dataset_name + "for reason: " + e)
                print_error("{}".format("=" * 40))
        # Combine the datasets
        os.makedirs(directory, exist_ok=True)
        combined_dataframe = pd.concat(dataframes)
        print(f"Number of rows in the final dataset: {len(combined_dataframe)}")
        total_rows = len(combined_dataframe)
        total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)

        # Calculate the max_batch_size based on adding n rows for every 1 GB of RAM
        max_batch_size = rows_per_gb * total_ram_gb
        rows_per_batch = int(math.ceil(min(total_rows, max_batch_size)))
        num_batches = math.ceil(total_rows / rows_per_batch)
        print(f"Splitting the dataset into {num_batches} batches")
        # Split the dataset into batches
        dataframes_batches = [combined_dataframe[i:i + rows_per_batch] for i in range(0, total_rows, rows_per_batch)]
        del combined_dataframe
        gc.collect()

        # Save each batch separately
        output_path = directory + "combined_datasets_batch_{}.parquet"
        for idx, df_batch in tqdm(enumerate(dataframes_batches, start=1)):
            # Shuffle the combined dataset
            df_batch = df_batch.sample(frac=1)
            batch_output_file = output_path.format(idx)
            df_batch.to_parquet(batch_output_file)
            print_success(f"Batch {idx} saved to {batch_output_file}")
            del df_batch
            gc.collect()

    def run(self, cache_dir=None):
        datasets = self.config.datasets
        columns = self.config.columns
        directory = self.config.directory
        rpg = self.config.rows_per_gb
        
        self._concatenate(directory, datasets, columns, rows_per_gb=rpg, cache_dir=cache_dir)
if __name__ == "__main__":
    datasets = {
    # The directory (key) can be either a Hugging Face dataset name or a local directory path
    "Local/directory/to/dataset": None,
    "vicgalle/alpaca-gpt4": None,
    "ChristophSchuhmann/essays-with-instructions": None,
    "checkai/instruction-poems": None,
    "pubmed_qa": "pqa_artificial",  # The value specifies the config name to load
    "BI55/MedText": None,
    "nampdn-ai/tiny-codes": None,
    "rombodawg/MegaCodeTraining112k": None,
}

    columns_to_include = {
    # This dictionary must have the same length as the 'datasets' dictionary, unless loading the same dataset multiple times for different configs
    "Local/directory/to/dataset": [
        ("User", "Input"),  # This specifies the input column to include, and its target column (MUST BE "Input" or "Output")
        ("Assistant", "Output")
    ],
    "TokenBender/code_instructions_120k_alpaca_style": [
        ("Concat(input and instruction)", "Input"), # This concatenates two different columns and includes it into a single "Input" column
        ("output", "Output")
    ],
    "C:\\Users\\Sebastian Gabarain\\Downloads\\1M-GPT4-Augmented.parquet": [
        ("question", "Input"),
        ("response", "Output")
    ],
    "vicgalle/alpaca-gpt4": [
        ("Concat(input and instruction)", "Input"),
        ("output", "Output")
    ],
    "ChristophSchuhmann/essays-with-instructions": [
        ("instructions", "Input"),
        ("essays", "Output")
    ],
    "checkai/instruction-poems": [
        ("INSTRUCTION", "Input"),
        ("RESPONSE", "Output")
    ],
    "pubmed_qa": [
        ("question", "Input"),
        ("long_answer", "Output")
    ],
    "BI55/MedText": [
        ("Prompt", "Input"),
        ("Completion", "Output")
    ],
    "nampdn-ai/tiny-codes": [
        ("prompt", "Input"),
        ("response", "Output")
    ],
    "C:\\Users\\Sebastian Gabarain\\Downloads\\3_5M-GPT3_5-Augmented.parquet": [
        ("question", "Input"),
        ("response", "Output")
    ],
    "rombodawg/MegaCodeTraining112k": [
        ("prompt", "Input"),
        ("completion", "Output")
    ]
}
    config = DatasetConcatConfig("D:\\Projects\\InstructMixData\\", datasets=datasets, columns=columns_to_include)
    concat = ChatDatasetConcatenator(config)
    concat.run()