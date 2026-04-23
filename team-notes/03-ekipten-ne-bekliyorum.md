# Gerçek Veriyi Nasıl Hazırlayacaksınız?

Bu dosyanın amacı şu: Eğer proje için gerçek fotoğraf toplama işini sen yapacaksan, aşağıdaki adımları uygula.

---

## 1. Nasıl görsel bulmalısınız?

İki seçenek var:

**Seçenek A: Kendiniz çekin**
Telefon veya kamera ile kırmızı nesneler içeren fotoğraflar çekin. Bu en kolay yol.

**Seçenek B: Internetten bulup indirebilirsiniz**
Ancak şu özelliklere dikkat edin:

- Nesneleri sayabilecek kadar net olsun
- Aynı renk nesnelerin olduğu fotoğraflar olsun
- Kaç nesne olduğu belli olsun (yazsa iyi, yoksa siz sayabilmelisiniz)

Internetten alıp almayayım diye düşünmeyin. Karar veremezseniz en kolay yol kendiniz çekmek.

**Öneri:** En az 4 farklı renk nesne kullanın.
Örnek: kırmızı, mavi, yeşil, sarı top/kutu/şişe gibi nesneler.

---

## 2. Fotoğraf seçerken neye dikkat etmelisiniz?

İyi fotoğraf için:

- Hedef renk net görünsün (bulanık olmasın)
- Nesneler sayılabilir olsun (yarım nesne olmasın)
- Fotoğraf çok karanlık veya çok parlak olmasın

**Farklı koşullar olsun:**

- Bazıları aydınlık, bazıları loş ortamda çekilsin
- Bazıları düz arka plan, bazıları karışık arka plan olsun
- Bazı fotoğraflarda nesneler tam ayrı, bazılarında hafif üst üste olsun

**Kötü fotoğraf örnekleri - bunlardan kaçının:**

- Bulanık fotoğraflar
- Çok karanlık fotoğraflar
- Nesnelerin yarısı kadraj dışında kalan fotoğraflar
- Birden fazla farklı renk karışık fotoğraflar

---

## 3. Kaç fotoğraf lazım?

Şu sayıları hedefleyin:

- **Renk başına:** 8-12 fotoğraf
- **Toplam:** en az 32 fotoğraf
- **En az:** 4 farklı renk

Yani örnek:
| Renk | Fotoğraf sayısı |
|------|----------------|
| Kırmızı | 8-12 |
| Mavi | 8-12 |
| Yeşil | 8-12 |
| Sarı | 8-12 |

---

## 4. Bu fotoğrafları nereye koyacaksınız?

Fotoğrafları şu klasöre koyun:

```
data/real/raw/
```

**Örnek dosya adları:**

- `kirmizi-01.ppm`
- `kirmizi-02.ppm`
- `mavi-01.ppm`
- `mavi-02.ppm`
- ...

**Desteklenen formatlar:** PPM veya PNG. Tercihen PPM.

**Boyut önerisi:** 640x480 veya benzeri makul boyutlar.

---

## 5. Metadata nedir ve ne yapacaksınız?

**Metadata, fotoğrafın açıklama dosyasıdır.**

Her fotoğraf için şu bilgileri içerir:

- Bu fotoğrafta kaç nesne var
- Nesnelerin rengi ne
- Işık koşulu nasıl
- Arka plan nasıl
- Nesneler üst üste mi

Bunu şöyle düşünün: her fotoğrafın yanında bir kısa not kartı. Sistemo bu kartı okuyup sonucu doğru mu diye kontrol ediyor.

---

## 6. Metadata dosyasını nasıl oluşturacaksınız?

Adım adım:

1. Şu dosyayı bulun: `data/real/metadata/dataset.template.json`

2. Bu dosyayı açın ve içindeki örnek kaydı kendi fotoğraflarınıza göre değiştirin

3. Her yeni fotoğraf için aynı yapıda bir kayıt daha ekleyin

4. **Dosyayı şu adla kaydedin:** `data/real/metadata/dataset.json`

**Önemli:** Sistem `dataset.json` dosyasını arıyor. Doğru adla kaydettiğinizden emin olun.

**Orijinal template kalır:**
`dataset.template.json` dosyası orijinal şablon olarak kalır. Bir şey olursa diye orijinali bozmadan bu dosyayı değiştirin.

**Örnek:**

```json
{
  "image_id": "kirmizi-01",
  "image_path": "data/real/raw/kirmizi-01.ppm",
  "target_color": "red",
  "expected_count": 4,
  "lighting": "controlled",
  "background": "plain",
  "overlap": "none"
}
```

---

## 7. Hangi alanları dolduracaksınız?

Metadata dosyasında şu alanlar var. Her birini düzgün doldurun:

| Alan             | Ne demek                         | Örnek değer                      |
| ---------------- | -------------------------------- | -------------------------------- |
| `image_id`       | Fotoğrafın kısa adı              | `kirmizi-01`                     |
| `image_path`     | Dosyanın repo içindeki yolu      | `data/real/raw/kirmizi-01.ppm`   |
| `target_color`   | Sayılacak ana renk               | `red`, `blue`, `green`, `yellow` |
| `expected_count` | Fotoğraftaki gerçek nesne sayısı | `3`, `4`, `5`                    |
| `lighting`       | Işık durumu                      | `controlled`, `dim`, `bright`    |
| `background`     | Arka plan tipi                   | `plain`, `cluttered`             |
| `overlap`        | Nesneler üst üste mi?            | `none`, `mild`, `heavy`          |

**Alanların açıklaması:**

- `lighting`:
  - `controlled`: normal oda ışığı
  - `dim`: loş ortam, az ışık
  - `bright`: çok parlak, bol ışık

- `background`:
  - `plain`: düz, sade arka plan
  - `cluttered`: karışık, detaylı arka plan

- `overlap`:
  - `none`: nesneler tam ayrı
  - `mild`: hafif temas var
  - `heavy`: nesneler birbirine girmiş

**Önemli:** `expected_count` alanını yazmadan önce fotoğrafı açıp nesneleri tek tek sayın. Emin olmadığınız sayıyı yazmayın.

---

## 8. Profile dosyası nedir?

Profile dosyası, sistemin renk ayarlarını tutan dosyadır. Başlangıçta bunu değiştirmeniz gerekmiyor.

Başlangıç için hazır dosya şurada:

```
configs/profiles/v1/multi-color-template.json
```

Veri toplama işini yapan kişinin ana işi bu dosya değil. Önce fotoğraflar ve metadata hazır olsun. Profile kısmına gerektiğinde ben bakarım.

---

## 9. Veri kontrolünü nasıl yapacaksınız?

Veriyi hazırladıktan sonra kontrol şu şekilde yapılır:

1. Terminali açın

2. Şu komutu çalıştırın:

```bash
make validate-real-dataset
```

Bu komut şunları kontrol eder:

- Metadata dosyası var mı
- Zorunlu alanlar dolu mu
- Fotoğraf yolları gerçekten klasörde mi
- Etiketler doğru yazılmış mı

**Hata çıkarsa?**

Hata mesajında ne yazıyorsa onu düzeltip komutu tekrar çalıştırın.

**Sık karşılaşılan hatalar:**

- Dosya yolu yanlış yazılmış
- Bir alan eksik kalmış
- Etiket yanlış yazılmış (örnek: `bright` yerine `birght`)
- Fotoğraf dosyası klasörde yok

Hata kalmayınca veri hazır demektir.

---

## 10. Özet: Yapmanız gerekenler

En kısa haliyle şu sıralamayı izleyin:

1. Fotoğrafları toplayın veya çekin
2. Fotoğrafları `data/real/raw/` klasörüne koyun
3. `dataset.template.json` dosyasını açın, içini doldurun ve `dataset.json` olarak kaydedin
4. Her fotoğraf için metadata kaydı ekleyin
5. `make validate-real-dataset` komutunu çalıştırın
6. Hata kalmayınca bana haber verin
