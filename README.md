
# Git-Release 

![](https://img.shields.io/badge/Python-3.6-blue?style=flat)
![](https://img.shields.io/badge/License-MIT-green?style=flat)

このパッケージは Git で管理されているプロジェクトから .gitignore されていないファイルのみを別ディレクトリに複製してくれるコマンド `git-release` を追加します。

このパッケージは、自分が RimWorld の MOD を Git で管理したいがために作成しました。
RimWorld はたとえ有効化されていなくても、同じ識別子の MOD があるだけでエラーを吐く事。
SteamWorkshop で公開する際に .gitignore が考慮されない事(当然ですが)。
それにより psd 等の秘匿したいファイルまでもがアップロードされてしまう事。
などがあり、このパッケージを作成しました。

自分は MOD を作成・編集する際に、
Git で管理されたプロジェクトを適当なディレクトリに配置し、
プロジェクトのビルド時に、このコマンドを使用して、プロジェクトを MOD フォルダに複製しています。

このパッケージは自分用に書いたものです。
そのため、最低限の要件さえ満たしてくれればよい、雑多な造りになっています。
回答するのが面倒なのでビルドやコード・仕様等の質問は一切受け付けません。
不具合も致命的なエラーでなければ、修正するつもりはありません。
詳しいひとに聞くか、自己解決を心がけてください。

## Usage

このパッケージをインストール後 `git-release` コマンドが追加されます。
このコマンドは「コピー元」と「コピー先」のふたつの引数を受け取ります。
コマンドの実行後「コピー元」のファイルから `.gitignore` された物を除くファイルが「コピー先」に複製されます。

```shell
git-release RainbowLampSource MOD/RainbowLamp 
```

オプション引数 `--ignore-files` を指定することで、独自の `.gitignore` を指定することもできます。
これによって SteamWorkshop でリリースする場合に秘匿したいファイルを複製しないようにできます。

```shell
git-release RainbowLampSource MOD/RainbowLamp --ignore-files .steamignore
```

コマンド `git-release` はこれらのオプション引数を受け取ります。

| Option | Description | 
| ---- | ---- | 
| --excludes     | 複製対象から排除するファイルの一覧を指定します。 | 
| --includes     | 複製対象に含めるファイルの一覧を指定します。 | 
| --ignore-files | 独自の `.gitignore` を追加します。 | 

## Installation 

```shell
python setup.py install
```

## License 

&copy; 2020 [tikubonn](https://twitter.com/tikubonn).<br>
this released under the [MIT License](LICENSE).
