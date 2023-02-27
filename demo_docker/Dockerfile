FROM python:3.10.0

SHELL [ "/bin/bash", "--login", "-c" ]

ENV USER_A=user_a
ENV USER_B=user_b
ENV USER_C=user_c

ENV GROUP_X=group_x
ENV GROUP_Y=group_y
ENV GROUP_Z=group_z

RUN useradd -s /bin/bash -m ${USER_A} \
    && apt-get update \
    && apt-get install -y sudo acl \
    && echo ${USER_A} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USER_A} \
    && chmod 0440 /etc/sudoers.d/${USER_A} \
    && useradd -s /bin/bash -m ${USER_B} \
    && useradd -s /bin/bash -m ${USER_C} \
    && groupadd ${GROUP_X} \
    && groupadd ${GROUP_Y} \
    && groupadd ${GROUP_Z} \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

USER ${USER_A}
RUN sudo mkdir /home/all_team_projects \
    && sudo mkdir /home/all_team_projects/some_project \
    && sudo touch /home/all_team_projects/some_project_file_one.txt \
    && sudo touch /home/all_team_projects/some_project_file_two.txt \
    && sudo chown -R ${USER_A}:${USER_A} /home/all_team_projects

COPY entrypoint.sh ./
RUN sudo chown ${USER_A}:${USER_A} ./entrypoint.sh && sudo chmod u+x ./entrypoint.sh

COPY hello.py ./
RUN sudo chown ${USER_A}:${USER_A} ./entrypoint.sh && sudo chmod u+x ./entrypoint.sh

ENTRYPOINT [ "/bin/bash", "./entrypoint.sh"]

