import asyncio
from pyrogram import Client

async def generate_and_send_string_session(api_id, api_hash):
    async with Client("tele", api_id=api_id, api_hash=api_hash) as app:
        string_session = await app.export_session_string()
        print("\n==== PYROGRAM SESSION STRING ====\n")
        print(string_session)
        print("\n=== COPY DAN SIMPAN ===\n")
        # Coba kirim ke Saved Messages (jika tidak error)
        try:
            await app.send_message(
                "me",
                f"<b>Your Pyrogram String Session:</b>\n\n<code>{string_session}</code>",
            )
            print("String session juga sudah dikirim ke 'Saved Messages'.")
        except Exception as e:
            print(f"Gagal kirim ke Saved Messages: {e}")

if __name__ == "__main__":
    api_id = int(input("Enter your API ID: "))
    api_hash = input("Enter your API Hash: ")
    asyncio.run(generate_and_send_string_session(api_id, api_hash))
