{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  packages = with pkgs; [
    nodejs
    prettierd
    eslint_d
    tailwindcss-language-server
    vue-language-server
    (python3.withPackages (p:
      with p; [
        azure-core
        azure-storage-blob
        beautifulsoup4
        fastapi
        numpy
        pandas
        scikit-learn
        uvicorn
        webauthn
      ]))
    basedpyright
    ruff
  ];
}
