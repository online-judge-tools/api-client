# Design Doc

link: [DESIGN.md](https://github.com/online-judge-tools/.github/blob/master/DESIGN.md) of [online-judge-tools](https://github.com/online-judge-tools) organization


## Objective

`oj-api` コマンドは、競技プログラミングのためのツールを作成するための API 基盤を提供する。
特にこれを [jmerle/competitive-companion](https://github.com/jmerle/competitive-companion) と共通の JSON 形式で提供する。


## Goals

-   ジャッジサーバとの通信機能を個別のツールから削除し、メンテコストを共通化し低減すること
-   ジャッジサーバとの通信機能を標準化し、ひとつの API ライブラリのメンテが止まっても依存ツールの開発が止まらないようにすること
-   ツール開発者の体験を向上させること


## Non-Goals

-   エンドユーザの体験を直接向上させること
    -   エンドユーザにとって使いやすいものツール開発者にとって使いやすいものは異なる


## Background

TODO: 書く


## Overview

TODO: 書く


## Detailed Design

-   API は JSON で提供する。Python ライブラリとしての提供は避ける。
    -   Python ライブラリは互換性を壊さないために未だ提供されているができれば消していきたい。規模が異なるのでそれほど酷くはないが、構造は[「悪い方が良い」原則と僕の体験談｜Rui Ueyama｜note](https://note.com/ruiu/n/n9948f0cc3ed3) と似ている。

TODO: もうすこし詳しく書く


## Security Considerations

コンテスト中のページの閲覧やコードの提出にはログインが必要である。
この際、ユーザのパスワードあるいはセッション情報が必要となる。
パスワードを平文で保存するのでなく、クッキーとして保持されるセッション情報のみを保存する用にする。
セッション情報のみでも悪用は可能だが、これは一般のブラウザを用いてログインした場合も同様であるため、許容できるだろう。


## Privacy Considerations

特になし。


## Metrics Considerations

難しい。


## Testing Plan

End-to-end tests と中心とし、schedule 機能を用いて定期実行する。
外部の web サービスをスクレイピングして利用するという形態上、本体コードに変化がなくても定期的にツールは動かなくなる。
