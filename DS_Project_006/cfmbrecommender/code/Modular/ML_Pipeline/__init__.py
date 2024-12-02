from pathlib import Path
import os
import sys
import pandas as pd

module_path = Path(__file__).parents[1]
sys.path.append(str(module_path))

LOW_RATING_THRESH = 300
NUM_RECOMMENDATIONS = 5


class DataPipeline:
    """
        A class used to create the collaborative filtering recommender 
        data pipeline.
        ...

        Attributes
        ----------
        output_path : str
            Output data text path
        data_path : str
            Input data text path
        data : df
            Input data
        filtered_data : df
            Truncated dataset with popular products with each row
            containing the normalized ratings for each user by product
        low_rating_threshold : int
            Used to truncate the dataset by setting the minimum number
            of customer review needed to keep a product
        user_prod_ratings : df
            Contains the count of products rated for each user in the
            dataset
        rated_products : df
            Contains the count of ratings for each product

        Methods
        -------
        perform_EDA()
            Descriptive statistics and visualizations
        preprocess_data()
            Label encoding, normalized rating feature creation and
            dataset truncation to accomodate processing limitations
        build_recommendation_engine()
            Create and save a dataframe with the top products as well
            as a pivoted dataframe with the user in the index and the 
            products as the columns that contains norm rating info

    """
    from ML_Pipeline.EDA import get_data_info, create_visualizations
    from ML_Pipeline.Preprocess import encode_data, create_features, get_popular_products
    from ML_Pipeline.Recommender import create_norm_rating_table
    from ML_Pipeline.SaveData import save_model_resources


    def __init__(self):

        self.output_path = os.path.join(module_path, "Output/")
        self.data_path = os.path.join(module_path, "Input/ratings_Beauty.csv")
        self.data = pd.read_csv(self.data_path)
        self.filtered_data = None
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
    """
        A class used to creates product recommendations for a user.
        ...

        Attributes
        ----------
        output_path : str
            Output data text path
        norm_rating_table_path : str
            Input data text path
        norm_rating_table : df
            Input data containing the normalized rating for each product
            by user
        num_recommendations : int
            The number of recommendations to be generated
        curr_userID : str
            The ID number of the current user for recommendations
        similar_user_list : list
            List of the top N similar users based on cosine similarities
        recommendataion_list : list
            List of the top N product number recommendations

        Methods
        -------
        get_user_recommendations()
            Preprocess the input resources, select a user at random,
            generate the top N recomendations based on similar users
            derived from cosine similarity calculations

        Returns
        -------
        rec_string : str
            String containing the current user, the top N similar users
            using cosine similarity and the top N recommendations

    """

    from ML_Pipeline.Recommender import (select_random_user,
                                         find_similar_users,
                                         find_products,
                                         prepare_input_data)

    def __init__(self):

        self.output_path = os.path.join(module_path, "Output/")
        self.norm_rating_table_path = os.path.join(module_path, "Output/Norm_Rating_Table.csv")
        self.norm_rating_table = pd.read_csv(self.norm_rating_table_path)
        self.num_recommendations = NUM_RECOMMENDATIONS
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
