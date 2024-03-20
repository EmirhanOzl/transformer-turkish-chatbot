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

Chatbot, Türkçe konuşmalardan oluşan bir veri kümesi üzerinde eğitilmiştir. Sağlanan veri setini kullanabilir veya kendi veri setinizi oluşturabilirsiniz. Veri kümesi aşağıdaki formatta olmalıdır:

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
