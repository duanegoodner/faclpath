FROM python:3.10.0

SHELL [ "/bin/bash", "--login", "-c" ]

ENV USER_A=user_a
ENV USER_A_HOME=/home/user_a
ENV USER_B=user_b
ENV GROUP_X=group_x

RUN useradd -s /bin/bash -m ${USER_A} \
    && apt-get update \
    && apt-get install -y sudo acl tree \
    && echo ${USER_A} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USER_A} \
    && chmod 0440 /etc/sudoers.d/${USER_A} \
    && useradd -s /bin/bash -m ${USER_B} \
    && groupadd ${GROUP_X} \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

USER ${USER_A}

RUN pip install git+https://github.com/duanegoodner/aclpath

RUN mkdir ${USER_A_HOME}/team_projects \
#    && chown -R ${USER_A}:${USER_A} ${USER_A_HOME}/team_projects \
    && chmod -R 744 ${USER_A_HOME}/team_projects \
    && chmod -R g+s ${USER_A_HOME}/team_projects \
    && sudo chown -R ${USER_A}:${GROUP_X} ${USER_A_HOME}/team_projects \
    && setfacl -R -m u:${USER_B}:rwx ${USER_A_HOME}/team_projects \
    && setfacl -R -m g:${GROUP_X}:rwx ${USER_A_HOME}/team_projects \
    && setfacl -R -d -m o::--- ${USER_A_HOME}/team_projects

COPY entrypoint.sh ./
RUN sudo chown ${USER_A}:${USER_A} ./entrypoint.sh && sudo chmod u+x ./entrypoint.sh

COPY facl_path_demo.py ${USER_A_HOME}
RUN sudo chown ${USER_A}:${USER_A} ${USER_A_HOME}/facl_path_demo.py && sudo chmod u+x ${USER_A_HOME}/facl_path_demo.py

ENTRYPOINT [ "/bin/bash", "./entrypoint.sh"]

