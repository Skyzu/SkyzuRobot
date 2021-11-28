import os
import time

import aiohttp

from SkyzuRobot.utils.uputils import humanbytes, time_formatter


async def download_file(url, file_name, message, start_time, bot):
    async with aiohttp.ClientSession() as session:
        time.time()
        await download_coroutine(session, url, file_name, message, start_time, bot)
    return file_name


async def download_coroutine(session, url, file_name, event, start, bot):

    CHUNK_SIZE = 1024 * 6  # 2341
    downloaded = 0
    display_message = ""
    async with session.get(url) as response:
        total_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        if "text" in content_type and total_length < 500:
            return await response.release()
        await event.edit(
            """**Initiating Download**
**URL:** {}
**File Name:** {}
**File Size:** {}
**© @Misszero_bot**""".format(
                url,
                os.path.basename(file_name).replace("%20", " "),
                humanbytes(total_length),
            ),
            parse_mode="md",
        )
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += CHUNK_SIZE
                now = time.time()
                diff = now - start
                if round(diff % 10.00) == 0:  # downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = (
                        round((total_length - downloaded) / speed) * 1000
                    )
                    estimated_total_time = elapsed_time + time_to_completion
                    try:
                        if total_length < downloaded:
                            total_length = downloaded
                        current_message = """Downloading : {}%
URL: {}
File Name: {}
File Size: {}
Downloaded: {}
ETA: {}""".format(
                            "%.2f" % (percentage),
                            url,
                            file_name.split("/")[-1],
                            humanbytes(total_length),
                            humanbytes(downloaded),
                            time_formatter(estimated_total_time),
                        )
                        if (
                            current_message != display_message
                            and current_message != "empty"
                        ):
                            print(current_message)
                            await event.edit(current_message, parse_mode="html")

                            display_message = current_message
                    except Exception as e:
                        print("Error", e)
                        # logger.info(str(e))
        return await response.release()
