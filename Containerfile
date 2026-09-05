FROM archlinux:latest
LABEL maintainers="q4niel <git.unrigged621@passmail.com>"
RUN pacman -Syu --noconfirm python3 python-pip clang wget tar
RUN pip3 install --break-system-packages requests
COPY ./src /Maul
WORKDIR /Maul
RUN wget https://github.com/mstorsjo/llvm-mingw/releases/download/20260826/llvm-mingw-20260826-msvcrt-ubuntu-22.04-x86_64.tar.xz
RUN mkdir /opt/llvm-mingw
RUN tar -xf llvm-mingw-20260826-msvcrt-ubuntu-22.04-x86_64.tar.xz -C /opt/llvm-mingw --strip-components=1
ENTRYPOINT ["python3", "main.py"]