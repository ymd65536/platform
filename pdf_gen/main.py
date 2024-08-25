from pdf_lib.create_pdf import create_pdf

if __name__ == "__main__":
    file_name = "./example.pdf"
    create_pdf(file_name)
    print(f"PDF created: {file_name}")

    file = open(f"./{file_name}", 'rb')

    # ファイルの内容を直接読み込む
    pdf_content = file.read()

    # 開いたファイル(f)を閉じる
    file.close()

    # ファイルを読み込んで別のファイルとして保存する
    as_file = open("./output/test.pdf", 'wb')
    as_file.write(pdf_content)
    as_file.close()
