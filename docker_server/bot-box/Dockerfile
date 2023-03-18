FROM ubuntu

RUN useradd -m botbox
WORKDIR /home/botbox/


RUN apt-get update
RUN apt-get install -y gnupg wget lsb-release software-properties-common git
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null
RUN apt-add-repository "deb https://apt.kitware.com/ubuntu/ $(lsb_release -cs) main"
RUN apt update
RUN apt-get install -y software-properties-common lsb-release curl vim tmux python3-venv python3-pip\
                        python3 python3-venv python3-dev python3-pip iputils-ping python-dotenv

USER botbox
RUN pip3 install -U discord.py
RUN chown -R botbox:botbox /home/botbox/


