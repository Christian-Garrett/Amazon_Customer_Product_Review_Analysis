import pandas as pd
import operator
import random
from sklearn.metrics.pairwise import cosine_similarity


MAX_USERS = 100

def create_norm_rating_table(self):

    self.norm_rating_table = pd.pivot_table(self.filtered_data,
                                           values='normalized_rating',
                                           index='UserId',
                                           columns='product')
    
    self.norm_rating_table.fillna(0, inplace=False)


def prepare_input_data(self):

    self.norm_rating_table.set_index('UserId', inplace=True)
    self.norm_rating_table = self.norm_rating_table.fillna(0)


def select_random_user(self):

    selecting_users = list(self.norm_rating_table.index)
    selecting_users = selecting_users[:MAX_USERS]
    rand_number = random.randrange(0, MAX_USERS-1, 1)
    self.curr_userID = selecting_users[rand_number]


def find_similar_users(self):

    # create a dataframe of just the current user
    user = \
        self.norm_rating_table.loc[self.norm_rating_table.index == self.curr_userID]

    # and a dataframe of all other users
    other_users = \
        self.norm_rating_table.loc[self.norm_rating_table.index != self.curr_userID]

    # calculate cosine similarity between user and each other user
    cos_similarities = cosine_similarity(user, other_users)[0].tolist()

    other_user_index = other_users.index.tolist()

    norm_rating_table_dict = dict(zip(other_user_index, cos_similarities))

    # sort by similarity
    norm_rating_table_dict_sorted = \
        sorted(norm_rating_table_dict.items(), key=operator.itemgetter(1))
    norm_rating_table_dict_sorted.reverse()

    # take the top N users
    most_similar_user_ratings = \
        norm_rating_table_dict_sorted[:self.num_recommendations]

    self.similar_user_list = [user[0] for user in most_similar_user_ratings]

def find_products(self):

    # getting all similar users
    similar_user_norm_ratings = \
        self.norm_rating_table.loc[self.norm_rating_table.index.isin(self.similar_user_list)]

    # getting mean ratings given for each users
    similar_user_norm_means = similar_user_norm_ratings.mean(axis=0)
    similar_user_norm_means_df = \
        pd.DataFrame(similar_user_norm_means, columns=['mean'])

    # for the current user data
    curr_user_norm_ratings_df = \
        self.norm_rating_table.loc[self.norm_rating_table.index == self.curr_userID]

    # transpose it so its easier to filter
    curr_user_norm_ratings_column = curr_user_norm_ratings_df.transpose()

    # rename the column as 'rating'
    curr_user_norm_ratings_column.columns = ['rating']

    # rows with a 0 value.
    curr_user_unrated_products = \
        curr_user_norm_ratings_column.loc[curr_user_norm_ratings_column['rating'] == 0]

    # generate a list of products the user has not used
    curr_user_unrated_product_list = \
        curr_user_unrated_products.index.tolist()

    # find the products the current user has not rated in the similar user data
    unrated_product_similar_user_data = \
        similar_user_norm_means_df.loc[similar_user_norm_means_df.index.isin(curr_user_unrated_product_list)]

    # order the dataframe
    unrated_product_similar_user_data_sorted = \
        unrated_product_similar_user_data.sort_values(by=['mean'], ascending=False)

    # take the top products
    top_similar_user_products = \
        unrated_product_similar_user_data_sorted.head(self.num_recommendations)

    self.recommendataion_list = \
        top_similar_user_products.index.tolist()
