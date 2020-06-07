# pulseaudio uses speexdsp, wine uses pulseaudio
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define beta rc3

%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}
%define lib32name %mklib32name %{name} %{major}
%define devel32name %mklib32name -d %{name}
%global optflags %{optflags} -O3 -DRELEASE

Summary:	Preprocessing, echo cancellation and jitter buffer helpers for Speex
Name:		speexdsp
Version:	1.2
Release:	0.%{beta}.6
License:	BSD
Group:		Sound
URL:		http://www.speex.org/
Source0:	http://downloads.us.xiph.org/releases/speex/%{name}-%{version}%{beta}.tar.gz
Patch0:		speexdsp-1.2rc3-fix-pkg-config-file.patch
Patch1:		speexdsp-1.2-rc3-aarch64.patch

%description
Preprocessing, echo cancellation and jitter buffer helpers for Speex

Speex is a patent-free audio codec designed especially for voice (unlike 
Vorbis which targets general audio) signals and providing good narrowband 
and wideband quality. This project aims to be complementary to the Vorbis
codec.

%package -n %{libname}
Summary:	Shared library of the Speex codec
Group:		System/Libraries

%description -n %{libname}
This package contains the shared library required for running
applications based on Speex.

%package -n %{develname}
Summary:	Speex development files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname -s -d speex} < 1.2-0.rc1.7

%description -n %{develname}
Speex development files.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Shared library of the Speex codec (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package contains the shared library required for running
applications based on Speex.

%package -n %{devel32name}
Summary:	Speex development files (32-bit)
Group:		Development/C
Requires:	%{develname} = %{version}
Requires:	%{lib32name} = %{version}

%description -n %{devel32name}
Speex development files.
%endif

%prep
%autosetup -n %{name}-%{version}%{beta} -p1
autoreconf -fi

export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 --disable-binaries
cd ..
%endif

mkdir build
cd build
%configure --enable-binaries

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

%files -n %{libname}
%{_libdir}/libspeexdsp.so.%{major}*

%files -n %{develname}
%doc %{_docdir}/speexdsp
%{_libdir}/libspeexdsp*.so
%{_includedir}/speex/*
%{_libdir}/pkgconfig/speexdsp.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libspeexdsp.so.%{major}*

%files -n %{devel32name}
%{_prefix}/lib/libspeexdsp*.so
%{_prefix}/lib/pkgconfig/speexdsp.pc
%endif
