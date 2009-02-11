%define		plugin	check_memcached
%include	/usr/lib/rpm/macros.perl
Summary:	Nagios plugin to observe memcached
Name:		nagios-plugin-%{plugin}
Version:	0.02
Release:	2
Epoch:		1
# same as perl
License:	GPL v1+ or Artistic
Group:		Networking
Source0:	http://www.cpan.org/modules/by-module/Nagios/Nagios-Plugins-Memcached-%{version}.tar.gz
# Source0-md5:	99154aa60b099a2563f8773f95fd0646
URL:		http://search.cpan.org/dist/Nagios-Plugins-Memcached/
BuildRequires:	perl-Nagios-Plugin
Patch0:		%{name}.patch
BuildRequires:	perl-Cache-Memcached
BuildRequires:	perl-Carp-Clan
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	nagios-core
Requires:	perl-Cache-Memcached
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Nagios plugin to check if memcached is up and running.

%prep
%setup -q -n Nagios-Plugins-Memcached-%{version}
%patch0 -p1
mv lib/Nagios/Plugin{s,}

cat > nagios.cfg <<'EOF'
# NOTE: This plugin can execute with all threshold options together.

### check response time(msec) for memcached
define command {
	command_name    %{plugin}_response
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -w 3 -c 5
}

### check cache size ratio(bytes/limit_maxbytes[%]) for memcached
define command {
	command_name    %{plugin}_size
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ --size-warning 60 --size-critical 80
}

### check cache hit ratio(get_hits/cmd_get[%]) for memcached
define command {
	command_name    %{plugin}_hit
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ --hit-warning 40 --size-critical 20
}
EOF

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	INSTALLSCRIPT=%{plugindir} \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}
cp -a nagios.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Nagios/Plugins/Memcached/.packlist

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/check_memcached
%{_mandir}/man3/Nagios::Plugin::Memcached.3pm*
%{perl_vendorlib}/Nagios/Plugin/Memcached.pm
