FROM archlinux:latest
RUN pacman -Syu --noconfirm python3 python-pip clang
RUN pip3 install --break-system-packages requests
COPY ./src /Maul
WORKDIR /Maul
ENTRYPOINT ["sh", "main.sh"]