import os


def save_model_resources(self):

    self.filtered_data.to_csv(os.path.join(self.output_path,
                                           'Top_Products.csv'))
    
    self.norm_rating_table.to_csv(os.path.join(self.output_path,
                                               'Norm_Rating_Table.csv'))
