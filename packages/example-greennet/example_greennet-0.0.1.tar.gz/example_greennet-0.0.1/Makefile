.PHONY: say_hello clean clean_pycache init_env push_pypi

all: say_hello
say_hello:
	@echo "===================================================="
	@echo "You can use these commands:"
	@echo "     make init_env"
	@echo "     make clean"
	@echo "     make clean_pycache"
	@echo "     make push_pypi"
	@echo "     make push_code [version=0.1.2]"

clean:
	@echo "Cleaning up..."
	find . -name '*.py[co]' -delete
	rm -rf ./build ./dist ./nalibs.egg-info

clean_pycache:
	@echo "Cleaning up..."
	rm -rf ./nalibs/__pycache__/ || true

# init_env:
# 	rm -rf env/
# 	python3 -m venv --prompt '|> nalibs <|' env
# 	source ./env/bin/activate; \
# 	env/bin/pip install -r requirements.txt
# 	@echo
# 	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
# 	@echo

push_pypi: clean_pycache clean
	@echo "Push to PyPi"
	source env/bin/activate; \
	python3 setup.py sdist bdist_wheel; \
	twine upload dist/*

# pip install nalibs==0.1.0
push_code:
	@echo "Bump nalibs version"
	git add .
	git commit -m "Bump nalibs ${version}"
	git push origin master
