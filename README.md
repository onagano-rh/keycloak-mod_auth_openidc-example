# Keycloak and Apache httpd with mod_auth_openidc Example


## Usage

1. プラグインの配置

[mod_auth_openidc-2.4.15-1.el8.x86_64.rpm](https://github.com/OpenIDC/mod_auth_openidc/releases) をダウンロードし ./httpd/ に置く。
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
  - Redirect URLが http://localhost:8080/app/callback になるようにする(`OIDCRedirectURI`にあわせる)
  - Valid post logout redirect URIsに http://localhost:8080/ を含める(保護されていない場所を指定しループを避ける)
  - 設定ウィザードの通りパブリッククライアントで可。`OIDCPKCEMethod`の設定でPKCEを有効にしている
  - ログアウト用の設定
    - "Front channel logout: Off"
    - "Backchannel logout URL: http://apache/app/callback"
      - Keycloakからはlocalhostでアクセスできないためホスト名はapacheとなる
      - 現状では [このプラグインが提供するログアウトエンドポイント](https://github.com/OpenIDC/mod_auth_openidc/wiki/OpenID-Connect-Session-Management#logout) を動作できていない。[IDトークンを用いて直接end_session_endpointを呼ぶ方法](https://access.redhat.com/documentation/en-us/red_hat_single_sign-on/7.6/html/securing_applications_and_services_guide/oidc#logout) ではログアウトできコールバックも呼べている
- テスト用のユーザを作成

また、ApacheからKeycloakへは内部的なURL http://keycloak:8080 でアクセスできるが、
ブラウザから見えるKeycloakのアドレスは http://localhost:8180 と異なるため、
Frontend URLの設定も必要になる。

- "Realm settings > General > Frontend URL" に "http://localhost:8180" を設定

4. 動作確認

http://localhost:8080/app/aaa 等の /app 以下の任意のURLでアクセスするとdemoレルムへのログインが求められ、
Pythonのhttp.serverが表示するHTTPヘッダーに"OIDC_CLAIM_"で始まるものが含まれることを
確認する。


## 参考

- 書籍 [認証と認可 Keycloak入門](https://www.ric.co.jp/book/new-publication/detail/2081) の第6.3章
- [OpenIDC/mod_auth_openidc](https://github.com/OpenIDC/mod_auth_openidc)
