%define	name	cheesetracker
%define	version	0.9.15.3
%define release	%mkrel 1

Summary:	Clone of the MS-DOS program Impulse Tracker
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://prdownloads.sourceforge.net/cheesetronic/%{name}-%{version}.tar.gz
Source11:	cheese_16x16.png
Source12:	cheese_32x32.png
Source13:	cheese_48x48.png
Patch0:		cheesetracker-0.9.9-lib64-fix.patch
License:	GPL
Group:		Sound
BuildRequires:	qt3-devel 
BuildRequires:	libsigc++1.2-devel
BuildRequires:	jackit-devel
BuildRequires:	libaudiofile-devel
BuildRequires:	libalsa-devel
BuildRequires:	scons
BuildRequires:  libgmp-devel
URL:		http://reduz.com.ar/cheesetronic/

%description 
Cheese Tracker is a program to create module music that aims to have
an interface and feature set similar to that of Impulse Tracker. It
also has some advantages such as oscilloscopes over each pattern
track, more detailed sample info, a more detailed envelope editor,
etc. So far it only works in UNIX, but all the interface/audio code is
fully modular and abstracted in individual classes, which should make
the porting of this program to other platforms extremely easy.


%prep
%setup -q
%patch0 -p1 -b .lib64

%build
unset QTDIR
scons %_smp_mflags

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
scons install prefix=$RPM_BUILD_ROOT%{_prefix}
rm -f $RPM_BUILD_ROOT%{_prefix}/bin/.sconsign
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):\
needs="x11"\
section="Multimedia/Sound"\
title="Cheesetracker"\
longtitle="A program for creating music modules"\
command="cheesetracker_qt"\
icon="%{name}.png" xdg="true"
EOF
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Cheesetracker
Comment=A program for creating music modules
Exec=cheesetracker_qt
Icon=%name
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-Multimedia-Sound;AudioVideo;Audio;Sequencer;
EOF

%{__install} -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
%{__install} -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
%{__install} -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

#install -D -m 644 debian/%name.1 %buildroot%_mandir/man1/%name.1


%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}

%postun
%{clean_menus}

%files
%defattr(-,root,root)
%doc cheesetracker/README cheesetracker/AUTHORS TODO ChangeLog
%doc cheesetracker/examples/*.* 
%doc cheesetracker/docs/*.*
%{_bindir}/cheesetracker_qt
#%_mandir/man1/%name.1*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%_datadir/applications/mandriva-*
%{_menudir}/%{name}


