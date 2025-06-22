FROM nixos/nix

RUN echo "experimental-features = nix-command flakes" >> /etc/nix/nix.conf
RUN echo "sandbox = false" >> /etc/nix/nix.conf
RUN echo "filter-syscalls = false" >> /etc/nix/nix.conf
RUN echo "build-users-group = " >> /etc/nix/nix.conf


RUN nix profile install nixpkgs#direnv

RUN echo 'eval "$(direnv hook bash)"' >> ~/.bashrc

WORKDIR /fray-benchmark

COPY . /fray-benchmark/

WORKDIR /fray-benchmark/tools/fray

RUN nix build

RUN direnv allow /fray-benchmark
RUN cd /fray-benchmark && \
    export NIX_BUILD_SHELL=/bin/bash && \
    nix develop --impure --no-write-lock-file --option sandbox false --command bash -c "./scripts/build.sh"


WORKDIR /fray-benchmark
CMD ["bash"]