# Keycloak and Apache httpd with mod_auth_openidc Example


## Usage

1. プラグインの配置

[mod_auth_openidc-2.4.14.4-1.el8.x86_64.rpm](https://github.com/OpenIDC/mod_auth_openidc/releases) をダウンロードし ./httpd/ に置く。
バージョンが異なる場合は適宜 ./httpd/Dockerfile も変更すること。

2. イメージのビルドと実行

```shell
docker-compose up # Or `podman compose up`
```
Podoman で代替する場合でも `docker-compose`　コマンドは入れておき、
`podman`　コマンドから `docker` コマンドへのエイリアスを作成しておく。
通常はパッケージを入れるだけでよいはず（`dnf install docker-compose podman-docker`）。
`docker` コマンドそのもの（moby-engineパッケージ）は必要ない。

3. 設定

以下のURLで3つのサーバにアクセスできる。

- Keycloak: http://localhost:8180/
- Apache httpd: http://localhost:8080/
- Python http.server: http://localhost:18080 (直接アクセス)
  - http://localhost:8080/app (プロキシ経由のアクセス)

Keycloakの管理画面に admin/password でログインし以下の設定を行う。

- demo レルムを作成
- reverse-proxy-app クライアントを登録
  - Redirect URLが http://localhost:8080/app/* になるようにする
  - コンフィデンシャルクライアントとして登録し、シークレットをメモして ./httpd/my-proxy.conf を編集しておく
    - `docker-compose restart apache` で再起動が必要
    - パブリッククライアントでPKCEを使えるかどうかは未確認
- テスト用のユーザを作成

また、ApacheからKeycloakへは内部的なURL http://keycloak:8080 でアクセスできるが、
ブラウザから見えるKeycloakのアドレスは http://localhost:8180 と異なるため、
Frontend URLの設定も必要になる。

- "Realm settings > General > Frontend URL" に "http://localhost:8180" を設定

4. 動作確認

http://localhost:8080/app/ 以下の任意のURLでアクセスするとdemoレルムへのログインが求められ、
Pythonのhttp.serverが表示するHTTPヘッダーに"OIDC_CLAIM_"で始まるものが含まれることを
確認する。


## 参考

- 書籍 [認証と認可 Keycloak入門](https://www.ric.co.jp/book/new-publication/detail/2081) の第6.3章
- [OpenIDC/mod_auth_openidc](https://github.com/OpenIDC/mod_auth_openidc)