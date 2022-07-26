# feishu-bitable-python-sdk
通过Python与飞书多维表格实现读删写等交互. Using Python to interact with Feishu Bitable

涉及到的包  
```
pandas
requests  
retry  
json
```

获取应用身份访问凭证authentication token
参考文档：https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/g
```
authen_token_paras = {
    "authen_token_url": authen_token_url,
    "authen_token_post_data": {"app_id": app_id,
                                 "app_secret": app_secret},
    "authen_token_name": authen_token_name
}
```

## 函数汇总说明
**参数说明**  
app_token和table_id为飞书多维表格标识  
参考文档：https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/bitable-overview  

### 1. 读取记录 get_records_from_feishu
```
readin_df = get_records_from_feishu(app_token, table_id, authen_token_paras)
```
功能：将指定多维表格具体table_id对应的表格数据读入python，以pandas.DataFrame的形式存储  

调用API参考文档：  
https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/list  



### 2. 清空记录 delete_records_of_feishu_per500
```
delete_records_of_feishu_per500(app_token, table_id, authen_token_paras)
```
功能：目前飞书提供的API是以每次最多500条的效率进行删除的，调用该函数可将多维表格指定table_id的具体表格的数据清空  

调用API参考文档：  
https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/list  
https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/delete
  
  
  
### 3. 新增记录 write_to_feishu_per500
```
write_to_feishu_per500(data_frame, app_token, table_id, authen_token_paras)
```
功能：目前飞书提供的API是以每次最多500条的效率进行写入的，调用该函数可将data_frame的内容写入指定多维表格指定table_id的具体表格  

调用API参考文档：  
https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/create
