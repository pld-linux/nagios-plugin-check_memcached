%define		plugin	check_memcached
%include	/usr/lib/rpm/macros.perl
Summary:	MemCached health check for Nagios
Name:		nagios-plugin-%{plugin}
Version:	1.1
Release:	0.1
License:	BSD
Group:		Networking
Source0:	check_memcached
URL:		http://zilbo.com/
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	nagios-core
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Nagios plugin to check if memcached is up and running.

%prep
%setup -qcT
%{__sed} %{SOURCE0} -e 's,@plugindir@,%{plugindir},' > %{plugin}

cat > nagios.cfg <<'EOF'
# Usage:
# %{plugin}
define command {
	command_name    %{plugin}
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -p $ARG1$ -k $ARG2$ -t $ARG3$
}
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}
install %{plugin} $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -a nagios.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
