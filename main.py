import requests
import os
from dotenv import load_dotenv
from random import randint


def download_image(comics_url, file_path, params1=''):
    response = requests.get(comics_url, params=params1)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def get_comic(params=None):
    comic_url = 'https://xkcd.com/info.0.json'
    response = requests.get(comic_url, params=params)
    response.raise_for_status()

    current_comic_num = response.json()['num']
    random_number = randint(1, current_comic_num)
    random_url_comic = f'https://xkcd.com/{random_number}/info.0.json'
    response = requests.get(random_url_comic, params=params)
    response.raise_for_status()

    data_comics = response.json()
    comic_img = data_comics['img']
    comic_alt = data_comics['alt']
    download_image(comic_img, 'comics.jpeg')
    return comic_alt


def upload_image(url_comic, file_path):
    with open(file_path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url_comic, files=files)
    response.raise_for_status()
    return response.json()['hash'], response.json()['photo'], response.json()['server']


def get_upload_url(vk_access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload  = {
      'v' : 5.131,
      'access_token' : vk_access_token
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def save_to_albumn(vk_access_token, photo, hash, server):
    comic_url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload  = {
      'v' : 5.131,
      'access_token' : vk_access_token,
      'server' : server,
      'photo' : photo,
      'hash' : hash
    }
    response = requests.get(comic_url, params=payload)
    response.raise_for_status()
    return response.json()['response'][0]['id'], response.json()['response'][0]['owner_id']


def save_comic(vk_access_token, owner_id, photo_id, alt, group_id):
    comic_url = 'https://api.vk.com/method/wall.post'
    payload  = {
      'v' : 5.131,
      'access_token' : vk_access_token,
      'owner_id' : group_id,
      'from_group' : 1,
      'attachments' : f'photo{owner_id}_{photo_id}',
      'message' : alt
    }
    response = requests.get(comic_url, params=payload)
    response.raise_for_status()
    return response.json()


def main():
    comic_alt = get_comic()
    load_dotenv()
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    vk_group_id = os.environ['VK_GROUP_ID']
    upload_url = get_upload_url(vk_access_token)
    photo_hash, params_photo, photo_server = upload_image(upload_url, 'comics.jpeg')
    photo_id, owner_id = save_to_albumn(vk_access_token, params_photo, photo_hash, photo_server)
    save_comic(vk_access_token, owner_id, photo_id, comic_alt, vk_group_id)
    os.remove("comics.jpeg")


if __name__ == "__main__":
    main()