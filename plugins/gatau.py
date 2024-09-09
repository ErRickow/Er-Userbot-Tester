payload = {"args": "Make body masterpiece potrait", "is_flux_dev": True}

response = requests.post("https://akeno.randydev.my.id//akeno/fluxai?api_key=y0y0y03rq", json=payload).json()

await message.reply_photo(response["randydev"]["output_url"], caption=response["caption"])