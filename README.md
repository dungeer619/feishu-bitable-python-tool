# feishu-bitable-python-sdk
通过Python与飞书多维表格实现读删写等交互. Using Python to interact with Feishu Bitable

涉及到的包  
```
requests  
retry  
json
```

通过飞书应用获取authentication token
```
authen_token_paras = {
    "authen_token_url": authen_token_url,
    "authen_token_post_data": {"app_id": app_id,
                                 "app_secret": app_secret},
    "authen_token_name": authen_token_name
}
```

