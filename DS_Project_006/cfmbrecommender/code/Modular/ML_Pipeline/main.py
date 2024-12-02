from pathlib import Path
import sys

module_path = Path(__file__).parents[1]
sys.path.append(str(module_path))

from ML_Pipeline import RecommenderEngine


def run_recommender():

    re_object = RecommenderEngine()
    print(re_object.get_user_recommendations())


if __name__ == '__main__':
    run_recommender()
