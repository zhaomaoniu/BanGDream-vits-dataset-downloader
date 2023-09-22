from utils import EventStoryDownload, VoiceDownload, get_broken_mp3_file

character_id = 900000
replace_tuples = [
    ("戸山", "とやま"),
    ("香澄", "かすみ"),
    ("市ヶ谷", "いちがや"),
    ("有咲", "ありさ"),
    ("牛込", "うしごめ"),
    ("里美", "りみ"),
    ("花園", "はなぞの"),
    ("山吹", "やまぶき"),
    ("沙綾", "さや"),
    ("宇田川", "うだがわ"),
    ("巴", "ともえ"),
    ("青葉", "あおば"),
    ("美竹", "みたけ"),
    ("蘭", "らん"),
    ("上原", "うえはら"),
    ("羽沢", "はざわ"),
    ("松原", "まつばら"),
    ("花音", "かのん"),
    ("瀬田", "せた"),
    ("薫", "かおる"),
    ("弦巻", "つるまき"),
    ("北沢", "きたざわ"),
    ("大和", "やまと"),
    ("麻弥", "まや"),
    ("氷川", "ひかわ"),
    ("日菜", "ひな"),
    ("丸山", "まるやま"),
    ("彩", "あや"),
    ("白鷺", "しらさぎ"),
    ("千聖", "ちさと"),
    ("若宮", "わかみや"),
    ("紗夜", "さよ"),
    ("湊", "みなと"),
    ("友希那", "ゆきな"),
    ("今井", "いまい"),
    ("白金", "しろかね"),
    ("燐子", "りんこ"),
    ("鳰原", "にゅばら"),
    ("令王那", "れおな"),
    ("朝日", "あさひ"),
    ("六花", "ろっか"),
    ("和奏", "わかな"),
    ("佐藤", "さと"),
    ("珠手", "たまで"),
    ("二葉", "ふたば"),
    ("桐ヶ谷", "きりがや"),
    ("透子", "とこ"),
    ("倉田", "くらた"),
    ("広町", "ひろまち"),
    ("七深", "ななみ"),
    ("八潮", "やしお"),
    ("瑠唯", "るい"),
    ("高松", "たかまつ"),
    ("燈", "ともり"),
    ("千早", "ちはや"),
    ("愛音", "あのん"),
    ("要", "かなめ"),
    ("楽奈", "らな"),
    ("長崎", "ながさき"),
    ("椎名", "しいな"),
    ("立希", "たき"),
    ("\n", ""),
    (" ", ""),
    ("　", "")
]

event_story = EventStoryDownload()
voice_downloader = VoiceDownload(character_id, replace_tuples)

print("Started to download event stories\n\n")

# event_story.run()

print(f"\n\nFinished downloading event stories, started to download voices of character {character_id}\n\n")


voice_downloader.run()

print(f"\n\nFinished downloading voices of {character_id}, started to get broken files\n\n")

broken_files = get_broken_mp3_file(f"voice/{character_id}/")

print(f"\n\nPlease delete these files: {broken_files}\n\n")