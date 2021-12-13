from TikTokApi import TikTokApi as tiktok
from helpers import process_results
import pandas as pd
import sys

def get_data(hashtag):
    verifyFp = "verify_kx4dojgt_A310k42o_YH9y_4PAP_BKRj_3auYq6afGSiW"
    api = tiktok.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)

    trending=api.by_hashtag(hashtag)
    flattened_data = process_results(trending)
    df=pd.DataFrame.from_dict(flattened_data,orient="index")
    df.to_csv("tiktokdata.csv",index=False)

# Running through command line
if __name__=="__main__":
    get_data(sys.argv[1])