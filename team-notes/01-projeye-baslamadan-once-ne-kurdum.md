# Projeye Başlamadan Önce Ne Kurdum?

Projeye başlamadan önce biraz çalışma düzenini kurmaya uğraştım. Çünkü en başta düzen kurulmayınca sonra kod da karışıyor, yapılan iş de takip edilmesi zor oluyor.

## GitHub tarafında ne yaptım?

- repo düzenini kurdum
- `main` dalını ana dal olarak bıraktım
- işleri doğrudan `main` üstünde değil, ayrı branch'lerde yapacak şekilde ilerledim
- GitHub üstünde çalışan otomatik kontrol akışını kullandım

`branch` demek, ana kodu bozmadan ayrı bir kolda çalışmak demek.

## Temel çalışma düzeni nasıldı?

Mantık kabaca şuydu:

- önce değişiklik yap
- sonra test et
- sonra commit at
- sonra GitHub'a gönder

## Kontrol tarafında ne kurdum?

Projede kodu direkt "tamamdır" diye bırakmamak için kontrol tarafını da hazırladım.

Bunun için ana komut şu:

```bash
make validate-pr
```

Bu komut şunlara bakıyor:

- kod düzeni düzgün mü
- bariz hata var mı
- testler geçiyor mu
- proje temel seviyede çalışıyor mu

## Makefile ne işe yarıyor?

`Makefile`, sık kullandığımız komutları kısa ve düzenli şekilde çalıştırmak için var.

Yani uzun uzun komut yazmak yerine:

- `make validate-pr`
- `make test`
- `make smoke-test`

gibi daha kısa komutlar kullanabiliyoruz.

Bu da ekip içinde aynı işleri herkesin aynı şekilde çalıştırmasını kolaylaştırıyor.

## Otomatik kontrol de var

Git hook da kurulu.

`pre-commit` veya `pre-push hook` demek, commit ya da push atmadan hemen önce otomatik çalışan küçük kontrol sistemi demek.

Amacı da şu: eksik ya da problemli bir şeyi yanlışlıkla GitHub'a göndermemek.

## GitHub Actions tarafında ne var?

GitHub tarafında da otomatik kontrol sistemi var.

`GitHub Actions` demek, GitHub üstünde otomatik çalışan kontrol akışı demek.

Yani bir şey GitHub'a gidince sadece bizim bilgisayarda değil, GitHub tarafında da tekrar kontrol ediliyor. Şu an bu kontroller çalışıyor ve projede kullanılan test düzeninin bir parçası.

Bunun amacı şu:

- yerelde kaçırılan bir hata varsa görmek
- `main` dalına problemli iş gitmesini zorlaştırmak
- projede ortak bir kalite kontrolü olması

## Kural dosyaları ne işe yarıyor?

- `CONTRIBUTING.md`: ekip olarak nasıl çalışacağımızı yazıyor
- `AGENTS.md`: AI araçları kullanılırsa onların da aynı kurala uymasını istiyor
- `README.md`: projede hangi komutlar var, genel yapı ne, onu anlatıyor

Yani ben önce biraz düzeni oturtmaya çalıştım. Böylece sonradan kim ne yaptı, ne test edildi, ne GitHub'a gitti daha net hale geldi.
