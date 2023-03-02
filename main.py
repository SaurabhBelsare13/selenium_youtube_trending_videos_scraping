
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import pandas as pd


YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"

def get_driver():
   chrome_options = Options()
   chrome_options.add_argument('--no-sandbox')
   chrome_options.add_argument('--disable-dev-shm-usage')

   driver = webdriver.Chrome(options=chrome_options)
   return driver

def get_videos(driver):
  driver.get(YOUTUBE_TRENDING_URL)
    
  VIDEO_DIV_TAG = "ytd-video-renderer"
  videos = driver.find_elements(By.TAG_NAME,VIDEO_DIV_TAG)
  return videos
  
def parse_video(video):
    
    title_tag = video.find_element(By.ID, 'video-title')
    title = title_tag.text
    
    url = title_tag.get_attribute('href')
    
    thumbnail_tag = video.find_element(By.TAG_NAME,'img')
    thumbnail_url = thumbnail_tag.get_attribute('src')
    
    channel_div = video.find_element(By.CLASS_NAME,'style-scope ytd-channel-name')
    channel_name = channel_div.text
    
    
    metadata_line = video.find_element(By.ID,'metadata-line')
    metadata_spans = metadata_line.find_elements(By.TAG_NAME,'span')
    views = metadata_spans[0].text.replace('views',' ')
    uploded = metadata_spans[1].text

    description = video.find_element(By.ID,'description-text')

    return { 
      'title': title, 
      'url': url, 
      'channel': channel_name,
      'description': description,
      'thumbnail_url': thumbnail_url,
      'views': views,
      'uploded':uploded
     }

  
if __name__ == "__main__":
  print('getting driver')
  driver = get_driver()
    
  print('fetching trending videos')
  videos = get_videos(driver)
    
  print(f'found {len(videos)} videos')
    
  print('parsing top 10 videos')
    
  videos_data = [parse_video(video) for video in videos[:10]]
  
  videos_df = pd.DataFrame(videos_data)
  print(videos_df)
  
  videos_df.to_csv('youtube_trend.csv')
  
  




