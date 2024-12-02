from pathlib import Path
import os
import sys
import pandas as pd

module_path = Path(__file__).parents[1]
sys.path.append(str(module_path))

LOW_RATING_THRESH = 300


class DataPipeline:

    from ML_Pipeline.EDA import get_data_info, create_visualizations
    from ML_Pipeline.Preprocess import encode_data, create_features, get_popular_products
    from ML_Pipeline.Recommender import create_norm_rating_table
    from ML_Pipeline.SaveData import save_model_resources


    def __init__(self):

        self.output_path = os.path.join(module_path, "Output/")
        self.data_path = os.path.join(module_path, "Input/ratings_Beauty.csv")
        self.data = pd.read_csv(self.data_path)
        self.encoded_data = None
        self.filtered_data = None
        self.similarity_table = None
        self.low_rating_threshold = LOW_RATING_THRESH
        self.user_prod_ratings = \
            self.data.groupby(by = \
                              "UserId")["ProductId"].count().sort_values(ascending=False)
        self.rated_products = \
            self.data.groupby(by = \
                              "ProductId")["Rating"].count().sort_values(ascending=False)
        
    def perform_EDA(self):

        self.get_data_info()
        self.create_visualizations()

    def preprocess_data(self):

        self.encode_data()
        self.create_features()
        self.get_popular_products()

    def build_recommendation_engine(self):

        self.create_norm_rating_table()
        self.save_model_resources()


class RecommenderEngine:

    from ML_Pipeline.Recommender import (select_random_user,
                                         find_similar_users,
                                         find_products,
                                         prepare_input_data)

    def __init__(self):

        self.output_path = os.path.join(module_path, "Output/")
        self.norm_rating_table_path = os.path.join(module_path, "Output/Norm_Rating_Table.csv")
        self.norm_rating_table = pd.read_csv(self.norm_rating_table_path)
        self.norm_rating_table_ = None
        self.norm_rating_table_encoded = None
        self.num_recommendations = 5
        self.curr_userID = None
        self.similar_user_list = None
        self.recommendataion_list = None


    def get_user_recommendations(self):

        self.prepare_input_data()
        self.select_random_user()  
        self.find_similar_users()
        self.find_products()

        rec_string = f"\nCurrent User: {self.curr_userID},\n\
Similar Users: {self.similar_user_list},\nRecommendations: {self.recommendataion_list}"

        return rec_string
