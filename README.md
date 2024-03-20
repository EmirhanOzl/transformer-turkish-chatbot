# Transformer Modeli ile Türkçe Chatbot

Bu depo, Transformer modeli kullanılarak oluşturulmuş bir Türkçe sohbet botunun kodunu içerir. Sohbet robotu, Türkçe konuşmalardan oluşan bir veri kümesi üzerinde eğitilmiştir ve kullanıcı girdilerine yanıtlar üretebilir.

## Dosyalar

* **model.py:** Kodlayıcı, kod çözücü ve dikkat mekanizmaları dahil olmak üzere Transformer model mimarisini tanımlar.
* **dataset.py:** Konuşma veri kümesinin yüklenmesi, ön işlenmesi ve tokenize edilmesi için fonksiyonlar içerir.
* **chatbot.py:** Yanıt oluşturma ve kullanıcı geri bildirimi toplama dahil olmak üzere etkileşimli sohbet işlevselliğini yönetir.
* **data/lines.txt:** Eğitim için kullanılan ham metin satırlarını depolar.
* **data/conversations.txt:** Eğitim için kullanılan konuşma çiftlerini içerir.

## Kullanım

1. **Depoyu klonlayın:**
```shell
git clone https://github.com/EmirhanOzl/transformer-turkish-chatbot.git
```
2. **Gerekli bağımlılıkları yükleyin:**
```shell
pip install -r requirements.txt
```
3. **Modeli eğitin:**
```shell
python train.py
```
4. **Chatbotu çalıştırın:**
```shell
python chatbot.py
```

## Eğitim Verileri

Chatbot, `data/` dizininde depolanan Türkçe konuşmalardan oluşan bir veri kümesi üzerinde eğitilmiştir. Sağlanan veri setini kullanabilir veya kendi veri setinizi oluşturabilirsiniz. Veri kümesi aşağıdaki formatta olmalıdır:

Veri kümesi iki dosyadan oluşmaktadır:

* **lines.txt:** Bu dosya eğitim için kullanılan ham metin satırlarını içerir. Her satır aşağıdaki formattadır:
```
[LINE_ID] +++$+++ [USER_ID] +++$+++ [MOVIE_ID] +++$+++ [CHARACTER_NAME] +++$+++ [TEXT]
```

* `LINE_ID` hattın kimliğidir.
* `USER_ID` hattı konuşan kullanıcının kimliğidir.
* `MOVIE_ID` konuşmanın hakkında olduğu filmin kimliğidir (isteğe bağlı).
* `CHARACTER_NAME` satırı söyleyen karakterin adıdır (isteğe bağlı).
* `TEXT` satırın metnidir.

* **conversations.txt:** Bu dosya eğitim için kullanılan konuşma çiftlerini içerir. Her satır aşağıdaki formattadır:
```
[USER_ID] +++$+++ [BOT_ID] +++$+++ [MOVIE_ID] +++$+++ [CONVERSATION]
```

* `USER_ID` kullanıcının kimliğidir.
* `BOT_ID` sohbet robotunun kimliğidir.
* `MOVIE_ID` konuşmanın hakkında olduğu filmin kimliğidir (isteğe bağlı).
* `CONVERSATION`, virgülle ayrılmış, konuşma dönüşlerini temsil eden satır kimliklerinin bir listesidir.

Sağlanan veri kümesini kullanabilir veya aynı formatta kendi veri kümenizi oluşturabilirsiniz.

**Not:** `MOVIE_ID` ve `CHARACTER_NAME` alanları isteğe bağlıdır ve yerine default birşey yazılabilir.



## Örnek çıktı

Aşağıda listelenen hiperparametreler kullanılarak aşağıdaki sonuçlar elde edilmiştir:

```python
self.save_model = "model.h5"
self.max_samples = 25000
self.max_length = 60
self.batch_size = 128
self.num_layers = 3
self.num_units = 512
self.d_model = 256
self.num_heads = 8
self.dropout = 0.1
self.activation = "relu"
self.epochs = 100
```

Training Results:
```
Epoch 100/100
24/24 [==============================] - 192s 8s/step - loss: 0.0145 - accuracy: 0.3174
```

Örnek çıktı:

**User:** Merhaba nasılsın?
**Bot:** Merhaba! Ben iyiyim, teşekkür ederim. Sana nasıl yardımcı olabilirim bugün?

**User:** Sence de gökyüzü çok güzel değil mi?
**Bot:** O zaman hemen başlayalım, bu filmi izlemek için daha fazla beklemek istemiyorum.

**User:** Sanırım uzaklara gideceğim.
**Bot:** Nereye gitmek istersin?

**User:** Nereye gitmek istersin?
**Bot:** Belki de dünya dışına. Sence dünya dışını görebilir miyiz?

**User:** Belki de dünya dışına. Sence dünya dışını görebilir miyiz?
**Bot:** Belki bir gün teknoloji bize bu imkanı sunar, kim bilir?

**User:** Belki bir gün teknoloji bize bu imkanı sunar, kim bilir?
**Bot:** Ne zaman istersen yardımcı olmaktan mutluluk duyarım. Yaratıcı bir süreç geçirmeni dilerim!


Not: Sohbet robotunun yanıtları, kullanılan eğitim verilerine ve hiperparametrelerine bağlı olarak değişebilir.

