import pandas as pd
import numpy as np
import plotly.graph_objects as go



class EDA:

    def __init__(self, file):

        self.df = pd.read_csv(file)
        self.user_prod_ratings = self.df.groupby(by = "UserId")["ProductId"].count().sort_values(ascending = False)
        self.rated_products = self.df.groupby(by = "ProductId")["Rating"].count().sort_values(ascending = False)

        self.data_info()
        self.visualizations()


    def data_info(self):

        print('df shape: ', self.df.shape)
        print('df head: \n', self.df.head())
        duplicates = self.df.duplicated(["UserId","ProductId", "Rating", "Timestamp"]).sum()
        print('\nNum duplicate records: ', duplicates)
        print('Num unique users:', len(self.df.UserId.unique()))
        print('Num unique products:', len(self.df.ProductId.unique()))
        print('Num total ratings: ', self.df.shape[0])
        print('\nNull values: \n', self.df.isnull().any())

        print('\nNumber of products with minimum of 5 reviews/ratings:',
              self.rated_products[self.rated_products>5].count())
        print('Number of products with minimum of 4 reviews/ratings:',
              self.rated_products[self.rated_products>4].count())
        print('Number of products with minimum of 3 reviews/ratings:',
              self.rated_products[self.rated_products>3].count())
        print('Number of products with minimum of 2 reviews/ratings:',
              self.rated_products[self.rated_products>2].count())
        print('Number of products with minimum of 1 reviews/ratings:',
              self.rated_products[self.rated_products>1].count())

    def product_rating_categories(self):
        
        # convert to make dataframe to analyse data
        number_of_ratings_given = pd.DataFrame(self.rated_products)
        print("Products with ratings given by users: \n", number_of_ratings_given.head())

        less_than_ten = []
        less_than_fifty_greater_than_ten = []
        greater_than_fifty_less_than_hundred = []
        greater_than_hundred = []
        average_rating = []

        for rating in number_of_ratings_given['Rating']:
            if rating <=10:
                less_than_ten.append(rating)
            if rating > 10 and rating <= 50:
                less_than_fifty_greater_than_ten.append(rating)
            if rating > 50 and rating <= 100:
                greater_than_fifty_less_than_hundred.append(rating)
            if rating > 100:
                greater_than_hundred.append(rating)

            average_rating.append(rating)
    
        print("\nRatings_count_less_than_ten: ", 
              len(less_than_ten))
        print("Ratings_count_greater_than_ten_less_than_fifty: ", 
              len(less_than_fifty_greater_than_ten))
        print("Ratings_count_greater_than_fifty_less_than_hundred: ", 
              len(greater_than_fifty_less_than_hundred))
        print("Ratings_count_greater_than_hundred: ", 
              len(greater_than_hundred))
        print("Average number of products rated by users: ", 
              np.mean(average_rating))

        x_values = ["Ratings_count_less_than_ten","Ratings_count_greater_than_ten_less_than_fifty",
           "Ratings_count_greater_than_fifty_less_than_hundred","Ratings_count_greater_than_hundred"]
        y_values = [len(less_than_ten),len(less_than_fifty_greater_than_ten),
                    len(greater_than_fifty_less_than_hundred),
                    len(greater_than_hundred)]
        plot = go.Figure([go.Bar(x = x_values, y = y_values, textposition='auto')])
        plot.add_annotation(
                x=1,
                y=100000,
                xref="x",
                yref="y")
        plot.update_layout(title_text='Ratings Count on Products',
                            xaxis_title="Ratings Range",
                            yaxis_title="Count of Rating")
        plot.write_image("cfmbrecommender/code/Modular/Output/ratings_count_categories.png", 
                         engine="kaleido")


    def visualizations(self):

        index = ['Total size of records', "Number of unique users","Number of unique products"]
        values =[len(self.df),len(self.df['UserId'].unique()),len(self.df['ProductId'].unique())]
        plot = go.Figure([go.Bar(x=index, y=values,textposition='auto')])
        plot.update_layout(title_text='Number of Users and Products w.r. to Total size of Data',
                            xaxis_title="Records",
                            yaxis_title="Total number of Records")
        plot.write_image("cfmbrecommender/code/Modular/Output/total_users_product.png", engine="kaleido")


        print("\nRange of Ratings: \n", self.df['Rating'].value_counts())
        print("\nRating Value Counts 1-5: ", list( self.df['Rating'].value_counts()))
        values = list(self.df['Rating'].value_counts())
        plot = go.Figure([go.Bar(x = self.df['Rating'].value_counts().index, 
                                 y = values, textposition='auto')])
        plot.update_layout(title_text='Ratings given by users',
                            xaxis_title="Rating",
                            yaxis_title="Total number of Ratings")
        plot.write_image("cfmbrecommender/code/Modular/Output/ratings_range.png", engine="kaleido")


        print("\nProducts which occurred the most: \n", self.df['ProductId'].value_counts().nlargest(5))
        values = list(self.df['ProductId'].value_counts())
        plot = go.Figure([go.Bar(x = self.df['ProductId'].value_counts().nlargest(5).index, 
                                 y = values, textposition='auto')])
        plot.update_layout(title_text='Most rated products',
                            xaxis_title="ProductID",
                            yaxis_title="Number of times occurred in the data")
        plot.write_image("cfmbrecommender/code/Modular/Output/popular_products.png", engine="kaleido")


        print("\nAverage rating given by each user: ", self.user_prod_ratings.head())
        plot = go.Figure(data=[go.Histogram(x=self.user_prod_ratings)])
        plot.update_layout(title_text='Average Rating by User',
                            xaxis_title="Num Ratings",
                            yaxis_title="Num Products")
        plot.write_image("cfmbrecommender/code/Modular/Output/avg_rating_by_user.png", engine="kaleido")


        print("\nAverage product rating: ", self.rated_products.head())
        plot = go.Figure(data=[go.Histogram(x=self.rated_products.nlargest(2000))])
        plot.update_layout(title_text='Number of Ratings for Top 2000 Products',
                            xaxis_title="Product",
                            yaxis_title="Number of ratings")
        plot.write_image("cfmbrecommender/code/Modular/Output/ratings_per_product.png", engine="kaleido")

        self.product_rating_categories()


    def get_data(self):
        return self.df
