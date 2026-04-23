# Sizden Ne Lazım?

Kod tarafı büyük ölçüde hazır. Bundan sonraki en önemli konu gerçek veri tarafı gibi duruyor.

## En çok ihtiyaç duyulan şey

Şu an en çok ihtiyaç duyulan şey gerçek dataset.

Bunun içinde de şunlar gerekiyor:

- gerçek görseller
- her görsel için doğru nesne sayısı
- her görsel için etiketler

Bu etiketler şunlar:

- `lighting`: ışık durumu
- `background`: arka plan tipi
- `overlap`: nesneler üst üste mi

## Bu neden önemli?

Çünkü proje sadece kod yazmak değil, sonucu gerçek veri üzerinde göstermek.

Gerçek veri olmadan:

- final karşılaştırma eksik kalır
- hangi yöntemin daha iyi olduğu net gösterilemez
- proje yarım kalmış gibi durur

## Burada hangi konularda desteğe ihtiyaç var?

1. Gerçek görsellerin repo içindeki doğru yere konması gerekiyor
2. Her görsel için doğru nesne sayısının yazılması gerekiyor
3. Metadata dosyasının template'e göre doldurulması gerekiyor
4. Sonuçlara birlikte bakıp yorum yapılması çok işimize yarar

`metadata` demek, görselin yanında tuttuğumuz açıklama bilgisi demek.

Bu işi yaparken doğrudan şu dosya ve klasörleri baz alabilirsiniz:

- görsel düzeni için: `data/real/`
- metadata şablonu için: `data/real/metadata/dataset.template.json`
- başlangıç profile dosyası için: `configs/profiles/v1/multi-color-template.json`
- veri kontrolü için: `make validate-real-dataset`

Yani ekipten biri gerçek veri tarafını hazırlayacaksa, sıfırdan format düşünmesine gerek yok. Bu yapıyı kullanabilir.

Metadata içinde özellikle boş kalmaması gereken şeyler:

- `image_id`
- `image_path`
- `target_color`
- `expected_count`
- `lighting`
- `background`
- `overlap`

## Özellikle dikkat edilirse iyi olur

- sayılar doğru olsun
- dosya isimleri karışmasın
- etiketler tutarlı olsun
- eksik görsel kalmasın
- metadata içindeki yol ile gerçek dosya yolu birbiriyle uyuşsun

Çünkü küçük veri hataları bütün sonucu bozabiliyor. Kod doğru olsa bile veri yanlışsa sonuç yine yanlış çıkıyor.

## Son aşamada bence en faydalı şeyler

- gerçek veriyi tamamlamak
- çıkan sonuçları birlikte yorumlamak
- eksik ya da saçma görünen sonuç varsa söylemek

Pratik akış olarak bence en kolayı şu:

1. görseller toplanır
2. metadata template doldurulur
3. `make validate-real-dataset` çalıştırılır
4. hata varsa düzeltilir
5. veri hazır olduğunda ben final çalıştırmaları yaparım

Kısacası ben daha çok kod tarafını toparladım. Buradan sonra veri bulma, veriyi düzgün hazırlama ve son kontrol tarafında desteğe ihtiyaç var.
