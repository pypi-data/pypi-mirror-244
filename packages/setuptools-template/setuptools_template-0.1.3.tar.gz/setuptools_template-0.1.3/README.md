
```powershell

$package_name="setuptools_template"
mkdir $package_name/src/$package_name
echo "" > $package_name/src/$package_name/__init__.py
echo "" > $package_name/src/$package_name/__main__.py
echo "" > $package_name/src/$package_name/_version.py
echo "" > $package_name/src/$package_name/main.py
mkdir tests
echo "" > tests/__init__.py
echo "" > tests/test_main.py
echo ".venv/" > $package_name/.gitignore
echo "venv/" >> $package_name/.gitignore
echo "dist/" >> $package_name/.gitignore
echo "build/" >> $package_name/.gitignore
echo "*_cache/" >> $package_name/.gitignore
echo "__pycache__/" >> $package_name/.gitignore
echo "*.egg-info/" >> $package_name/.gitignore

cd $package_name
git init
git add .
git commit -m "feat: init project"
git tag -a v0.1.0 -m "Version 0.1.0"

python -m venv .venv

❯ python -m pip list
Package Version
------- -------
pip     23.2.1


python -m pip install --upgrade pip build setuptools setuptools_scm wheel twine
python -m pip list



python -m pip freeze > requirements-dev.txt
cat requirements-dev.txt





```


# new_setup-py_command

- https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html
