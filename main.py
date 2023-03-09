import gspread
import requests
import json
from oauth2client.service_account import ServiceAccountCredentials


page_access_token = ''
page_id = ''
name_credentials = ''
name_google_sheets = ''

# Lấy danh sách bài viết từ fanpage Facebook
url = 'https://graph.facebook.com/v13.0/' + page_id + \
    '/feed?fields=message,full_picture,permalink_url&access_token=' + page_access_token
response = requests.get(url)
data = json.loads(response.text)
posts = data['data']


# Tạo kết nối đến Google Sheets
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    name_credentials, scope)
client = gspread.authorize(creds)
sheet = client.open(name_google_sheets).sheet1

# Ghi thông tin các bài viết vào Google Sheets
row = 1
for post in posts:
    caption = post.get('message', '')
    image_url = post.get('full_picture', '')
    post_url = post.get('permalink_url', '')

    # Tìm giá sản phẩm trong caption
    start_index = caption.find("Giá:")
    end_index = caption.find("k", start_index)

    # Nếu tìm thấy giá sản phẩm trong caption, cắt và copy giá sang cột mới
    price = ''
    if start_index != -1 and end_index != -1:
        price = caption[start_index+4:end_index+1].strip()

    # Ghi thông tin vào Google Sheets
    sheet.update_cell(row, 1, caption)
    sheet.update_cell(row, 2, price)
    sheet.update_cell(row, 3, image_url)
    sheet.update_cell(row, 4, post_url)

    row += 1
