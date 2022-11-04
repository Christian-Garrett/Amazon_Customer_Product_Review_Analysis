import pandas as pd
import operator
import random

from sklearn.metrics.pairwise import cosine_similarity




class Recommender:

    def __init__(self, data, filtered_ratings_data):

        self.data = data
        self.filtered_ratings_data = filtered_ratings_data
        self.similarity_table = self.create_similarity_table()
        self.curr_user = self.select_new_user()


    def select_new_user(self):

        selecting_users = list(self.similarity_table.index)
        selecting_users = selecting_users[:100]
        rand_number = random.randrange(0,99,1)
        user = selecting_users[rand_number]

        return user


    def create_similarity_table(self):

        similarity = pd.pivot_table(self.filtered_ratings_data, values='normalized_rating',
                                    index='UserId', columns='product')
        similarity = similarity.fillna(0)

        return similarity


    def get_similar_users(self, user_id, top_recs):
        '''
        :param user_id: the user we want to recommend
        :param similarity_table: the user-item matrix
        :return: Similar users to the user_id.
        '''

        # create a dataframe of just the current user
        user = self.similarity_table[self.similarity_table.index == user_id]
        # and a dataframe of all other users
        other_users = self.similarity_table[self.similarity_table.index != user_id]
        # calculate cosine similarity between user and each other user
        similarities = cosine_similarity(user, other_users)[0].tolist()

        indices = other_users.index.tolist()
        index_similarity = dict(zip(indices, similarities))

        # sort by similarity
        index_similarity_sorted = sorted(index_similarity.items(), key=operator.itemgetter(1))
        index_similarity_sorted.reverse()

        # take users
        top_users_similarities = index_similarity_sorted[:top_recs]
        users = []
        for user in top_users_similarities:
            users.append(user[0])

        return users


    def get_products(self, user_id, similar_users, top_recommendations=5):
        '''
        :param user_id: user for whom we want to recommend
        :param similar_users: top 5 similar users
        :param similarity_table: the user-item matrix
        :param top_recommendations: no. of recommendations
        :return: top_x_recommended_products
        '''

        # taking the data for similar users
        similar_user_products = self.data[self.data.UserId.isin(similar_users)]

        # getting all similar users
        similar_users = self.similarity_table[self.similarity_table.index.isin(similar_users)]

        #getting mean ratings given by users
        similar_users = similar_users.mean(axis=0)
        similar_users_df = pd.DataFrame(similar_users, columns=['mean'])

        # for the current user data
        user_df = self.similarity_table[self.similarity_table.index == user_id]

        # transpose it so its easier to filter
        user_df_transposed = user_df.transpose()

        # rename the column as 'rating'
        user_df_transposed.columns = ['rating']

        # rows with a 0 value.
        user_df_transposed = user_df_transposed[user_df_transposed['rating'] == 0]

        # generate a list of products the user has not used
        products_not_rated = user_df_transposed.index.tolist()

        # filter avg ratings of similar users for only products the current user has not rated
        similar_users_df_filtered = similar_users_df[similar_users_df.index.isin(products_not_rated)]

        # order the dataframe
        similar_users_df_ordered = similar_users_df_filtered.sort_values(by=['mean'], ascending=False)

        # take the top products
        top_products = similar_users_df_ordered.head(top_recommendations)
        top_products_indices = top_products.index.tolist()

        return top_products_indices


    def get_customer(self):
        return self.curr_user


    def get_recommendations(self, curr_user, num_recs=5):

        similar_users = self.get_similar_users(curr_user, num_recs)
        recommended_products_indices = self.get_products(curr_user, similar_users, num_recs)

        return similar_users, recommended_products_indices





