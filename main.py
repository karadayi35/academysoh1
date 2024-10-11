from telethon import TelegramClient, events
import re

# Telegram API bilgileri - https://my.telegram.org/apps üzerinden alınabilir.
api_id = '16200120'  # Telegram API ID
api_hash = '6611d0556f6f8dc7b9190803cc442dec'  # Telegram API Hash

# Kullanacağınız hesapların telefon numaraları ve session isimleri
accounts = [
    ('+447599168809 ', 'session_1'),
    ('+447957201395 ', 'session_2'),
    ('+447903319837 ', 'session_4'),
    ('+447879090554 ', 'session_5'),
    ('+447393306945 ', 'session_6'),
    ('+447901829995 ', 'session_7'),
    ('+447555132839 ', 'session_8'),
    ('+447887221883 ', 'session_9'),
    ('+46760749893 ', 'session_10'),
    ('+353873812868 ', 'session_11'),
    ('+85270945200 ', 'session_12'),
    ('+37367713916 ', 'session_13'),
    ('+447469301950 ', 'session_14'),
    ('+447562118006 ', 'session_15'),
    ('+447856096750 ', 'session_16'),
    ('+447517007599  ', 'session_17'),
    ('+447926762107 ', 'session_18'),
    ('+447563091691 ', 'session_19'),
    ('+447939686582 ', 'session_20'),
    ('+447961267689 ', 'session_21'),
    ('+447957613256  ', 'session_22'),

    ('+447538366715 ', 'session_24'),
    ('+447930877620 ', 'session_25'),
    ('+447932346011 ', 'session_26'),
    ('+447985132321  ', 'session_27'),
    ('+447908575748 ', 'session_28'),
    ('+447517007674 ', 'session_29'),
    ('+447745161785 ', 'session_30'),
    ('+447742588629 ', 'session_31'),
    ('+447752559964 ', 'session_32'),
    ('+447729389626 ', 'session_33'),
    ('+447599168979 ', 'session_34'),
    ('+447801101779 ', 'session_35'),
    ('+447907325741 ', 'session_36'),
    ('+447951829503  ', 'session_44'),
    ('+447563041929  ', 'session_45'),
    ('+447763916635  ', 'session_47'),
    ('+447932516781  ', 'session_48'),
]

# Kaynak gruplar ve hedef grup
source_groups = ['https://t.me/ogedayprochat', 'https://t.me/ekremabianalizsohbet', 'https://t.me/hebelehubsohbet']  # Mesajların çekileceği gruplar
target_group = 'https://t.me/rouletteacademyturkey'  # Mesajların gönderileceği grup

# Yasaklı kelimeler listesi
banned_keywords = ['ekremabi', 'OgedayPRO', 'ogeday', '!orisbet', '!fixbet', '!olaycasino', '!enbet', '!betplay', '!gamobet']

# Telegram istemcilerini başlatmak için async fonksiyonu
async def start_clients():
    clients = []
    for phone_number, session_name in accounts:
        client = TelegramClient(session_name, api_id, api_hash)
        await client.start(phone_number)
        clients.append(client)
    return clients

# URL, medya ve yasaklı kelimeler içeren mesajları filtreleyen fonksiyon
def is_valid_message(message):
    # URL içeren mesajları filtrele
    url_pattern = r'(https?://\S+|www\.\S+)'
    if re.search(url_pattern, message.text):
        return False

    # Medya içerikli mesajları filtrele
    if message.media:
        return False

    # Yasaklı kelimeler içeren mesajları filtrele
    for keyword in banned_keywords:
        if keyword.lower() in message.text.lower():
            return False

    return True

# Kaynak gruplardan gelen mesajları hedef gruba gönderme fonksiyonu
async def forward_messages(clients):
    client_index = 0  # Hesap döngüsünü başlatmak için başlangıç indeksi

    for source_group in source_groups:
        source_client = clients[client_index]

        @source_client.on(events.NewMessage(chats=source_group))
        async def handler(event):
            nonlocal client_index
            message = event.message

            # Sadece geçerli mesajları al
            if is_valid_message(message):
                try:
                    # Mesajı hedef gruba hızlı bir şekilde gönder
                    await clients[client_index].send_message(target_group, message.text)

                    # Hesabı hemen değiştir ve sıradaki hesaba geç
                    client_index = (client_index + 1) % len(clients)

                except Exception as e:
                    print(f"Hata oluştu: {e}")
                    # Eğer bir hata varsa, sıradaki hesaba geç
                    client_index = (client_index + 1) % len(clients)

        print(f"Mesajlar {source_group} grubundan çekilmeye başlandı...")

    await source_client.run_until_disconnected()

# Ana fonksiyon
async def main():
    clients = await start_clients()
    await forward_messages(clients)

# Botu başlat
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
