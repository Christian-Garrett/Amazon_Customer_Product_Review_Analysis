from cfmbrecommender.code.Modular.ML_Pipeline.EDA import EDA
from cfmbrecommender.code.Modular.ML_Pipeline.Preprocess import Preprocess
from cfmbrecommender.code.Modular.ML_Pipeline.Recommender import Recommender




file = 'cfmbrecommender/code/Modular/Input/ratings_Beauty.csv'
low_rating_threshold = 200


def run():

    raw_data = EDA(file)

    explored_data_df = raw_data.get_data()

    ratings = Preprocess(explored_data_df, low_rating_threshold)

    encoded_ratings_df = ratings.get_data()

    matrix = Recommender(explored_data_df, encoded_ratings_df)

    new_customer = matrix.get_customer()

    similar_users, recommendation_indices = matrix.get_recommendations(new_customer)

    



run()


