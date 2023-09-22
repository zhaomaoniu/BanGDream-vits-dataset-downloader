# BanGDream-vits-dataset-downloader

适用于vits训练的BanGDream数据集下载工具

## 环境要求

请确保已安装以下第三方库，并将ffmpeg添加至环境变量中：

- aiohttp
- pygame

## 用法

按照以下步骤进行配置和使用该工具：

1. 使用任意文本编辑器打开`__init__.py`文件。
2. 将`character_id`的值更改为您想要训练的角色ID，并保存文件。
   - 您可以从[此处](https://bestdori.com/api/characters/all.2.json)获取角色ID。
3. 在`utils.py`文件的第十行找到`EVENT_NUM`，将其值修改为当前活动的ID。如果您不知道活动的ID，可以选择一个较大的值（大约300-400），但这可能会导致稍后下载数据所需的时间稍长，并且Bestdori拒绝访问的可能性较大。
4. 现在可以运行代码了。打开命令行窗口并执行以下命令：

   ```
   python __init__.py
   ```

   如果一切顺利，数据将会下载完毕。如果您遇到类似于"远程主机拒绝访问"的错误，请稍等两分钟后再试一次。
   
5. 程序运行结束后，将会输出以下信息："Please delete these files: "。请按照提示删除输出的文件，因为它们是损坏的。如果输出为空，表示无需删除任何文件。
6. 如果一切正确，您将在项目文件夹下看到一个新的名为`voice`的文件夹。该文件夹中有一个以角色ID为名称的子文件夹，其中包含以语音内容命名的多个MP3文件。
7. 进入该子文件夹，手动删除一些您认为对模型训练不利的文件。
8. 然后，打开`create_dataset.py`文件，编辑第6到8行的参数，并保存文件。（如果您希望训练其他类型的模型，可以尝试修改第10到19行的参数）
9. 运行以下命令：

   ```
   python create_dataset.py
   ```

10. 等待一段时间，数据集将根据您的配置准备好。

## 感谢

- MyGO!!!!!: 驱使我继续完善这个项目
- WindowsSov8: 提供乐队故事章节数获取的方法
- [Bestdori](https://bestdori.com/): 提供数据
- [ChatGPT](https://chat.openai.com/): 提供代码辅助
- [BingAI](https://bing.com): 提供代码辅助
