FROM python:3.10.0

SHELL [ "/bin/bash", "--login", "-c" ]

ENV USER_A=user_a
ENV USER_B=user_b
ENV GROUP_X=group_x

RUN useradd -s /bin/bash -m ${USER_A} \
    && apt-get update \
    && apt-get install -y sudo acl \
    && echo ${USER_A} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USER_A} \
    && chmod 0440 /etc/sudoers.d/${USER_A} \
    && useradd -s /bin/bash -m ${USER_B} \
    && groupadd ${GROUP_X} \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

USER ${USER_A}

RUN sudo mkdir /home/all_team_projects \
    && sudo chown -R ${USER_A}:${USER_A} /home/all_team_projects \
    && sudo chmod -R 744 /home/all_team_projects \
    && sudo chmod -R g+s /home/all_team_projects \
    && setfacl -R -m u:${USER_B}:rwx /home/all_team_projects \
    && setfacl -R -m g:${GROUP_X}:rwx /home/all_team_projects

COPY entrypoint.sh ./
RUN sudo chown ${USER_A}:${USER_A} ./entrypoint.sh && sudo chmod u+x ./entrypoint.sh

COPY facl_path_demo.py ./
RUN sudo chown ${USER_A}:${USER_A} ./facl_path_demo.py && sudo chmod u+x ./facl_path_demo.py

ENTRYPOINT [ "/bin/bash", "./entrypoint.sh"]

