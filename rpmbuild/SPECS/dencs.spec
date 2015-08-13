%global commit c0dc755d6bcb0d6d0b7f99d77e70539a08f39544
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global openssl_version 1.0.2d
%global openssl_builddir %{_builddir}/gcoin-%{commit}/openssl-%{openssl_version}-build
%global bdb_version 5.3.28
%global bdb_builddir %{_builddir}/gcoin-%{commit}/db-%{bdb_version}/build_unix

Name:       dencs
Version:    0
Release:    0.20150813git%{shortcommit}%{?dist}
Summary:    Dencs core daemon - reference client and server

Group:      Applications/System
License:    MIT
URL:        http://fountain-opennet.org
Source0:    https://github.com/OpenNetworking/gcoin/archive/%{commit}/gcoin-%{commit}.tar.gz
Source1:    https://www.openssl.org/source/openssl-%{openssl_version}.tar.gz
Source2:    http://download.oracle.com/berkeley-db/db-%{bdb_version}.tar.gz

BuildRequires: autoconf automake libtool boost-devel

%if 0%{?rhel} >= 7 || 0%{?fedora} >= 18
BuildRequires: libdb-cxx-devel
%endif

%if 0%{?fedora} >= 16
BuildRequires: miniupnpc-devel
%endif

%description

%prep
%if 0%{?rhel} < 7 && 0%{?fedora} < 18
%setup -q -n gcoin-%{commit} -a 1 -a 2
%else
%setup -q -n gcoin-%{commit} -a 1
# -q : quiet, -n : naming the directory, -a : only unpack the n-th source after changing directory, ,
%endif


%build
%if 0%{?rhel} < 7 && 0%{?fedora} < 18
cd %{_builddir}/gcoin-%{commit}/db-%{bdb_version}/build_unix
CC='cc -fPIC' CXX='c++ -fPIC' ../dist/configure \
    --disable-shared --enable-static --enable-cxx
make %{?_smp_mflags}
%define bdb_args CXXFLAGS='-g -O2 -I%{bdb_builddir}' LDFLAGS='-L%{bdb_builddir}'
%endif

cd %{_builddir}/gcoin-%{commit}/openssl-%{openssl_version}
CC='cc -fPIC' ./config --prefix=%{openssl_builddir}
make all install_sw

cd %{_builddir}/gcoin-%{commit}
autoreconf -fiv
%configure --enable-tests=no \
    CRYPTO_CFLAGS='-I%{openssl_builddir}/include' \
    CRYPTO_LIBS='%{openssl_builddir}/lib/libcrypto.a' \
    SSL_CFLAGS='-I%{openssl_builddir}/include' \
    SSL_LIBS='%{openssl_builddir}/lib/libssl.a -ldl' \
    %{bdb_args}
make %{?_smp_mflags}


%install
cd %{_builddir}/gcoin-%{commit}
install -m 755 -d %{buildroot}%{_libexecdir}/dencs
install -m 755 src/bitcoind %{buildroot}%{_libexecdir}/dencs
install -m 755 src/bitcoin-cli %{buildroot}%{_libexecdir}/dencs

install -m 755 -d %{buildroot}%{_bindir}
install -m 755 src/bitcoind %{buildroot}%{_bindir}
install -m 755 src/bitcoin-cli %{buildroot}%{_bindir}
printf '#!/bin/sh\n%{_libexecdir}/dencs/bitcoind -gcoin "$@"\n' > %{buildroot}%{_bindir}/dencsd
printf '#!/bin/sh\n%{_libexecdir}/dencs/bitcoin-cli -gcoin "$@"\n' > %{buildroot}%{_bindir}/dencs-cli
chmod 755 %{buildroot}%{_bindir}/dencsd
chmod 755 %{buildroot}%{_bindir}/dencs-cli


%files
%attr(555, root, root) %{_bindir}/dencsd
%attr(555, root, root) %{_bindir}/dencs-cli
%attr(555, root, root) %{_libexecdir}/dencs/bitcoind
%attr(555, root, root) %{_libexecdir}/dencs/bitcoin-cli

%attr(555, root, root) %{_bindir}/bitcoind
%attr(555, root, root) %{_bindir}/bitcoin-cli

%doc COPYING README.md


%changelog
#* Thu Aug 08 2015 kevin <j84255801912@gmail.com> - 0.0.20150813gitc0dc755
- Use the latest commit in branch no_fee_DEV

* Fri Jul 31 2015 Mai-Hsuan Chia <j84255801912@gmail.com> - 0.0.20150731git7264200
- Use the latest commit in branch no_fee_DEV

* Thu Jul 23 2015 Mai-Hsuan Chia <j84255801912@gmail.com> - 0.0.20150723gite511b1b
- Use the latest commit in branch no_fee_DEV

* Tue Jul 14 2015 Mai-Hsuan Chia <j84255801912@gmail.com> - 0.0.20150714git8f919d0
- Use the newer commit in branch no_fee_DEV

* Mon Jul 06 2015 Mai-Hsuan Chia <j84255801912@gmail.com> - 0.0.20150706gite9ade5f
- Use the newer commit in branch no_fee_DEV

* Mon May 11 2015 Mai-Hsuan Chia <j84255801912@gmail.com> - 0.0.20150511git5fe2ead
- Use the newer commit in branch no_fee_DEV

* Wed Apr 22 2015 Mai-Hsuan Chia <j84255801912@gmail.com> - 0-0.20150422git39212ee
- Use the newer commit in branch no_fee_DEV

* Mon Apr 20 2015 Mai-Hsuan Chia <j84255801912@gmail.com> - 0-0.20150420git9a831a8
- Use the newer commit in branch no_fee_DEV

* Tue Apr 07 2015 Mai-Hsuan Chia <j84255801912@gmail.com> - 0-0.20150407git554f141
- Use the newer commit in branch no_fee_DEV
- Install bitcoind, bitcoin-cli.

* Thu Mar 05 2015 Mai-Hsuan Chia <j84255801912@gmail.com> - 0-0.20150305git91ff4c0
- Use the newer commit in branch no_fee_DEV

* Tue Jan 20 2015 Ting-Wei Lan <lantw44@gmail.com> - 0-0.20150120git8681b9e
- Rename gcoin to dencs
- Update bundled OpenSSL to 1.0.1l

* Thu Oct 16 2014 Ting-Wei Lan <lantw44@gmail.com> - 0-0.20141016gita9c5d66
- Update bundled OpenSSL to 1.0.1j

* Wed Oct 15 2014 Ting-Wei Lan <lantw44@gmail.com> - 0-0.20141015gita9c5d66
- Initial packaging
