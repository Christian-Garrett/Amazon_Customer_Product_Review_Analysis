from pathlib import Path
import sys

module_path = Path(__file__).parents[0]
sys.path.append(str(module_path))

from ML_Pipeline import DataPipeline


dp_object = DataPipeline()

dp_object.perform_EDA()
dp_object.preprocess_data()
dp_object.build_recommendation_engine()
