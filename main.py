import requests
import os
from dotenv import load_dotenv
from random import randint


def download_image(comics_url, file_path):
    response = requests.get(comics_url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def get_comic():
    comic_url = 'https://xkcd.com/info.0.json'
    response = requests.get(comic_url)
    response.raise_for_status()

    current_comic_num = response.json()['num']
    random_number = randint(1, current_comic_num)
    random_comic_url = f'https://xkcd.com/{random_number}/info.0.json'
    response = requests.get(random_comic_url)
    response.raise_for_status()

    comic_response = response.json()
    comic_img = comic_response['img']
    comic_alt = comic_response['alt']
    download_image(comic_img, 'comics.jpeg')
    return comic_alt


def upload_image(url_comic, file_path):
    with open(file_path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url_comic, files=files)
    response.raise_for_status()
    response = response.json()
    check_response(response)
    return response['hash'], response['photo'], response['server']


def get_upload_url(vk_access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload  = {
      'v' : 5.131,
      'access_token' : vk_access_token
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response = response.json()
    check_response(response)
    return response['response']['upload_url']


def save_comic_to_albumn(vk_access_token, photo, photo_hash, photo_server):
    comic_url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload  = {
      'v' : 5.131,
      'access_token' : vk_access_token,
      'server' : photo_server,
      'photo' : photo,
      'hash' : photo_hash
    }
    response = requests.get(comic_url, params=payload)
    response.raise_for_status()
    response = response.json()
    check_response(response)
    return response['response'][0]['id'], response['response'][0]['owner_id']


def publish_comic_to_wall(vk_access_token, owner_id, photo_id, alt, group_id):
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
    response = response.json()
    check_response(response)
    return response


def check_response(response_content):
    if response_content.get('error'):
        raise requests.exceptions.HTTPError


def main():
    comic_alt = get_comic()
    load_dotenv()
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    vk_group_id = os.environ['VK_GROUP_ID']
    try:
        upload_url = get_upload_url(vk_access_token)
        photo_hash, params_photo, photo_server = upload_image(upload_url, 'comics.jpeg')
        photo_id, owner_id = save_comic_to_albumn(vk_access_token, params_photo, photo_hash, photo_server)
        publish_comic_to_wall(vk_access_token, owner_id, photo_id, comic_alt, vk_group_id)
    except requests.exceptions.HTTPError:
        print('Ошибка при запросе к вк')
    finally:
        os.remove("comics.jpeg")


if __name__ == "__main__":
    main()