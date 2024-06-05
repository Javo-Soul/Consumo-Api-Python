import request.request as re


def main():
    url = 'https://api.jikan.moe/v4/top/anime'
    api = re.requestApi(url)
    url = api.requestAnime()
    print(url)

if __name__ == '__main__':
    main()

