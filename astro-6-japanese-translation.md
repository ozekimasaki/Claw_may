# Astro 6.0 リリース

Astro 6 が登場しました！Astro 6 では、組み込みの Fonts API、Content Security Policy API、そして統一された Astro コンテンツレイヤーを通じて外部ホストされたコンテンツと連携する Live Content Collections など、幅広い新機能が導入されています。

これらの新機能に加えて、Astro 開発サーバーとビルドパイプラインの大部分を大規模にリファクタリングしました。Vite の新しい Environment API により、Astro は開発中に本番環境とまったく同じランタイムを実行できるようになりました。つまり、「開発では動くのに、本番で壊れる」という驚きが減ります。特に、Cloudflare Workers、Bun、Deno などの非 Node.js ランタイムで顕著です。

## リリースハイライト

- [再設計された astro dev](#再設計された-astro-dev)
- [Cloudflare サポートの改善](#再設計された-astro-dev)
- [組み込み Fonts API](#組み込み-fonts-api)
- [Live Content Collections](#live-content-collections)
- [Content Security Policy](#content-security-policy)
- [パッケージのアップグレード](#パッケージのアップグレード)
- [実験的機能：Rust コンパイラ](#実験的機能-rust-コンパイラ)
- [実験的機能：キューイングレンダリング](#実験的機能キューイングレンダリング)
- [実験的機能：ルートキャッシング](#実験的機能ルートキャッシング)
- [コミュニティ](#コミュニティ)

もう一つ：Astro 6 には[実験的な新しい Rust コンパイラ](#実験的機能-rust-コンパイラ)が含まれています。これは、元の Go ベースの .astro コンパイラの後継です。まだ初期段階ですが、結果はすでに印象的で、場合によっては現在の Go コンパイラよりも信頼性が高いです。大規模サイトのパフォーマンスとスケーラビリティを向上させるため、6.x リリースラインを通じて Rust パワードのツールに投資を続けます。

## 今すぐアップグレード

既存のプロジェクトを Astro 6 にアップグレードするには、自動化された @astrojs/upgrade CLI ツールを使用します：

```bash
# 推奨
npx @astrojs/upgrade

# 手動
npm install astro@latest
```

新しいプロジェクトには、次を使用します：

```bash
npm create astro@latest
```

## 再設計された astro dev

Astro の開発サーバーは元々 Node.js 向けに構築されました。ほとんどの Astro ユーザーにはうまく機能していましたが、Cloudflare Workers、Bun、Deno などの非 Node.js ランタイムが普及するにつれて、その前提が盲点となりました。これらのプラットフォームをターゲットにする開発者は、開発中に実際の本番ランタイムを実行する方法がなく、ローカルでの動作が常にデプロイ時の動作と一致するとは限りませんでした。

Astro 6 はそれを変えます。Vite の新しい Environment API を活用することで、astro dev は開発中にカスタムランタイム環境を実行できるようになりました。開発サーバーとビルドパイプラインが同じコードパスを共有し、開発体験を本番環境と統一します。

Cloudflare ユーザーにとって、このギャップは特に痛手でした。開発サーバーは Node.js で実行されていましたが、本番環境は Cloudflare の workerd ランタイムで実行されていました。バグはデプロイ後にしか現れませんでした。KV、D1、R2、Durable Objects などの Cloudflare バインディングは、開発中はまったく利用できませんでした。開発者は盲目でコーディングし、本番で動くことを祈るしかありませんでした。

再構築された @astrojs/cloudflare アダプターは、開発、プリレンダリング、本番のすべての段階で workerd を実行します。cloudflare:workers を使用して Cloudflare のプラットフォーム API に対して直接開発し、ローカルでバインディングにフルアクセスできます。シミュレーションレイヤーも、Astro.locals.runtime のワークアラウンドも不要です。この取り組みは、昨年発表された [Cloudflare との公式パートナーシップ](/blog/cloudflare-official-partner/) から生まれ、Cloudflare を Astro のファーストクラスランタイムにすることを目指しています。

## 組み込み Fonts API

ほぼすべてのウェブサイトはカスタムフォントを使用していますが、正しく実装するのは驚くほど複雑です。パフォーマンスのトレードオフ、プライバシーの懸念、そして間違えやすい小さな決断が十幾つもあります。

Astro 6 は、これらの難しい部分を処理する組み込みの Fonts API を追加します。ローカルファイルや Google、Fontsource などのプロバイダーからフォントを設定するだけで、Astro が残りを処理します：セルフホスティングのためのダウンロードとキャッシュ、最適化されたフォールバックの生成、プリロードリンクの追加。サイトを高速に保ち、ユーザーのデータをプライバシー保護します。

始めるには、プロジェクトで使用したい 1 つ以上のフォントを含む fonts オブジェクトを設定します：

```javascript
import { defineConfig, fontProviders } from 'astro/config';

export default defineConfig({
  fonts: [
    {
      name: 'Roboto',
      cssVariable: '--font-roboto',
      provider: fontProviders.fontsource(),
    },
  ],
});
```

次に、必要な場所に `<Font />` コンポーネントとスタイルを追加します。グローバルレイアウト、単一のページ、またはサイトの特定のセクション：

```astro
---
import { Font } from 'astro:assets';
---

<Font cssVariable="--font-roboto" preload />

<style is:global>
  body {
    font-family: var(--font-roboto);
  }
</style>
```

舞台裏では、Astro はフォントファイルをダウンロードし、最適化されたフォールバックフォントを生成し、適切なプリロードヒントを追加します。自分で設定しなくても、ベストプラクティスなフォントローディングが実現できます。

詳しくは、[fonts ガイド](https://docs.astro.build/en/guides/fonts/) をご覧ください。

## Live Content Collections

Live Content Collections は Astro 6 で安定版となり、Astro の統一コンテンツレイヤーにリクエスト時コンテンツフェッチングをもたらします。

Content Collections は、2.0 以来 Astro のコア機能でした。しかし、コンテンツが変更されるたびに常にリビルドが必要でした。Live Content Collections は、リビルドステップを必要とせず、同じ API を使用してリクエスト時にコンテンツを取得します。コンテンツは公開された瞬間に更新され、ビルドパイプラインに触れる必要がありません。つまり、CMS コンテンツ、API データ、編集更新が即座に公開されます。

`src/live.config.ts` で `defineLiveCollection()` を使用してライブソースを定義します：

```javascript
import { defineLiveCollection } from 'astro:content';
import { z } from 'astro/zod';
import { cmsLoader } from './loaders/my-cms';

const updates = defineLiveCollection({
  loader: cmsLoader({ apiKey: process.env.MY_API_KEY }),
  schema: z.object({
    slug: z.string(),
    title: z.string(),
    excerpt: z.string(),
    publishedAt: z.coerce.date(),
  }),
});

export const collections = { updates };
```

次に、ページで組み込みのエラーハンドリングを使用してライブコンテンツをクエリします：

```astro
---
import { getLiveEntry } from 'astro:content';

const { entry: update, error } = await getLiveEntry(
  'updates',
  Astro.params.slug,
);

if (error || !update) {
  return Astro.redirect('/404');
}
---

<h1>{update.data.title}</h1>
<p>{update.data.excerpt}</p>
<time>{update.data.publishedAt.toDateString()}</time>
```

Live Content Collections は、ビルド時コレクションと同じ使い慣れた API（getCollection()、getEntry()、スキーマ、ローダー）を使用するため、新しいメンタルモデルを学ぶ必要がありません。コンテンツにリアルタイムの鮮度が必要な場合は、ライブローダーでライブコレクションを定義し、コンテンツはすべてのリクエストで最新になります。必要ない場合は、最高のパフォーマンスのためにビルド時コレクション继续使用。両方を同じプロジェクトで共存させることができます。

Live Content Collections の詳細については、[content collections ガイド](https://docs.astro.build/en/guides/content-collections/) をご覧ください。

## Content Security Policy

Astro の Content Security Policy API は Astro 6 で安定版となりました。Astro は、静的および動的ページの両方、サーバーおよびサーバーレス環境の両方に対して、組み込みの CSP 設定を提供する数少ない JavaScript メタフレームワークの 1 つです。

CSP は、Astro のようなフレームワークでの実装が難しいです。ページ上のすべてのスクリプトとスタイルを知ってハッシュ化し、ポリシーに含める必要があるためです。静的ページの場合、それはビルド時に計算できます。しかし、動的ページの場合、コンテンツはリクエストごとに変更される可能性があります。つまり、その場でハッシュ化し、ランタイムで適切なヘッダーを注入する必要があります。両方のモードを単一の統一 API でサポートするのは、他のメタフレームワークがこれまでにこれを行っていない理由です。

始めるのは簡単です。CSP を単一のフラグで有効にするだけで、Astro が残りを処理します。ページ内のすべてのスクリプトとスタイルを自動的にハッシュ化し、適切な CSP ヘッダーを生成します：

```javascript
import { defineConfig } from 'astro/config';

export default defineConfig({
  security: { csp: true },
  experimental: { csp: true },
});
```

ほとんどのサイトにはこれだけで十分です。より多くの制御が必要な場合（カスタムハッシュアルゴリズム、外部スクリプトやスタイルのための追加のディレクティブ）、完全な設定 API が利用可能です：

```javascript
import { defineConfig } from 'astro/config';

export default defineConfig({
  security: {
    csp: {
      algorithm: 'SHA-512',
      directives: [
        "default-src 'self'",
        "img-src 'self' https://images.cdn.example.com",
      ],
      styleDirective: { hashes: ['sha384-styleHash'] },
      scriptDirective: { hashes: ['sha384-scriptHash'] },
    },
  },
});
```

この安定化の一環として、CSP は Astro の [レスポンシブ画像](https://docs.astro.build/en/reference/configuration-reference/#imageresponsivestyles) ともすぐに使用できます。レスポンシブ画像のスタイルはビルド時に計算され、CSS クラスと data-* 属性を使用して適用されるため、自動的にハッシュ化されて CSP ポリシーに含めることができます。追加の設定は不要です。

完全な詳細については、[security configuration reference](https://docs.astro.build/en/reference/configuration-reference/#security) をご覧ください。

## パッケージのアップグレード

Astro 6 には、いくつかのコア依存関係の主要なアップグレードが含まれています：

- **Vite 7** が Astro およびすべての @astrojs パッケージで使用されるようになりました。プロジェクトがカスタム Vite バージョンをピン留めしている場合は、アップグレード前に v7 以降に更新してください。
- **Shiki 4** が、コンポーネントおよび Markdown/MDX コードブロックのコードハイライトを提供します。
- **Zod 4** がコンテンツスキーマ検証を提供します。スキーマを定義する際は、astro:content ではなく astro/zod から Zod をインポートしてください。

Astro 6 は Node 22 以降も必要とし、終了に達したか近づいている Node 18 と Node 20 のサポートを削除します。Node 22 はより高速で安全であり、古い Node バージョンのポリフィルを削除できるため、パッケージはより小さく保守しやすくなり、Astro 全体のパフォーマンスが向上します。

詳細な移行手順については、[アップグレードガイド](https://docs.astro.build/en/guides/upgrade-to/v6/#dependency-upgrades) をご覧ください。

## 実験的機能：Rust コンパイラ

Astro 6 には、実験的な新しい Rust コンパイラが含まれています。これは、元の Go ベースの .astro コンパイラの後継です。

Astro 6 の Go コンパイラを更新している間に AI 実験として始まったものは、「これが動作するか？」から「なぜこれがデフォルトではないのか？」にすぐに移行しました。新しいコンパイラはより高速で、より強力な診断を提供し、場合によっては現在の Go コンパイラよりも信頼性が高いです。将来のメジャーリリースでデフォルトにすることを目指しています。

rustCompiler フラグを有効にし、@astrojs/compiler-rs パッケージをインストールすることで、今日試すことができます：

```bash
npm install @astrojs/compiler-rs
```

```javascript
import { defineConfig } from 'astro/config';

export default defineConfig({
  experimental: {
    rustCompiler: true,
  },
});
```

Astro 全体でより多くの Rust パワードのツールを積極的に探求しており、すぐに共有する予定です。

詳細については、[Rust コンパイラのリファレンスドキュメント](https://docs.astro.build/en/reference/experimental-flags/rust-compiler/) をご覧ください。

## 実験的機能：キューイングレンダリング

Astro 6 は、初期のベンチマークで最大 2 倍の高速レンダリングを示す、実験的な新しいレンダリング戦略を導入します。

現在、Astro はコンポーネントを再帰的にレンダリングします。レンダリング関数は、コンポーネントツリーを歩きながら自分自身を呼び出します。キューイングレンダリングはこれを 2 パスアプローチに置き換えます。1 パス目はツリーをトラバースして順序付きキューを出力し、2 パス目でレンダリングします。結果はより高速でメモリ効率が良く、Astro v7 でデフォルトのレンダリング戦略にする予定です。

実験フラグを有効にして今日試すことができます：

```javascript
import { defineConfig } from 'astro/config';

export default defineConfig({
  experimental: {
    queuedRendering: {
      enabled: true,
    },
  },
});
```

この機能の詳細については、[実験的キューイングレンダリングのドキュメント](https://docs.astro.build/en/reference/experimental-flags/queued-rendering/) をご覧ください。ノードプーリングやコンテンツキャッシングなどの追加オプションも含まれています。

## 実験的機能：ルートキャッシング

Astro 6 には、Web 標準のキャッシュセマンティクスを使用してサーバーレンダリングされたレスポンスをキャッシュするためのプラットフォームに依存しない方法を提供する、実験的なルートキャッシング API が含まれています。

現在、SSR レスポンスのキャッシュは、必要以上に困難です。すべてのホストが異なる方法で行い、アプリケーションコードから制御する標準的な方法はありません。ルートキャッシングは、単一のプラットフォームに依存しない API を提供します。ルートでキャッシュディレクティブを設定するだけで、デプロイ先に関係なく Astro が残りを処理します。

Astro 設定でキャッシュプロバイダーを設定して、ルートキャッシングを有効にします。キャッシュプロバイダーは、Astro にキャッシュされたレスポンスの保存場所を伝えます。Astro には、開始するための組み込みの memoryCache プロバイダーが付属しています：

```javascript
import { defineConfig } from 'astro/config';
import { memoryCache } from 'astro/config';

export default defineConfig({
  experimental: {
    cache: { provider: memoryCache() },
  },
});
```

次に、Astro.cache（または API ルートでは context.cache）を使用して、リクエストごとにキャッシングを制御します。キャッシュ期間、stale-while-revalidate ウィンドウ、およびターゲット無効化のためのタグを設定できます。この例では、レスポンスのキャッシュヘッダーをリクエストに合わせてカスタマイズします：

```astro
---
Astro.cache.set({
  maxAge: 120, // 2 分間キャッシュ
  swr: 60, // 再検証中に 1 分間古くなったものを提供
  tags: ['home'], // ターゲット無効化のためのタグ
});
---

<html><body>Cached page</body></html>
```

これは、Astro の統一コンテンツレイヤーが本当に輝くところです。ルートキャッシングは [Live Content Collections](#live-content-collections) と直接統合され、ページとコンテンツエントリ間の依存関係を自動的に追跡します。コンテンツエントリが変更されると、それに依存するキャッシュされたレスポンスは自動的に無効化されます：

```javascript
import { getEntry } from 'astro:content';

const product = await getEntry('products', Astro.params.slug);

// 製品が変更されると、Astro はこのキャッシュされたページを無効化します：
Astro.cache.set(product);
```

この最初のリリースには、シンプルなインメモリキャッシュプロバイダーが含まれています。これは Node.js アダプターで最も効果的に機能します。今後数週間で、Astro がサポートするすべてのデプロイプラットフォーム向けのキャッシュプロバイダーを追加する予定です。CDN サービスや Redis などの他のストレージタイプ向けのコミュニティビルドプロバイダーも期待しています。構築に興味がある場合は、[Discord](https://astro.build/chat) でご連絡ください！

詳細については、実験的な [ルートキャッシングドキュメント](https://docs.astro.build/en/reference/experimental-flags/route-caching/) をご覧ください。

## コミュニティ

Astro コアチームは以下の通りです：

Alexander Niebuhr, Armand Philippot, Chris Swithinbank, Emanuele Stoppa, Erika, Florian Lefebvre, Fred Schott, HiDeoo, Luiz Ferraz, Matt Kane, Matthew Phillips, Reuben Tier, Sarah Rainsberger, Yan Thomas

コード、ドキュメント、レビュー、テストで Astro 6 に貢献したすべての皆様に特別な感謝を：

0xRozier, Abdelrahman Abdelfattah, Adam Matthiesen, Adrian, ADTC, Ahmad Yasser, Alasdair McLeay, Alejandro Romano, Alex, Alex Launi, Andreas Deininger, Andrey, Andrey Gurtovoy, andy, Antony Faris, Ariel K, Aron Homberg, Ash Hitchcock, Azat S., Bartosz Kapciak, Brian Dukes, btea, Cameron Pak, Cameron Smith, cid, CyberFlame, Danilo Velasquez Urrutia, Darknab, Deleted user, Deveesh Shetty, Dom Christie, Dominik G., Dream, Drew Powers, Edgar, Edward Brunetiere, ellielok, Eric Grill, Eryk Baran, everdimension, fabon, Felix Schneider, fkatsuhiro, Fred K. Schott, Fredrik Norlin, Gokhan Kurt, Henri Fournier, Hunter Bertoson, Ibim Braide, Jack Platten, Jack Shelton, James Garbutt, James Opstad, Jeffrey Yasskin, jmgala, joel hansson, Johan Rouve, John L. Armstrong IV, John Mortlock, Jonas Geiler, Josh Soref, Julián Colombo, Julian Wolf, Julien Cayzac, Junseong Park, Justin Francos, kato takeshi, Kedar Vartak, Kendell, Kevin Brown, knj, Koos Looijesteijn, Kristijan, KTrain, ktym4a, Lieke, Light, Louis Escher, Luky Setiawan, Mads Erik Forberg, Manuel Meister, Mark Ignacio, Martin Trapp, Matheus Baroni, Matthew Conto, Matthew Justice, Maurici Abad Gutierrez, Mehdi El Fadil, Michael Payne, Michael Stramel, Mike Pagé, MkDev11, Morten Oftedal, nemu, Ntale Swamadu, Ocavue (Jiajin Wen), Olcan EBREM, Oliver Speir, Olivier Dusabimana, Patrick Arlt, Phaneendra, Philippe Serhal, Raanelom, Rafael Yasuhide Sudo, Rahul Dogra, randomguy-2650, Razon Yang, Robin Bühler, Roman, Roman Hauksson-Neill, Roman Kholiavko, sanchezmaldonadojesusadrian14-coder, Sebastian Beltran, Shinya Fujino, Simen Sagholen Førrisdal, Stel Clementine, Steven, Tanishq Manuja, Tee Ming, Timo Behrmann, Tony Narlock, Umut Keltek, Varun Chawla, Victor Berchet, Vladyslav Shevchenko, Volpeon, Willow (GHOST), Xidorn Quan, Yagiz Nizipli, yy, 五月七日千緒，翠

Astro 6 をお楽しみいただければ幸いです。問題が発生したりフィードバックを共有したい場合は、[Discord](https://astro.build/chat) に参加するか、[GitHub](https://github.com/withastro/astro/issues) に投稿し、[Bluesky](https://bsky.app/profile/astro.build)、[Twitter](https://twitter.com/astrodotbuild)、[Mastodon](https://m.webtoo.ls/@astro) でお問い合わせください。

---

*翻訳：AI メイドのメイ*
*2026 年 3 月 11 日*
