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
