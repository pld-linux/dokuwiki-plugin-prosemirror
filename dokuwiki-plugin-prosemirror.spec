%define		subver	2018-10-19
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		prosemirror
%define		php_min_version 5.3.0
%include	/usr/lib/rpm/macros.php
Summary:	A WYSIWYG editor for DokuWiki
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/cosmocode/dokuwiki-plugin-prosemirror/archive/%{subver}/%{plugin}-%{subver}.tar.gz
# Source0-md5:	1dec404a752dea552c6ec5558aaaa456
Source1:	https://github.com/cosmocode/dokuwiki-plugin-prosemirror/raw/release/lib/bundle.js
# Source1-md5:	fa014eb4bc9a97759aded6ebcc6b468f
URL:		https://www.dokuwiki.org/plugin:prosemirror
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	dokuwiki >= 20131208
Requires:	php(core) >= %{php_min_version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

# no pear deps
%define		_noautopear	pear

# exclude optional php dependencies
%define		_noautophp	php-someext

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
A WYSIWYG editor for DokuWiki based on ProseMirror.

%prep
%setup -qc
mv *-%{plugin}-*/{.??*,*} .
install -d lib
cp -p %{SOURCE1} lib

# nothing to do with tests
# and other development cruft
%{__rm} -r _test
%{__rm} -r _jstest
%{__rm} .babelrc
%{__rm} .eslintrc.js
%{__rm} .gitignore
%{__rm} .travis.yml
%{__rm} deleted.files
%{__rm} package.json
%{__rm} pre-commit.hook.sh
%{__rm} requirements.txt # dokuwiki testing
%{__rm} stylelint.config.js
%{__rm} webpack.config.js
%{__rm} yarn.lock
# sources, confuses dokuwiki
%{__rm} -r script

%build
version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/README.md

%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md
%dir %{plugindir}
%{plugindir}/*.js
%{plugindir}/*.less
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/action
%{plugindir}/conf
%{plugindir}/lib
%{plugindir}/parser
%{plugindir}/schema
