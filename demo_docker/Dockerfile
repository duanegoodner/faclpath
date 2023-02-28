FROM python:3.10.0

SHELL [ "/bin/bash", "--login", "-c" ]

ENV USER_A=user_a
ENV USER_A_HOME=/home/user_a
ENV USER_B=user_b
ENV GROUP_X=group_x

# create user w/ sudo rights; do everything else in Dockerfile as that user
RUN useradd -s /bin/bash -m ${USER_A} \
    && apt-get update \
    && apt-get install -y sudo acl \
    && echo ${USER_A} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USER_A} \
    && chmod 0440 /etc/sudoers.d/${USER_A}
USER ${USER_A}

# create a group, another use, and a directory to use in our pygetfacl demo
ENV TEST_DIR=${USER_A_HOME}/test_dir
RUN sudo groupadd ${GROUP_X} \
    && sudo useradd -s /bin/bash -m ${USER_B} \
    && mkdir ${TEST_DIR}

# modify permission and ACL settings on test_dir so we have something \
# interesting to see when we test ACL.getfacl()
RUN  chmod -R 744 ${TEST_DIR} \
    && chmod -R g+s ${TEST_DIR} \
    && sudo chown -R ${USER_A}:${GROUP_X} ${TEST_DIR} \
    && setfacl -R -m u:${USER_B}:rwx ${TEST_DIR} \
    && setfacl -R -m g:${GROUP_X}:rwx ${TEST_DIR} \
    && setfacl -R -d -m o::--- ${TEST_DIR}

# install pygetfacl
RUN pip install git+https://github.com/duanegoodner/pygetfacl

# set up container entrypoint
COPY entrypoint.sh ./
RUN sudo chown ${USER_A}:${USER_A} ./entrypoint.sh && sudo chmod u+x ./entrypoint.sh
ENTRYPOINT [ "/bin/bash", "./entrypoint.sh"]

