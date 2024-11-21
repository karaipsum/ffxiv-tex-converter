@echo off
:: 获取当前批处理文件所在的目录
set current_dir=%~dp0

:: 获取拖拽进来的文件夹路径
set folder=%1

:: 检查路径是否有效
if not exist "%folder%" (
    echo 无效的文件夹路径: %folder%
    pause
    exit /b
)

:: 切换到批处理文件所在目录
cd /d "%current_dir%"

:: 执行转换命令
echo 正在将 DDS 文件转换为 TEX 文件...
python ffxiv_tex_converter-edit.py -d "%folder%" -c dds-to-tex

:: 提示完成
echo 转换完成!
pause
