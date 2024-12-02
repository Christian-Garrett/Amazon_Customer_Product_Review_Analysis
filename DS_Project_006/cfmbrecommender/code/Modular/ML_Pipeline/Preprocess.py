import pandas as pd
from sklearn import preprocessing


def encode_data(self):

    label_encoder = preprocessing.LabelEncoder()

    self.data['user'] = \
        label_encoder.fit_transform(self.data['UserId'])
    self.data['product'] = \
        label_encoder.fit_transform(self.data['ProductId'])


def create_features(self):
        
        # average rating given by each user
        average_rating = self.data.groupby(by="user", as_index=False)['Rating'].mean()

        # merge with the dataset as we will be using that later
        self.data = pd.merge(self.data, average_rating, on="user")

        # renaming columns
        self.data = \
            self.data.rename(columns={"Rating_x": "real_rating",
                                      "Rating_y": "average_rating"})

        self.data['normalized_rating'] = \
            self.data['real_rating'] - self.data['average_rating']


def get_popular_products(self):

    real_product_ratings = self.data.groupby('product')['real_rating'].count()
    real_product_ratings_df = pd.DataFrame(real_product_ratings)

    filtered_ratings_per_product = \
        real_product_ratings_df.loc[real_product_ratings_df.real_rating >= self.low_rating_threshold]
    popular_products = filtered_ratings_per_product.index.tolist()
    self.filtered_data = self.data.loc[self.data["product"].isin(popular_products)]

    print("Filtered rated product in the dataset: \n", self.filtered_data.head())
    print("The size of dataset has changed from ", 
            len(self.data), " to ", len(self.filtered_data))
