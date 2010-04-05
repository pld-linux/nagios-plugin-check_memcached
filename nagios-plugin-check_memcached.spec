#
# Conditional build:
%bcond_without	autodeps	# don't BR packages needed only for resolving deps
%bcond_without	tests	# do not perform "make test"
#
%define		plugin	check_memcached
%include	/usr/lib/rpm/macros.perl
Summary:	Nagios plugin to observe memcached
Name:		nagios-plugin-%{plugin}
Version:	0.02
Release:	8
Epoch:		1
# same as perl
License:	GPL v1+ or Artistic
Group:		Networking
Source0:	http://www.cpan.org/modules/by-module/Nagios/Nagios-Plugins-Memcached-%{version}.tar.gz
# Source0-md5:	99154aa60b099a2563f8773f95fd0646
Source1:	%{plugin}.cfg
Patch0:		%{name}.patch
URL:		http://search.cpan.org/dist/Nagios-Plugins-Memcached/
BuildRequires:	perl-Nagios-Plugin
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with autodeps} || %{with tests}
BuildRequires:	perl-Cache-Memcached
BuildRequires:	perl-Carp-Clan
%endif
Requires:	nagios-common
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

%build
%{__perl} Makefile.PL \
	--skipdeps \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}
mv $RPM_BUILD_ROOT{%{_bindir},%{plugindir}}/%{plugin}
sed -e 's,@plugindir@,%{plugindir},' %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Nagios/Plugins/Memcached/.packlist

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/check_memcached
%{_mandir}/man3/Nagios::Plugin::Memcached.3pm*
%{perl_vendorlib}/Nagios/Plugin/Memcached.pm
