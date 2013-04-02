使用方法
1.build.cfgをプロジェクトフォルダに作成し、必要に応じて以下の項目を記述する
※1項目1行
必須項目
    1.ファイル先頭に"[pj]"と記述する。
    2.ソースコードの入ったディレクトリを"src="に続けて記述する。(注1,2,3,4)
    3."version="に続けて、Modのバージョンを記述する。
任意事項
    4.リソースが納めてあるディレクトリがあれば"res="に続けて記述する。(注1,2,3,4)
    5.そのMODのビルドにAPIが必要なら必要なAPIの名前を"api="に続けて記述する。(注1,2,5)
    6.そのMODをAPIとして出力したければ出力したいAPIの名前を"capif="に続けて記述する。(注1,6)
    7.ソースコード及びリソースファイルの中で書き換えたい文字列があれば、"rep="に続けて記述する。(注7)
    8.出力ファイル名及び場所を指定したければ"out="に続けて記述する。(注1,3,9)
    9.reobfuscate_srgと同等の出力ファイルが欲しい場合は、"srg=True"と記述する。
    10.(非推奨)Minecraftのバージョンを手動で指定したければ"mcv="に続けて記述する。(注8)
注
    1.ディレクトリの分割文字は"/"である
        ex)"dir"フォルダ内の"ff"フォルダを指定する場合は、"dir/ff"
    2.複数の項目を指定する際は":"で区切る(=Windowsだと絶対パスの指定は不可能)
        ex)"a"フォルダと"b"フォルダと"c/d"フォルダを指定する場合は、"a:b:c/d"
    3.プロジェクトフォルダからの相対パスで指定する
        ex)"プロジェクトフォルダ/a/b/c"は、"a/b/c"
    4.末尾に"/"がある場合は、そのフォルダの中身をコピーする。ない場合はそのフォルダごとコピーする
        ex)"src"と指定した場合、宛先フォルダに"src"フォルダが生成される。
        ex)"src/"と指定した場合、宛先フォルダ直下に、"src"の中身がコピーされる。
    5.任意事項6で指定した名前に一致させる
        ex)"capif=TestCraft"と指定して出力したAPIを使いたければ、"api=TestCraft"と指定する。
    6.自動で必要な場所に保存されるので、自分でコピーしたりしなくてよい
        ex)"capif=TestCraft"と指定して一度Buildすれば別のプロジェクトからAPIとして使用出来る。
    7.各項目は"|"で分割し、変換前と変換後の文字列は"="で区切る
        ex)"@TEST@"を"flower"に、"#TEST#"を"rose"に変換したければ、"@TEST@=flower|#TEST#=rose"と指定する。
    8.eclipseのプロジェクトをセットアップする際に自動で入力されるので、手動での設定は非推奨
        ex)update eclipse project fileを実行すれば、自動でmcvのオプションの内容が指定される。
    9.デフォルトでは、"プロジェクトフォルダ/dist/(Minecraftのバージョン)/(プロジェクト名)-(MODのバージョン).zip"に出力される。
なお、どの項目も余分なスペースが入っているとエラーが出るため注意すること。
2.当リポジトリの中身を、プロジェクトフォルダの1つ上(ワークスペースフォルダ)に全て(SampleProjectと.gitとreadme類を除く)コピーする。
3.boot.batかboot.shを起動する。
4.初回起動時は自動でforgeのインストールが始まるため、指示に従ってMinecraftとForgeのバージョンを指定する。
5.(初回起動時はForgeインストールが終わり次第)メニューが表示されるため、行いたいことを選ぶ。
    '0. exit'
        スクリプトを終了する
    '1. build project (an project chosen by user) *current minecraft version is unavailable'
        次の画面で選択した1つのプロジェクトをビルドする。(項目の後に出てるMinecraftのバージョンは無効(build.cfgに記述されたバージョンが使用される))
    '2. update eclipse project file (all projects)'
        build.cfgが存在するプロジェクトフォルダ全てに、現在選択中のバージョンのForgeに合わせたeclipseプロジェクトをインストールする。
    '3. update eclipse project file (some projects chosen by user)'
        build.cfgが存在するプロジェクトフォルダの中で、ユーザーが選んだ複数のフォルダに現在選択中のバージョンのForgeに合わせたeclipseプロジェクトをインストールする。
    '4. update eclipse project file (an project chosen by user)'
        build.cfgが存在するプロジェクトフォルダの中で、ユーザーが選んだ1つのフォルダに現在選択中のバージョンのForgeに合わせたeclipseプロジェクトをインストールする。
    '5. install new minecraft forge'
        新しくForgeをインストールする。(1つのMinecraftのバージョンに対して1つのForgeしか存在できない。そのため、すでにあるMinecraftのバージョンを選択すると、上書きされる。)
    '6. change minecraft version'
        現在選択中のMinecraftバージョンを変更する。
6.基本的に選択画面では、先に候補が出るのでその中から該当するものを選択していく。