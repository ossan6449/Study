import os
import csv
import math
import time
import datetime as dt
import xlsxwriter as xw

# 作成するシートの情報
# 1:ソート順,2:作成するシート名,3:非表示フラグ　0:表示(目次に記載しない), 1:表示(目次にも表示), 2:非表示
sheetnames = (
    (1, '表紙', 0),
    (2, '目次',0),
    (3, '１．注意事項',1),
    (4, '２．概略', 1),
    (5, '３．変数一覧', 1),
    (6, '４．カテゴリ一覧', 1),
    (7, '５．カテゴリ統合情報', 1),
    (8, '６．モデル評価', 1),
    (9, '７．ヒストグラム（生データ）', 1),
    (10, '８．ヒストグラム（クレンジング済）', 1),
    (11, '９．デシル分布（生データ）', 1),
    (12, '１０．デシル分布（クレンジング済）', 1),
    (13, '１１．効果指標一覧（正）', 1),
    (14, '１２．効果指標一覧（負）', 1),
    (15, 'グラフ元データ（ヒストグラム（生データ））', 2),
    (16, 'グラフ元データ（ヒストグラム（クレンジング済））', 2),
    (17, 'グラフ元データ（チャート）', 2),
    (18, 'グラフ元データ（デシル分布（生データ））', 2),
    (19, 'グラフ元データ（デシル分布（クレンジング済））', 2)
)

# データファイルと読込先シートの対応情報
# 1:No,2:データファイル名,3:シート名,4:区切り文字,開始位置(行),開始位置(列
datafiles = (
    (1, 'cleansed-header.csv', '３．変数一覧', ','),
    (2, 'histogram_org.csv', 'グラフ元データ（ヒストグラム（生データ））', ','),
    (3, 'histogram.csv', 'グラフ元データ（ヒストグラム（クレンジング済））', ','),
    (4, 'chart.csv', 'グラフ元データ（チャート）', ','),
    (5, 'decimalDistribution_org.csv', 'グラフ元データ（デシル分布（生データ））', ','),
    (6, 'decimalDistribution.csv', 'グラフ元データ（デシル分布（クレンジング済））', ','),
    (7, 'basicInfo.ini', '２．概略', '=')
)

# headFile = "cleansed-header.csv"                      # ヘッダー情報
# histFile_org = "histogram_org.csv"                    # ヒストグラム-生
# histFile = "histogram.csv"                            # ヒストグラム-クレンジング
# chartFile = "chart.csv"                               # チャート
# deciDistFile_org = "decimalDistribution_org.csv"      # デシル分布-生
# deciDistFile = "decimalDistribution.csv"              # デシル分布-クレンジング
# indicatorXmlFile = "modelCategoryIndicator.xml"       #
# integrationRuleFile = "integrationRule-info.csv"      #
# basicInfoFile = "basicInfo.ini"                       #

# ヘッダー情報（変数名）
header =[]

# ヒストグラムグラフ化範囲情報
# データ読込時に取得、グラフ作成時に使用
histOrgDataRanges = [] # ヒストグラム-生データ
histDataRanges = []    # ヒストグラム-クレンジング済みデータ

# チャートデータシートの最終行数を保持する
# データ読込時に取得、グラフ作成時に使用
chartEndRow = None

# デシル分布グラフ化範囲情報
# データ読込時に取得、グラフ作成時に使用
decylOrgDataRanges = [] # デシル分布-生データ
decylDataRanges = []    # デシル分布-クレンジング済みデータ

# 基本情報
basicInfo =[]

#
# WorkBook & WorkSheet作成(xlsx)
#
def createBook(xlsxfile):
    # ファイルの存在チェック
    if os.path.exists(xlsxfile):
        os.remove(xlsxfile)
    book = xw.Workbook(xlsxfile)
    for no, sheetname, flg in sorted(sheetnames):
        # ワークシート追加
        sheet = book.add_worksheet(sheetname)
        # 印刷サイズを A4サイズ に設定
        sheet.set_paper(9)

        # シートの非表示判定
        if flg == 2 :
            sheet.hide()
        else:
            # ヘッダー／フッター作成
            sheet.set_header('&L&7取り扱い注意\n&G',{'image_left': 'bodais.png'})
            sheet.set_footer("&L&7Copyright(c) 2014 i’s FACTORY Co., Ltd.All rights reserved. &R &P / &N")
            # シートを白色に設定 (範囲：A～ZZ) ※シート全体を対象にすると時間がかかるので範囲を限定
            fmt = book.add_format({'bg_color': 'white'})
            sheet.set_column('A:ZZ', 1.50, fmt)

    return book

#
# データの読込(xlsx)
#
def readDataFile(book,datafolder):
    # グローバル変数の使用宣言
    global header               # ヘッダー情報(変数名)
    global histOrgDataRanges    # ヒストグラム(生データ)のグラフ化範囲
    global histDataRanges       # ヒストグラム(クレンジング済み)のグラフ化範囲
    global chartEndRow          # チャートデータの最終行
    global decylOrgDataRanges   # デシル分布-生データ
    global decylDataRanges      # デシル分布-クレンジング済みデータ
    global basicInfo            # 基本情報

    # フォーマット定義
    fmt1 = book.add_format({'num_format':'0.00'})

    # 読込むデータファイルの数だけループする
    for no, datafile, sheetname, delim in sorted(datafiles):
        # データファイルの読込
        f = open( datafolder + datafile,'r',encoding='utf-8')
        # 出力先のシートを開く
        sheet = book.get_worksheet_by_name(sheetname)
        # no:ファイルの区別に使用
        no = int(no)
        # ヘッダーフラグ：初期値=Flase
        headerflg = False
        # i: ヘッダーのカウンタ
        i = 0

        # ヘッダーのデータを読込む
        if no == 1:
            for header in csv.reader(f, delimiter=delim):
                # ヘッダーのデータの"番号"は使用しないので削除
                header.remove('番号')
            # ヘッダー情報を読み終えたら次のループへ
            continue

        # ヒストグラム ／ デシル分布
        if no in (2, 3, 5, 6):
            # 行カウンタ初期化
            rowcnt = 0
            # Whole Answer Ratio フラグ初期化
            warflg = False
            warvalue = None
            # sample_count_group フラグ初期化
            scgflg = False

            # 読込んだデータファイルの行数ループする
            for line in csv.reader(f, delimiter=delim):
                # 列カウンタ初期化
                colcnt = 0
                # カテゴリ名フラグ 初期化
                categoryflg = False

                # デシル分布（生データ) グラフ化範囲取得
                if (no == 5) and ("category_name" in line[1]):
                    decylOrgDataRanges.append([header[i -1],rowcnt + 1, colcnt, rowcnt + 10, len(line) -1])
                # デシル分布（クレンジング済み)　グラフ化範囲取得
                if (no == 6) and ("category_name" in line[1]):
                    decylDataRanges.append([header[i -1],rowcnt + 1, colcnt, rowcnt + 10, len(line) -1])
                # デシル分布　行ごとの合計値を算出
                if no in (5,6):
                    if "sample_count_group" in line[1]:
                        sum = 0;
                        for n in range(2,len(line)):
                            sum += numConv(line[n])
                    else:
                        scgflg = False

                # 読込んだ行の要素数ループする
                for field in line:
                    # フラグと値による処理の分岐
                    if headerflg:
                        # ヒストグラム（生データ) グラフ化範囲取得
                        if no == 2: histOrgDataRanges.append([header[i],rowcnt, colcnt])
                        # ヒストグラム（クレンジング済み)　グラフ化範囲取得
                        if no == 3: histDataRanges.append([header[i],rowcnt, colcnt])
                        # ヘッダーを設定する
                        sheet.write(rowcnt, colcnt, header[i])
                        i += 1
                    # war = whole_answer_ratio
                    elif warflg:
                        # warflgをFalseに戻す
                        warflg = False
                        # whole answer ratioの値を保持する
                        warvalue = numConv(field)
                    elif categoryflg & ((field != '-9999') & (field != '9999')):
                        # ひとつ上の行にwhole answer ratioの値を設定する
                        sheet.write(rowcnt -1, colcnt, warvalue)
                        # カテゴリ列は通常通り設定する
                        sheet.write(rowcnt, colcnt, numConv(field))
                    elif categoryflg & (field == '-9999'):
                        # ひとつ上の行にwhole answer ratioの値を設定する
                        sheet.write(rowcnt -1, colcnt, warvalue)
                        # カテゴリ列の値で'-9999'の場合は欠損値と判断する
                        sheet.write(rowcnt, colcnt,'（欠損）')
                    elif categoryflg & (field == '9999'):
                        # ひとつ上の行にwhole answer ratioの値を設定する
                        sheet.write(rowcnt -1, colcnt, warvalue)
                        # カテゴリ列の値で'9999'の場合はカテゴリ範囲外と判断する
                        sheet.write(rowcnt, colcnt,'（カテゴリ範囲外）')
                    elif scgflg & (colcnt > 1):
                        # '0.00'表示にする
                        sheet.write(rowcnt, colcnt, numConv(field) / sum * 100, fmt1)
                    else:
                        # 数値型と判断できる場合は数値変換する
                        sheet.write(rowcnt, colcnt, numConv(field))

                    # 値による処理の分岐
                    if field  == 'column':
                        # 値が'column'の場合は'変数名'に置換する
                        sheet.write(rowcnt, colcnt, '変数名')
                        # 値が'column'の場合はheaderflg=Trueを設定し、次の処理でヘッダーの値を設定する
                        headerflg = True
                    elif field == 'category_name':
                        # ヒストグラム（生データ) グラフ化範囲取得
                        if no == 2: histOrgDataRanges[i -1].append(len(line) -1)
                        # ヒストグラム（クレンジング済み)　グラフ化範囲取得
                        if no == 3: histDataRanges[i -1].append(len(line) -1)
                        # j: デシル分布　生データ／クレンジング済み用カウンタ  1 to 10
                        if no in (5, 6) : j = 1
                        # 値が'category_name'の場合は'カテゴリ名'に置換する
                        sheet.write(rowcnt, colcnt, 'カテゴリ名')
                        # 値が'categoryflg'の場合、その列のデータはカテゴリ番号、カテゴリ名と判断する
                        categoryflg = True
                    elif "sample_count_group" in field:
                        # sample_count_group01～10 ⇒ [j]
                        sheet.write(rowcnt, colcnt, '[' + str(j) + ']')
                        scgflg = True
                        j += 1
                    elif field == 'sample_count':
                        # 値が'answer_ratio'の場合は'レスポンス率'に置換する
                        sheet.write(rowcnt, colcnt, 'サンプル数')
                    elif field == 'answer_ratio':
                        # 値が'answer_ratio'の場合は'レスポンス率'に置換する
                        sheet.write(rowcnt, colcnt, 'レスポンス率')
                    elif field == 'whole_answer_ratio':
                        # 値が'column'の場合は'平均レスポンス率'に置換する
                        sheet.write(rowcnt, colcnt, '平均レスポンス率')
                        # 値が'whole_answer_ratio'の場合はwarflg=Trueを設定する
                        warflg = True
                    else:
                        headerflg = False
                    colcnt += 1
                rowcnt += 1

        # チャート chart.csv
        elif no == 4 :
            # 行カウンタ初期化
            rowcnt = 0
            # 読込んだデータファイルの行数ループする
            for line in csv.reader(f,delimiter = delim):
                # 列カウンタ初期化
                colcnt = 0
                # 最初のデータ行(ヘッダー部除く）の1列目と2列目を取得
                if rowcnt == 1:
                    x1 = numConv(line[0])
                    y1 = numConv(line[1])

                # 読込んだ行の要素数ループする
                for field in line:
                    # 数値型と判断できる場合は数値変換する
                    sheet.write(rowcnt, colcnt, numConv(field))
                    colcnt += 1
                rowcnt += 1

            # 最後ののデータ行の1列目と2列目を取得
            x2 = numConv(line[0])
            y2 = numConv(line[1])
            responseAvg = numConv(line[2])

            # 下記の計算式はExcelVBAの内容を転用
            A = (y2 - y1) / (x2 - x1)
            B = y1 - A * x1

            # 再度全行分ループする
            f.close()
            f = open(datafolder + datafile, 'r', encoding='utf-8')
            line = None
            # 行カウンタ初期化
            rowcnt = 0
            # 読込んだデータファイルの行数ループする
            for line in csv.reader(f, delimiter=delim):
                # ヘッダーはスキップする
                if rowcnt == 0:
                    rowcnt += 1
                    continue

                # 数値型と判断できる場合は数値変換する
                sheet.write(rowcnt, 6, A * int(line[0]) + B)
                sheet.write(rowcnt, 7, responseAvg)
                rowcnt += 1

            # 最終行数取得（グラフ作成時に使用）
            chartEndRow = rowcnt

            # チャートのデータシートの項目名を設定する
            sheet.write('A1', 'スコア降順位')
            sheet.write('B1', '累積レスポンス率')
            sheet.write('C1', '累積レスポンス率\n(スコア降順位までの平均)')
            sheet.write('D1', 'ID')
            sheet.write('E1', '正解フラグ')
            sheet.write('F1', 'レスポンス率')
            sheet.write('G1', '累積レスポンス率\n(モデル非使用時)')
            sheet.write('H1', '平均レスポンス率')

        # 基本情報の読込み
        elif no  == 7:
            for line in csv.reader(f, delimiter=delim):
                # リストに格納
                basicInfo.append(line)
            # 最初の1行([INFO])を削除
            basicInfo.pop(0)
    f.close
    return

# 文字列型 ⇒ 数値型 型変換処理
# 引数：文字列型
# int型に変換できる値はint型に変換し、float型に変換できる値はfloat型に変換する
# int型にもfloat型にも変換できない値はそのまま返す。
def numConv(s):
    try:
        int(s)
    except:
        try:
            float(s)
        except:
            return(s)
        return float(s)
    return int(s)


#
# データの読込(xlsx)
#
def createSheet(book):
    # 表紙
    createFrontPage(book, sheetnames[0][1])
    # 目次
    createContents(book, sheetnames[1][1])
    # １．注意事項
    createNotes(book, sheetnames[2][1])
    # ２．概略
    createBasicInfo(book, sheetnames[3][1])
    # ３．変数一覧
    createVariableList(book, sheetnames[4][1])
    # ４．カテゴリ一覧
    createCategoryList(book, sheetnames[5][1])
    # ５．カテゴリ統合情報
    createCategoryInfo(book, sheetnames[6][1])
    # ６．モデル評価
    createModelSheet(book, sheetnames[7][1])
    # ７．ヒストグラム（生データ）
    createHistSheet(book,sheetnames[8][1])
    # ８．ヒストグラム（クレンジング済）
    createHistSheet(book, sheetnames[9][1])
    # ９．デシル分布（生データ））
    createDecylSheet(book, sheetnames[10][1])
    # １０．デシル分布（クレンジング済）
    createDecylSheet(book, sheetnames[11][1])
    # １１．効果指標一覧（正）
    createIndicator(book, sheetnames[12][1])
    # １２．効果指標一覧（負）
    createIndicator(book, sheetnames[13][1])

    return


#
# 表紙
#
def createFrontPage(book,sheetname):
    # 該当するシートを取得
    sheet = book.get_worksheet_by_name(sheetname)
    # フォーマット定義
    fmt1 = book.add_format({'font_name': 'Meiryo UI', 'size': 28, 'bold': True, 'align': 'center',
                            'border': None, 'bg_color': 'white', 'valign': 'vcenter'})
    fmt2 = book.add_format({'font_name': 'Meiryo UI', 'size': 24, 'bold': True, 'align': 'vcenter',
                            'border': None, 'bg_color': 'white',
                            'valign': 'center'})
    fmt3 = book.add_format({'font_name': 'Meiryo UI', 'size': 24, 'bold': False, 'align': 'center',
                            'border': None, 'bg_color': 'white', 'valign': 'vcenter'})
    fmt4 = book.add_format({'font_name': 'Meiryo UI', 'size': 18, 'bold': False, 'align': 'center',
                            'border': None, 'bg_color': 'white','valign': 'vcenter'})
    fmt5 = book.add_format({'top': 6, 'bg_color': 'white'})
    fmt6 = book.add_format({'bottom': 6, 'bg_color': 'white'})
    fmt7 = book.add_format({'right': 6, 'bg_color': 'white'})
    fmt8 = book.add_format({'left': 6, 'bg_color': 'white'})
    fmt9 = book.add_format({'top': 6, 'right': 6, 'bg_color': 'white'})
    fmt10 = book.add_format({'top': 6, 'left': 6, 'bg_color': 'white'})
    fmt11 = book.add_format({'bottom': 6, 'right': 6, 'bg_color': 'white'})
    fmt12 = book.add_format({'bottom': 6, 'left': 6, 'bg_color': 'white'})

    sheet.merge_range('C22:AK22', '【bodais解析レポート】',fmt1)
    sheet.merge_range('C25:AK25', '[スコアリング]',fmt2)
    sheet.merge_range('C27:AK27', 'モデル',fmt3)
    sheet.merge_range('C29:AK29', 'Version 1.0',fmt4)
    sheet.merge_range('C31:AK31', dt.date.today().strftime('%Y/%m/%d'),fmt4)

    # Top  Border
    for i in range(2,37):
        sheet.write(16, i, '', fmt5)
    # Top  Border
    for i in range(2,37):
        sheet.write(34, i, '', fmt6)
    # Right Border
    for i in range(18,36):
        sheet.write('AL' + str(i), '', fmt7)
    # Left Border
    for i in range(18,36):
        sheet.write('B' + str(i), '', fmt8)
    # Top Right Border
    sheet.write('AL17', '', fmt9)
    # Top Leftt Border
    sheet.write('B17', '', fmt10)
    # Bottom Right Border
    sheet.write('AL35', '', fmt11)
    # Bottom Left Border
    sheet.write('B35', '', fmt12)

    return


#
# 目次
#
def createContents(book,sheetname):
    sheet = book.get_worksheet_by_name(sheetname)
    fmt1 = book.add_format({'font_name':'Meiryo UI','size': 16,'bold': True, 'bg_color': 'white'})
    fmt2 = book.add_format({'font_name': 'Meiryo UI', 'size':12,'bold': False, 'bg_color': 'white'})
    fmt3 = book.add_format({'font_name': 'Meiryo UI', 'size': 12,'underline':'True','font_color':'blue', 'bg_color': 'white'})

    sheet.write('C2', '目次',fmt1)
    i = 4
    # 目次作成
    for no, sheetname, flg in sorted(sheetnames):
        # 目次に表示するシートのみ処理対象とする
        if flg == 1:
            sheet.merge_range('D' + str(i) + ':' + 'R' + str(i), '', fmt3)
            sheet.write_url('D' + str(i),"internal:'" + sheetname + "'!A1", fmt3, string = sheetname )
            sheet.write('W' + str(i), '・・・・・',fmt2)
            sheet.write('AG' + str(i), 'page表示',fmt2)
            i += 2

    return


#
# １．注意事項
#
def createNotes(book,sheetname):
    sheet = book.get_worksheet_by_name(sheetname)
    fmt1 = book.add_format({'font_name':'Meiryo UI','size': 16,'bold': True, 'bg_color': 'white'})
    fmt2 = book.add_format({'font_name':'Meiryo UI','size': 8,'bold': False, 'bg_color': 'white'})

    sheet.write('B2','注意事項',fmt1)
    sheet.write('B4','・本資料に記載されている内容は本資料発行時点のものであり、予告なく変更することがあります。',fmt2)
    sheet.write('B5', '・本資料に記載された当社製品および技術情報の使用に関連し発生した第三者の特許権、著作権その他の知的財産権の', fmt2)
    sheet.write('B6', '　侵害等に関し、当社は、一切その責任を負いません。当社は、本資料に基づき当社または第三者の特許権、著作権',fmt2)
    sheet.write('B7', '　その他の知的財産権を何ら許諾するものではありません。',fmt2)
    sheet.write('B8', '・本資料を改編など行わず、そのまま複製をする場合には、本資料のフッターに記載されている当社の著作権表示を外さずにご使用ください。',fmt2)
    sheet.write('B9', '・本資料を改編、一部変更、抜粋、他の資料またはデータなど組み合わせなどによる使用の場合には、本資料のフッターに記載されている、',fmt2)
    sheet.write('B10', '　当社の著作権表示を外してご使用ください。',fmt2)
    sheet.write('B11', '・本資料に記載されている情報は、正確を期すために作成したものですが、誤りがないことを保証するものではありません。',fmt2)
    sheet.write('B12', '　万一、本資料に記載されている情報の誤りに起因する損害がお客様に生じた場合においても',fmt2)
    sheet.write('B13', '　当社は、一切その責任を負いません。',fmt2)
    sheet.write('B15', '注 1.本資料において使用されている「当社」とは、株式会社アイズファクトリーをいいます。',fmt2)
    sheet.write('B16', '注 2.このページで使用されている「本資料」とは、bodaisのレポート出力機能を使って作成された、当該エクセルファイルをいいます。',fmt2)
    sheet.write('B18', '※レポート内のグラフの元データは非表示シートとなっています。',fmt2)
    sheet.write('B19', '　 ご利用の際はシートタブを右クリックして頂き、コンテキストメニューから「再表示」を選択することにより閲覧が可能です。',fmt2)

    return


#
# ２．概略
#
def createBasicInfo(book,sheetname):
    # 該当するシートを取得
    sheet = book.get_worksheet_by_name(sheetname)
    # フォーマット定義
    fmt1 = book.add_format({'font_name':'Meiryo UI','size': 12,'bold': True, 'align': 'center',
                            'border': None,'bg_color': 'white','valign': 'vcenter'})
    fmt2 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True, 'align': 'vcenter',
                            'border': 1,'font_color': 'white', 'bg_color': 'green',
                            'valign':'center'})
    fmt3 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True, 'align': 'center',
                            'border': 1,'bg_color': 'white','valign':'vcenter'})
    fmt4 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': False, 'align': 'center',
                            'border': 1,'bg_color': 'white', 'valign':'vcenter'})
    fmt5 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': False, 'align': 'left',
                            'border': 1,'bg_color': 'white', 'valign':'vcenter', 'text_wrap':True})
    fmt6 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': False, 'align': 'center',
                            'border': None,'bg_color': 'white', 'valign':'vcenter'})

    # 概略レポート
    sheet.merge_range('B2:AK2', '概略レポート', fmt1)

    # 基本情報
    sheet.merge_range('B4:AK4', '基本情報', fmt2)
    sheet.merge_range('B5:M5', '会社名', fmt3)
    sheet.merge_range('B6:M6', 'ジョブ名', fmt3)
    sheet.merge_range('B7:M7', 'モデル名', fmt3)
    sheet.merge_range('B8:M8', '担当者', fmt3)
    sheet.merge_range('B9:M9', 'モデル作成日', fmt3)
    sheet.merge_range('N5:AK5', '', fmt4)
    sheet.merge_range('N6:AK6', '', fmt4)
    sheet.merge_range('N7:AK7', '', fmt4)
    sheet.merge_range('N8:AK8', '', fmt4)
    sheet.merge_range('N9:AK9', '', fmt4)

    # 基本データ
    sheet.merge_range('B12:AK12', '基本データ', fmt2)
    sheet.merge_range('B13:M13', 'モデル評価値', fmt3)
    sheet.merge_range('B14:M14', '評価値とは？', fmt3)
    sheet.merge_range('B15:M15', '行数', fmt3)
    sheet.merge_range('B16:M16', '列数', fmt3)
    sheet.merge_range('B17:M17', '備考', fmt3)
    sheet.merge_range('N13:AK13', '', fmt4)
    sheet.merge_range('N14:AK14', '正解が上位に集まっている「良い」ランキングかどうかを数値で評価したものです。'
                                  '1に近いほど「良い」ランキングであるとみなせます。'
                                  '評価値0.7以上が「良い」目安となります。',fmt5)
    sheet.set_row(13,45)
    sheet.merge_range('N15:AK15', '', fmt4)
    sheet.merge_range('N16:AK16', '', fmt4)
    sheet.merge_range('N17:AK17', '', fmt4)

    # 正解へ負の影響のある効果指標 上位10
    sheet.merge_range('B20:AK20', '正解へ正の影響のある効果指標　上位10', fmt2)
    sheet.merge_range('B21:M21', '変数名', fmt3)
    sheet.merge_range('N21:Y21', 'カテゴリ', fmt3)
    sheet.merge_range('Z21:AK21', '効果指標', fmt3)

    for i in range(22,32):
        sheet.merge_range('B' + str(i) + ':M' + str(i), '', fmt4)
        sheet.merge_range('N' + str(i) + ':Y' + str(i), '', fmt4)
        sheet.merge_range('Z' + str(i) + ':AK' + str(i), '', fmt4)

    # 正解へ負の影響のある効果指標 上位10
    sheet.merge_range('B34:AK34', '正解へ負の影響のある効果指標　上位10', fmt2)
    sheet.merge_range('B35:M35', '変数名', fmt3)
    sheet.merge_range('N35:Y35', 'カテゴリ', fmt3)
    sheet.merge_range('Z35:AK35', '効果指標', fmt3)

    for i in range(36,46):
        sheet.merge_range('B' + str(i) + ':M' + str(i), '', fmt4)
        sheet.merge_range('N' + str(i) + ':Y' + str(i), '', fmt4)
        sheet.merge_range('Z' + str(i) + ':AK' + str(i), '', fmt4)

    # 概略レポート
    sheet.merge_range('B47:AK47','※その他の効果指標については「効果指標一覧（正）」と「効果指標一覧（負）」シートをご参照下さい。', fmt6)

    # 基本情報
    global basicInfo
    #基本情報を入力
    for name, value in basicInfo:
        if name == 'job_name':
            sheet.write('N6', value, fmt4)
        elif name == 'model_name' :
            sheet.write('N7', value, fmt4)
        elif name == 'model_complete_dt':
            sheet.write('N9', value.split()[0].replace('-','/'), fmt4)
        elif name == 'model_roc':
            sheet.write('N13', "{:.2}".format(float(value)), fmt4)
        elif name == 'file_row_num':
            sheet.write('N15', str("{:,}".format(int(value))) + '行', fmt4)
        elif name == 'file_column_num':
            sheet.write('N16', value + '列', fmt4)

    return


#
# ３．変数一覧
#
def createVariableList(book,sheetname):
    # ヘッダー情報
    global header
    # 該当するシートを取得
    sheet = book.get_worksheet_by_name(sheetname)
    # フォーマット定義
    fmt1 = book.add_format({'font_name':'Meiryo UI','size': 12,'bold': True, 'align': 'center',
                            'border': None,'bg_color': 'white', 'valign': 'vcenter'})
    fmt2 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True, 'align': 'vcenter',
                            'border': 1,'font_color': 'white', 'bg_color': 'green', 'valign':'center'})
    fmt3 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': False, 'align': 'center',
                            'border': None,'bg_color': 'white', 'valign': 'vcenter',
                            'top': 1, 'left': 1, 'bottom': 1, 'right': 1})

    # 変数一覧
    sheet.merge_range('B2:AK2', '変数一覧', fmt1)
    # 変数一覧
    sheet.merge_range('B4:AK4', '変数一覧', fmt2)

    i = 1
    row = 5
    # 変数の記載
    for header in header:
        # 変数の記載を３列に振り分ける
        if i == 1:
            sheet.merge_range('B' + str(row) + ':' + 'M' + str(row), '', fmt3)
            sheet.merge_range('N' + str(row) + ':' + 'Y' + str(row), '', fmt3)
            sheet.write('B' + str(row) + ':' + 'M' + str(row), header, fmt3)
            sheet.merge_range('Z' + str(row) + ':' + 'AK' + str(row), '', fmt3)
        elif i == 2:
            sheet.write('N' + str(row) + ':' + 'Y' + str(row), header, fmt3)
        elif i == 3:
            sheet.write('Z' + str(row) + ':' + 'AK' + str(row), header, fmt3)

        # カウンタが3になったらリセット
        if i == 3:
            i = 1
            row += 1
        else:
            i += 1

    return


#
# ４．カテゴリ一覧
#
def createCategoryList(book,sheetname):
    # 該当するシートを取得
    sheet = book.get_worksheet_by_name(sheetname)
    # フォーマット定義
    fmt1 = book.add_format({'font_name':'Meiryo UI','size': 12,'bold': True, 'align': 'center',
                            'border': None,'bg_color': 'white', 'valign': 'vcenter'})
    fmt2 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True, 'align': 'vcenter',
                            'border': 1,'font_color': 'white', 'bg_color': 'green','valign':'center'})
    fmt3 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True, 'align': 'center',
                            'border': 1,'bg_color': 'silver', 'valign':'vcenter'})

    # カテゴリ一覧
    sheet.merge_range('B2:AK2', 'カテゴリ一覧', fmt1)
    # カテゴリ一覧
    sheet.merge_range('B4:AK4', 'カテゴリ一覧', fmt2)
    # 変数名
    sheet.merge_range('B5:S5', '変数名', fmt3)
    sheet.merge_range('T5:AK5', 'カテゴリ値', fmt3)

    return

#
# ５．カテゴリ統合情報
#
def createCategoryInfo(book,sheetname):
    # 該当するシートを取得
    sheet = book.get_worksheet_by_name(sheetname)
    # フォーマット定義
    fmt1 = book.add_format({'font_name':'Meiryo UI','size': 12,'bold': True, 'align': 'center',
                            'border': None,'bg_color': 'white', 'valign': 'vcenter'})
    fmt2 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True, 'align': 'vcenter',
                            'border': 1,'font_color': 'white', 'bg_color': 'green',
                            'valign':'center'})
    fmt3 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True, 'align': 'center',
                            'border': 1,'bg_color': 'silver', 'valign':'vcenter'})

    # カテゴリ統合情報
    sheet.merge_range('B2:AK2', 'カテゴリ統合情報', fmt1)
    # カテゴリ統合情報
    sheet.merge_range('B4:AK4', 'カテゴリ統合情報', fmt2)
    # 変数名
    sheet.merge_range('B5:M5', '変数名', fmt3)
    sheet.merge_range('N5:Y5', '統合前カテゴリ', fmt3)
    sheet.merge_range('Z5:AK5', '統合後カテゴリ', fmt3)

    return


#
# ６．モデル評価
#
def createModelSheet(book,sheetname):
    # 該当するシートを取得
    sheet = book.get_worksheet_by_name(sheetname)
    # フォーマット定義
    fmt1 = book.add_format({'font_name':'Meiryo UI','size': 12,'bold': True, 'align': 'center',
                            'border': None,'bg_color': 'white', 'valign': 'vcenter'})
    fmt2 = book.add_format({'font_name':'Meiryo UI','size': 10,'bold': True, 'align': 'vcenter',
                            'border': 1,'font_color': 'white', 'bg_color': 'green', 'valign':'center'})
    fmt3 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True, 'align': 'center',
                            'border': 1,'bg_color': 'white', 'valign':'vcenter'})
    fmt4 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': False, 'align': 'center',
                            'border': 1,'bg_color': 'white', 'valign':'vcenter',
                            'num_format':'#,0.00'})
    fmt5 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': False, 'align': 'left',
                            'border': 1,'bg_color': 'white', 'valign':'vcenter', 'text_wrap':True})
    fmt6 = book.add_format({'font_name':'Meiryo UI','size': 18,'bold': True, 'align': 'vcenter',
                            'border': 1,'font_color': 'white', 'bg_color': 'green', 'valign':'center'})
    # モデル評価
    sheet.merge_range('B2:AK2', 'モデル評価', fmt1)
    # ゲインチャート
    sheet.merge_range('B4:AK4', 'ゲインチャート', fmt6)
    sheet.merge_range('B5:M5', '評価値', fmt3)
    sheet.merge_range('B6:M6', 'ゲインチャートとは？', fmt3)
    sheet.merge_range('N5:AK5','',fmt4)
    sheet.write_formula('N5'," ='" + sheetnames[3][1] + "'!N13:AK13",fmt4)
    sheet.merge_range('N6:AK6','ゲインチャートとは、横軸にスコア降順位、縦軸にスコア降順位までの累積レスポンス数を描いた曲線です。'
                                '予測モデルを使用した場合と、予測モデル未使用の場合の差分がわかります。'
                                '曲線（予測モデル使用）と直線（予測モデル未使用）を比較し、'
                                '膨らみが大きいほうが、より効果的なモデルといえます。', fmt5)
    sheet.set_row(5, 65)
    # レスポンスチャート・スコアチャート
    sheet.merge_range('B28:AK28', 'レスポンスチャート・スコアチャート', fmt2)
    sheet.merge_range('B29:M29', 'レスポンスチャートとは？', fmt3)
    sheet.merge_range('B30:M30', 'スコアチャートとは？', fmt3)
    sheet.merge_range('N29:AK29','レスポンスチャートとは、横軸にスコア降順位、縦軸にスコア降順位までの累積レスポンス率（累積レスポンス数÷アクション数）を描いた曲線です。'
                                   '目標とするレスポンス率を条件とした場合に、どれだけアクションできるかが分かります。'
                                   '（DM配信を例に取ると、図の場合に、目標とするレスポンス率を8%前後とするなら、約10,000通配信が可能といえます）', fmt5)
    sheet.set_row(28, 65)
    sheet.merge_range('N30:AK30','スコアチャートとは、横軸にスコア降順位、縦軸にスコアを描いた曲線です。'
                                   'アクション数を条件として、さらに1回のアクションを行う場合の期待度を表します。'
                                   '（DM配信を例に取ると、図の場合に、10,000通既に配信しているなら、それから1通配信する場合には3.7%のレスポンスが期待できる、といえます）', fmt5)
    sheet.set_row(29, 65)

    return


#
# ７．ヒストグラム（生データ）／ ８．ヒストグラム（クレンジング済）
#
def createHistSheet(book,sheetname):
    # 該当するシートを取得
    sheet = book.get_worksheet_by_name(sheetname)
    # フォーマット定義
    fmt1 = book.add_format({'font_name':'Meiryo UI','size': 12,'bold': True, 'align': 'center',
                            'border': None,'bg_color': 'white', 'valign': 'vcenter'})
    fmt2 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True,'border': 1,'font_color': 'white',
                            'bg_color': 'green','valign':'center'})
    fmt3 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True, 'align': 'center',
                            'border': 1,'bg_color': 'white', 'valign':'vcenter'})
    fmt5 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': False, 'align': 'left',
                            'border': 1,'bg_color': 'white', 'valign':'vcenter', 'text_wrap':True})

    #  ヒストグラム（生データ）／ ヒストグラム（クレンジング済）
    sheet.merge_range('B2:AK2', sheetname.split('．')[1], fmt1)
    # ヒストグラム
    sheet.merge_range('B4:AK4', 'ヒストグラム', fmt2)
    sheet.merge_range('B5:M5', 'ヒストグラムとは？', fmt3)
    sheet.merge_range('N5:AK5','ヒストグラムとは縦軸に度数、横軸に階級をとった統計グラフの一種です。'
                                '棒グラフで度数、折れ線グラフで各項目毎のレスポンス率 を表現しています。'
                                '左の縦軸についている目盛が度数、右側の縦軸についている目盛がレスポンス率を表しています。', fmt5)
    sheet.set_row(4, 60)
    # ヒストグラムインデックス
    sheet.merge_range('AQ7:BN7', 'ヒストグラムインデックス', fmt2)

    return


#
# ９．デシル分布（生データ）／ １０．デシル分布（クレンジング済）
#
def createDecylSheet(book,sheetname):
    # 該当するシートを取得
    sheet = book.get_worksheet_by_name(sheetname)
    # フォーマット定義
    fmt1 = book.add_format({'font_name':'Meiryo UI','size': 12,'bold': True, 'align': 'center',
                            'border': None,'bg_color': 'white', 'valign': 'vcenter'})
    fmt2 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True, 'border': 1,
                            'font_color': 'white', 'bg_color': 'green','align': 'center', 'valign':'center'})
    fmt3 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True, 'align': 'center',
                            'border': 1,'bg_color': 'white', 'valign':'vcenter'})
    fmt5 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': False, 'align': 'left',
                            'border': 1,'bg_color': 'white', 'valign':'vcenter', 'text_wrap':True})

    #  デシル分布（生データ）／ デシル分布（クレンジング済）
    sheet.merge_range('B2:AK2', sheetname.split('．')[1], fmt1)
    # デシル分布
    sheet.merge_range('B4:AK4', 'デシル分布', fmt2)
    sheet.merge_range('B5:M5', 'デシル分布とは？', fmt3)
    sheet.merge_range('N5:AK5','デシル分布とは顧客をスコアの高い順に並べ、10等分し、10のグループに分けた場合の属性分布のことです。'
                                'グラフの目盛りの1が10等分した中で一番スコアの高い集団、10がスコアの一番低い集団を表しています。\n'
                                '※グラフには5%未満の値は表示されていません。', fmt5)
    sheet.set_row(4, 70)
    # ヒストグラムインデックス
    sheet.merge_range('AQ7:BN7', 'デシル分布インデックス', fmt2)

    return


#
# １１．効果指標一覧（正）／ １２．効果指標一覧（負）
#
def createIndicator(book,sheetname):
    # 該当するシートを取得
    sheet = book.get_worksheet_by_name(sheetname)
    # フォーマット定義
    fmt1 = book.add_format({'font_name':'Meiryo UI','size': 12,'bold': True, 'align': 'center',
                            'border': None,'bg_color': 'white', 'valign': 'vcenter'})
    fmt2 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True, 'align': 'vcenter',
                            'border': 1,'font_color': 'white', 'bg_color': 'green', 'valign':'center'})
    fmt3 = book.add_format({'font_name':'Meiryo UI','size': 9,'bold': True, 'align': 'center',
                            'border': 1,'bg_color': 'silver', 'valign':'vcenter'})

    #  効果指標一覧（正）／ 効果指標一覧（負）
    if sheetname == sheetnames[12][1]:
        sheet.merge_range('B2:AK2', '正の影響のある効果指標　一覧', fmt1)
    elif sheetname == sheetnames[13][1]:
        sheet.merge_range('B2:AK2', '負の影響のある効果指標　一覧', fmt1)

    # デシル分布
    sheet.merge_range('B4:AK4', '効果指標一覧', fmt2)
    sheet.merge_range('B5:M5', '変数', fmt3)
    sheet.merge_range('N5:Y5', 'カテゴリ', fmt3)
    sheet.merge_range('Z5:AK5', '効果指標', fmt3)

    return

#
# 各シートのグラフ作成
#
def createGraph(book):

    # ヒストグラムグラフ化範囲情報(生データ)
    global histOrgDataRanges
    # 8行目からチャートを追加
    chartRow = 8
    i = 1
    for  header, startRow, startCol, endCol in histOrgDataRanges:
        # ヒストグラム作成 -７．ヒストグラム（生データ）
        createHistogram(book, sheetnames[14][1], sheetnames[8][1], i, header, startRow, startCol, endCol,chartRow)
        chartRow += 17 # 17行ごとにチャートを追加
        i += 1

    # ヒストグラムグラフ化範囲情報(クレンジング済み)
    global histDataRanges
    # 8行目からチャートを追加
    chartRow = 8
    i = 1
    for header, startRow, startCol, endCol in histDataRanges:
        # ヒストグラム作成 -８．ヒストグラム（クレンジング済）
        createHistogram(book, sheetnames[15][1], sheetnames[9][1], i, header, startRow, startCol, endCol,chartRow)
        chartRow += 17 # 17行ごとにチャートを追加
        i += 1

    # チャートデータ開始行(ヘッダー部除く)
    startRow = 2
    # チャートデータ最終行
    global chartEndRow
    endRow = chartEndRow
    # ゲイン、レスポンス、スコアチャート-６．モデル評価
    createCharts(book, sheetnames[16][1], sheetnames[7][1], startRow, endRow)

    # デシル分布　グラフ化範囲情報(生データ)
    global decylOrgDataRanges
    # 8行目からチャートを追加
    chartRow = 8
    j = 1
    for header, startRow, startCol, endRow, endCol in decylOrgDataRanges:
        # デシル分布（生データ）
        createDecyl(book, sheetnames[17][1], sheetnames[10][1], j, header, startRow, startCol, endRow, endCol,chartRow)
        chartRow += 17 # 17行ごとにチャートを追加
        j += 1

    # デシル分布　グラフ化範囲情報(クレンジング済み)
    global decylDataRanges
    # 8行目からチャートを追加
    chartRow = 8
    j = 1
    for header, startRow,startCol, endRow,endCol in decylDataRanges:
        # デシル分布 （クレンジング済）
        createDecyl(book, sheetnames[18][1], sheetnames[11][1], j, header, startRow, startCol, endRow, endCol,chartRow)
        chartRow += 17 # 17行ごとにチャートを追加
        j += 1

    return


#
# ヒストグラム作成
#
def createHistogram(book,datasheetname, graphsheetname, cnt, header, startrow,startcol,endcol,chartInsRow):
    # 該当するシートを取得
    graphsheet = book.get_worksheet_by_name(graphsheetname)
    # チャート作成
    chart1 = book.add_chart({'type': 'column'})
    chart2 = book.add_chart({'type': 'line'})
    # チャートにデータを追加
    # サンプル数
    chart1.add_series({'name': 'サンプル数','values': ["'" + datasheetname + "'", startrow + 3, startcol, startrow + 3, endcol],
                       'categories': ["'" + datasheetname + "'", startrow + 2, startcol, startrow + 2, endcol],
                       'fill':{'color': '#99CC00'},'gap': 20,
                       'data_labels': {'value': True, 'position':'inside_base','num_format': '#,##0',
                                       'font':{'name':'Meiryo UI'}}})
    # レスポンス率
    chart2.add_series({'y2_axis':'True','name': 'レスポンス率','values': ["'" + datasheetname + "'", startrow + 4, startcol, startrow + 4, endcol],
                       'line':{'color':'#FF9900'},
                       'data_labels': {'value': True,'position':'right','num_format': '0%',
                                        'font': {'name': 'Meiryo UI'}}})
    # 平均レスポンス率
    chart2.add_series({'y2_axis':'True','name': '平均レスポンス率','values': ["'" + datasheetname + "'", startrow + 1, startcol, startrow + 1, endcol],
                       'line':{'color':'#FF0000','dash_type': 'square_dot'},
                       'data_labels': {'value': True, 'position':'above','num_format': '0%',
                                       'font':{'name': 'Meiryo UI','color':'red'}}})
    # ラベル設定
    chart1.set_title({'name': [ "'" + datasheetname + "'", startrow, startcol],'name_font':{'name':'Meiryo UI'}})
    chart1.set_x_axis({'name': 'カテゴリ', 'name_font':{'name':'Meiryo UI'},'line':{'none': True}})
    chart1.set_y_axis({'name': 'サンプル数', 'num_format': '#,##0','name_font':{'name':'Meiryo UI'}})
    chart2.set_y2_axis({'name': 'レスポンス率', 'num_format': '0%','major_unit': 0.1,'name_font':{'name':'Meiryo UI'}})
    # チャート結合
    chart1.combine(chart2)
    # シートにチャートを挿入
    graphsheet.insert_chart('B' + str(chartInsRow), chart1,{'x_scale': 1.2, 'y_scale': 1.0})
    # 凡例を削除
    chart1.set_legend({'none':'True'})
    # プロットエリアの背景色
    chart1.set_plotarea({
        'fill':{'color':'#F3F3F3'}
    })

    # フォーマット定義
    fmt1 = book.add_format({'font_name': 'Meiryo UI', 'size': 11,'underline':'True','align': 'center','font_color':'blue',
                            'top': 1, 'left': 1, 'bottom': 1, 'right': 1, 'bg_color': 'white'})
    fmt2 = book.add_format({'font_name': 'Meiryo UI', 'size': 11,'underline':'True','align': 'center','font_color':'blue'})

    # 変数名とリンクの挿入
    if cnt % 2 == 1:
        graphsheet.merge_range('AQ' + str(math.ceil(cnt / 2)  + 7) + ':' + 'BB' + str(math.ceil(cnt / 2)  + 7), '', fmt1)
        graphsheet.merge_range('BC' + str(math.ceil(cnt / 2)  + 7) + ':' + 'BN' + str(math.ceil(cnt / 2)  + 7), '', fmt1,)
        graphsheet.write_url('AQ' + str(math.ceil(cnt / 2)  + 7), "internal:'" + graphsheetname + "'!A" + str(chartInsRow + 14), fmt1,string = header)
    else:
        graphsheet.write_url('BC' + str(math.ceil(cnt / 2)  + 7), "internal:'" + graphsheetname + "'!A" + str(chartInsRow + 14), fmt1,string = header)

    # リンク「シート最上部へ戻る」を挿入
    if cnt > 3:
        graphsheet.merge_range('AQ' + str(chartInsRow) + ':' + 'BB' + str(chartInsRow), '', fmt2)
        graphsheet.write_url('AQ' + str(chartInsRow), "internal:'" + graphsheetname + "'!A1", fmt2, string = 'シート最上部へ戻る')

    return


#
#   モデル評価のグラフ作成
# （ゲインチャート／レスポンスチャート／スコアチャート）
#
def createCharts(book, datasheetname, graphsheetname, startRow, endRow):
    # 該当するシートを取得
    graphsheet = book.get_worksheet_by_name(graphsheetname)

    # チャート1作成
    chart1 = book.add_chart({'type': 'scatter','subtype': 'smooth'})
    # チャートにデータを追加
    chart1.add_series({'name': '', 'categories': "='" + datasheetname + "'!A" + str(startRow) + ':A' + str(endRow),
                       'values': "='" + datasheetname + "'!B" + str(startRow) + ':B' +  str(endRow),
                       'line':{'color': 'green'},'font':{'name':'Meiryo UI'}})
    chart1.add_series({'name': '', 'categories': "='" + datasheetname + "'!A" + str(startRow) + ':A' + str(endRow),
                       'values': "='" + datasheetname + "'!G" + str(startRow) + ':G' +  str(endRow),
                       'line':{'color': '#C0C0C0'},'font':{'name':'Meiryo UI'}})
    # ラベル設定
    chart1.set_title({'name': 'ゲインチャート','name_font':{'name':'Meiryo UI','size':10}})
    chart1.set_x_axis({'name': 'スコア降順', 'min': 0, 'max':30000, 'major_unit': 5000,
                       'name_font': {'name': 'Meiryo UI', 'size': 10}})
    chart1.set_y_axis({'name': '累積レスポンス数','name_font':{'name':'Meiryo UI','size':10}})
    # シートにチャートを挿入
    graphsheet.insert_chart('B8', chart1,{'x_scale': 1.2, 'y_scale': 1.3, 'x_offset': 5, 'y_offset': 5})
    # 凡例を削除
    chart1.set_legend({'none':'True'})
    # プロットエリアの背景色
    chart1.set_plotarea({
            'layout': {'x': 0.15, 'y': 0.15,'width': 0.8, 'height': 0.7},
            'fill':{'color':'#F3F3F3'}
    })
    # チャート2作成
    chart2 = book.add_chart({'type': 'scatter','subtype': 'smooth'})
    # チャートにデータを追加
    chart2.add_series({'name': '', 'categories': "='" + datasheetname + "'!A" + str(startRow) + ':A' + str(endRow),
                       'values': "='" + datasheetname + "'!C" + str(startRow) + ':C' +  str(endRow),
                       'line':{'color': 'green'},'font':{'name':'Meiryo UI'}})
    chart2.add_series({'name': '', 'categories': "='" + datasheetname + "'!A" + str(startRow) + ':A' + str(endRow),
                       'values': "='" + datasheetname +  "'!H" + str(startRow) + ':H' +  str(endRow),
                       'line':{'color': '#C0C0C0'},'font':{'name':'Meiryo UI'}})
    # ラベル設定
    chart2.set_title({'name': 'レスポンスチャート','name_font':{'name':'Meiryo UI','size':10}})
    chart2.set_x_axis({'name': 'スコア降順', 'min': 0, 'max':30000, 'major_unit': 10000,
                       'name_font': {'name': 'Meiryo UI', 'size': 10}})
    chart2.set_y_axis({'name': '累積レスポンス数', 'num_format': '0%', 'min': 0, 'max':1, 'major_unit': 0.5,
                       'name_font':{'name':'Meiryo UI','size':10}})
    # シートにチャートを挿入
    graphsheet.insert_chart('B33', chart2,{'x_scale': 0.6, 'y_scale': 0.76, 'x_offset': 5, 'y_offset': 5})
    # 凡例を削除
    chart2.set_legend({'none':'True'})
    # プロットエリアの背景色
    chart2.set_plotarea({
            'layout': {'x': 0.2, 'y': 0.2,'width': 0.65, 'height': 0.5},
            'fill':{'color':'#F3F3F3'}
    })
    # チャート3作成
    chart3 = book.add_chart({'type': 'scatter','subtype': 'smooth'})
    # チャートにデータを追加
    chart3.add_series({'name': '', 'categories': "='" + datasheetname + "'!A" + str(startRow) + ':A' + str(endRow),
                       'values': "='" + datasheetname + "'!F" + str(startRow) + ':F' +  str(endRow),
                       'line':{'color': 'green'},'font':{'name':'Meiryo UI'}})
    # ラベル設定
    chart3.set_title({'name': 'スコアチャート','name_font':{'name':'Meiryo UI','size':10}})
    chart3.set_x_axis({'name': 'スコア降順', 'min': 0, 'max':30000, 'major_unit': 10000,
                       'name_font':{'name':'Meiryo UI','size':10}})
    chart3.set_y_axis({'name': 'スコア', 'num_format': '0%', 'min': 0, 'max':1, 'major_unit': 0.5,
                       'name_font':{'name':'Meiryo UI','size':10}})
    # シートにチャートを挿入
    graphsheet.insert_chart('T33', chart3,{'x_scale': 0.6, 'y_scale': 0.76, 'x_offset': 5, 'y_offset': 5})
    # 凡例を削除
    chart3.set_legend({'none':'True'})
    # プロットエリアの背景色
    chart3.set_plotarea({
            'layout': {'x': 0.2, 'y': 0.2,'width': 0.65, 'height': 0.5},
            'fill':{'color':'#F3F3F3'}
    })

    return


#
#   デシル分布　生データ／クレンジング済み
#
def createDecyl(book, datasheetname, graphsheetname, cnt, header, startrow, startcol, endrow, endcol,chartInsRow):
    # 該当するシートを取得
    graphsheet = book.get_worksheet_by_name(graphsheetname)
    # チャート作成
    chart1 = book.add_chart({'type': 'column', 'subtype': 'stacked'})

    # グラフ作成処理
    for i in range(startcol + 1 ,endcol):
        # チャートにデータを追加
        chart1.add_series({'name': ["'" + datasheetname + "'", startrow -1, startcol + 1 + i, startrow -1, startcol + 1 + i],
                           'categories':  ["'" + datasheetname + "'", startrow, startcol + 1, endrow, startcol + 1],
                           'values': ["'" + datasheetname + "'", startrow, startcol + 1 + i, endrow, startcol + 1 + i],
                           'data_labels': {'value': True, 'position':'center','num_format': '#.#0'},
                           'font':{'name':'Meiryo UI'},'gap': 20,})
        # ラベル設定
        chart1.set_title({'name': ["'" + datasheetname + "'", startrow -2 , startcol + 2], 'name_font': {'name': 'Meiryo UI'}})
        chart1.set_y_axis({'name': '構成比', 'num_format': '0_ "%"','min': 0, 'max': 100, 'minor_unit': 10,'major_unit': 50,
                           'name_font':{'name':'Meiryo UI'}})
        chart1.set_x_axis({'name': 'スコア降順グループ番号','name_font':{'name':'Meiryo UI'}})

    # シートにチャートを挿入
    graphsheet.insert_chart('B' + str(chartInsRow), chart1,{'x_scale': 1.2, 'y_scale': 1.0})
    # プロットエリアの背景色
    chart1.set_plotarea({
        'fill':{'color':'#F3F3F3'}
    })

    # フォーマット定義
    fmt1 = book.add_format({'font_name': 'Meiryo UI', 'size': 11,'underline':'True','align': 'center','font_color':'blue',
                            'top': 1, 'left': 1, 'bottom': 1, 'right': 1, 'bg_color': 'white'})
    fmt2 = book.add_format({'font_name': 'Meiryo UI', 'size': 11,'underline':'True','align': 'center','font_color':'blue'})

    # リンクの挿入
    if cnt % 2 == 1:
        graphsheet.merge_range('AQ' + str(math.ceil(cnt / 2)  + 7) + ':' + 'BB' + str(math.ceil(cnt / 2)  + 7), '', fmt1)
        graphsheet.merge_range('BC' + str(math.ceil(cnt / 2)  + 7) + ':' + 'BN' + str(math.ceil(cnt / 2)  + 7), '', fmt1,)
        graphsheet.write_url('AQ' + str(math.ceil(cnt / 2)  + 7), "internal:'" + graphsheetname + "'!A" + str(chartInsRow + 14), fmt1,string = header)
    else:
        graphsheet.write_url('BC' + str(math.ceil(cnt / 2)  + 7), "internal:'" + graphsheetname + "'!A" + str(chartInsRow + 14), fmt1,string = header)

    # リンク「シート最上部へ戻る」を挿入
    if cnt > 3:
        graphsheet.merge_range('AQ' + str(chartInsRow) + ':' + 'BB' + str(chartInsRow), '', fmt2)
        graphsheet.write_url('AQ' + str(chartInsRow), "internal:'" + graphsheetname + "'!A1", fmt2, string = 'シート最上部へ戻る')

    return


if __name__ == '__main__':
    #try:
        # 開始処理
        print(dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        start_time = time.time()

        # 初期値設定
        report = 'Report.xlsx'
        folder = './'

        # WorkBook(xlsx)とSheetを作成
        book = createBook(folder + report)
        # データファイルの読込／加工／書込
        readDataFile(book, folder)
        # 各シートの作り込み
        createSheet(book)
        # 各グラフの作成
        createGraph(book)

    #except Exception as errmsg :
    #    print(errmsg)
    #finally:
        # 出力先Excelを閉じる
        book.close()

        # 終了処理
        print(dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        end_time = time.time()
        execution_time = end_time - start_time
        print(str(round(execution_time,2)) + 'sec')


