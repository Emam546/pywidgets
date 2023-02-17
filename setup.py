from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Lightweight utility package for common computer vision tasks."
LONG_DESCRIPTION = "A series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization, displaying Matplotlib images, sorting contours, detecting edges, and much more easier with OpenCV and both Python 2.7 and Python 3."
import os


def package_files(directory):
    paths = []
    for path, directories, filenames in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


# Setting up
setup(
    name="pywidgets",
    version=VERSION,
    author="Emam_ahsour",
    author_email="emam54637@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=[
        "cv-imutils",
        "pykeyboard-input",
        "langdetect",
        "gTTS",
        "pyperclip",
    ],
    keywords=[
        "python",
        "tkinter",
        "tools",
        "pywidgets",
        "widgets",
        "tkinter widgets",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    package_data={
        "": package_files("./pywidgets/tk/Img/icons")+package_files("./pywidgets/tk/pdf_viewer/icons")+package_files("./pywidgets/tk/Img_editor/icons")+package_files("./pywidgets/tk/Img_editor/side_bar/icons")+package_files("./pywidgets/tk/Img_editor/buttonsbar/icons")+package_files("./pywidgets/tk/widgets/text_reader/icons")+package_files("./pywidgets/tk/widgets/color_picker/icons")
    },
    include_package_data=True,
)
