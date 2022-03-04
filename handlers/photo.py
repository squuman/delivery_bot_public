import time


async def save_photo(photo):
    path = f'./storage/{round(time.time() * 10000000)}.jpg'
    await photo.download(path)

    return path
