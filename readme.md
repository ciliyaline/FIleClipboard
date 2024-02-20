# 文件剪贴板

需求书：[需求书](./doc.html)

## 后端

暂时还是用 venv 虚拟环境

```powershell
python -m venv .venv
.\.venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

更新 requirements.txt

```powershell
# 保证在虚拟环境中
python -m pip freeze > requirements.txt
```

如果会用，建议使用更好的Python包管理工具 [PDM](https://pdm.fming.dev/)
