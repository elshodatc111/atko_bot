# 🎓 ATKO Koreys Tili O'quv Markazi Boti

Ushbu bot o'quv markazlari uchun mo'ljallangan bo'lib, o'quvchilarni ro'yxatga olish, ularga darslarni avtomatik yetkazish va CRM tizimini boshqarish imkonini beradi.

## 🚀 Imkoniyatlar
- **Avtomatlashtirilgan darslar:** O'quvchi tanlagan vaqtda har kuni yangi dars yuboriladi.
- **CRM va Statistika:** Foydalanuvchi ma'lumotlarini bazada saqlash va Excel hisobot yaratish.
- **Log tizimi:** Har bir harakat (Start, Telefon yuborish, Reklama) alohida kanallarga yoziladi.
- **Admin Panel:** Reklama yuborish va dars videolarini oson qo'shish.

## 📁 Kerakli Kanallar
Bot to'liq ishlashi uchun quyidagi 5 ta kanal/guruh yaratilishi va Bot ularda **Admin** bo'lishi shart:
1. **LOG_START:** Botni ishga tushirganlar haqida ma'lumot.
2. **LOG_PHONE_1:** Telefon raqamini yuborgan o'quvchilar ro'yxati.
3. **LOG_PHONE_2:** Adminlar yuborgan postlar va ularning hisoboti.
4. **LOG_STATS:** Kunlik Excel hisobot va umumiy statistika.
5. **Yopiq Guruh:** Barcha dars videolari saqlanadigan ombor.

## 🛠 O'rnatish

## 1. Loyihani yuklab oling:
```bash
git clone [https://github.com/usernamingiz/atko_bot.git](https://github.com/usernamingiz/atko_bot.git)
cd atko_bot
```
## 2. Virtual muhit yarating va faollashtiring:
```bush
# Windows uchun:
python -m venv venv
venv\Scripts\activate

# Mac/Linux uchun:
source venv/bin/activate
```
## 3. Zaruriy kutubxonalarni o'rnating:
```bush
pip install aiogram python-dotenv apscheduler pandas openpyxl
```
## 4. ⚙️ 2-qadam: Sozlamalar (.env fayli)
```bush
Loyiha papkasida .env nomli fayl yarating va ichiga quyidagi ma'lumotlarni o'zingizniki bilan almashtirib yozing:
BOT_TOKEN=8215009701:AAFpoVkjG9... (BotFather'dan olingan token)
ADMIN_IDS=298760527,517159637   (Adminlar ID raqamlari, vergul bilan)
```
Kanallar va Guruhlar (ID raqamlari -100 bilan boshlanishi shart)
```bush
PRIVATE_CONTENT_GROUP_ID=-1003673892415  # Videolar ombori
LOG_START=-1003765609587                # 1-kanal (Start bosganlar logi)
LOG_PHONE_1=-1003804946836              # 2-kanal (Telefon yuborganlar logi)
LOG_PHONE_2=-1003804946836              # 3-kanal (Admin reklamalari logi)
LOG_STATS=-1003725583688               # 4-kanal (Excel va statistika logi)
```
## 📁 3-qadam: Telegram Kanallar Tartibi
Bot to'liq ishlashi uchun sizda quyidagi tuzilma bo'lishi va Bot ularning barchasida Admin bo'lishi shart:

Yopiq Guruh: Bu yerga dars videolari yuklanadi.

LOG_START Kanali: Botga kirgan har bir yangi foydalanuvchi ma'lumoti tushadi.

LOG_PHONE_1 Kanali: Faqat darsni boshlash uchun telefon yuborgan o'quvchilar tushadi.

LOG_PHONE_2 Kanali: Adminlar yuborgan har bir reklama va uning natijasi tushadi.

LOG_STATS Kanali: Har kuni 09:00 da bot yangi Excel hisobotini shu yerga tashlaydi.

## 🚀 4-qadam: Botni Ishga Tushirish
Hamma sozlamalar tayyor bo'lgach, terminalda quyidagi buyruqni bering:
python main.py

👨‍💻 Adminlar Uchun Qo'llanma
📢 Reklama yuborish
Botga /post buyrug'ini yuboring.

Auditoriyani tanlang (Barcha yoki faqat Telefon raqami borlar).

Reklama matni, rasm yoki videosini yuboring va tasdiqlang.

## 🎬 Video dars qo'shish
Videoni Yopiq guruhga yuklang.

O'sha videoni Botga Forward (uzatish) qiling.

Bot dars raqamini so'raganda, dars tartib raqamini (masalan: 1) yuboring.

## 📊 Excel hisobot

⚠️ Muhim Eslatmalar
Bot videolarni nusxalashdan himoyalangan (protect_content=True).

Har kuni soat 09:00 da avtomatik hisobot yuboriladi (Toshkent vaqti bilan).

Log kanallariga ma'lumotlar takrorlanmasdan, faqat bir marta yuboriladi.
