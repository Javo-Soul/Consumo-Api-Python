import modules.request.request as re

def main():
    url = 'https://api.jikan.moe/v4/top/anime'
    try:
        api = re.RequestApi(url)
        response = api.request_anime()
        if response:
            print(response)
        else:
            print("No se recibió respuesta de la API.")
    except Exception as e:
        print(f"Error durante la solicitud a la API: {e}")

if __name__ == '__main__':
    main()

