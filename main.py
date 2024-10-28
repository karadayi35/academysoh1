import asyncio
import re
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

# Telegram API bilgileri
api_id = '16200120'  
api_hash = '6611d0556f6f8dc7b9190803cc442dec'  

# Hesap telefon numaraları ve session isimleri
accounts = [
    ('+447599168809', 'session_1'), ('+447957201395', 'session_2'),
    ('+447903319837', 'session_4'), ('+447879090554', 'session_5'),
    ('+447393306945', 'session_6'), ('+447901829995', 'session_7'),
    ('+447555132839', 'session_8'), ('+447887221883', 'session_9'),
    ('+46760749893', 'session_10'),  ('+353873812868', 'session_11'),
    ('+85270945200', 'session_12'),  ('+37367713916', 'session_13'),
    ('+447469301950', 'session_14'), ('+447562118006', 'session_15'),
    ('+447856096750', 'session_16'), ('+447517007599', 'session_17'),
    ('+447926762107', 'session_18'), ('+447563091691', 'session_19'),
    ('+447939686582', 'session_20'), ('+447961267689', 'session_21'),
    ('+447957613256', 'session_22'), ('+447538366715', 'session_24'),
    ('+447930877620', 'session_25'), ('+447932346011', 'session_26'),
    ('+447985132321', 'session_27'), ('+447908575748', 'session_28'),
    ('+447517007674', 'session_29'), ('+447745161785', 'session_30'),
    ('+447742588629', 'session_31'), ('+447752559964', 'session_32'),
    ('+447729389626', 'session_33'), ('+447599168979', 'session_34'),
    ('+447801101779', 'session_35'), ('+447907325741', 'session_36'),
    ('+447951829503', 'session_44'), ('+447563041929', 'session_45'),
    ('+447763916635', 'session_47'), ('+447932516781', 'session_48'),
]

# Kaynak ve hedef grup ID'leri
source_groups = [-1001981851047, -1002068077471]  # Grup ID'leri
target_group = -1002188591527  # Hedef grup ID'si

# Yasaklı kelimeler
banned_keywords = [
    'ekremabi', 'OgedayPRO', 'ogeday', '!orisbet', '!fixbet', 
    '!olaycasino', '!enbet', '!betplay', '!gamobet'
]

# Telegram istemcilerini başlatmak için async fonksiyonu
async def start_clients():
    clients = []
    for phone_number, session_name in accounts:
        client = TelegramClient(session_name, api_id, api_hash)
        await client.start(phone_number)
        clients.append(client)
    return clients

# URL, medya ve yasaklı kelimeler içeren mesajları filtreleme fonksiyonu
def is_valid_message(message):
    url_pattern = r'(https?://\S+|www\.\S+)'
    if re.search(url_pattern, message.text):
        return False
    if message.media:
        return False
    for keyword in banned_keywords:
        if keyword.lower() in message.text.lower():
            return False
    return True

# Kaynak gruplardan gelen mesajları hedef gruba yönlendirme fonksiyonu
async def forward_messages(clients):
    client_index = 0  # Hesap döngüsünü başlatmak için başlangıç indeksi

    for source_group in source_groups:
        source_client = clients[client_index]

        @source_client.on(events.NewMessage(chats=source_group))
        async def handler(event):
            nonlocal client_index
            message = event.message

            if is_valid_message(message):
                try:
                    # Mesajı hedef gruba gönder
                    await clients[client_index].send_message(target_group, message.text)
                    print(f"Mesaj gönderildi: {message.text}")

                    # Her mesaj arasında kısa gecikme ekle
                    await asyncio.sleep(0.2)  

                    # Hesapları sırayla döndür
                    client_index = (client_index + 1) % len(clients)

                except FloodWaitError as e:
                    print(f"Flood wait hatası: {e.seconds} saniye bekleniyor...")
                    await asyncio.sleep(e.seconds)  # Flood wait süresi boyunca bekle

                except Exception as e:
                    print(f"Hata oluştu: {e}")
                    # Hata durumunda sıradaki hesaba geç
                    client_index = (client_index + 1) % len(clients)

        print(f"Mesajlar {source_group} grubundan çekilmeye başlandı...")

    await source_client.run_until_disconnected()

# Ana fonksiyon
async def main():
    clients = await start_clients()
    await forward_messages(clients)

# Botu başlat
if __name__ == '__main__':
    asyncio.run(main())
