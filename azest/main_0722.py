import pandas as pd
import psycopg2

# 接続情報
connection_config = {
    'host': '211.1.237.174',
    'port': '5432',
    'database': 'pushdb',
    'user': 'apuser',
    'password': 'apuser2018'
}

# 接続
connection = psycopg2.connect(**connection_config)


# mainスクリプト

# 各月のデータをDataFrame化
data_for_tableau_2019_02 = fetch_month_data(2, 23, 28)
data_for_tableau_2019_03 = fetch_month_data(3, 1, 31)
data_for_tableau_2019_04 = fetch_month_data(4, 1, 30)
data_for_tableau_2019_05 = fetch_month_data(5, 1, 31)
data_for_tableau_2019_06 = fetch_month_data(6, 1, 30)

# 各月のデータをDataFrameを結合
data_for_tableau = pd.concat([data_for_tableau_2019_02, data_for_tableau_2019_03, data_for_tableau_2019_04, data_for_tableau_2019_05, data_for_tableau_2019_06])

# CSVで出力
data_for_tableau.to_csv('人流分析用データ_0722.csv')


#sqlの日付を変数にしてforで回して1ヶ月分のデータに整形する

def fetch_month_data(month, start_day, end_day):

    month = conversion_to_date_format(month)

    for i in range(start_day, end_day + 1):
        
        date = conversion_to_date_format(i)

        # locationsとdevicesを結合するSQL
        sql_locations = "SELECT * FROM locations_2019" + month + date + " LEFT JOIN devices ON locations_2019" + month + date + ".uuid = devices.uuid WHERE devices.push_uuid IS NOT NULL"
        # push_historyとpush_contentsを結合するSQL
        sql_push_history = "SELECT * FROM push_history_2019" + month + date + " INNER JOIN push_contents ON push_history_2019" + month + date + ".push_id = push_contents.push_id WHERE push_history_2019" + month + date + ".language = push_contents.language"


        # DataFrameでロード：locations, devices
        locations = pd.read_sql(sql=sql_locations, con=connection, index_col='id' )

        # DataFrameでロード：push_history,push_contents
        push_history = pd.read_sql(sql=sql_push_history, con=connection )

        # DataFrame：push_history を整形
        push_history = format_push_history(push_history)

        # locations, push_historyを結合させる
        data_for_tableau = pd.merge(locations, push_history, on='push_uuid', how='left')

        # date = start_day の時はそのまま、それ以上の時はDataFrameを結合する
        if i == start_day:
            master_data_for_tableau = data_for_tableau
        else:
            master_data_for_tableau = pd.concat([master_data_for_tableau, data_for_tableau])

    return master_data_for_tableau


# 以下、Util関数
# TODO: 別ファイルに切り分け


def conversion_to_date_format(i):
    if i < 10:
        date = '0' + str(i)
    else:
        date = str(i)

    return date

# push_historyには同一のpush_uuidを持つ人に複数回push配信を行っている
# locationsとmergeする際にこの情報を失わない様にpush_historyのdfを整形する
'''
カラム名：'push_uuid', 'user_language', 'push_id', 'created_at', 'push_id', 'push_language', 'title', 'content', 'url', 'created_at', 'updated_at'

以下のように修正したい
'push_uuid', 'push_history_language', 'title', 'push_id','push_history_created_at_*', 'push_id_*', 'content_*', 'url_*'  ( * = 1,2,..., 10)
'''

def format_push_history(push_history_df):

    # カラム名を修正
    #'push_uuid', 'push_history_language', 'push_history_push_id','push_history_created_at', 'push_contents_push_id', 'push_contents_language', 'title','content', 'url', 'push_contents_created_at','push_contents_updated_at'
    col = push_history_df.columns.values
    col[1]  = 'push_history_language'
    col[2]  = 'push_history_push_id'
    col[3]  = 'push_history_created_at'
    col[4]  = 'push_contents_push_id'
    col[5]  = 'push_contents_language'
    col[9]  = 'push_contents_created_at'
    col[10] = 'push_contents_updated_at'
    push_history_df.columns = col

    # 必要なカラムをリスト化
    push_uuid_list               = push_history_df['push_uuid']
    push_history_created_at_list = push_history_df['push_history_created_at']
    push_id_list                 = push_history_df['push_history_push_id']
    content_list                 = push_history_df['content']
    url_list                     = push_history_df['url']

    # push_uuid, push_history_language, title の　master配列を作成 
    master_push_history = push_history_df.loc[:,['push_uuid','push_history_language', 'title']].drop_duplicates()

    master_push_uuid_list             = master_push_history['push_uuid']
    master_push_history_language_list = master_push_history['push_history_language']
    master_title_list                 = master_push_history['title']


    # push_history_created_at, push_id, content, url の master配列を作成
    master_push_count                      = []
    master_push_history_created_at_list_01 = []
    master_push_id_list_01                 = []
    master_content_list_01                 = []
    master_url_list_01                     = []
    master_push_history_created_at_list_02 = []
    master_push_id_list_02                 = []
    master_content_list_02                 = []
    master_url_list_02                     = []
    master_push_history_created_at_list_03 = []
    master_push_id_list_03                 = []
    master_content_list_03                 = []
    master_url_list_03                     = []
    master_push_history_created_at_list_04 = []
    master_push_id_list_04                 = []
    master_content_list_04                 = []
    master_url_list_04                     = []
    master_push_history_created_at_list_05 = []
    master_push_id_list_05                 = []
    master_content_list_05                 = []
    master_url_list_05                     = []
    master_push_history_created_at_list_06 = []
    master_push_id_list_06                 = []
    master_content_list_06                 = []
    master_url_list_06                     = []
    master_push_history_created_at_list_07 = []
    master_push_id_list_07                 = []
    master_content_list_07                 = []
    master_url_list_07                     = []
    master_push_history_created_at_list_08 = []
    master_push_id_list_08                 = []
    master_content_list_08                 = []
    master_url_list_08                     = []
    master_push_history_created_at_list_09 = []
    master_push_id_list_09                 = []
    master_content_list_09                 = []
    master_url_list_09                     = []
    master_push_history_created_at_list_10 = []
    master_push_id_list_10                 = []
    master_content_list_10                 = []
    master_url_list_10                     = []

    for master_push_uuid in master_push_uuid_list:
        # userごとのpush配信情報を保持しておくための配列を作成・初期化
        user_push_history_created_at = []
        user_push_id_list            = []
        user_content_list            = []
        user_url_list                = []

        for push_uuid, push_history_created_at, push_id, content, url in zip(push_uuid_list, push_history_created_at_list, push_id_list, content_list, url_list):
            if master_push_uuid == push_uuid:
                user_push_history_created_at.append(push_history_created_at)
                user_push_id_list.append(push_id)
                user_content_list.append(content)
                user_url_list.append(url)
        
        master_push_count.append( len(user_push_history_created_at) )

        master_push_history_created_at_list_01 .append( user_push_history_created_at[0] )
        master_push_id_list_01                 .append( user_push_id_list[0] )
        master_content_list_01                 .append( user_content_list[0] )
        master_url_list_01                     .append( user_url_list[0] )
         
        master_push_history_created_at_list_02 .append( user_push_history_created_at[1] if len(user_push_history_created_at) >= 2   else 'NULL' )
        master_push_id_list_02                 .append( user_push_id_list[1]            if len(user_push_id_list)            >= 2   else 'NULL' )
        master_content_list_02                 .append( user_content_list[1]            if len(user_content_list)            >= 2   else 'NULL' )
        master_url_list_02                     .append( user_url_list[1]                if len(user_url_list)                >= 2   else 'NULL' )

        master_push_history_created_at_list_03 .append( user_push_history_created_at[2] if len(user_push_history_created_at) >= 3   else 'NULL' )
        master_push_id_list_03                 .append( user_push_id_list[2]            if len(user_push_id_list)            >= 3   else 'NULL' )
        master_content_list_03                 .append( user_content_list[2]            if len(user_content_list)            >= 3   else 'NULL' )
        master_url_list_03                     .append( user_url_list[2]                if len(user_url_list)                >= 3   else 'NULL' )

        master_push_history_created_at_list_04 .append( user_push_history_created_at[3] if len(user_push_history_created_at) >= 4   else 'NULL' )
        master_push_id_list_04                 .append( user_push_id_list[3]            if len(user_push_id_list)            >= 4   else 'NULL' )
        master_content_list_04                 .append( user_content_list[3]            if len(user_content_list)            >= 4   else 'NULL' )
        master_url_list_04                     .append( user_url_list[3]                if len(user_url_list)                >= 4   else 'NULL' )

        master_push_history_created_at_list_05 .append( user_push_history_created_at[4] if len(user_push_history_created_at) >= 5   else 'NULL' )
        master_push_id_list_05                 .append( user_push_id_list[4]            if len(user_push_id_list)            >= 5   else 'NULL' )
        master_content_list_05                 .append( user_content_list[4]            if len(user_content_list)            >= 5   else 'NULL' )
        master_url_list_05                     .append( user_url_list[4]                if len(user_url_list)                >= 5   else 'NULL' )

        master_push_history_created_at_list_06 .append( user_push_history_created_at[5] if len(user_push_history_created_at) >= 6   else 'NULL' )
        master_push_id_list_06                 .append( user_push_id_list[5]            if len(user_push_id_list)            >= 6   else 'NULL' )
        master_content_list_06                 .append( user_content_list[5]            if len(user_content_list)            >= 6   else 'NULL' )
        master_url_list_06                     .append( user_url_list[5]                if len(user_url_list)                >= 6   else 'NULL' )

        master_push_history_created_at_list_07 .append( user_push_history_created_at[6] if len(user_push_history_created_at) >= 7   else 'NULL' )
        master_push_id_list_07                 .append( user_push_id_list[6]            if len(user_push_id_list)            >= 7   else 'NULL' )
        master_content_list_07                 .append( user_content_list[6]            if len(user_content_list)            >= 7   else 'NULL' )
        master_url_list_07                     .append( user_url_list[6]                if len(user_url_list)                >= 7   else 'NULL' )

        master_push_history_created_at_list_08 .append( user_push_history_created_at[7] if len(user_push_history_created_at) >= 8   else 'NULL' )
        master_push_id_list_08                 .append( user_push_id_list[7]            if len(user_push_id_list)            >= 8   else 'NULL' )
        master_content_list_08                 .append( user_content_list[7]            if len(user_content_list)            >= 8   else 'NULL' )
        master_url_list_08                     .append( user_url_list[7]                if len(user_url_list)                >= 8   else 'NULL' )

        master_push_history_created_at_list_09 .append( user_push_history_created_at[8] if len(user_push_history_created_at) >= 9   else 'NULL' )
        master_push_id_list_09                 .append( user_push_id_list[8]            if len(user_push_id_list)            >= 9   else 'NULL' )
        master_content_list_09                 .append( user_content_list[8]            if len(user_content_list)            >= 9   else 'NULL' )
        master_url_list_09                     .append( user_url_list[8]                if len(user_url_list)                >= 9   else 'NULL' )

        master_push_history_created_at_list_10 .append( user_push_history_created_at[9] if len(user_push_history_created_at) >= 10  else 'NULL' )
        master_push_id_list_10                 .append( user_push_id_list[9]            if len(user_push_id_list)            >= 10  else 'NULL' )
        master_content_list_10                 .append( user_content_list[9]            if len(user_content_list)            >= 10  else 'NULL' )
        master_url_list_10                     .append( user_url_list[9]                if len(user_url_list)                >= 10  else 'NULL' )
    

    master = pd.DataFrame(
            data={
                'push_uuid'                  : master_push_uuid_list,
                'push_history_language'      : master_push_history_language_list,
                'title'                      : master_title_list,
                'push_count'                 : master_push_count,
                'push_history_created_at_01' : master_push_history_created_at_list_01,
                'push_id_01'                 : master_push_id_list_01,
                'content_01'                 : master_content_list_01,
                'url_01'                     : master_url_list_01,
                'push_history_created_at_02' : master_push_history_created_at_list_02,
                'push_id_02'                 : master_push_id_list_02,
                'content_02'                 : master_content_list_02,
                'url_02'                     : master_url_list_02,
                'push_history_created_at_03' : master_push_history_created_at_list_03,
                'push_id_03'                 : master_push_id_list_03,
                'content_03'                 : master_content_list_03,
                'url_03'                     : master_url_list_03,
                'push_history_created_at_04' : master_push_history_created_at_list_04,
                'push_id_04'                 : master_push_id_list_04,
                'content_04'                 : master_content_list_04,
                'url_04'                     : master_url_list_04,
                'push_history_created_at_05' : master_push_history_created_at_list_05,
                'push_id_05'                 : master_push_id_list_05,
                'content_05'                 : master_content_list_05,
                'url_05'                     : master_url_list_05,
                'push_history_created_at_06' : master_push_history_created_at_list_06,
                'push_id_06'                 : master_push_id_list_06,
                'content_06'                 : master_content_list_06,
                'url_06'                     : master_url_list_06,
                'push_history_created_at_07' : master_push_history_created_at_list_07,
                'push_id_07'                 : master_push_id_list_07,
                'content_07'                 : master_content_list_07,
                'url_07'                     : master_url_list_07,
                'push_history_created_at_08' : master_push_history_created_at_list_08,
                'push_id_08'                 : master_push_id_list_08,
                'content_08'                 : master_content_list_08,
                'url_08'                     : master_url_list_08,
                'push_history_created_at_09' : master_push_history_created_at_list_09,
                'push_id_09'                 : master_push_id_list_09,
                'content_09'                 : master_content_list_09,
                'url_09'                     : master_url_list_09,
                'push_history_created_at_10' : master_push_history_created_at_list_10,
                'push_id_10'                 : master_push_id_list_10,
                'content_10'                 : master_content_list_10,
                'url_10'                     : master_url_list_10
            },
            columns=['push_uuid', 'push_history_language', 'title','push_count',
                     'push_history_created_at_01', 'push_id_01', 'content_01', 'url_01', 
                     'push_history_created_at_02', 'push_id_02', 'content_02', 'url_02', 
                     'push_history_created_at_03', 'push_id_03', 'content_03', 'url_03', 
                     'push_history_created_at_04', 'push_id_04', 'content_04', 'url_04',
                     'push_history_created_at_05', 'push_id_05', 'content_05', 'url_05',
                     'push_history_created_at_06', 'push_id_06', 'content_06', 'url_06',
                     'push_history_created_at_07', 'push_id_07', 'content_07', 'url_07',
                     'push_history_created_at_08', 'push_id_08', 'content_08', 'url_08',
                     'push_history_created_at_09', 'push_id_09', 'content_09', 'url_09',
                     'push_history_created_at_10', 'push_id_10', 'content_10', 'url_10'
                    ]
        )
        
    return master