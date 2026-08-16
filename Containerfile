FROM archlinux:latest
LABEL maintainers="q4niel <git.unrigged621@passmail.com>"
RUN pacman -Syu --noconfirm python3 python-pip clang mingw-w64-gcc
RUN pip3 install --break-system-packages requests
COPY ./src /Maul
WORKDIR /Maul
ENTRYPOINT ["python3", "main.py"]