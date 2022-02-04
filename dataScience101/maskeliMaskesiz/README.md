# With Mask? Without Mask?

## Genel Bilgiler
Medikal maskelerin takılıp takılmadığının görüntüler üzerinde belirleyen bir sitem oluşturduk. Projenin adım adım nasıl oluşturulduğu diğer başlıklarda açıklanacaktır. Projemizde Python programlama dilini ve OpenCV, Keras ve  Tensorflow  kütüphanelerini  kullandık. Keras, en kısa tanımıyla bir Derin Öğrenme kütüphanesidir. Yapı olarak TensorFlow ve Theano kütüphanelerini kullanarak çalışır, bu kütüphanelerin zorlayıcı yazım biçimlerine nazaran işlemlerinizi daha hızlı ve basitçe gerçekleştirmeye yardımcı fonksiyonları içerir. Yüz tespiti içinde “haar”ı kullandık. train, validation ve test verileri https://www.kaggle.com/ dan alınmıştır.

## Gerekli Kütüphanelerin Eklenmesi
* Pandas ve numpy kütüphaneleri verilerin temizlenmesi ve indexlenmesinde kullanılır. 
* os dosya ve dizin işlemleri için kullanılan  modüldür.
* shuffle ile oluşturulan veri kümelerini karıştırırız.
* Matplotlib veri görselleştirmesinde kullandığımız temel python kütüphanesidir.
* Cv2 (Open Source Computer Vision Library) açık kaynak kodlu Bilgisayarla Görme kütüphanesidir. Resimler üzerindeki istenilen değişiklikleri yapmak için kullanılır.
* Distance diziler arasındaki benzerlikleri hesaplamak için yardımcılar sağlar.
* VGG-19, 19 katman derinliğine sahip evrimsel bir sinir ağıdır.
* keras.callbacks modeli eğitirken verilen değerlere göre karşılaştırma yaparak kaydetme ve öğrenme olayını erken sonlandırma işlemleri için kullanılır.

## Verinin Hazırlanması
Bu aşamada klasörlerde maskeli ve maskesiz olarak ayrılmış olan verileri; eğitim, doğrulama ve test adında veri gruplarına indexleme işlemi gerçekleştirilir. İndexleme işleminden sonra veriler öğrenme modeli için gerçek zamanlı döngüye alma işlemi için yığınlar oluşturulur. Eğitim seti için 5000 maskesiz ve 5000 maskeli olmak üzere toplam 10000 resim kullanımıştır. Doğrulama (validation) içinde maskeli 400 ve maskesiz olmak üzere 800 fotoğraf kullanılmıştır.

## Modelin Oluşturulması ve Eğitimi
Modeli oluştururken her aşamada hangi işlemin ne işe yaradığı yorum satırları ile ifade edilmiştir. Burada yukarıda bahsedilen 19 katmanlı bir model kullandık.

## Modelin Yüklenmesi ve Test Edilmesi
Modelimi test veri kümesiyle test ediyoruz ve tek tek resimler üzerinde test ettikten sonra loss function ve karmaşıklık matrisi aşağıdaki gibi çıkmıştır.

## Modelin Sınıflandırma İşlemine Tabi Tutulması
Sınıflandırma işlemine geçmeden önce resmi dosyadan okuduktan sonra “haar” yüz tanıma sistemine sokarak resim üzerindeki yüzleri bir “yuzler” değişkeninin içerisine atar. Daha sonra resim üzerindeki tespit edilen koordinatlara göre yüzleri keserek modele göre sınıflandırma işlemine tabi tutulur. Çıkan değer ‘0’a yakın ise maskeli olarak sınıflandırılarak yüz çevresine yeşil renkte çerçeve çizilir ve çerçeve kenarına “maskeli” yazar. Çıkan değer ‘1’e yakın ise maskesiz olarak sınıflandırılarak yüz çevresine kırmızı renkte çerçeve çizilir ve çerçeve kenarına “maskesiz” yazar. Eğer sistem yüz bulamaz ise çıktı olarak “Resim üzerinde yüz tespit edilemedi!” uyarısı döndürür.

## Sonuç
Train, validation ve test verilerinde sadece yüz olan resimler üzerinde öğrenme modeli oluşturulduğu için bizim çekipte modele maskeli ya da maskesiz olarak sınıflandırmasını istediğimiz resme genellikle maskesiz yanıtı alınmıştır. Sebebi de modeli sadece yüzleri kullanarak tanıttık fakat bizim çektiğimiz resimlerde yüzden başka çevremizdeki ortamda bulunmaktadır. Bundan dolayı bizde sistemin doğru çalışması adına yüzü tespit edip (kırpıp) onu modele sorduk ve doğal olarak sonuçlar iyileşti. Ayrıca yüz tespitinde kullanılan algoritmanın da başarıyı etkileyen faktörlerin başında gelmektedir, yüzü ne kadar iyi bulursa modelimiz daha iyi sınıflandırma yapabilmektedir. Eğittiğimiz modeli kendi resimlerimiz üzerindeki sonuçlarına bakacak olursak başarılı oldu diyebiliriz.