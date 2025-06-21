FROM nixos/nix

RUN echo "experimental-features = nix-command flakes" >> /etc/nix/nix.conf
RUN echo "sandbox = false" >> /etc/nix/nix.conf
RUN nix profile install nixpkgs#direnv

RUN echo 'eval "$(direnv hook bash)"' >> ~/.bashrc

WORKDIR /fray-benchmark

COPY . /fray-benchmark/
RUN direnv allow /fray-benchmark
RUN cd /fray-benchmark && nix develop --impure --no-write-lock-file 

CMD ["bash"]