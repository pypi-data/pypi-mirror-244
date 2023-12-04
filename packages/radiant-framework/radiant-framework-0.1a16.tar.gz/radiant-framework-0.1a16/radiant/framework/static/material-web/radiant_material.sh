#!/usr/bin/bash

# Función para el contenido de compile.sh
run_compile() {
    echo "Compilling index.js for Radiant-Framework"
    cat index.js
    npx rollup -p @rollup/plugin-node-resolve index.js > material-$(npm view @material/web version).js
    echo "Compiled as material-$(npm view @material/web version).js"
    sed -i '/^import '\''@material\/web\// s/^/\/\//' material-$(npm view @material/web version).js
}

# Función para el contenido de compile_git.sh
run_compile_git() {
    echo "Compilling index.js for Radiant-Framework"
    cat index_git.js
    npx rollup -p @rollup/plugin-node-resolve index_git.js > material-git.js
    echo "Compiled as material-git.js"
    sed -i '/^import '\''@material\/web\// s/^/\/\//' material-git.js
}

# Función para el contenido de generate.sh
run_generate() {
rm -f index.js
    echo "Generating index.js"
    find * -mindepth 1 -maxdepth 1 -name "*.js" ! -name "*_test.js" -exec sh -c '
        if ! grep -q "harness" "$1"; then
            printf "import '"'"'@material/web/%s/%s'"'"';\n" "$(dirname "$1")" "$(basename "$1")" >> index.js
        fi
    ' _ {} \;
    cat index.js
}

# Función para el contenido de generate_git.sh
run_generate_git() {
    npm install
    npm install rollup @rollup/plugin-node-resolve
    npm run build
    rm -f index_git.js
    echo "Generating index_git.js"
    find * -mindepth 1 -maxdepth 1 -name "*.js" ! -name "*_test.js" -exec sh -c '
        if ! grep -q "harness" "$1"; then
            printf "import '"'"'./%s/%s'"'"';\n" "$(dirname "$1")" "$(basename "$1")" >> index_git.js
        fi
    ' _ {} \;
    cat index_git.js
}

# Verificar el argumento pasado al script
case "$1" in
    compile)
        run_compile
        ;;
    compile_git)
        run_compile_git
        ;;
    generate)
        run_generate
        ;;
    generate_git)
        run_generate_git
        ;;
    *)
        echo "Uso: $0 {compile|compile_git|generate|generate_git}"
        exit 1
esac
