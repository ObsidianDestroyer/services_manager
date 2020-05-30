Name: Services Manager
Version: 0.1
Release: 0.1
Summary: Application to manage services running on your server
License: MIT

%description
This application is built for manage services on your server.

%build
python setup.py bdist_rpm

%install
sudo dnf install pipenv
pipenv install --system

%clean
rm -rf %{buildroot}

%files
./logs
./services_manager
./sqlite
./templates
./.env
./.gitignore
./__main__.py
./Pipfile
./Pipfile.lock
./setup.py
