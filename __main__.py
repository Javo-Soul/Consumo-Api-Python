import modules.request.request as re

def main():
    url = 'https://api.jikan.moe/v4/top/anime'
    api = re.RequestApi(url)
    url = api.request_anime()
    print(url)

if __name__ == '__main__':
    main()

