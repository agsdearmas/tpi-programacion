- Clonar repo:
git clone https://github.com/agsdearmas/tpi-programacion.git

- Cambiarse a rama develop (no usar master)
git checkout develop

- Crear rama de feature (Pararse siempre en rama develop)
git checkout -B feat/menu
cp src/dataset_base.csv src/dataset.csv

- Proceso de push (siempre desde rama feature)
(nomenclatura de commits:) ("add/fix: descripcion breve del commit")

- (ejemplo)
git add .
git commit -m "add: se agregan validaciones a las opciones del menu"
git push -u origin feat/menu

- Hacer pull request
Ir a GitHub > pestaña PullRequests > New Pull Request
Elegir base: develop, compare: feat/menu
Asignar Reviewer