from icecream import ic
import requests, json

#測試使用requests套件是否可取回傳值: OK

#新增資料 - POST
result_post_users = requests.post('http://127.0.0.1:8000/users',
                 json={'username':'ma3331'})
ic(result_post_users)

result_post_u_table = requests.post('http://127.0.0.1:8000/u_table/',
                 json={
                     'u_name': 'hung03',
                     'u_age': 250,
                     'u_email': 'hung031@gmail.com'
                 })
ic(result_post_u_table)


#查詢資料 - GET
result_get_u_table_all = requests.get('http://127.0.0.1:8000/u_table/')
result_json = result_get_u_table_all.json()
ic(result_get_u_table_all)

#刪除資料 - DELETE
result_delete_u_table = requests.delete('http://127.0.0.1:8000/u_table/14')
ic(result_delete_u_table)

#修改資料 - PUT
edit_json = {
  "u_name": "mark-02",
  "u_age": 199,
  "u_email": "mark-02@mgial.com"
}
result_put_u_table = requests.put(f'http://127.0.0.1:8000/u_table?u_id={3}', json.dumps(edit_json))
ic(result_put_u_table)
print(edit_json) # -> type: dict
print(json.dumps(edit_json)) # -> type: str
print(type(edit_json))

ic(json.dumps(edit_json)[0]) #驗證 : 已轉型成串列

get_air_shop = requests.get('http://127.0.0.1:8000/air_shop_all/').json()
if get_air_shop:
    print('success!!')
    print(get_air_shop)
