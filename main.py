from scraper import download_data
import pandas as pd


class main:

    #download_data()
    data = pd.read_excel('data/CDOTRM_CD_Crash_Listing_-_2022.xlsx')

    print(data.columns)
    
    
  
if __name__ == "__main__":
    main()
