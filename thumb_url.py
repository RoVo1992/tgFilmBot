from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
import pprint
from config import gd_folder_id

pp = pprint.PrettyPrinter(indent=4)
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_INFO = {'type': 'service_account', 'project_id': 'eloquent-grail-285018', 'private_key_id': 'b08b385eb51199f3bb089b442f7f640013dbc125', 'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQD0YfRiBrZNAuOq\nma4vlJ+BALJ5ZZOk7NBh6ASKerscCUMpvDoacG7vOwlhuL0+dp/dalS2Y3SYPYaq\neAtaEYFQOFhWrE9YbySbQLB3Mb7QZQuYp4WhMpu97WlcqdfCtv9P3fYzv9verUQN\nfxaAPTXExjWc9Z5wnA+rPuVYOEk1r7ZnKVo5btDMuHAWfEHi7PvFqbCwT3Qyg/S6\nBaza4Q8g+0Ovj8qnilOA+t/a/0H6PwIUYff3RmpSEERCJkltaLOT48HVsfpJRVFo\nO8eP4RmA2zgtom34YC8t+Au1FZV9E8fqVHn1ROWr1fT4LDGLVw5mr7LCQldMxZIE\n3DQlOOkrAgMBAAECggEABVw+rYXDKuZE0yGi0fVbGEvJHmONfQEawwMBUn5Fq2RC\nnmA8EAdmT4YGeye/suaMNCGYcRW2YX57/TI74YJfyUArI9+Mr/5kGamuFTc4nb6R\npgwKoNII234hIQCytFkqOXi/ZTwwmO5I/1jJyA9PphzI4UP78TFjIJj1E93MMUq5\n5wAcpuDxOBqx+TGlvJAhJg4OxZeewETh2dhYRwm0uOlko+jvVIAyBMCK6p2+QW/a\nZhKkodjy3nH2v39LtLxqjte9cSHmdwRO028BHOx5/xAF8pnE5JCGIep2D6886srK\nDq6H3ndU6g6SFbZfjU11nrsPIJITKEIHn1DzQhPqbQKBgQD6Q1CDBk096GR5jmxH\nh02xPrZocp7+pqQIhnTlej9WwobzSMf7kiWJAirIS9JVodYqqJvCrrqwoEaGzJp4\no4DGCuI0obU8Z0SvGjNPrZh0kMImGm8ClrmtdNWWS5QQQxXe9lvVUxXIo1o0rADp\nxRx/U+qHHns8xAdlB1e44qZ4FwKBgQD5/CGP4Kj90yhoK7PrXHKNuN3xTs4MrENG\nGEiK8BVuLL9eU80FDi05c/BLteGGtvRQFo1cpGycVDuuavEzLRQhT/cVMfemH3uh\njKku+FnBPypBEWGiWdRUO5EOAbeNPC5gXY+m3DRjZbbwmQVjyq3Lf/6g+djIYHY/\n++bcfZOwDQKBgQCiEEVrFAGhPYUTUq+8AlrFlR76tH9R2QgQnUHF+UxbGs3ZbiBT\nQWkdOFIMM02aNptCNL3pbM1o4+HIGWdPCFKz7QhfnPiIjTdlTUo9JuW7VqLjmeqZ\nepHzSd2m3nqbrVXUdSUzGALbUy1vPpO4zvSNYAJYTdzwlOFVA1RDXkL/MQKBgQCr\ngtT0Bctr+ofqkLFsdY0StxdvDAZKo5W0bcy3pmjNol3Ztd0f7s4QcP8Ysrz81GFi\n4VYzjYwG5bPcwvqhhfgdsuNu401p6IfGGt+onjPWZiPzaJ136fHHqOaomXz5paSb\n8RUyAjrfR1XwVMxh3xjGWha1EzYspCH9XDLUbEP7sQKBgQC2VhmWqLFbwfyXiDqR\nSfzvuBFZMZzqE/Frag0EUzrSQGSMbIniE0mucaMvJjAKO0Yz/ldNY0tGszzTszCl\ny/X6L6lqkzbQ/xpvmWEPBqO0gKb5r4zyJDyulcaOovZKGfeMH85XF+MOcEBp9iHo\ng7sEtYYPolzsaWpZ+DERyqGC7Q==\n-----END PRIVATE KEY-----\n', 'client_email': '481390355996-compute@developer.gserviceaccount.com', 'client_id': '112667296822991894657', 'auth_uri': 'https://accounts.google.com/o/oauth2/auth', 'token_uri': 'https://oauth2.googleapis.com/token', 'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs', 'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/481390355996-compute%40developer.gserviceaccount.com'}

credentials = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_INFO, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

folder_id = gd_folder_id


def get_thumb_url(name: str = None) -> 'str':

    results = service.files().list(pageSize=100,
                                   fields="nextPageToken, files( thumbnailLink, name)").execute()
    return [film['thumbnailLink'] for film in results['files'] if film['name'] == name+'_thumb.JPEG'][0]


def push_thumb(name: str):
    file_name = name+'_thumb.JPEG'
    file_path = 'photo/'+name+'_thumb.JPEG'
    file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }
    media = MediaFileUpload(file_path, resumable=True)
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()
print(get_thumb_url('Нефть'))