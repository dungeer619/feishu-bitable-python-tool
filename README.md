# feishu-bitable-python-sdk
通过Python与飞书多维表格实现读删写等交互. Using Python to interact with Feishu Bitable

涉及到的包  
```
pandas
requests  
retry  
json
```

获取应用身份访问凭证authentication token，详见参考文档，
其中authen_token_name取值如"tenant_access_token"  
参考文档：<font size="0.5">https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/g</font>
```
authen_token_paras = {
    "authen_token_url": authen_token_url,
    "authen_token_post_data": {"app_id": app_id,
                                 "app_secret": app_secret},
    "authen_token_name": authen_token_name
}
```

## 总函数概览
**参数说明**  
app_token 和 table_id 为飞书多维表格标识  
参考文档：<font size="0.5">https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/bitable-overview</font>  
  
&nbsp;

### 1. 读取记录 get_records_from_bitable
```
readin_df = get_records_from_feishu(app_token, table_id, authen_token_paras)
```
功能：将指定多维表格具体table_id对应的表格数据读入python，以pandas.DataFrame的形式存储  

  
调用API参考文档：  
<font size="0.5">https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/list</font>  
  
&nbsp;

### 2. 清空记录 delete_records_of_bitable_per500
```
delete_records_of_feishu_per500(app_token, table_id, authen_token_paras)
```
功能：目前飞书提供的API是以每次最多500条的效率进行删除的，调用该函数可将多维表格指定table_id的具体表格的数据清空  


调用API参考文档：  
<font size="0.5">https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/list</font>  
<font size="0.5">https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/delete</font>
  
&nbsp;

### 3. 新增记录 write_to_bitable_per500
```
write_to_feishu_per500(data_frame, app_token, table_id, authen_token_paras)
```
功能：目前飞书提供的API是以每次最多500条的效率进行写入的，调用该函数可将data_frame的内容写入指定多维表格指定table_id的具体表格  


调用API参考文档：  
<font size="0.5">https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/create</font>

&nbsp;

## 函数详细说明  
**理解说明**  
详细函数主要为单次进行读、删、写等操作的函数，为总函数提供能够循环调用的内容。  

&nbsp;
### 1. 读取记录 get_records_from_bitable  
调用API参考文档：  
<font size="0.5">https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/list</font>  
### 1.1 read_from_bitable   
```
read_from_bitable(app_token, table_id, authen_token_paras)
```  
功能：调用飞书API做单次读入，目前飞书开放的读取效率是500行/次。  
返回结果类型：http response  

&nbsp;
### 1.2 read_from_bitable_by_page   
```
read_from_bitable_by_page(page_token, app_token, table_id, authen_token_paras)
```  
功能：对飞书多维表格按页读取  
参数说明：  
&#8195;&#8195;page_token:  分页标记，详见调用API参考文档  
功能详细说明:  
&#8195;&#8195;由于目前飞书多维表格读取效率为500条/次，所以多维表格允许按页读取，按页读取需要持有上一页的 page_token \(详见调用API参考文档\)，所以为了能够完整读取多维表格数据，设计本函数按页读取记录。  
返回结果类型：http response  

&nbsp;
### 1.3 get_records_from_bitable
```
result_df = get_records_from_bitable(app_token, table_id, authen_token_paras)
```
功能：调用函数1.1，函数1.2，来对 app_token 和 table_id 识别的具体的一个多维表格表单进行完整读取    
功能详细说明:  
&#8195;&#8195;调用一次函数1.1，获取到该表单总行数`totalNum`，创建DataFrame `readin_df`存储第一次读取的记录。通过`totalNum`来判断需要进行读取操作的循环次数，然后循环调用函数1.2，对读取到的结果与第一次读取创建的DataFrame进行拼接，以最终形成记录数完整的读取结果。  
返回结果类型：pandas.DataFrame

&nbsp;  
### 2. 清空记录 delete_records_of_bitable_per500  
调用API参考文档：  
<font size="0.5">https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/list</font>  
<font size="0.5">https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/delete</font>  

### 2.1 get_records_to_del
```
get_records_to_del(read_response)
```
功能：对于读操作返回的http response `read_response`，从中分离出每一条记录的 record_id 并进行拼接，返回`read_response`中包含的 record_id，返回类型为list.  
参数说明：  
&#8195;&#8195;read_response：调用一次函数1.1返回的结果    
返回结果类型：list  

&nbsp;
### 2.2 delete_records_of_bitable
```
delete_records_of_bitable(app_token, table_id, records_to_del, authen_token_paras)
```
功能：调用飞书API做单次删除，目前飞书开放的删除效率为500条/次  
参数说明：  
&#8195;&#8195;records_to_del：调用一次函数2.1返回的结果    

&nbsp;
### 2.3 delete_records_of_bitable_per500
```
delete_records_of_bitable_per500(app_token, table_id, authen_token_paras)
```
功能：循环调用函数2.2直至调用函数1.1获取到的当前表单总记录为空，也就意味着将该表单完整删除  

&nbsp;  
### 3. 新增记录 write_to_bitable_per500  
调用API参考文档：  
<font size="0.5">https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/create</font>  

### 3.1 write_to_bitable
```
write_to_bitable(app_token, table_id, data_json_str, authen_token_paras)
```
功能：调用飞书API做单次写入，目前飞书开放的读取效率是500行/次，返回写入结果的 http response  
参数说明：  
&#8195;&#8195;data_json_str: 内容为json格式的字符串，存储要写入的内容    
返回结果类型：http response  

&nbsp;  
### 3.2 write_to_bitable_per500
```
write_to_bitable_per500(data_frame, app_token, table_id, authen_token_paras)
```
功能：循环调用函数3.1，来对 app_token 和 table_id 识别的具体的一个多维表格表单进行完整写入    
注意：使用本函数的前提是，写入的多维表格其表头已经建立好，也就是说字段名称和字段类型已经声明好，且即将写入数据的字段与其保持一致
参数说明：  
&#8195;&#8195;data_frame: 要写入的内容，类型为 pandas.DataFrame    
功能详细说明:  
&#8195;&#8195;获取`data_frame`的行数计算需要循环写入的循环次数，通过循环调用写入函数，对`data_frame`内容分次写入目标多维表格具体表单。  
