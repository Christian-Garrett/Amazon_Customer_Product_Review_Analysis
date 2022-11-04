import pandas as pd
from sklearn import preprocessing



class Preprocess:

    def __init__(self, data, low_limit):

        self.data = data
        self.low_limit = low_limit
        self.label_encoder = preprocessing.LabelEncoder()
        self.encoded_data = self.encode_data()


    def encode_data(self):

        dataset = self.data
        dataset['user'] = self.label_encoder.fit_transform(self.data['UserId'])
        dataset['product'] = self.label_encoder.fit_transform(self.data['ProductId'])
        
        # average rating given by each user
        average_rating = dataset.groupby(by="user", as_index=False)['Rating'].mean()

        # let's merge it with the dataset as we will be using that later
        dataset = pd.merge(dataset, average_rating, on="user")

        # renaming columns
        dataset = dataset.rename(columns={"Rating_x": "real_rating", "Rating_y": "average_rating"})

        dataset['normalized_rating'] = dataset['real_rating'] - dataset['average_rating']

        rating_of_product = dataset.groupby('product')['real_rating'].count()
        ratings_of_products_df = pd.DataFrame(rating_of_product)

        filtered_ratings_per_product = ratings_of_products_df[ratings_of_products_df.real_rating >= self.low_limit]
        popular_products = filtered_ratings_per_product.index.tolist()
        filtered_ratings_data = dataset[dataset["product"].isin(popular_products)]

        print("Filtered rated product in the dataset: \n", filtered_ratings_data.head())
        print("The size of dataset has changed from ", 
              len(dataset), " to ", len(filtered_ratings_data))

        return filtered_ratings_data


    def get_data(self):
        return self.encoded_data


