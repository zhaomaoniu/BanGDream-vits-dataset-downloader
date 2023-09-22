import aiohttp
import asyncio
import pygame
import os
import json

pygame.mixer.init()
pymusic = pygame.mixer.music

EVENT_NUM = 235
BAND_EVENTS = [235]


def fix_filename(filename: str, replace_tuples: list):
    for i in list('\/:*?"<>|（）()『』'):
        filename = filename.replace(i, "")
    for x, y in replace_tuples:
        filename = filename.replace(x, y)
    return filename


def get_relative_file_paths(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder_path)
            file_paths.append(folder_path + relative_path)
    return file_paths


def get_broken_mp3_file(filepath: str):
    result = []
    for file_name in get_relative_file_paths(filepath):
        pymusic.load(file_name)
        pymusic.set_volume(0)
        try:
            pymusic.play()
            pymusic.stop()
        except pygame.error:
            pymusic.stop()
            result.append(file_name)

    return result


class StoryDownload:
    def __init__(self, tasks):
        self.session = None
        self.tasks = tasks

    async def fetch_data(self, url):
        async with self.session.get(url) as response:
            if response.status == 200:
                try:
                    return json.loads(await response.text())
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON for {url}: {e}")
        return None

    async def main(self):
        self.session = aiohttp.ClientSession()
        await asyncio.gather(*self.tasks)
        await self.session.close()


class EventStoryDownload(StoryDownload):
    def __init__(self):
        super().__init__(self._tasks)

    async def get_chapter_num(self, event_id) -> int:
        data = await self.fetch_data(f"https://bestdori.com/api/events/{event_id}.json")
        return len(data["stories"]) + 1

    async def download(self, event_id):
        chapter_range = range(await self.get_chapter_num(event_id))
        for event_chapter in chapter_range:
            if event_id not in BAND_EVENTS:
                url = f"https://bestdori.com/assets/jp/scenario/eventstory/event{event_id}_rip/Scenarioevent{str(event_id).zfill(2)}-{str(event_chapter).zfill(2)}.asset"
            else:
                # 此处仍不完善
                url = f"https://bestdori.com/assets/jp/scenario/eventstory/event{event_id}_rip/Scenarioband8-{str(event_chapter).zfill(3)}.asset"
            filename = f"eventstory/event{str(event_id).zfill(2)}-{str(event_chapter).zfill(2)}.json"
            if os.path.exists(filename):
                print(f"File {filename} already exists")
                return
            if content := await self.fetch_data(url):
                with open(filename, "w", encoding="UTF-8") as file:
                    json.dump(content, file, indent=4)
                print(f"Downloaded {filename}")

    @property
    def _tasks(self):
        tasks = []
        for event_id in range(1, EVENT_NUM + 1):
            tasks.append(self.download(event_id))
        return tasks

    def run(self):
        if not os.path.exists("eventstory"):
            os.makedirs("eventstory")

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())


class VoiceDownload:
    def __init__(self, character_id, replace_tuples):
        self.character_id = character_id
        self.replace_tuples = replace_tuples
        self.session = None

        os.makedirs(os.path.dirname(f"voice/{self.character_id}/"), exist_ok=True)

    async def download_voice(self, event_id, event_chapter, voice_id, voice_content):
        url = f"https://bestdori.com/assets/jp/sound/voice/scenario/eventstory{event_id}_{event_chapter - 1}_rip/{voice_id}.mp3"
        async with self.session.get(url) as response:
            if response.status == 200:
                filename = f"voice/{self.character_id}/{voice_content}.mp3"
                content = await response.content.read()
                if len(content) != 14413:
                    with open(filename, "wb") as file:
                        file.write(content)
                    print(f"Downloaded {filename} from {url}")
                    await asyncio.sleep(0.05)
            else:
                print(f"Failed to download {url}")

    async def main(self):
        self.session = aiohttp.ClientSession()
        file_path = "eventstory/event{}-{}.json"
        tasks = []
        download_payloads = set()
        for event_id in range(1, EVENT_NUM + 1):
            for event_chapter in range(999):
                if os.path.exists(
                    file_path.format(
                        str(event_id).zfill(2), str(event_chapter).zfill(2)
                    )
                ):
                    with open(
                        file_path.format(
                            str(event_id).zfill(2), str(event_chapter).zfill(2)
                        ),
                        "r",
                        encoding="UTF-8",
                    ) as f:
                        event_story: dict = json.load(f)
                    talk_datas = event_story["Base"]["talkData"]
                    for talk_data in talk_datas:
                        for voice_data in talk_data["voices"]:
                            voice_id = voice_data["voiceId"]
                            character_id = voice_data["characterId"]
                            voice_content = fix_filename(
                                talk_data["body"], self.replace_tuples
                            )
                            if character_id == self.character_id:
                                download_payloads.add(
                                    (
                                        event_id,
                                        event_chapter,
                                        voice_id,
                                        voice_content,
                                    )
                                )
        print(f"Need to download {len(download_payloads)} voices in total")
        for payload in download_payloads:
            tasks.append(self.download_voice(*payload))
        await asyncio.gather(*tasks)
        await self.session.close()

    # TODO: 输出数据集文本

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())
